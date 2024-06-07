from dataclasses import dataclass
import datetime
from .member import Member
@dataclass
class Message:
    sender:Member
    sentAt: datetime.datetime
    message:str 

    def __str__(self):
        return f"{self.sentAt.strftime("%H:%M:%S")} | {self.sender.username}: {self.message}"