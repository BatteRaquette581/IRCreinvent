import socket
import threading
def handle_conn(conn,addr):
    while True:
        msg = conn.recv(1024).decode()
        if not msg:
            continue
        conn.send((str(addr)+": "+msg).encode())
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = input("Server Port: ")
s.bind(("127.0.0.1",int(port)))
s.listen()
while True:
    conn, addr = s.accept()
    threading.Thread(target=handle_conn,args=(conn,addr),daemon=True).start()



