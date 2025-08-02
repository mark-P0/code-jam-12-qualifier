from enum import Enum
from node import Node
from dataclasses import dataclass


class NodeMethods:
    def __init__(self, node: Node):
        self.node = node

    @property
    def classes(self, *, sep=" "):
        class_attr = self.node.attributes.get("class")
        if class_attr is None:
            return []

        classes = class_attr.split(sep)

        return classes


class SelectorType(Enum):
    TAG = "tag"
    ID = "id"
    CLASS = "class"


@dataclass
class SelectorPrefixItem:
    char: str
    selector_type: SelectorType


class SelectorPrefix:
    items = (
        SelectorPrefixItem(char="#", selector_type=SelectorType.ID),
        SelectorPrefixItem(char=".", selector_type=SelectorType.CLASS),
    )

    @classmethod
    def from_type(cls, selector_type: SelectorType):
        for item in cls.items:
            if item.selector_type == selector_type:
                return item.char

        return None

    @classmethod
    def from_char(cls, char: str):
        for item in cls.items:
            if item.char == char:
                return item.selector_type

        return None

    @classmethod
    def is_prefix(cls, char: str):
        return any(item.char == char for item in cls.items)


class SelectorItemPart:
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

    @property
    def prefix(self):
        return SelectorPrefix.from_type(self.type)


class SelectorItemParts:
    def __init__(self, selector: str):
        self.selector = selector

        self.tags = [
            part.text
            for part_str in self.__generate_string_parts()
            if (part := SelectorItemPart(part_str)) and part.type == SelectorType.TAG
        ]
        self.ids = [
            part.text
            for part_str in self.__generate_string_parts()
            if (part := SelectorItemPart(part_str)) and part.type == SelectorType.ID
        ]
        self.classes = [
            part.text
            for part_str in self.__generate_string_parts()
            if (part := SelectorItemPart(part_str)) and part.type == SelectorType.CLASS
        ]

    def __generate_string_parts(self):
        """
        Break selector string into (still string) parts

        ```
        selector = "article.container#card.bg-red-500.overflow-hidden"

        [*__generate_string_parts(selector)] == [
            "article",
            ".container",
            "#card",
            ".bg-red-500",
            ".overflow-hidden"
        ]
        ```
        """

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


class SelectorItem(SelectorItemParts):
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
    def __init__(self, selector: str, *, sep=", "):
        item_strs = selector.split(sep)

        self.selectors = [SelectorItem(item) for item in item_strs]

    def is_match(self, node: Node):
        has_any_matching_selector = any(
            selector.is_match(node) for selector in self.selectors
        )

        return has_any_matching_selector


Selector = SelectorList
