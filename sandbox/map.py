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

    def addBiEdge(
            self,
            a: 'Node',
            b: 'Node'
    ) -> None:
        a.adjacent.add(b)
        b.adjacent.add(a)


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

    unit = 150

    a = createNodeInArea(map, areaA, "A", (0, 0))
    b = createNodeInArea(map, areaA, "B", (unit, 0))
    c = createNodeInArea(map, areaA, "C", (0, unit))
    d = createNodeInArea(map, areaA, "D", (unit, unit))
    e = createNodeInArea(map, areaA, "E", (-unit, -unit))

    areaA.addBiEdge(a, b)
    areaA.addBiEdge(a, e)
    areaA.addBiEdge(a, c)
    areaA.addBiEdge(b, d)
    areaA.addBiEdge(c, d)


def main() -> None:
    map = Map(LocationHolder())

    fillMap(map)

    drawer.MapWindow(map)


if __name__ == "__main__":
    main()
