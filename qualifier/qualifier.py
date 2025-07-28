from __future__ import annotations
from node import Node
from selector import Selector


def generate_nodes(node: Node):
    yield node

    for child in node.children:
        yield from generate_nodes(child)


def generate_matching_nodes(node: Node, selector: str):
    selector_obj = Selector(selector)

    for current_node in generate_nodes(node):
        if selector_obj.is_match(current_node):
            yield current_node


def query_selector_all(node: Node, selector: str) -> list[Node]:
    """
    Given a node, the function will return all nodes, including children,
    that match the given selector.
    """

    return [*generate_matching_nodes(node, selector)]
