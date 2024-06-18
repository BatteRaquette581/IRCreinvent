from functools import wraps
from typing import Callable, Iterable

from ....src.member import Member
from .commandreturntype import CommandReturnType

CommandType = Callable[[Member, Iterable[str]], CommandReturnType]
commands: dict[str, CommandType] = {}
command_descriptions: dict[str, str] = {}

'''def command(command_func: CommandType) -> CommandType:
    @wraps(command_func)
    def wrapper(name: str, description: str):
        commands[name] = wrapper()
        command_descriptions[name] = description
        return command_func
    return wrapper'''

def register_command(command_func: CommandType, name: str, description: str) -> None:
    commands[name] = command_func
    command_descriptions[name] = description
