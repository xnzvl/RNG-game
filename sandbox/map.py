from typing import Dict, Optional, Set
from typing import Tuple as Pair


class Map:
    def __init__(
            self,
            locationHolder: 'LocationHolder'
    ) -> None:
        self.areas: Dict[str, Area] = {}
        self.locationHolder = locationHolder

    def showArea(
            self
    ) -> None:
        pass


class LocationHolder:
    def __init__(self) -> None:
        self.area: Optional[Area] = None
        self.node: Optional[Node] = None


class Area:
    def __init__(
            self,
            areaName: str,
            areaAnchor: Pair[int, int]
    ) -> None:
        self.nodes: Set[Node] = set()
        self.name = areaName
        self.anchor = areaAnchor


class Node:
    def __init__(
            self,
            nodeName: str,
            nodePosition: Pair[int, int],
            locationHolder: LocationHolder
    ) -> None:
        self.name = nodeName
        self.adjacent: Set[Node] = set()
        self.position = nodePosition
        self.locationHolder = locationHolder


def createArea(
        map: Map,
        areaName: str,
        areaAnchor: Pair[int, int]
) -> Area:
    area = Area(areaName, areaAnchor)
    map.areas[areaName] = area

    return area


def createNodeInArea(
        map: Map,
        area: Area,
        nodeName: str
) -> Node:
    node = Node(nodeName, map.locationHolder)
    area.nodes.add(node)

    return node


def main() -> None:
    map = Map(LocationHolder())


if __name__ == "__main__":
    main()
