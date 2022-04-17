from Crypto.PublicKey import RSA
import Crypto.Signature.PKCS1_v1_5 as sign_PKCS1_v1_5  # 用于签名/验签
from Crypto.Cipher import PKCS1_v1_5  # 用于加密
from Crypto import Random
from Crypto import Hash
import base64
# 下面生成一对2048bit的密钥：
x = RSA.generate(2048)

s_key = x.export_key()  # 私钥
g_key = x.publickey().export_key()  # 公钥

# 从文件导入密钥 -- 通过私钥生成公钥  (公钥不会变 -- 用于只知道私钥的情况)--2
# with open('c.pem','rb')as x:
#     s_key = RSA.importKey(x.read())
# # new_g_key = s_key.publickey().export_key()
# # print(new_g_key)
# cert = s_key.export_key("DER")  #生成证书 -- 它和私钥是唯一对应的
# print(cert)

# 实现RSA 非对称加解密
my_private_key = s_key  # 私钥
my_public_key = g_key  # 公钥

'''
作用：对信息进行公钥加密，私钥解密。
应用场景：
    A想要加密传输一份数据给B，担心使用对称加密算法易被他人破解（密钥只有一份，一旦泄露，则数据泄露），故使用非对称加密。
    信息接收方可以生成自己的秘钥对，即公私钥各一个，然后将公钥发给他人，私钥自己保留。

    A使用公钥加密数据，然后将加密后的密文发送给B，B再使用自己的私钥进行解密，这样即使A的公钥和密文均被第三方得到，
    第三方也要知晓私钥和加密算法才能解密密文，大大降低数据泄露风险。
'''


def encrypt_with_rsa(plain_text):
    # 先公钥加密
    cipher_pub_obj = PKCS1_v1_5.new(RSA.importKey(my_public_key))
    _secret_byte_obj = cipher_pub_obj.encrypt(plain_text.encode())

    return _secret_byte_obj


def decrypt_with_rsa(_secret_byte_obj):
    # 后私钥解密
    cipher_pri_obj = PKCS1_v1_5.new(RSA.importKey(my_private_key))
    _byte_obj = cipher_pri_obj.decrypt(_secret_byte_obj, Random.new().read)
    plain_text = _byte_obj.decode()
    return plain_text


def executer_without_signature():
    # 加解密验证
    text = "I love CA!"
    assert text == decrypt_with_rsa(encrypt_with_rsa(text))
    print("rsa test success！")