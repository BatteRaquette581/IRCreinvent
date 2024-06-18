from dataclasses import dataclass

@dataclass
class CommandReturnType:
    private_message: str = None
    broadcast: str = None
