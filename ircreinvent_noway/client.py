import socket
import threading
from atexit import register
from os import system

running = True

def clear_console():
    try:
        system("cls")
    except:
        system("clear")

def on_exit():
    global running
    conn.send("!exit".encode())
    running = False

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

clear_console()
print("""
\x1b[38;2;250;130;130m    ________  ______          _                       __ 
\x1b[38;2;250;250;130m   /  _/ __ \/ ____/_______  (_)___ _   _____  ____  / /_
\x1b[38;2;90;250;90m   / // /_/ / /   / ___/ _ \/ / __ \ | / / _ \/ __ \/ __/
\x1b[38;2;90;250;250m _/ // _, _/ /___/ /  /  __/ / / / / |/ /  __/ / / / /_  
\x1b[38;2;175;130;250m/___/_/ |_|\____/_/   \___/_/_/ /_/|___/\___/_/ /_/\__/\033[0m""")
print()
s = socket.socket()
hs = input("Server Host Name (IP:Port): ")
us = input("Username: ")
s.connect((hs.split(":")[0], int(hs.split(":")[1])))
s.send(us.encode())
threading.Thread(target = send_msg, args = (s,)).start()
threading.Thread(target = wait_msg, args = (s,)).start()
register(on_exit)
