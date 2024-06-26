from ....src.member import Member
from ..api import registerCommand, CommandReturnType, StandardCommandReturnType
from ....src.messages import Messages

from typing import Iterable
from time import perf_counter

def ping(member: Member, arguments: Iterable[str]) -> CommandReturnType:
    t1 = perf_counter()
    Messages.sendMessage(member.socket, "/ping >  Measuring your latency...", member.aesKey)
    t2 = perf_counter()
    time_taken_ms = (t2 - t1) * 1000
    lines = ["*******************", "Pong!", f"Ping/latency: {time_taken_ms}ms", "*******************"]
    return StandardCommandReturnType(privateMessage = "\n".join(lines))

registerCommand(ping, name = "ping", description = "Measures your latency.")
