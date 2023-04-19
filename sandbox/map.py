from typing import Dict, Optional, Set
from typing import Tuple as Pair

import drawer


class Map:
    def __init__(
            self,
            locationHolder: 'LocationHolder'
    ) -> None:
        self.areaDict: Dict[str, Area] = {}
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
        self.nodeDict: Dict[str, Node] = {}
        self.name = areaName
        self.anchor = areaAnchor
        self.edges: Set[Pair[Node, Node]] = set()

    def addEdge(
            self
    ) -> None:
        pass


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
    map.areaDict[areaName] = area

    return area


def createNodeInArea(
        map: Map,
        area: Area,
        nodeName: str,
        nodePosition: Pair[int, int]
) -> Node:
    node = Node(nodeName, nodePosition, map.locationHolder)
    area.nodeDict[nodeName] = node

    return node


def fillMap(
        map: Map
) -> None:
    areaA = createArea(map, "A", (0, 0))
    map.locationHolder.area = areaA

    unit = 60

    createNodeInArea(map, areaA, "node0_A", (0, 0))
    createNodeInArea(map, areaA, "node1_A", (unit, 0))
    createNodeInArea(map, areaA, "node2_A", (0, unit))


def main() -> None:
    map = Map(LocationHolder())

    fillMap(map)

    drawer.MapWindow(map)


if __name__ == "__main__":
    main()
