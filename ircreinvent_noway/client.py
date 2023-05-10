import socket
import threading
def send_msg(conn):
    while True:
        msg = input()
        conn.send(msg.encode())
def wait_msg(conn):
    while True:
        msg = conn.recv(1024).decode()
        print(msg, end = "\n")
s = socket.socket()
port = input("Server Port: ")
hs = input("Server Host Name: ")
us = input("Username: ")
s.connect((hs, int(port)))
s.send(f"!j {us}".encode())
threading.Thread(target = send_msg, args = (s,)).start()
threading.Thread(target = wait_msg, args = (s,)).start()