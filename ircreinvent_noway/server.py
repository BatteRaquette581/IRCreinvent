import collections
import socket
import threading
from typing import Optional


class ChatRoom:
    def __init__(self, name: str, public: bool, allowed_members : Optional[list[str]]):
        self.name = name
        self.public = public
        self.messages = collections.deque()
        self.messages.append(f"This is start of {self.name} chatroom\n")
        if not self.public: self.allowed_members = allowed_members

    def add_message(self, message: str):
        self.messages.append(message)

    def read_newest_message(self):
        return self.messages[len(self.messages) - 1]

    def read_all_messages(self):
        return [message for message in self.messages]

    def change_name(self, name: str):
        self.name = name

    def get_name(self):
        return self.name


class Member:
    def __init__(self, username: str, address: tuple, connection: socket.socket, chatroom: ChatRoom, connected : bool):
        self.username = username
        self.address = address
        self.connection = connection
        self.chatroom = chatroom
        self.connected = connected


def handle_connection_read(member: Member):
    latest_message = ""
    previous_message = ""
    while member.connected:
        if latest_message == previous_message:
            latest_message = member.chatroom.read_newest_message()
            continue
        member.connection.sendall(latest_message.encode())
        previous_message = latest_message


def commands(member: Member, message: str):
    global_ = globals()
    member.connection.send(("Avaliable commands:\n" + ("\n".join([element for element in global_ if
                                                                  str(global_[element]).startswith("<function") and
                                                                  not element.startswith(
                                                                      "handle_connection")]))).encode())


def rooms(member: Member,args):

    member.connection.send((("Available Chatrooms:\n") + "\n".join(
        [c.name for c in list(filter(lambda chatroom: chatroom.public, chatrooms))])).encode())


def exit(member: Member,args):
    member.chatroom.add_message(f"System: {member.username} has left the chat\n")
    member.connected = False
    member.connection.shutdown(2)
    member.connection.close()
    members.remove(member)


def join(member: Member,args):

    if len(args) < 1: return
    chatroom_name = args[0]
    chatroom = list(filter(lambda chatroom: chatroom.name == chatroom_name, chatrooms))
    if not chatroom:
        rooms(member)
        return
    member.chatroom = chatroom[0]
    member.connection.send("\n".join(member.chatroom.read_all_messages()).encode())


def croom(member: Member, args):
    if len(args) < 2: return
    inherit = ""
    if len(args) == 3: inherit = args[2]

    name = args[0]
    public = True if args[1] == "True" else False
    chatroom = ChatRoom(name, public,None)
    if inherit:
        parent = list(filter(lambda chatroom: chatroom.name == inherit, chatrooms))
        if not parent:
            member.connection.send("Parent chatroom not found".encode())
            return
        messages = parent[0].read_all_messages()[1:]
        for message in messages: chatroom.add_message(message)

    chatrooms.append(chatroom)
    member.connection.send(f"Created Chatroom {name}".encode())


def delroom(member: Member, args):

    if len(args) < 1:
        member.connection.send("Not enough parameters".encode())
        return

    name = args[0]
    if name == "Public":
        member.connection.send("No you can't delete Public".encode())
        return
    try:
        chatrooms.remove(list(filter(lambda chatroom: chatroom.name == name, chatrooms))[0])
    except IndexError:
        member.connection.send(f"Chatroom {name} doesn't exist".encode())
        return
    member.connection.send(f"Deleted Chatroom {name}".encode())


def handle_connection_write(member: Member):
    while member.connected:
        message = member.connection.recv(1024).decode()
        if not message: continue
        if message.startswith("!"):
            try:
                args = message.split(" ")
                globals()[args[0][1:]](member,args[1:])

            except KeyError:
                member.connection.send("Command not found".encode())

            continue
        member.chatroom.add_message(f"{member.username}: {message}")


members = []
chatrooms = []
port = int(input("Server Port: "))
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket.bind(("localhost", port))
socket.listen()

public_chatroom = ChatRoom("Public", True,None)
chatrooms.append(public_chatroom)

while True:
    conn, address = socket.accept()

    print(f"New Connection from {address[0]} on port {address[1]}")

    username = conn.recv(1024).decode()

    print(f"IP {address[0]} with port {address[1]} set username as {username}")

    member = Member(username, address, conn, public_chatroom,True)
    members.append(member)

    member.connection.send("\n".join(member.chatroom.read_all_messages()).encode())
    member.chatroom.add_message(f"System: {username} has joined the chat\n")

    threading.Thread(target=handle_connection_read, args=tuple([member]), daemon=True).start()
    threading.Thread(target=handle_connection_write, args=tuple([member]), daemon=True).start()

    del address, username, conn
