from ....src.member import Member
from ..api import register_command, CommandReturnType
from ..api.command import command_descriptions

from typing import Iterable

def help(member: Member, arguments: Iterable[str]) -> CommandReturnType:
    if len(arguments) == 0:
        help_strings = ["********************", "/help Command List", ""]
        for command_name, description in command_descriptions.items():
            help_strings.append(f"/{command_name} - {description}")
        help_strings.append("********************")
        return CommandReturnType(private_message = "\n".join(help_strings))
    elif len(arguments) == 1:
        if arguments[0] in command_descriptions.keys():
            return CommandReturnType(private_message = f"/{arguments[0]}: {command_descriptions[arguments[0]]}")
        else:
            return CommandReturnType(private_message = f"Unknown command: {arguments[0]}")
    else:
        return CommandReturnType(private_message = "The /help command cannot take in more than 1 argument. Type /help for a list of commands, or type /help (command name) for a command's description.")

register_command(help, name = "help", description = "Provides a list of all the commands with their descriptions!")
