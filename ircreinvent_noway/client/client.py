import socket
import threading
from atexit import register
import os
global running
import rsa
running = True

def clear_console():

    os_name = os.name
    match os_name:
        case 'nt':
            os.system('cls')
        case 'posix':
            os.system('clear')
        case _:
            print("Unknown OS: " + os_name)

def handleSending(sock,publicKey):
    while True:
        message=input()

        if message == "QUIT": 
            Messages.sendMessage(sock,message,publicKey)
            sock.close()
            os._exit(1)
        Messages.sendMessage(sock,message,publicKey)
def handleReceiving(sock,privateKey):
    while True:
        message = Messages.receiveMessage(sock,privateKey)
        print(message)

class Messages:
    @staticmethod
    def sendMessage(sock: socket.socket,message: str,public_key: rsa.PublicKey):
        sock.send(rsa.encrypt(message.encode(),public_key))
    def receiveMessage(sock:socket.socket, private_key: rsa.PrivateKey):
        return rsa.decrypt(sock.recv(4096),private_key).decode()

clear_console()

print("""
                    ____  ____    ______
   __  __  ____    /  _/ / __ \  / ____/
  / / / / / __ \   / /  / / / / / /    
 / /_/ / / /_/ /  / /  / _, _/ / /___   
 \__, /  \__,_/ /___/ /_/ |_|  \____/   
/____/                              """)
print()
s = socket.socket()
ip, *port = input("Server Host Name (IP:Port): ").split(":")

if port: port = port[0] # weird python shenanigans
if not port: port = 22954  

us = input("Username: ")
s.connect((ip, int(port)))

if os.path.exists("public.pem") and os.path.exists("private.pem"):
    print("Using existing keys")
    with open("public.pem","rb") as f:
        public = rsa.PublicKey.load_pkcs1(f.read())
    with open("private.pem","rb") as f:
        private = rsa.PrivateKey.load_pkcs1(f.read())
else: 
    print("Generating keys (This may take few minutes)...")
    public,private = rsa.newkeys(4096+11)
    print("Done!")
    with open("public.pem","wb") as f:
        f.write(public.save_pkcs1())
    with open("private.pem","wb") as f:
        f.write(private.save_pkcs1())

print(f"Public key:\n{public.save_pkcs1().decode()}\n")

serverPublicKey = rsa.PublicKey.load_pkcs1(s.recv(4096+11))

print(f"Server public key:\n{serverPublicKey.save_pkcs1().decode()}\n")

Messages.sendMessage(s,us,serverPublicKey)
s.send(public.save_pkcs1())

print("type QUIT to quit")
currentChunk = b""
latest = []
buffer = b""
while True:
    currentChunk = s.recv(8192)
    if currentChunk[-7:] == b"__END__": 
        buffer += currentChunk[:-7]
        break
    buffer += currentChunk

latest = buffer.split(b"__END_MSG__")
latest = latest[:-1]
for message in latest:
    print(rsa.decrypt(message,private).decode())
    

    




threading.Thread(target=handleReceiving,args=(s,private,)).start()
threading.Thread(target=handleSending,args=(s,serverPublicKey,)).start()


