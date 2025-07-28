from enum import Enum


class SelectorType(Enum):
    TAG = "tag"
    ID = "id"
    CLASS = "class"


class SelectorCharPrefix:
    @classmethod
    def check(cls, char: str):
        if char == "#":
            return SelectorType.ID

        if char == ".":
            return SelectorType.CLASS

        return None


class SelectorChar: ...


class SelectorWord:
    def __init__(self):
        self.reset()

    def reset(self):
        self.text = ""
        self.type = None


class SelectorParts:
    def __init__(self, selector: str):
        self.selector = selector

        self.tags = []
        self.ids = []
        self.classes = []

        self.__separate()

    def __separate(self): ...


class SingleSelector: ...
