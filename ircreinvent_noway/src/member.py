from dataclasses import dataclass
import socket
@dataclass
class Member:
    username: str
    socket: socket.socket
    aesKey: bytes