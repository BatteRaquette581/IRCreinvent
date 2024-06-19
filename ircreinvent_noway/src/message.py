from dataclasses import dataclass
import datetime
from .member import Member
@dataclass
class Message:
    sender:Member
    sentAt: datetime.datetime
    message:str 

    def __str__(self):
        # if Message.sender is None, it's the server.
        # a quite hacky solution, but this needs to stay in order to make the onuserjoin and leave events work using the message class
        if self.sender:
            username = self.sender.username
        else:
            username = "Server"
        return f'{self.sentAt.strftime("%H:%M:%S")} | {username}: {self.message}'