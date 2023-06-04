import math
import heapq
import time
import tkinter as tk

from typing import Dict, List, Tuple, Set

import map


Vertex = Tuple[int, int]

DELAY = 0.01  # float seconds
CUSTOM = False

HEIGHT = 51
WIDTH = 2 * HEIGHT

UNIT = 15
RADIUS = UNIT // 3

SOURCE = (-WIDTH // 4, 0)
TARGET = (WIDTH // 4, 0)

FORBIDDEN: Set[Vertex] = set()

COLOUR_CURRENT = "red"
COLOUR_FORBIDDEN = "#8d2dfa"
COLOUR_HIT = "white"
COLOUR_IN_HEAP = "#0398fc"
COLOUR_POPPED = "#20445c"
COLOUR_SOURCE = "#9fed18"
COLOUR_TARGET = "#ed7818"

# ========================================

ADJACENTS: Dict[Vertex, Set[Vertex]] = {}


def draw_vertex(
        canvas: tk.Canvas,
        vertex: Vertex,
        colour: str
) -> None:
    x, y = vertex

    canvas.create_oval(
        (x + WIDTH // 2) * UNIT + RADIUS, (-y + HEIGHT // 2) * UNIT + RADIUS,
        (x + WIDTH // 2) * UNIT - RADIUS, (-y + HEIGHT // 2) * UNIT - RADIUS,
        fill=colour,
        outline=colour,
        state="disabled"
    )
    canvas.update()


def draw_edge(
        canvas: tk.Canvas,
        vertex_a: Vertex,
        vertex_b: Vertex
) -> None:
    a_x, a_y = vertex_a
    b_x, b_y = vertex_b

    canvas.create_line(
        (a_x + WIDTH // 2) * UNIT, (-a_y + HEIGHT // 2) * UNIT,
        (b_x + WIDTH // 2) * UNIT, (-b_y + HEIGHT // 2) * UNIT,
        fill="black"
    )
    canvas.update()


def get_adjacent_from_position(
        vertex: Vertex
) -> Set[Vertex]:
    adjacent: Set[Vertex] = set()
    x, y = vertex

    for tmp_x in range(-1, 2):
        for tmp_y in range(-1, 2):
            maybe_adj = (x + tmp_x, y + tmp_y)

            if maybe_adj not in FORBIDDEN and maybe_adj != vertex:
                adjacent.add(maybe_adj)

    return adjacent


def get_adjacent_from_dict(
        vertex: Vertex
) -> Set[Vertex]:
    return ADJACENTS.get(vertex, set())


def distance(
        vertex_a: Vertex,
        vertex_b: Vertex
) -> float:
    a_x, a_y = vertex_a
    b_x, b_y = vertex_b

    return math.sqrt((a_x - b_x) ** 2 + (a_y - b_y) ** 2)


# THE PATHFINDING FUNCTION
def seeker(
        canvas: tk.Canvas,
        source: Vertex,
        target: Vertex
) -> None:
    heap: List[Tuple[float, Vertex]] = list()
    lowest_priorities: Dict[Vertex, float] = dict()

    heapq.heappush(
        heap, (distance(source, target), source)
    )

    while len(heap) > 0:
        priority, vertex = heapq.heappop(heap)
        draw_vertex(canvas, vertex, COLOUR_CURRENT)
        time.sleep(DELAY)

        travelled = priority - distance(vertex, target)

        if vertex == target:
            draw_vertex(canvas, vertex, COLOUR_HIT)
            return

        for adjacent in get_adjacent(vertex):
            alt_prio = travelled \
                + distance(vertex, adjacent) \
                + distance(adjacent, target)

            if adjacent not in lowest_priorities or \
                    alt_prio < lowest_priorities[adjacent]:
                draw_vertex(canvas, adjacent, COLOUR_IN_HEAP)
                draw_edge(canvas, vertex, adjacent)

                heapq.heappush(
                    heap, (alt_prio, adjacent)
                )
                lowest_priorities[adjacent] = alt_prio

        draw_vertex(canvas, vertex, COLOUR_POPPED)
        draw_vertex(canvas, SOURCE, COLOUR_SOURCE)

    print("unreachable")
    return None


def forbid_area(
        vertex_a: Vertex,
        vertex_b: Vertex
) -> None:
    x0, y0 = vertex_a
    x1, y1 = vertex_b

    for x in range(min(x0, x1), max(x0, x1) + 1):
        for y in range(min(y0, y1), max(y0, y1) + 1):
            FORBIDDEN.add((x, y))


def init_forbidden() -> None:
    # forbid_area((-WIDTH // 4 - 2, 2), (-WIDTH // 4 + 2, 2))
    # forbid_area((-WIDTH // 4 - 2, -2), (-WIDTH // 4 + 2, -2))
    # forbid_area((-WIDTH // 4 + 2, -2), (-WIDTH // 4 + 2, 2))

    forbid_area((-1, 13), (1, -13))
    forbid_area((-13, 7), (13, 5))
    forbid_area((-13, -7), (13, -5))

    # forbid_area((WIDTH // 4 - 2, 2), (WIDTH // 4 + 2, 2))
    # forbid_area((WIDTH // 4 - 2, -2), (WIDTH // 4 + 2, -2))
    # forbid_area((WIDTH // 4 - 2, -2), (WIDTH // 4 - 2, 2))


def map_to_vertices() -> None:
    the_map = map.init_map()

    for area in the_map.get_areas():
        for node in area.get_nodes():
            ADJACENTS[node.position] = set([n.position for n in node.get_adjacent()])


def custom_config() -> None:
    global SOURCE, TARGET, WIDTH, HEIGHT, UNIT, RADIUS, DELAY

    DELAY = 0.5

    SOURCE = (4, 4)
    TARGET = (-4, -4)

    WIDTH = 10
    HEIGHT = 10

    UNIT = 50
    RADIUS = 10


def draw_forbidden(
        canvas: tk.Canvas
) -> None:
    for vertex in FORBIDDEN:
        draw_vertex(canvas, vertex, COLOUR_FORBIDDEN)


def main() -> None:
    seeking = 0

    def start_seeker() -> None:
        nonlocal seeking
        seeking += 1

        if seeking == 1:
            seeker(canvas, SOURCE, TARGET)
        else:
            seeking = 2

    if CUSTOM:
        custom_config()
        map_to_vertices()
    else:
        init_forbidden()  # edit body of this func to manage forbidden areas

    window = tk.Tk()
    window.title("MAP-shortest_path_finder:testing")
    canvas = tk.Canvas(window, width=WIDTH * UNIT, height=HEIGHT * UNIT)
    canvas.pack()

    canvas.bind_all("q", lambda _: start_seeker())

    draw_forbidden(canvas)
    draw_vertex(canvas, SOURCE, COLOUR_SOURCE)
    draw_vertex(canvas, TARGET, COLOUR_TARGET)

    window.mainloop()


if __name__ == "__main__":
    get_adjacent = get_adjacent_from_dict if CUSTOM else get_adjacent_from_position
    main()
