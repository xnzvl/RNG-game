from typing import Tuple, Set


Vertex = Tuple[float, float]


class Map:
    def __init__(
            self,
            name: str
    ) -> None:
        self.name = name
        self.areas: Set[Node] = set()

        self.cur_area: Area
        self.cur_level: Level
        self.cur_node: Node
        self.cur_target: Node

    @staticmethod
    def travel() -> None:
        pass


class Area:
    def __init__(
            self,
            name: str
    ) -> None:
        self.name = name
        self.map_offset: Vertex

        self.levels: Set[Level] = set()


class Level:
    def __init__(
            self,
            name: str
    ) -> None:
        self.name = name
        self.mean_center: Vertex

        self.nodes: Set[Node] = set()


class Node:
    def __init__(
            self,
            name: str,
            position: Vertex
    ) -> None:
        self.name = name
        self.position = position


def main() -> None:
    pass


if __name__ == '__main__':
    main()
