import socket
import threading
import datetime
from dataclasses import dataclass
import rsa
import os
@dataclass
class Member:
    username: str
    socket: socket.socket
    openKey: rsa.PublicKey
@dataclass
class Message:
    sender:Member
    sentAt: datetime.datetime
    message:str 

    def __str__(self):
        return f"{self.sentAt.strftime("%H:%M:%S")} | {self.sender.username}: {self.message}"


class Messages:
    @staticmethod
    def sendMessage(sock: socket.socket,message: Message,public_key: rsa.PublicKey):
        sock.send(rsa.encrypt(str(message).encode(),public_key))
    @staticmethod
    def receiveMessage(sock:socket.socket, private_key: rsa.PrivateKey,length=4096):

        return rsa.decrypt(sock.recv(length),private_key).decode()
    @staticmethod
    def sendString(sock: socket.socket, message:str,public_key:rsa.PublicKey):
        sock.send(rsa.encrypt(message.encode(),public_key))

class Logging:
    def __init__(self,path="./logs"):
        self.path = path

    def log(self,message:str):
        print(message,file=open(f"{self.path}/log-{datetime.date.today().strftime("%d-%m-%Y")}.log","a"))

    def getLatestMessages(self,n=30):
        logfiles = [f for f in os.listdir(self.path) if os.path.isfile(os.path.join(self.path, f))]
        messages = []
        for file in logfiles:
            if len(messages)>=n: break
            messages.append(f"{file[4:-4]:-^30}") # file[4:-4]: log-01-23-4567.log -> 01-23-4567
            with open(os.path.join(self.path, file),"r") as f:
                line = "\0"
                while line != "" and len(messages)<n:
                    messages.append(line)
                    line = f.readline()
        return messages

                     
            

@dataclass
class Server:
    port: int = 22954
    host: str = "localhost"
    openKey: rsa.PublicKey = None
    privateKey: rsa.PrivateKey = None
    __membersMutex: threading.Lock = threading.Lock()
    __handleClientsThread: threading.Thread = None
    logger: Logging = Logging()

    def __getUsername(self,sock,addr):
        try:
            return Messages.receiveMessage(sock,self.privateKey)
        except:
            print(f"Error getting username from {addr[0]}")
            return None

    def __getUserPublicKey(self,sock,username):
        try:
            return rsa.PublicKey.load_pkcs1(sock.recv(4096+11))
            
        except:
            print(f"Error getting public key from {username}")
            return None

    def __sendLatestMessages(self,sock,publicKey,username):
        latest = self.logger.getLatestMessages() 
        try:
            for message in latest:
                
                    Messages.sendString(sock,message,publicKey)
                    # duct-tape: add \0 after each message
                    sock.send(b"__END_MSG__")

            sock.send(b"__END__")
        except:
            return None
            print(f"Error sending latest message to {username}")
        return "\0"

    def handleClients(self):
        while True:
            sock,addr = self.socket.accept()
            sock.send(self.openKey.save_pkcs1())

            username = self.__getUsername(sock,addr)
            if not username:
                continue
            publicKey = self.__getUserPublicKey(sock,username)
            if not publicKey:
                continue

            successfully = self.__sendLatestMessages(sock,publicKey,username)
            if not successfully:
                continue

            self.__membersMutex.acquire()
            member = Member(username,sock,publicKey)            

            self.members.append(member)

            handleThread = threading.Thread(target=self.handleMessages,args=(member,))
            handleThread.start()
            self.__membersMutex.release()


    def handleMessages(self,member):

        while True:
            try:
                message = Messages.receiveMessage(member.socket,self.privateKey)
            except:
                print(f"Error getting message from {member.username}")
                return self.members.remove(member)
                
            message = Message(member,datetime.datetime.now(),message)
            if message.message=="QUIT":
                return self.members.remove(member)

            self.broadcast(message)
            self.logger.log(message)

    def broadcast(self,message:Message):
        for m in self.members:
            try:
                Messages.sendMessage(m.socket,message,m.openKey)
            except:
                print(f"Error sending message to {m.username}")
                

    def start(self):
        self.members = []
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.bind((self.host,self.port))
        self.socket.listen()
        self.__handleClientsThread = threading.Thread(target=self.handleClients)
        self.__handleClientsThread.start()


    def stop(self):
        self.socket.close(5)
        self.__handleClientsThread.stop()
        members=[]

if os.path.exists("./public.pem") and os.path.exists("./private.pem"):
    print("Using existing keys")
    with open("./public.pem","rb") as f:
        public = rsa.PublicKey.load_pkcs1(f.read())
    with open("./private.pem","rb") as f:
        private = rsa.PrivateKey.load_pkcs1(f.read())
else: 
    print("Generating keys (This may take few minutes)...")
    public,private = rsa.newkeys(4096+11)
    print("Done!")
    with open("./public.pem","wb") as f:
        f.write(public.save_pkcs1())
    with open("./private.pem","wb") as f:
        f.write(private.save_pkcs1())

a = Server(openKey=public,privateKey=private)
a.start()
print("Server started!")