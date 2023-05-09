import socket
import threading

def handle_connection(connection, address):
    BUF = 1024
    while True:
        msg = connection.recv(BUF).decode()
        if not msg:
            continue
        connection.send(f"{str(address)}: {msg}").encode()

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = input("Server Port: ")
sock.bind(("127.0.0.1", int(port)))
sock.listen()
while True:
    connection, address = sock.accept()
    threading.Thread(
        target = handle_connection,
        args = (connection, address),
        daemon = True
    ).start()