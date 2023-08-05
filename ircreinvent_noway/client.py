import socket
import threading

running = True

def send_msg(conn):
    global running
    while running:
        msg = input()
        conn.send(msg.encode())
        if msg == "!exit":
            running = False

def wait_msg(conn):
    global running
    while running:
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