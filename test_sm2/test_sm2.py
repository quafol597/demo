import binascii
import base64
from gmssl import sm2, func
# from gmssl.utils import PrivateKey


def get_keys(pub, pri):
    with open(pri, 'r', encoding='utf-8') as f:
        pri_str = ''.join(f.readlines()[1:-1]).replace('\n', '')
        pri_key = base64.b64decode(pri_str.encode()).decode()
    with open(pub, 'r', encoding='utf-8') as f :
        pub_str = ''.join(f.readlines()[1:-1]).replace('\n', '')
        pub_key = base64.b64decode(pub_str.encode()).decode()
    return pub_key, pri_key


class Sm2Algorithm(object):

    def __init__(self, pub_key, pri_key):
        self.pub_key = pub_key,
        self.pri_key = pri_key
        self.sm2_crypt = sm2.CryptSM2(public_key=pub_key, private_key=pri_key)

    def encrypt_decrypt(self, message):
        # 加密
        buff = self.sm2_crypt.encrypt(message.encode())
        ciphertext = base64.b64encode(buff).decode()
        print('ciphertext:', ciphertext)

        # 解密
        message = self.sm2_crypt.decrypt(base64.b64decode(ciphertext))
        print(message.decode())

    def sign_verify(self, message):
        k = func.random_hex(self.sm2_crypt.para_len)  # 生成随机数
        sign = self.sm2_crypt.sign(message.encode(), k)  # 十六进制签名
        print(sign)

        b = self.sm2_crypt.verify(sign, message.encode())
        print(b)

    def key_to_pem(self, key, key_type):
        key = base64.b64encode(key.encode()).decode()

        buff = []
        for i in range(len(key) // 64 + 2):
            buff.append(key[i * 64:(i + 1) * 64])

        if key_type == 'public':
            key_pem = '-----BEGIN PUBLIC KEY-----\n' + '\n'.join(buff) + '-----END PUBLIC KEY-----'
            with open('pub.pem', 'w', encoding='utf-8') as f:
                f.write(key_pem)
        elif key_type == 'private':
            key_pem = '-----BEGIN PRIVATE KEY-----\n' + '\n'.join(buff) + '-----END PRIVATE KEY-----'
            with open('pri.pem', 'w', encoding='utf-8') as f:
                f.write(key_pem)
        else:
            raise ValueError(f'key_type only accepted "public" or "private", but got {key_type}')
        return key_pem





if __name__ == '__main__':
    # 16进制的公钥和私钥
    message = '这是一条信息'
    pub_key, pri_key = get_keys('pub.pem', 'pri.pem')
    a = Sm2Algorithm(pub_key, pri_key)

    a.encrypt_decrypt(message)
    # a.sign_verify(message)
