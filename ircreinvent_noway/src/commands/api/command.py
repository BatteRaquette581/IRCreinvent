from typing import Callable, Iterable

from ....src.member import Member
from .commandreturntype import CommandReturnType

CommandType = Callable[[Member, Iterable[str]], CommandReturnType]
commands: dict[str, CommandType] = {}
commandDescriptions: dict[str, str] = {}

def registerCommand(commandFunc: CommandType, name: str, description: str) -> None:
    commands[name] = commandFunc
    commandDescriptions[name] = description
