"""
python数据类型:
    bytes, str, int, float, list, dict, tuple,
msg_b  # bytes
msg_s  # str
msg_l  # list
msg_i  # int
msg_x  # hex
msg_f  # float
msg_d  # dict
msg_t  # tuple
"""

import base64
import binascii
import json
from gmssl import sm2, func
import jpype
import os
import traceback


def generate_hex_keys(basedir):
    """
    生成公私钥对字典
    basedir: jar和lib包的目录
    return: {"privateKey": "...", "publicKey": "...", "code": "200"}
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
    print('pub_key:', len(pub_key), pub_key)
    print('pri_key:', len(pri_key), pri_key)

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

def write_pem(pub_key_pem, pri_key_pem):
    with open('pum_pem', 'w', encoding='utf-8') as f:
        f.write(pub_key_pem)
    with open('pri_pem', 'w', encoding='utf-8') as f:
        f.write(pri_key_pem)


def read_pem():
    with open('pum_pem', 'r', encoding='utf-8') as f:
        pub_pem = f.read()
    with open('pri_pem', 'r', encoding='utf-8') as f:
        pri_pem = f.read()
    return pub_pem, pri_pem


def pem_to_key(pub_pem: str, pri_pem: str):
    """return 16进制密钥对"""

    pub_str = ''.join(pub_pem.split('\n')[1:-1])
    pub_key = base64.b64decode(pub_str).decode()

    pri_str = ''.join(pri_pem.split('\n')[1:-1])
    pri_key = base64.b64decode(pri_str).decode()

    return pub_key, pri_key


def encrypt(pub_key, pri_key, msg:str):
    """return base64编码后的字符串: cipher_text"""
    encrypter =  sm2.CryptSM2(public_key=pub_key, private_key=pri_key)
    buff = encrypter.encrypt(msg.encode())
    cipher_text = base64.b64encode(buff).decode()
    return buff, cipher_text


def decrypt(pub_key, pri_key, cipher_text):
    buff = base64.b64decode(cipher_text)
    encrypter = sm2.CryptSM2(public_key=pub_key, private_key=pri_key)
    try:
        msg_bytes = encrypter.decrypt(buff)
        msg = msg_bytes.decode()
    except:
        return '---> 解密失败, 异常信息如下: ' + '\n' + traceback.format_exc()

    return msg


def sign(pub_key, pri_key, msg:str):
    encrypter = sm2.CryptSM2(public_key=pub_key, private_key=pri_key)
    k = func.random_hex(encrypter.para_len)  # 生成随机数
    signature = encrypter.sign(msg.encode(), k)  # 十六进制签名

    return signature


def verify(pub_key, pri_key, sign, msg:str):
    encrypter = sm2.CryptSM2(public_key=pub_key, private_key=pri_key)
    bool_ = encrypter.verify(sign, msg.encode())
    return bool_

def cipher_to_ten(origin_cipher):
    print(f'origin_cipher: {len(origin_cipher)}', origin_cipher, sep='\n')
    ten_cipher = [i for i in origin_cipher]
    print(f'ten_cipher: {len(ten_cipher)}', ten_cipher, sep='\n')
    return ten_cipher

if __name__ == '__main__':
    msg = '这是一条信息'

    # <1> 获取公私钥对: hex
    # <1.1> 生成公私钥对: pem
    # keys = generate_hex_keys("sm2")
    # pub_pem, pri_pem = key_to_pem(keys)
    # <1.2> 读取公私钥对
    # pub_pem, pri_pem = read_pem()
    # pub_hex_key, pri_hex_key = pem_to_key(pub_pem, pri_pem)
    # <1.3> 自定义公私钥对
    pub_hex_key = '4237bb976d99830e48083da5ff497e5a4ceef163e6c69db05fe25914579c802266635b4b83fa29c67c1fbe2a204b5e4f7f2a331eb3afa9f57bedc0127a74574f'
    pri_hex_key = '443bd4875656bdc23208f1cf56abb29f711c3f197ce5b92745535e40a7d73c53'
    # print('pub_key:', pub_hex_key)
    # print('pri_key:', pri_hex_key)

    # <2> 加密和解密
    # <2.1> 加密
    buff_b, cipher_text = encrypt(pub_hex_key, pri_hex_key, msg)
    buff_x = bytes.hex(buff_b)
    buff_l = [i for i in buff_b]
    print('buff_b:', len(buff_b), buff_b)
    print("buff_x:", len(buff_x), buff_x)
    print("buff_l:", len(buff_l), buff_l)
    print('cipher_text:', len(cipher_text), cipher_text)
    # <2.2> 解密
    msg2 = decrypt(pub_hex_key, pri_hex_key, cipher_text)
    print('msg2:', msg2)

    # <3> 签名和验签
    # <3.1> 签名
    signature_x = sign(pub_hex_key, pri_hex_key, msg)  # 签名: hex
    signature_b = bytes.fromhex(signature_x)  # 签名: bytes
    signature_l = [i for i in signature_b]  # 签名: list
    signature_b2 = b''.join([chr(i).encode('latin-1') for i in signature_l])
    print(f'signature_x: {len(signature_x)}', signature_x)  # 64个字节
    # print('signature_b:', len(signature_b), signature_b)  # 64个字节
    # print('signature_l:', len(signature_l), signature_l)  # 64个字节
    # print('signature_b2:', len(signature_b2), signature_b2)  # 64个字节
    # <3.2> 验签
    bool_ = verify(pub_hex_key, pri_hex_key, signature_x, msg)
    print('bool_:', bool_)






    # origin_cipher = b"\x84\xdaf\xdb\xa1@\x85\xea\x96}\x04\xd4\xa3;\xa4\xa2\xcf\xd8\x9f2$i-\xc8\x1f\xf1'\x1aOT5\xe3\r\x9d\x88\xb4}\xbb\x9b\xb2\xf4'\n\xb1\x1d\xf9\t\xa9\x96\xca\x8e\x0bb\xa0m\xe16\x800\xd0\x98\xd7\xb8\x97g\xa2\x90\xcf\x0c8\x15\xb4;V=\x8eM\x0bDJP\xd2:c\xd5\x80+O\xed\xafud\xda\xdf\xc3\t\x83:\xbe\x8e\xfd\x93\xeeN\xa9\xbf\xc6="

    # print('cipher_text:', cipher_text, sep='\n')
    # cipher_text2 = 'BONjg27cEbWRUuxb/P7nGpplyzYjuhduzT/j7jpxBEjxWNgfy9kHgm0UcBQyihIsY79kSj+5sy4SrEbLUDz10TWc4Rw2+Lyc+4Bu9LvZcQGNHfVp30nh5hl1cs7qdpN1SfM5KMYwNc4z4Fep'
    # print(base64.b64decode(cipher_text))
    # print(base64.b64decode(cipher_text2))

    # ten_origin_cipher = [4, 90, -26, 91, 33, -64, 5, 106, 22, -3, -124, 84, 35, -69, 36, 34, 79, 88, 31, -78, -92, -23, -83, 72, -97, 113, -89, -102, -49, -44, -75, 99, -115, 29, 8, 52, -3, 59, 27, 50, 116, -89, -118, 49, -99, 121, -119, 41, 22, 74, 14, -117, -30, 32, -19, 97, -74, 0, -80, 80, 24, 87, 56, 23, -25, 34, 16, 79, -116, -72, -107, 52, -69, -42, -67, 14, -51, -117, -60, -54, -48, 82, -70, -29, 85, 0, -85, -49, 109, 47, -11, -28, 90, 95, 67, -119, 3, -70, 62, 14, 125, 19, 110, -50, 41, 63, 70, -67]
    # ten_origin_cipher2 = [i+128 for i in ten_origin_cipher]
    # print("ten_origin_cipher2:", ten_origin_cipher2, sep='\n')
    #
    # origin_cipher = b''.join([chr(i).encode() for i in ten_origin_cipher2])

    # print(f"origin_cipher: {len(origin_cipher)}", origin_cipher, sep='\n')
    # print(f"origin_cipher: {len(origin_cipher1)}", origin_cipher1, sep='\n')
    # print(f"origin_cipher: {len(origin_cipher2)}", origin_cipher2, sep='\n')

    # msg2 = obj.decrypt(origin_cipher)
    # print('msg2:', msg2)


