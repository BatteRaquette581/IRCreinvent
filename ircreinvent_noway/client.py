import socket
import threading
s = socket.socket()
port = input("Server Port: ")
hs = input("Server Host Name: ")
s.connect((hs,int(port)))
s.send("halooosodoas dasfdhgfdhgdfg".encode())
msg = s.recv(1024)
print(msg.decode())




