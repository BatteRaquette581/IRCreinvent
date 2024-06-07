from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
class AESWrapper:
    def encrypt(data: bytes,key:bytes):
        cipher = AES.new(key,AES.MODE_CBC)
        return cipher.iv + cipher.encrypt(pad(data,AES.block_size))
    def decrypt(ciphertext:bytes,iv:bytes,key:bytes):
        cipher = AES.new(key,AES.MODE_CBC,iv)
        return unpad(cipher.decrypt(ciphertext),AES.block_size).decode()