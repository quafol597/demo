#!/usr/bin/env python
# coding: utf-8

import json
from base64 import b64encode, b64decode
from datetime import datetime
import rsa
from .exceptions import ApiUtilsException, ApiUtilsValidationError


class APIUtils(object):
    @property
    def appid(self):
        return self._appid

    @property
    def sign_type(self):
        return self._sign_type

    @property
    def my_private_key(self):
        """签名"""
        return self._my_pri_key

    @property
    def oppsite_pub_key(self):
        """验签"""
        return self._oppsite_pub_key

    def __init__(self,
                 appid,
                 my_pri_key_path=None,  # 自己的私钥
                 my_pri_key_string=None,
                 oppsite_pub_key_path=None,  # 对方的公钥
                 oppsite_pub_key_string=None,
                 sign_type="RSA2",
                 debug=True):
        """
        <1> generate attributes of instance
        <2> generate RSA key objects
        """
        self._appid = str(appid)
        self._my_pri_key_path = my_pri_key_path
        self._my_pri_key_string = my_pri_key_string
        self._oppsite_pub_key_path = oppsite_pub_key_path
        self._oppsite_pub_key_string = oppsite_pub_key_string

        self._my_pri_key = None
        self._oppsite_pub_key = None

        if sign_type not in ("RSA", "RSA2"):
            raise ApiUtilsException(None, "Unsupported sign type {}".format(sign_type))
        self._sign_type = sign_type

        if debug is True:
            self._gateway = "https://127.0.0.1:8000/dev/gateway"
        else:
            self._gateway = "https://127.0.0.1:8000/gateway"

        # <2> generate RSA key objects
        self._load_key()

    def _load_key(self):
        """get RSA Key objects from the path or string"""
        content = self._my_pri_key_string
        if not content:
            with open(self._my_pri_key_path) as fp:
                content = fp.read()
        self._my_pri_key = rsa.PrivateKey.load_pkcs1(content.encode())

        content = self._oppsite_pub_key_string
        if not content:
            with open(self._oppsite_pub_key_path) as fp:
                content = fp.read()
        self._oppsite_pub_key = rsa.PublicKey.load_pkcs1(content.encode())

    def _sign(self, unsigned_string: str) -> str:
        """
        通过如下方法调试签名
        方法1
            key = rsa.PrivateKey.load_pkcs1(open(self._app_private_key_path).read())
            sign = rsa.sign(unsigned_string.encode(), key, "SHA-256")
            sign = base64.b64encode(sign).decode().  # 用base64 编码，再转换为str.
        方法2
            key = RSA.importKey(open(self._app_private_key_path).read())
            signer = PKCS1_v1_5.new(key)
            signature_x = signer.sign(SHA.new(unsigned_string.encode()))
            sign = base64.b64encode(sign).decode().
        方法3
            echo "abc" | openssl sha1 -sign alipay.key | openssl base64
        """
        if self._sign_type == "RSA":  # RSA
            signature = rsa.sign(unsigned_string.encode(), self.my_private_key, "SHA-1")
        else:  # RSA2
            signature = rsa.sign(unsigned_string.encode(), self.my_private_key, "SHA-256")
        # 用base64 编码，再转换为str.
        sign = b64encode(signature).decode()
        return sign

    @staticmethod
    def _ordered_data(data: dict):
        complex_keys = [k for k, v in data.items() if isinstance(v, dict)]

        # 将字典类型的数据dump出来
        for key in complex_keys:
            data[key] = json.dumps(data[key], separators=(',', ':'), ensure_ascii=False)  # seperators参数去字典中的空格

        return sorted([(k, v) for k, v in data.items()])

    def build_body(self, biz_content, method=None, return_url=None):
        """在biz_content字典外层封装一些信息"""
        body = {
            "app_id": self._appid,
            "charset": "utf-8",
            "sign_type": self._sign_type,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "version": "1.0",
            "biz_content": biz_content
        }

        if method is not None:
            body["method"] = method

        if return_url is not None:
            body["return_url"] = return_url

        return body

    def sign_data(self, data: dict):
        ordered_items = self._ordered_data(data)
        unsigned_string = "&".join("{}={}".format(k, v) for k, v in ordered_items)
        signature = self._sign(unsigned_string)

        return signature

    def _verify(self, raw_content: str, signature: str):
        """
            验签:
        """

        try:
            signature = b64decode(signature.encode())
            method_name = rsa.verify(raw_content.encode(), signature, self.oppsite_pub_key)
        except Exception:
            return False
        if method_name:
            return True

    def verify(self, body: dict, signature: str) -> bool:

        unsigned_items = self._ordered_data(body)
        message = "&".join(u"{}={}".format(k, v) for k, v in unsigned_items)
        return self._verify(message, signature)

    def api_apiutils_books(self, subject, return_url=None, **kwargs) -> dict:
        """
            <1> 包装用户原始信息, 并添加签名.
            <2> 向小安发送请求,
            <3> 返回content字典, PS:
                content = {
                    "result": ...,  # 小安响应数据
                    "signature_x": ...  # 小安签名, 用于self.verify函数验签
                }
        """
        biz_content = {"subject": subject,}
        biz_content.update(kwargs)  # biz_content 用户传入接口的数据. type: dict

        body = self.build_body(  # body 在 biz_content 外添加时间戳, 加密类型等信息. type: dict
            biz_content,
            "api_apiutils_books",
            return_url=return_url
        )

        signature = self.sign_data(body)  # 对 body 字典进行签名, 返签名
        return self.send_request(body, signature)  # 携带用户信息及签名, 向小安发送请求

    def send_request(self, body, signature):
        import requests
        gateway_url = 'http://127.0.0.1:8000/dev/gateway/'
        data = {'body': json.dumps(body), 'signature_x': signature}
        response = requests.post(url=gateway_url, data=data)
        content = response.content.decode()
        # content 包含result和signature两个字段, type: json_str
        return json.loads(content)


if __name__ == '__main__':
    pass

