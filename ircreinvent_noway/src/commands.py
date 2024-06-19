from .commandRegistry import CommandRegistry,CommandNotFoundError
from .commandParser import CommandParser
from .command import Command

class Commands:
    __commandRegistry: CommandRegistry
    __commandParser: CommandParser

    def __init__(self,prefix:str="/"):
        self.__commandParser = CommandParser(prefix)
        self.__commandRegistry = CommandRegistry()

    def add(self,name:str,command:Command):
        self.__commandRegistry.addCommand(name,command)

    def get(self,name:str):
        return self.__commandRegistry.getCommand(name)

    def getAll(self):
        return self.__commandRegistry.getAllCommands()

    def isCommand(self,string:str):
        return self.__commandParser.isCommand(string)


    def execute(self,string:str,context:dict):
        context.update({
            "commands":self,
            "commandParser":self.__commandParser,
            "commandRegistry":self.__commandRegistry
            })
        name,params = self.__commandParser.parseCommand(string)
        return self.__commandRegistry.getCommand(name).execute(args=params,context=context)


