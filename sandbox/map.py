from typing import Dict, Optional, Set
from typing import Tuple as Pair

import drawer


class Location_holder:
    def __init__(self) -> None:
        self.area: Optional[Area] = None
        self.node: Optional[Node] = None


class Map:
    def __init__(
            self,
            location_holder: Location_holder
    ) -> None:
        self.area_dict: Dict[str, Area] = {}
        self.location_holder = location_holder

    def show_area(
            self
    ) -> None:
        pass


class Area:
    def __init__(
            self,
            area_name: str,
            area_anchor: Pair[int, int]
    ) -> None:
        self.node_dict: Dict[str, Node] = {}
        self.name = area_name
        self.anchor = area_anchor


class Node:
    def __init__(
            self,
            node_name: str,
            node_position: Pair[int, int],
            location_holder: Location_holder
    ) -> None:
        self.name = node_name
        self.adjacent: Set[Node] = set()
        self.position = node_position
        self.location_holder = location_holder


def add_bi_edge(
        a: Node,
        b: Node
) -> None:
    a.adjacent.add(b)
    b.adjacent.add(a)


def create_area(
        my_map: Map,
        area_name: str,
        area_anchor: Pair[int, int]
) -> Area:
    area = Area(area_name, area_anchor)
    my_map.area_dict[area_name] = area

    return area


def create_node_in_area(
        my_map: Map,
        area: Area,
        node_name: str,
        node_position: Pair[int, int]
) -> Node:
    node = Node(node_name, node_position, my_map.location_holder)
    area.node_dict[node_name] = node

    return node


def fill_map(
        my_map: Map
) -> None:
    area_a = create_area(my_map, "A", (0, 0))
    my_map.location_holder.area = area_a

    unit = 150

    a = create_node_in_area(my_map, area_a, "A", (0, 0))
    b = create_node_in_area(my_map, area_a, "B", (unit, 0))
    c = create_node_in_area(my_map, area_a, "C", (0, unit))
    d = create_node_in_area(my_map, area_a, "D", (unit, unit))
    e = create_node_in_area(my_map, area_a, "E", (-unit, -unit))

    add_bi_edge(a, b)
    add_bi_edge(a, e)
    add_bi_edge(a, c)
    add_bi_edge(b, d)
    add_bi_edge(c, d)


def main() -> None:
    my_map = Map(Location_holder())

    fill_map(my_map)

    drawer.MapWindow(my_map)


if __name__ == "__main__":
    main()
