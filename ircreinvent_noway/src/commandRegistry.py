class CommandNotFoundError(Exception):
    pass

class CommandRegistry:
    __registry: dict

    def __init__(self):
        self.__registry = {}
    
    def addCommand(self,name:str,callback:callable):
        self.__registry[name] = callback
    
    def getCommand(self,name:str):
        try:
            return self.__registry[name]
        except KeyError as e:
            raise CommandNotFoundError(f"Command {name} not found") from e
    