import random
import tkinter as tk

from typing import Set, Tuple, Union

IntFloat = Union[int, float]
Vertex = Tuple[IntFloat, IntFloat]


UNIT = 20
RADIUS = 5
RANGE = 22

WIN_SIDE = (RANGE * 2 + 3) * UNIT

X = WIN_SIDE // 2
Y = X


def randfloat(
        a: int,
        b: int
) -> float:
    assert a < b
    return a + (b - a) * random.random()


def generate_vertices(
        vertices: Set[Vertex],
        number: int
) -> None:
    vertices_num = 0

    while vertices_num < number:
        coords = (randfloat(-RANGE, RANGE), randfloat(-RANGE, RANGE))

        if coords not in vertices:
            vertices.add(coords)
            vertices_num += 1


def place_vertex(
        canvas: tk.Canvas,
        vertex: Vertex,
        fill: str,
        label: str = None
) -> None:
    x, y = vertex

    canvas.create_oval(
        X + x * UNIT - RADIUS, Y + y * UNIT - RADIUS,
        X + x * UNIT + RADIUS, Y + y * UNIT + RADIUS,
        fill=fill,
        state="disabled"
    )

    if label is not None:
        canvas.create_text(
            X + x * UNIT + 2 * RADIUS,
            Y + y * UNIT - 2 * RADIUS,
            anchor="w",
            fill=fill,
            state="disabled",
            text=label
        )


def setup_canvas(
        canvas: tk.Canvas,
        number_of_vertices: int
) -> Set[Vertex]:
    vertices: Set[Vertex] = set()

    generate_vertices(vertices, number_of_vertices)

    for vertex in vertices:
        place_vertex(canvas, vertex, "gray")

    return vertices


def center_vertex(
        canvas: tk.Canvas,
        vertices: Set[Vertex]
) -> None:
    x_min, x_max = None, None
    y_min, y_max = None, None

    for x, y in vertices:
        if x_min is None or x < x_min:
            x_min = x
        if x_max is None or x > x_max:
            x_max = x

        if y_min is None or y < y_min:
            y_min = y
        if y_max is None or y > y_max:
            y_max = y

    assert x_min is not None and \
        x_max is not None and \
        y_min is not None and \
        y_max is not None

    place_vertex(
        canvas,
        ((x_min + x_max) / 2, (y_min + y_max) / 2),
        "blue",
        "B"
    )


def mean_vertex(
        canvas: tk.Canvas,
        vertices: Set[Vertex]
) -> None:
    x_sum: IntFloat = 0
    y_sum: IntFloat = 0

    for x, y in vertices:
        x_sum += x
        y_sum += y

    place_vertex(
        canvas,
        (x_sum / len(vertices), y_sum / len(vertices)),
        "green",
        "C"
    )


def main() -> None:
    window = tk.Tk()
    window.title("MAP-map_centre:testing")

    canvas = tk.Canvas(window, width=WIN_SIDE, height=WIN_SIDE)
    canvas.pack()

    # ==========================================

    vertices = setup_canvas(canvas, 20)

    place_vertex(canvas, (0, 0), "red", "A")

    center_vertex(canvas, vertices)
    mean_vertex(canvas, vertices)

    # ==========================================

    window.mainloop()


if __name__ == '__main__':
    main()
