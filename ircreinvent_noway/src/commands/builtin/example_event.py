from ....src.member import Member
from ..api import registerEvent, CommandReturnType, StandardCommandReturnType, EventType

def welcomeUser(user: Member) -> CommandReturnType:
    return StandardCommandReturnType(broadcast = f"Please welcome {user.username}!")

registerEvent(EventType.onUserJoin, welcomeUser)
