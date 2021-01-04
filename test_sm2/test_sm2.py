import base64
import binascii
import json
from gmssl import sm2, func
import jpype
import os


def generate_hex_keys(basedir):
    """
    生成公私钥对字典
    :param basedir: jar和lib包的目录
    :return: {"privateKey": "...", "publicKey": "...", "code": "200"}
    """
    jarpath = os.path.join(basedir, 'sm2', 'sm2-1.0-SNAPSHOT.jar')
    lib = os.path.join(basedir, "lib")
    a, b, c = [os.path.join(lib, i) for i in os.listdir(lib)]

    jvmpath = jpype.getDefaultJVMPath()

    jpype.startJVM(jvmpath, "-ea", f"-Djava.class.path={jarpath};{a};{b};{c}")
    Sm2Service = jpype.JClass("com.xiaoantimes.commons.api.Sm2Service")
    keys = Sm2Service.generateKeys()

    jpype.shutdownJVM()
    return json.loads(keys)


def key_to_pem(keys: dict) -> (str, str):
    """将公私钥对字典转化为pem格式, 元组."""
    # <1> dict中取出16进制公私钥对
    pub_key = keys['publicKey']
    pri_key = keys['privateKey']

    # <2> 16进制公钥转pem格式
    key1 = base64.b64encode(pub_key.encode()).decode()
    buff1 = []
    for i in range(len(key1) // 64 + 2):
        buff1.append(key1[i * 64:(i + 1) * 64])
    pub_key_pem = '-----BEGIN PUBLIC KEY-----\n' + '\n'.join(buff1) + '-----END PUBLIC KEY-----'

    # <3> 16进制私钥转pem格式
    key2 = base64.b64encode(pri_key.encode()).decode()
    buff2 = []
    for i in range(len(key2) // 64 + 2):
        buff2.append(key2[i * 64:(i + 1) * 64])
    pri_key_pem = '-----BEGIN PRIVATE KEY-----\n' + '\n'.join(buff2) + '-----END PRIVATE KEY-----'

    return pub_key_pem, pri_key_pem


def get_keys(pub_pem, pri_pem):
    """return 16进制密钥对"""
    # with open(pri, 'r', encoding='utf-8') as f:
    #     pri_str = ''.join(f.readlines()[1:-1]).replace('\n', '')
    #     pri_key = base64.b64decode(pri_str.encode()).decode()
    #
    # with open(pub, 'r', encoding='utf-8') as f :
    #     pub_str = ''.join(f.readlines()[1:-1]).replace('\n', '')
    #     pub_key = base64.b64decode(pub_str.encode()).decode()
    pub_str = ''.join(pub_pem.split('\n')[1:-1]).replace('\n', '')
    pub_key = base64.b64decode(pub_str).decode()

    pri_str = ''.join(pri_pem.split('\n')[1:-1]).replace('\n', '')
    pri_key = base64.b64decode(pri_str).decode()

    return pub_key, pri_key


class Sm2Algorithm(object):

    def __init__(self, pub_key: hex, pri_key: hex):
        self.pub_key = pub_key,
        self.pri_key = pri_key
        self.sm2_crypt = sm2.CryptSM2(public_key=pub_key, private_key=pri_key)

    def encrypt_decrypt(self, msg: str):
        """加密和解密"""
        # 加密
        buff = self.sm2_crypt.encrypt(msg.encode())
        cipher_text = base64.b64encode(buff).decode()
        print('cipher_text:', cipher_text)
        cipher_text = 'hehe'
        # 解密
        try:
            msg = self.sm2_crypt.decrypt(base64.b64decode(cipher_text))
        except Exception:
            return print("解密失败")

        print('message:', msg.decode())

    def sign_verify(self, msg: str):
        """签名和验签"""
        k = func.random_hex(self.sm2_crypt.para_len)  # 生成随机数
        sign = self.sm2_crypt.sign(msg.encode(), k)  # 十六进制签名
        print('sign:', sign)

        b = self.sm2_crypt.verify(sign, msg.encode())
        print('verify:', b)


if __name__ == '__main__':
    keys = generate_hex_keys("sm2")
    pub_pem, pri_pem = key_to_pem(keys)
    # with open('pum_pem', 'w', encoding='utf-8') as f:
    #     f.write(pub_pem)
    # with open('pri_pem', 'w', encoding='utf-8') as f:
    #     f.write(pri_pem)

    message = '这是一条信息'
    pub_hex_key, pri_hex_key = get_keys(pub_pem, pri_pem)
    print('pub_key:', pub_hex_key)
    print('pri_key:', pub_hex_key)
    sm2 = Sm2Algorithm(pub_hex_key, pri_hex_key)

    sm2.encrypt_decrypt(msg=message)
    sm2.sign_verify(msg=message)
