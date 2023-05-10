import socket
import threading


def handle_connection(connection, address):
    #try:
        BUF = 1024
        while True:
            msg = connection.recv(BUF).decode()
            if not msg:
                continue
            print(f"{str(members[address])}: {msg}")
            for conn in members_socks:
                conn.send(f"{str(members[address])}: {msg}".encode())
    #except:
        # doesn't work T_T 
     #   for connect in members_socks:
     #       connect.send(f"{username} has left the chat!".encode())
     #   connection.close()
     #   return


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = input("Server Port: ")
sock.bind(("127.0.0.1", int(port)))
sock.listen()
members_socks = []

members = {}
while True:
    connection, address = sock.accept()
    username = connection.recv(1024).decode()
    members[address] = username
    for connect in members_socks:
        connect.send(f"{username} has entered the chat!".encode())

    members_socks.append(connection)

    threading.Thread(
        target=handle_connection,
        args=(connection, address),
        daemon=True
    ).start()
