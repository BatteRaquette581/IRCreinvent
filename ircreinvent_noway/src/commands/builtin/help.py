from ....src.member import Member
from ..api import registerCommand, CommandReturnType, StandardCommandReturnType
from ..api.command import commandDescriptions

from typing import Iterable

def help(member: Member, arguments: Iterable[str]) -> CommandReturnType:
    if len(arguments) == 0:
        helpStrings = ["********************", "/help Command List", ""]
        for commandName, description in commandDescriptions.items():
            helpStrings.append(f"/{commandName} - {description}")
        helpStrings.append("********************")
        return StandardCommandReturnType(privateMessage = "\n".join(helpStrings))
    elif len(arguments) == 1:
        if arguments[0] in commandDescriptions.keys():
            return StandardCommandReturnType(privateMessage = f"/{arguments[0]}: {commandDescriptions[arguments[0]]}")
        else:
            return StandardCommandReturnType(privateMessage = f"Unknown command: {arguments[0]}")
    else:
        return StandardCommandReturnType(privateMessage = "The /help command cannot take in more than 1 argument. Type /help for a list of commands, or type /help (command name) for a command's description.")

registerCommand(help, name = "help", description = "Provides a list of all the commands with their descriptions!")
