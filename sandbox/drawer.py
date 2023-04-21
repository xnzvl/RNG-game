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
        self.canvas.bind("<Button-1>", lambda _: self.refresh())

        self.anchor = 400, 400
        self.root.resizable(False, False)
        self.root.title("MAP-area:testing")

        if location.node is not None:
            self.refresh()

        self.canvas.pack()
        self.root.mainloop()

    def refresh(self) -> None:
        self.canvas.delete("all")

        self.draw_edges()
        self.draw_nodes()

    def draw_edges(self) -> None:
        for src in self.area.node_dict.values():
            for dst in src.get_adjacent():
                draw_edge(self.canvas, src, dst, self.anchor)

    def draw_nodes(self) -> None:
        for node in self.area.node_dict.values():
            draw_node(self.canvas, node, self.anchor)


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
        anchor: Pair[int, int]
) -> None:
    anchor_x, anchor_y = anchor
    node_x, node_y = node.position
    x = anchor_x + node_x
    y = anchor_y - node_y

    colour = "red" if node == node.location_holder.node else (
        "blue" if node == node.location_holder.target else "black"
    )

    canvas.create_text(x + 5, y - 5, anchor="sw", text=node.id)
    canvas.tag_bind(
        canvas.create_rectangle(x - 5, y - 5, x + 5, y + 5, fill=colour),
        "<Button-1>",
        lambda _: set_target(node)
    )


def set_target(
        target: map.Node
) -> None:
    lh = target.location_holder

    if target == lh.target:
        lh.node = target
        lh.target = None

    lh.target = target
