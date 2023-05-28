from typing import Tuple as Pair

import tkinter as tk
import map


SOURCE_COLOUR = "red"

TARGET_COLOUR = "#008cff"
TRACK_COLOUR = "#296aa3"
PATH_COLOUR = TRACK_COLOUR


UNIT = 100
CANVAS_CENTER = (5, 5)


class Display_map:
    def __init__(
            self,
            map: map.Map
    ) -> None:
        self.map = map

        self.root = tk.Tk()
        self.canvas = tk.Canvas(width=UNIT * 10, height=UNIT * 10)
        self.canvas.bind("<Button-1>", lambda _: self.refresh())

        # self.root.resizable(False, False)
        self.root.title("MAP-area:testing")

        self.canvas.pack()

        self.refresh()
        self.root.mainloop()

    def refresh(
            self
    ) -> None:
        self.canvas.delete("all")

        self.draw_edges()
        self.draw_nodes()

    def draw_nodes(
            self
    ) -> None:
        for area in self.map.get_areas():
            for node in area.get_nodes():
                draw_node(self.canvas, node, area.anchor, self.map)

    def draw_edges(
            self
    ) -> None:
        for area in self.map.get_areas():
            for src in area.get_nodes():
                for dst in src.get_adjacent():
                    draw_edge(self.canvas, src, dst, area.anchor, self.map)


def draw_edge(
        canvas: tk.Canvas,
        node_a: map.Node,
        node_b: map.Node,
        area_anchor: Pair[int, int],
        map: map.Map
) -> None:
    canvas_x, canvas_y = CANVAS_CENTER
    area_x, area_y = area_anchor
    a_x, a_y = node_a.position
    b_x, b_y = node_b.position

    line_colour = PATH_COLOUR \
        if node_a in map.path_nodes and node_b in map.path_nodes \
        else "gray"

    canvas.create_line(
        (a_x + area_x + canvas_x) * UNIT, (-a_y + area_y + canvas_y) * UNIT,
        (b_x + area_x + canvas_x) * UNIT, (-b_y + area_y + canvas_y) * UNIT,
        fill=line_colour,
        width=2
    )


def draw_node(
        canvas: tk.Canvas,
        node: map.Node,
        area_anchor: Pair[int, int],
        map: map.Map
) -> None:
    canvas_x, canvas_y = CANVAS_CENTER
    area_x, area_y = area_anchor
    node_x, node_y = node.position

    x = (canvas_x + area_x + node_x) * UNIT
    y = (canvas_y + area_y - node_y) * UNIT

    match node:
        case map.current_node:
            colour = SOURCE_COLOUR
        case map.current_target:
            colour = TARGET_COLOUR
        case _:
            colour = TRACK_COLOUR if node in map.path_nodes else "black"

    canvas.create_text(x + 5, y - 5, anchor="sw", text=node.id)
    canvas.tag_bind(
        canvas.create_rectangle(x - 5, y - 5, x + 5, y + 5, fill=colour),
        "<Button-1>",
        lambda _: map.set_target(node)
    )
