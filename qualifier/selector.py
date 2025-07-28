from node import Node
from typing import Literal


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


class SingleSelector:
    def __init__(self, selector: str):
        self.selector = selector

        self.tags: list[str] = []
        self.ids: list[str] = []
        self.classes: list[str] = []

        self.__separate()

    def __separate(self):
        class SelectorWord:
            word = ""
            word_type: Literal["tag", "class", "id", None] = None

            @classmethod
            def reset(cls):
                cls.word = ""
                cls.word_type = None

            @classmethod
            def finalize(cls):
                if cls.word_type == "tag":
                    self.tags.append(cls.word)
                if cls.word_type == "id":
                    self.ids.append(cls.word)
                if cls.word_type == "class":
                    self.classes.append(cls.word)

                cls.reset()

        class SelectorChar:
            prefixes = ["#", "."]

            @classmethod
            def is_prefix(cls, char: str):
                return char in cls.prefixes

        for idx, char in enumerate(self.selector):
            is_selector_prefix = SelectorChar.is_prefix(char)

            if idx == 0 and not is_selector_prefix:
                SelectorWord.word_type = "tag"
                SelectorWord.word += char

                continue

            if is_selector_prefix:
                SelectorWord.finalize()

                if char == ".":
                    SelectorWord.word_type = "class"
                if char == "#":
                    SelectorWord.word_type = "id"

                continue

            SelectorWord.word += char

        SelectorWord.finalize()

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
