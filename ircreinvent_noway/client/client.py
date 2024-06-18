from pathlib import Path
import sys
import importlib
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
import socket
import threading
from atexit import register
import os
import time
import datetime
from ..src.messages import Messages
import rsa



def clear_console():

    os_name = os.name
    match os_name:
        case 'nt':
            os.system('cls')
        case 'posix':
            os.system('clear')
        case _:
            print("Unknown OS: " + os_name)

def handleSending(sock,aesKey):
    while True:
        message=input()
        Messages.sendMessage(sock,message,aesKey)
        if message.lower().startswith("/quit"): 
            # pseudo-command stuff, see the server function which handles the message for more info
            break

    sock.close()
    os._exit(1)
def handleReceiving(sock,aesKey):
    while True:
        message = Messages.receiveMessage(sock,aesKey)
        if not message:
            print("Lost connection to server... exiting")
            os._exit()
        print(message)


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

public,private = rsa.newkeys(344)


#1 send public key to server
s.send(public.save_pkcs1())

#2 get aes key from server
aesKey = Messages.receiveRSAMessage(s,private)
#3 send username
Messages.sendMessage(s,us,aesKey)



#4 get latest messages
messages = Messages.receiveMessage(s,aesKey).split("\0")
for message in messages:
    print(message)

print("Enter /quit to quit.")

threading.Thread(target=handleReceiving,args=(s,aesKey,)).start()
threading.Thread(target=handleSending,args=(s,aesKey,)).start()


