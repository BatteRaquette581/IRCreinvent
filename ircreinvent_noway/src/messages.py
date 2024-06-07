import rsa
from dataclasses import dataclass
from Crypto import Random
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
from .encryption import AESWrapper
from .message import Message
import socket
class Messages:
    @staticmethod
    def sendRSAMessage(sock: socket.socket,message: Message | str | bytes,public_key: rsa.PublicKey):
        if isinstance(message,Message):
            message = str(message).encode()
        if isinstance(message,str):
            message = message.encode()
        
        
        sock.send(rsa.encrypt(message,public_key))
    @staticmethod
    def sendMessage(sock: socket.socket,message: Message | str, aesKey: bytes):
        if isinstance(message,Message):
            message = str(message).encode()
        if isinstance(message,str):
            message = message.encode()

        ciphered = AESWrapper.encrypt(message,aesKey) 
        sock.send(pad(str(len(ciphered)).encode(),64)) # send message length
        return sock.send(ciphered)
    
    @staticmethod
    def receiveMessage(sock:socket.socket,key:bytes):
        length = int(unpad(sock.recv(64),64).decode())
        message = sock.recv(length)
        iv = message[:16]
        message = message[16:]
        plaintext = AESWrapper.decrypt(ciphertext=message,iv=iv,key=key)
        return plaintext
    
    @staticmethod
    def receiveRSAMessage(sock:socket.socket,privateKey:rsa.PrivateKey,length=4096):
        return rsa.decrypt(sock.recv(length),privateKey)