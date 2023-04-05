from typing import Tuple, Set

# import tkinter as tk


class Location():
    def __init__(
            self,
            verbose: bool
    ) -> None:
        self.area = None
        self.node = None

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
            node: str,
            area: str
    ) -> None:
        self.node = node
        self.area = area

        if self.verbose:
            print(f"[NEW LOCATION]: {self.area} | {self.node}")

    def getLocation(
            self
    ) -> Tuple[str, str]:
        return self.area, self.node


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


class RegularNode(Node):
    def __init__(
            self,
            nodeId:   str,
            location: Location
    ) -> None:
        super().__init__(nodeId, location)

        self.adjacent = set()

    def addAjacent(
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


def testRegulars() -> None:
    location = Location(True)

    node_Aa = RegularNode("a", location)
    node_Ab = RegularNode("b", location)
    node_Ac = RegularNode("c", location)

    node_Aa.addAjacent({node_Ab, node_Ac})
    node_Ab.addAjacent({node_Aa, node_Ac})
    node_Ac.addAjacent({node_Aa, node_Ab})

    for n in [node_Aa, node_Ab, node_Ac]:
        assert len(n.adjacent) == 2

    node_Aa.arrive()
    currentNode = node_Aa
    currentNode.travelTo(node_Ab)
    currentNode.travelTo(node_Ac)


def main() -> None:
    testRegulars()


if __name__ == '__main__':
    main()
