
import socket
import threading
from dataclasses import dataclass
from pathlib import Path
import sys
import importlib
import time
import datetime
import events
import rsa
from Crypto import Random

from src.message import Message
from src.messages import Messages
from src.logging import Logging
from.src.member import Member

def import_parents(level=2):
    global __package__
    file = Path(__file__).resolve()
    parent, top = file.parent, file.parents[level]
    
    sys.path.append(str(top))
    try:
        sys.path.remove(str(parent))
    except ValueError: # already removed
        pass

    __package__ = '.'.join(parent.parts[len(top.parts):])
    importlib.import_module(__package__) # won't be needed after that


if __name__ == '__main__' and __package__ is None:
    import_parents() 


                     
            

@dataclass
class Server:
    port: int = 22954
    host: str = "localhost"
    openKey: rsa.PublicKey = None
    privateKey: rsa.PrivateKey = None
    __membersMutex: threading.Lock = threading.Lock()
    __handleClientsThread: threading.Thread = None
    logger: Logging = Logging()
    eventBus: events.Events = events.Events(("onUserJoin","onUserLeave","onMessageSend"))
    running: bool = True
        
    def __getUsername(self,sock,addr,aesKey):
        try:
            return Messages.receiveMessage(sock,key=aesKey)
        except Exception as e:
            print(e)
            print(f"Error getting username from {addr[0]}")
            return None

    def __getUserPublicKey(self,sock,addr):
        try:
            return rsa.PublicKey.load_pkcs1(sock.recv(344))
            
        except:
            print(f"Error getting public key from {addr[0]}")
            return None

    def __sendLatestMessages(self,sock,aesKey,username):
        latest = "\0".join(self.logger.getLatestMessages())

        try:

            Messages.sendMessage(sock,latest,aesKey)
        except Exception as e:
            print(e)
            print(f"Error sending latest messages to {username}")
            return None
            
        return "\0"
    
    def __sendAESKey(self,sock,aesKey,publicKey,addr):
        try:
            Messages.sendRSAMessage(sock,aesKey,publicKey)
            return True
        except Exception as e:
            print(e)
            print(f"Error sending to {addr[0]}")
            return None

    def __memberHandshake(self,sock,addr):
        aesKey = Random.new().read(32)

        publicKey = self.__getUserPublicKey(sock,addr)
        if not publicKey:
            return (None,None)

        successfully = self.__sendAESKey(sock,aesKey,publicKey,addr)
        if not successfully:
            return (None,None)

        username = self.__getUsername(sock,addr,aesKey)

        if not username:
            return (None,None)

        successfully = self.__sendLatestMessages(sock,aesKey,username)
        if not successfully:
            return (None,None)

        return (username,aesKey)

    def handleClients(self):
        while self.running:
            sock,addr = self.socket.accept()

            username,aesKey = self.__memberHandshake(sock,addr)

            if not (username or aesKey):
                sock.close()
                continue
            

            self.__membersMutex.acquire()
            member = Member(username,sock,aesKey)            

            self.members.append(member)
            self.eventBus.onUserJoin(member)
            handleThread = threading.Thread(target=self.handleMessages,args=(member,))
            handleThread.start()
            self.__membersMutex.release()


    def handleMessages(self,member):

        while self.running:
            try:
                message = Messages.receiveMessage(member.socket,member.aesKey)
            except:
                print(f"Error getting message from {member.username}")
                return self.eventBus.onUserLeave(member)
                
            message = Message(member,datetime.datetime.now(),message)
            if message.message=="QUIT":
                return self.eventBus.onUserLeave(member)
            self.eventBus.onMessageSend(message)


    def broadcast(self,message:Message):
        for m in self.members:
            try:
                Messages.sendMessage(m.socket,message,m.aesKey)
            except:
                print(f"Error sending message to {m.username}")
    
    def onMessageSend(self,message:Message):
        self.broadcast(message)
        self.logger.log(message)

    def onUserJoin(self,user:Member):
        self.eventBus.onMessageSend(f"User {user.username} has joined the chat!")


    def onUserLeave(self,user:Member):
        self.members.remove(user)
        user.socket.close()
        self.eventBus.onMessageSend(f"User {user.username} has left the chat!")



    def start(self):
        self.members = []
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

        self.socket.bind((self.host,self.port))
        self.socket.listen()

        self.eventBus.onMessageSend += self.onMessageSend
        self.eventBus.onUserJoin += self.onUserJoin
        self.eventBus.onUserLeave += self.onUserLeave

        self.__handleClientsThread = threading.Thread(target=self.handleClients)
        self.__handleClientsThread.start()



    def stop(self):
        self.socket.close() 
        self.running = False
        self.eventBus.onMessageSend -= self.onMessageSend
        self.eventBus.onUserJoin -= self.onUserJoin
        self.eventBus.onUserLeave -= self.onUserLeave

        members=[]
while True:
    try:
        a = Server()
        a.start()
        print("Server started!")
        break
    except Exception as e:
        print(e)
        print("Retrying in a second...")
        time.sleep(1)
