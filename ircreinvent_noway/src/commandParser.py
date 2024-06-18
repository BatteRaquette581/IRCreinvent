from .command import Command
from dataclasses import dataclass

class CommandParser:
    prefix: str
    
    def __init__(self,prefix:str = "/"):
        self.prefix = prefix
    
    def isCommand(self,string:str):
        return string.startswith(self.prefix)
    
    def parseCommand(self,string:str):
        if not self.isCommand(string):
            return (None,None)
        tokens = string[len(self.prefix):].split(" ")
        if len(tokens) < 1:
            return (None,None)
        name = tokens[0]
        parameters = tokens[1:]
        return (name,parameters)
