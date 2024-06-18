from .messageTypes import MessageTypes
class Command:
    description: str
    __command: callable

    def execute(self,*args,**context):
        if len(args) != len(list(self.__command.__code__.co_varnames)):
            return {
                "message":f"Missing parameter(s): {", ".join(self.__command.__code__.co_varnames)}",
                "type":MessageTypes.Private,
                "recepient":context["sender"]
            }
        return self.__command(*args,**context)