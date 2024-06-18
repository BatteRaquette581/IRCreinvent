from functools import wraps
from typing import Callable, Iterable

from ....src.member import Member
from .commandreturntype import CommandReturnType

CommandType = Callable[[Member, Iterable[str]], CommandReturnType]
commands: dict[str, CommandType] = {}
command_descriptions: dict[str, str] = {}

def register_command(command_func: CommandType, name: str, description: str) -> None:
    commands[name] = command_func
    command_descriptions[name] = description
