from typing import Tuple as Pair

import tkinter as tk
import map


class AreaWindow:
    def __init__(
            self,
            area: map.Area,
            location: map.Location_holder
    ) -> None:
        self.area = area

        self.root = tk.Tk()
        self.canvas = tk.Canvas(width=800, height=800)

        self.anchor = 400, 400
        self.root.resizable(False, False)
        self.root.title("MAP-area:testing")

        if location.node is not None:
            self.draw_edges()
            self.draw_nodes()

        self.canvas.pack()
        self.root.mainloop()

    def draw_edges(self) -> None:
        for src in self.area.node_dict.values():
            for dst in src.get_adjacent():
                draw_edge(self.canvas, src, dst, self.anchor)

    def draw_nodes(self) -> None:
        for node in self.area.node_dict.values():
            draw_node(self.canvas, node, self.anchor, "red" if node == node.location_holder.node else "black")


def draw_edge(
        canvas: tk.Canvas,
        node_a: map.Node,
        node_b: map.Node,
        anchor: Pair[int, int]
) -> None:
    x_a, y_a = node_a.position
    x_b, y_b = node_b.position

    x_anchor, y_anchor = anchor

    canvas.create_line(x_a + x_anchor, -y_a + y_anchor, x_b + x_anchor, -y_b + y_anchor)


def draw_node(
        canvas: tk.Canvas,
        node: map.Node,
        anchor: Pair[int, int],
        colour: str
) -> None:
    anchor_x, anchor_y = anchor
    node_x, node_y = node.position
    x = anchor_x + node_x
    y = anchor_y - node_y

    canvas.create_rectangle(x - 5, y - 5, x + 5, y + 5, fill=colour)
    canvas.create_text(x + 5, y - 5, anchor="sw", text=node.id)
