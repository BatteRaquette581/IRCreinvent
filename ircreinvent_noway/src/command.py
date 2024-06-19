from .messageTypes import MessageTypes
class Command:
    description: str
    __command: callable

    def __init__(self,command:callable,description:str):
        self.__command = command
        self.description = description
    
    def execute(self,args,context):
        requiredArgs = list(self.__command.__code__.co_varnames).remove("context")
        if requiredArgs and len(args) != len(requiredArgs):
            return {
                "message":f"Missing parameter(s): {", ".join(list(self.__command.__code__.co_varnames)[len(args):])}",
                "type":MessageTypes.Private,
                "recepient":context["sender"]
            }
        if not requiredArgs:
            return self.__command(context=context)
        return self.__command(**dict(zip(requiredArgs, args)),context=context)