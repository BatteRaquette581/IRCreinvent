from typing import Callable
from enum import Enum

EventType = Enum("EventType", ["onMessageSend", "onUserJoin", "onUserLeave"])

registeredEvents: dict[EventType, list[Callable]] = {
    EventType.onMessageSend: [],
    EventType.onUserJoin: [],
    EventType.onUserLeave: [],
}

def registerEvent(eventType: EventType, func: Callable) -> None:
    registeredEvents[eventType].append(func)
