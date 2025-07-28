"""
div.container#card.bg-red-500.overflow-hidden
div .container #card .bg-red-500 .overflow-hidden
"""

from enum import Enum
from node import Node


class NodeMethods:
    def __init__(self, node: Node):
        self.node = node

    @property
    def classes(self, sep=" "):
        class_attr = self.node.attributes.get("class")
        if class_attr is None:
            return []

        classes = class_attr.split(sep)

        return classes


class SelectorType(Enum):
    TAG = "tag"
    ID = "id"
    CLASS = "class"


class SelectorPrefix:
    items = (
        ("#", SelectorType.ID),
        (".", SelectorType.CLASS),
    )

    @classmethod
    def from_type(cls, given_selector_type: SelectorType):
        for char, selector_type in cls.items:
            if selector_type == given_selector_type:
                return char

        return None

    @classmethod
    def from_char(cls, given_char: str):
        for char, selector_type in cls.items:
            if char == given_char:
                return selector_type

        return None

    @classmethod
    def is_prefix(cls, given_char: str):
        return any(given_char == char for char, _ in cls.items)


class SelectorPart:
    def __init__(self, part: str):
        self.part = part

    @property
    def type(self):
        if len(self.part) == 0:
            raise ValueError("Cannot get selector type from empty string")

        selector_type = SelectorPrefix.from_char(self.part[0])
        if selector_type is None:
            return SelectorType.TAG

        return selector_type

    @property
    def text(self):
        if self.type == SelectorType.TAG:
            return self.part

        return self.part[1:]  # Without prefix


class SelectorParts:
    def __init__(self, selector: str):
        self.selector = selector

        self.tags: list[str] = []
        self.ids: list[str] = []
        self.classes: list[str] = []

        self.__parse_selector()

    def __generate_string_parts(self):
        word = ""

        for idx, char in enumerate(self.selector):
            is_prefix = SelectorPrefix.is_prefix(char)

            if idx == 0:
                word += char
                continue

            if is_prefix:
                yield word
                word = ""

            word += char

        yield word

    def __parse_selector(self):
        for part_str in self.__generate_string_parts():
            part = SelectorPart(part_str)

            if part.type == SelectorType.TAG:
                self.tags.append(part.text)
            elif part.type == SelectorType.ID:
                self.ids.append(part.text)
            elif part.type == SelectorType.CLASS:
                self.classes.append(part.text)


class SingleSelector(SelectorParts):
    def __is_matching_tag(self, node: Node):
        if len(self.tags) == 0:
            return True

        is_tag_match = node.tag in self.tags

        return is_tag_match

    def __is_matching_id(self, node: Node):
        if len(self.ids) == 0:
            return True

        node_id = node.attributes.get("id")
        is_id_match = node_id in self.ids

        return is_id_match

    def __is_matching_classes(self, node: Node):
        if len(self.classes) == 0:
            return True

        node_classes = NodeMethods(node).classes
        if len(node_classes) == 0:
            return False  # At this point, selector has (requires) classes, but this node has none

        is_classes_match = all(cls in node_classes for cls in self.classes)

        return is_classes_match

    def is_match(self, node: Node):
        is_node_match = all(
            [
                self.__is_matching_tag(node),
                self.__is_matching_id(node),
                self.__is_matching_classes(node),
            ]
        )

        return is_node_match


class SelectorList:
    def __init__(self, selector: str, sep=", "):
        parts = selector.split(sep)

        self.selectors = [SingleSelector(part) for part in parts]

    def is_match(self, node: Node):
        has_any_matching_selector = any(
            selector.is_match(node) for selector in self.selectors
        )

        return has_any_matching_selector


Selector = SelectorList
