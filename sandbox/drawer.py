from typing import Tuple as Pair

import tkinter as tk
import map


class MapWindow:
    def __init__(
            self,
            map: map.Map
    ) -> None:
        self.map = map

        self.root = tk.Tk()
        self.canvas = tk.Canvas(width=800, height=800)

        self.anchor = 400, 400
        self.root.resizable(False, False)
        self.root.title("Map")

        if map.locationHolder.area is not None:
            self.drawEdges()
            self.drawNodes()

        self.canvas.pack()
        self.root.mainloop()

    def drawEdges(self) -> None:
        for src in self.map.locationHolder.area.nodeDict.values():
            for dst in src.adjacent:
                drawEdge(self.canvas, src, dst, self.anchor)

    def drawNodes(self) -> None:
        for node in self.map.locationHolder.area.nodeDict.values():
            drawNode(self.canvas, node, self.anchor)


def drawEdge(
        canvas: tk.Canvas,
        nodeA: map.Node,
        nodeB: map.Node,
        anchor: Pair[int, int]
) -> None:
    xA, yA = nodeA.position
    xB, yB = nodeB.position

    xAnchor, yAnchor = anchor

    canvas.create_line(xA + xAnchor, yA + yAnchor, xB + xAnchor, yB + yAnchor)


def drawNode(
        canvas: tk.Canvas,
        node: map.Node,
        anchor: Pair[int, int]
) -> None:
    anchorX, anchorY = anchor
    nodeX, nodeY = node.position
    x = anchorX + nodeX
    y = anchorY + nodeY

    canvas.create_rectangle(x - 5, y - 5, x + 5, y + 5, fill="black")
    canvas.create_text(x + 5, y - 5, anchor="sw", text=node.name)
