import socket
import threading

def handle_connection(connection, address,members_socks):
    BUF = 1024
    while True:
        msg = connection.recv(BUF).decode()
        if not msg:
            continue
        for connect in members_socks:
            connect.send(f"{str(address)}: {msg}".encode())

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = input("Server Port: ")
sock.bind(("127.0.0.1", int(port)))
sock.listen()
members_socks = []
while True:
    connection, address = sock.accept()
    members_socks.append( connection)
    threading.Thread(
        target = handle_connection,
        args = (connection, address,members_socks),
        daemon = True
    ).start()
