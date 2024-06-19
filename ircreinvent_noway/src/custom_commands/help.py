from ..command import Command
from ..messageTypes import MessageTypes

class HelpCommand(Command):
    description: str = "Provides a list of all the commands with their descriptions!"

    def execute(self, *args, **context):
        commands = context["commandRegistry"].getAllCommands()
        if len(args) == 0:
            help_strings = ["********************", "/help Command List", ""]
            for command_name in commands.keys():
                description = commands[command_name].description
                help_strings.append(f"/{command_name} - {description}")
            help_strings.append("********************")
            return {
                "message": "\n".join(help_strings),
                "type": MessageTypes.Private,
                "recepient": context["sender"]
            }
        elif len(args) == 1:
            if args[0] in commands.keys():
                return {
                    "message": f"/{args[0]} - {commands[args[0]].description}",
                    "type": MessageTypes.Private,
                    "recepient": context["sender"]
                }
            else:
                return {
                    "message": f"Unknown command: {args[0]}",
                    "type": MessageTypes.Private,
                    "recepient": context["sender"]
                }
        else:
            return {
                "message": "The /help command cannot take in more than 1 argument. Type /help for a list of commands, or type /help (command name) for a command's description.",
                "type": MessageTypes.Private,
                "recepient": context["sender"]
            }
        