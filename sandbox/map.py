from typing import List, Optional, Set, Tuple

import abc

import drawer


class Map:
    def __init__(
            self
    ) -> None:
        self.current_area:   Optional['Area'] = None
        self.current_node:   Optional['Node'] = None
        self.current_target: Optional['Node'] = None

        self.areas: Set['Area'] = set()

    def add_area(
            self,
            area: 'Area'
    ) -> None:
        self.areas.add(area)

    def get_areas(
            self,
    ) -> Set['Area']:
        return self.areas

    def set_area(
            self,
            area: 'Area'
    ) -> None:
        self.current_area = area

    def set_current_node(
            self,
            node: 'Node'
    ) -> None:
        self.current_node = node

    def set_target(
            self,
            node: 'Node'
    ) -> None:
        if self.current_target == node:
            self.set_current_node(node)
        else:
            self.current_target = node


class Area:
    def __init__(
            self,
            anchor: Tuple[int, int],
            id: str
    ) -> None:
        self.anchor = anchor
        self.id = id
        self.nodes: Set[Node] = set()

    def add_node(
            self,
            node: 'Node'
    ) -> 'Node':
        self.nodes.add(node)
        return node

    def get_nodes(
            self
    ) -> Set['Node']:
        return self.nodes


class Node(abc.ABC):
    def __init__(
            self,
            id: str,
            position: Tuple[int, int]
    ) -> None:
        self.id = id
        self.position = position

    @abc.abstractmethod
    def get_adjacent(
            self
    ) -> Set['Node']:
        ...


class Cross_node(Node):
    def __init__(
            self,
            id: str,
            position: Tuple[int, int]
    ) -> None:
        super().__init__(id, position)

        self.adjacent: Set[Node] = set()

    def get_adjacent(
            self
    ) -> Set[Node]:
        return self.adjacent

    def add_adjacent(
            self,
            node: Node
    ) -> None:
        self.adjacent.add(node)


class Jump_node(Node):
    def __init__(
            self,
            node_id: str,
            node_position: Tuple[int, int],
            jump_target: Node
    ) -> None:
        super().__init__(node_id, node_position)

        self.jump_target = jump_target

    def get_adjacent(
            self
    ) -> Set[Node]:
        tmp = set()
        tmp.add(self.jump_target)
        return tmp


def create_edge(
        node_a: Cross_node,
        node_b: Cross_node
) -> None:
    node_a.add_adjacent(node_b)
    node_b.add_adjacent(node_a)


def link_node_with(
        src: Cross_node,
        targets: List[Cross_node]
) -> None:
    for target in targets:
        create_edge(src, target)


def init_map() -> Map:
    the_map = Map()

    area_A = Area((0, 0), "AREA-A")

    a = area_A.add_node(Cross_node("A", (-4, 4)))
    b = area_A.add_node(Cross_node("B", (-3, 4)))
    c = area_A.add_node(Cross_node("C", (0, 4)))
    d = area_A.add_node(Cross_node("D", (3, 4)))
    e = area_A.add_node(Cross_node("E", (4, 4)))
    f = area_A.add_node(Cross_node("F", (-2, 3)))
    g = area_A.add_node(Cross_node("G", (1, 3)))
    h = area_A.add_node(Cross_node("H", (-4, 2)))
    i = area_A.add_node(Cross_node("I", (0, 2)))
    j = area_A.add_node(Cross_node("J", (4, 2)))
    k = area_A.add_node(Cross_node("K", (-2, 1)))
    l = area_A.add_node(Cross_node("L", (2, 1)))
    m = area_A.add_node(Cross_node("M", (-3, 0)))
    n = area_A.add_node(Cross_node("N", (0, 0)))
    o = area_A.add_node(Cross_node("O", (3, 0)))
    p = area_A.add_node(Cross_node("P", (-1, -1)))
    q = area_A.add_node(Cross_node("Q", (2, -1)))
    r = area_A.add_node(Cross_node("R", (-4, -2)))
    s = area_A.add_node(Cross_node("S", (0, -2)))
    t = area_A.add_node(Cross_node("T", (4, -2)))
    u = area_A.add_node(Cross_node("U", (-2, -3)))
    v = area_A.add_node(Cross_node("V", (1, -3)))
    w = area_A.add_node(Cross_node("W", (-4, -4)))
    x = area_A.add_node(Cross_node("X", (0, -4)))
    y = area_A.add_node(Cross_node("Y", (3, -4)))
    z = area_A.add_node(Cross_node("Z", (4, -4)))

    the_map.set_current_node(n)
    the_map.add_area(area_A)

    link_node_with(a, [b, f, h])
    link_node_with(b, [a, f, h])
    link_node_with(c, [f, g, i, k])
    link_node_with(d, [e, f, g, j])
    link_node_with(e, [d, g, j, l])
    link_node_with(f, [a, b, c, d, h, i])
    link_node_with(g, [c, d, e, i, l])
    link_node_with(h, [a, b, f, m])
    link_node_with(i, [c, f, g, k, l])
    link_node_with(j, [d, e, l, o, q])
    link_node_with(k, [c, i, m, n, p])
    link_node_with(l, [d, e, g, i, j])
    link_node_with(m, [a, h, r, u, w])
    link_node_with(n, [k, p, s])
    link_node_with(o, [j, l, q, t])
    link_node_with(p, [m, n, s, x])
    link_node_with(q, [j, o, s, t, v])
    link_node_with(r, [m, u, w])
    link_node_with(s, [n, p, q, v, x])
    link_node_with(t, [o, q, v, y, z])
    link_node_with(u, [k, r, w, x])
    link_node_with(v, [q, s, t, x, y, z])
    link_node_with(w, [r, u])
    link_node_with(x, [p, s, u, v])
    link_node_with(y, [t, v, z])
    link_node_with(z, [q, t, v, y])

    return the_map


def main() -> None:
    the_map = init_map()
    drawer.Display_map(the_map)


if __name__ == "__main__":
    main()
