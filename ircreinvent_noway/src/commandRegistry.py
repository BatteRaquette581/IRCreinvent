from .command import Command
class CommandNotFoundError(Exception):
    pass

class CommandRegistry:
    __registry: dict

    def __init__(self):
        self.__registry = {}
    
    def addCommand(self,name:str,command:Command):
        self.__registry[name] = command
    
    def getCommand(self,name:str) -> Command:
        try:
            return self.__registry[name]
        except KeyError as e:
            raise CommandNotFoundError(f"Command {name} not found") from e
    
    def getAllCommands(self):
        return self.__registry