from ....src.member import Member
from ..api import register_event, CommandReturnType, EventType

def welcome_user(user: Member) -> CommandReturnType:
    return CommandReturnType(broadcast = f"Please welcome {user.username}!")

register_event(EventType.onUserJoin, welcome_user)
