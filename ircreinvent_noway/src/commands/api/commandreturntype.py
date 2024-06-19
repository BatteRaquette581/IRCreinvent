from dataclasses import dataclass
from typing import TypedDict
from enum import Enum

from ....src.member import Member


@dataclass
class StandardCommandReturnType:
    privateMessage: str = None
    broadcast: str = None

DictCommandReturnMessageType = Enum("DictCommandReturnMessageType", ["Broadcast", "Private"])

class DictCommandReturnType(TypedDict):
    message: str
    messageType: DictCommandReturnMessageType = DictCommandReturnMessageType.Private
    recipient: Member

CommandReturnType = StandardCommandReturnType | DictCommandReturnType

def getPrivateMessage(commandReturn: CommandReturnType) -> str:
    if isinstance(commandReturn, StandardCommandReturnType):
        return commandReturn.privateMessage
    if isinstance(commandReturn, DictCommandReturnType):
        if commandReturn["messageType"] == DictCommandReturnMessageType.Private:
            return commandReturn["message"]
        else:
            return None
    raise "Unknown command return: " + commandReturn

def getBroadcast(commandReturn: CommandReturnType) -> str:
    if isinstance(commandReturn, StandardCommandReturnType):
        return commandReturn.broadcast
    if isinstance(commandReturn, DictCommandReturnType):
        if commandReturn["messageType"] == DictCommandReturnMessageType.Broadcast:
            return commandReturn["message"]
        else:
            return None
    raise "Unknown command return: " + commandReturn
