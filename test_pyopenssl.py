import rsa
import base64

from OpenSSL.crypto import PKey
from OpenSSL.crypto import TYPE_RSA, FILETYPE_PEM, FILETYPE_ASN1, TYPE_EC
from OpenSSL.crypto import dump_privatekey, dump_publickey


def raw():
    pk = PKey()
    pk.generate_key(TYPE_RSA, 512)
    pub = dump_publickey(FILETYPE_PEM, pk)
    pri = dump_privatekey(FILETYPE_ASN1, pk)

    pubkey = rsa.PublicKey.load_pkcs1_openssl_pem(pub)
    prikey = rsa.PrivateKey.load_pkcs1(pri, 'DER')

    print(pubkey.save_pkcs1())
    print(prikey.save_pkcs1())

    data = rsa.encrypt(b'hello', pubkey)
    data = base64.b64encode(data)

    print(data)

    data0 = rsa.decrypt(base64.b64decode(data), prikey)


def test_pem():
    pk = PKey()
    pk.generate_key(TYPE_RSA, 512)
    pub = dump_publickey(FILETYPE_PEM, pk)
    pri = dump_privatekey(FILETYPE_ASN1, pk)

    pubkey = rsa.PublicKey.load_pkcs1(pub)
    prikey = rsa.PrivateKey.load_pkcs1(pri)

    print(pubkey.save_pkcs1())
    print(prikey.save_pkcs1())

    data = rsa.encrypt(b'hello', pubkey)
    data = base64.b64encode(data)

    print(data)

    data0 = rsa.decrypt(base64.b64decode(data), prikey)


if __name__ == '__main__':
    # raw()

    test_pem()




