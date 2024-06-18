from typing import Callable
from enum import Enum

EventType = Enum("EventType", ["onMessageSend", "onUserJoin", "onUserLeave"])

registered_events: dict[EventType, list[Callable]] = {
    EventType.onMessageSend: [],
    EventType.onUserJoin: [],
    EventType.onUserLeave: [],
}

def register_event(event_type: EventType, func: Callable) -> None:
    registered_events[event_type].append(func)
