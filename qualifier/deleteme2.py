"""
selector = 'div.container#card'
[
    Part(type='tag',text='div',prefix=None),
    Part(type='class',text='container',prefix='.'),
    Part(type='id',text='card',prefix='#'),
]
"""

from enum import Enum
from dataclasses import dataclass
from pprint import pprint


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


@dataclass
class SelectorPart:
    type: SelectorType
    text: str

    def __str__(self):
        prefix = SelectorPrefix.from_type(self.type)
        if prefix is None:
            return self.text

        return prefix + self.text

    @classmethod
    def from_string(cls, selector: str):
        word = ""
        word_type: SelectorType | None = None

        for idx, char in enumerate(selector):
            prefix_type = SelectorPrefix.from_char(char)

            if idx == 0 and prefix_type is None:
                word_type = SelectorType.TAG
                word += char

                continue

            if prefix_type is not None:
                ## End of word
                if word_type is None:
                    raise ValueError("End of word but no word type set")

                yield SelectorPart(
                    type=word_type,
                    text=word,
                )

                ## Start of new word
                word = ""
                word_type = prefix_type

                continue

            word += char

        ## End of word
        if word_type is None:
            raise ValueError("End of word but no word type set")

        yield SelectorPart(
            type=word_type,
            text=word,
        )


pprint(
    [
        str(part)
        for part in SelectorPart.from_string(
            "div.container#card.bg-red-500.overflow-hidden"
        )
    ]
)


"""
div.container#card.bg-red-500.overflow-hidden
div .container #card .bg-red-500 .overflow-hidden

"""
