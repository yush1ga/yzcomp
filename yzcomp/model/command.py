from typing import List, Any


class Option:
    def __init__(
            self,
            names: List[str] = [],
            arguments: Any = [],  # Func or List[str]
            description: str = ''
    ):
        self.names = names
        # flag option if arguments list is empty
        self.arguments = arguments
        self.description = description


class Command:
    def __init__(
            self,
            name: str,
            arguments: Any = [],  # Func or List[cmd] or List[str]
            options: List[Option] = [],
            description: str = ''
    ):
        self.name = name
        self.arguments = arguments
        self.options = options
        self.description = description


class Func:
    def __init__(
            self,
            name,
    ):
        self.name = name
