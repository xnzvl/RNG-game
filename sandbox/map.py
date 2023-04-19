from typing import Dict, Optional, Set
from typing import Tuple as Pair

import drawer


class Location_holder:
    def __init__(self) -> None:
        self.node: Optional[Node] = None


class Area:
    def __init__(
            self,
            area_id: str,
            area_anchor: Pair[int, int]
    ) -> None:
        self.node_dict: Dict[str, Node] = {}
        self.id = area_id
        self.anchor = area_anchor

    def add_node(
            self,
            node: 'Node'
    ) -> 'Node':
        self.node_dict[node.id] = node
        return node


class Node:
    def __init__(
            self,
            node_id: str,
            node_position: Pair[int, int],
            location_holder: Location_holder
    ) -> None:
        self.id = node_id
        self.position = node_position
        self.location_holder = location_holder

    def get_adjacent(self) -> Set['Node']:
        raise ValueError("should be overriden")


class Cross_node(Node):
    def __init__(
            self,
            node_id: str,
            node_position: Pair[int, int],
            location_holder: Location_holder
    ) -> None:
        super().__init__(node_id, node_position, location_holder)

        self.adjacent: Set[Node] = set()

    def get_adjacent(self) -> Set[Node]:
        return self.adjacent


class Jump_node(Node):
    def __init__(
            self,
            node_id: str,
            node_position: Pair[int, int],
            location_holder: Location_holder,
            jump_target: Node
    ) -> None:
        super().__init__(node_id, node_position, location_holder)

        self.jump_target = jump_target

    def get_adjacent(self) -> Set[Node]:
        tmp = set()
        tmp.add(self.jump_target)
        return tmp


def prepare_area(
        area: Area,
        location_holder: Location_holder
) -> None:
    unit = 175

    a = area.add_node(Cross_node("A", (0, 0), location_holder))
    b = area.add_node(Cross_node("B", (-unit, 0), location_holder))
    c = area.add_node(Cross_node("C", (0, -2 * unit), location_holder))
    d = area.add_node(Cross_node("D", (-unit, -unit), location_holder))
    e = area.add_node(Cross_node("E", (unit, 0), location_holder))
    f = area.add_node(Cross_node("F", (-unit, unit), location_holder))
    g = area.add_node(Cross_node("G", (-2 * unit, -unit), location_holder))
    h = area.add_node(Cross_node("H", (-2 * unit, -2 * unit), location_holder))
    i = area.add_node(Cross_node("I", (unit, 2 * unit), location_holder))
    j = area.add_node(Cross_node("J", (-2 * unit, 2 * unit), location_holder))
    k = area.add_node(Cross_node("K", (2 * unit, -2 * unit), location_holder))
    l = area.add_node(Cross_node("L", (2 * unit, 2 * unit), location_holder))
    m = area.add_node(Cross_node("M", (2 * unit, unit), location_holder))

    location_holder.node = a


def main() -> None:
    area = Area("A", (0, 0))
    location_holder = Location_holder()

    prepare_area(area, location_holder)

    drawer.AreaWindow(area, location_holder)


if __name__ == "__main__":
    main()
