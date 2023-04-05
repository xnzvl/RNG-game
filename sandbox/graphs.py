from typing import Optional, Set

# import tkinter as tk
import random


class Location():
    def __init__(
            self,
            verbose: bool
    ) -> None:
        self.area: Optional[str] = None
        self.node: Optional[str] = None

        self.verbose = verbose

    def setNode(
            self,
            node: str
    ) -> None:
        self.node = node

        if self.verbose:
            print(f"[new node]: {self.node}")

    def setLocation(
            self,
            node: Optional[str],
            area: Optional[str]
    ) -> None:
        self.node = node
        self.area = area

        if self.verbose:
            if node is None and area is None:
                print("travelling")
            else:
                print(f"[NEW LOCATION]: {self.area} | {self.node}")


class Node:
    def __init__(
            self,
            nodeId:   str,
            location: Location
    ) -> None:
        self.nodeId = nodeId
        self.location = location

    def travelTo(
            self,
            destination: 'Node'
    ) -> None:
        self.location.setLocation(None, None)
        destination.arrive()

    def arrive(
            self
    ) -> None:
        self.location.setNode(self.nodeId)


class JumpNode(Node):
    def __init__(
            self,
            nodeId:   str,
            target:   Node,
            location: Location
    ) -> None:
        super().__init__(nodeId, location)

        self.jumpTarget = target

    def travelTo(
            self,
            destination: Node
    ) -> None:
        super().travelTo(destination)

    def arrive(
            self
    ) -> None:
        super().arrive()

        self.travelTo(self.jumpTarget)


class RegularNode(Node):
    def __init__(
            self,
            nodeId:   str,
            location: Location
    ) -> None:
        super().__init__(nodeId, location)

        self.adjacent: Set[Node] = set()

    def addAdjacent(
            self,
            newOnes: Set[Node]
    ) -> None:
        self.adjacent |= newOnes

    def travelTo(
            self,
            destination: Node
    ) -> None:
        assert destination in self.adjacent

        super().travelTo(destination)


def goToNode(
        source:      Node,
        destination: Node
) -> Node:
    source.travelTo(destination)
    return destination


# =============================================================================


def createSmallArea(
        aName:    str,
        location: Location
) -> Set[RegularNode]:
    area: Set[RegularNode] = set()

    for nName in range(ord('a'), ord('f') + 1):
        area.add(RegularNode(f"{aName}_{chr(nName)}", location))

    for node in area:
        choice = random.choice(list(area.copy() ^ {node}))

        choice.adjacent.add(node)
        node.adjacent.add(choice)

    return area


def testRegulars() -> None:
    locationHolder = Location(True)
    area_A = createSmallArea("A", locationHolder)

    for node in area_A:
        print(node.nodeId, [n.nodeId for n in node.adjacent])


def main() -> None:
    testRegulars()


if __name__ == '__main__':
    main()
