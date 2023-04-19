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

        self.drawArea()

        self.canvas.pack()
        self.root.mainloop()

    def drawArea(self) -> None:
        area = self.map.locationHolder.area

        if area is None:
            return

        for node in area.nodeDict.values():
            drawNode(self.canvas, node, self.anchor)


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
