import math
import heapq
import time
import tkinter as tk

from typing import Dict, List, Tuple, Set

import map


Vertex = Tuple[int, int]

DELAY = 0.01  # float seconds
CUSTOM = False

HEIGHT = 24
WIDTH = 2 * HEIGHT

UNIT = 27
RADIUS = UNIT // 3

SOURCE = (-WIDTH // 4, 0)
TARGET = (WIDTH // 4, 0)

FORBIDDEN: Set[Vertex] = set()

COLOUR_FORBIDDEN = "#5400a8"
COLOUR_HIT = "red"
COLOUR_SOURCE = "#00eaff"
COLOUR_TARGET = "#ff8d00"

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

    for x_add in range(-1, 2):
        for y_add in range(-1, 2):
            tmp_x = x + x_add
            tmp_y = y + y_add
            tmp_vertex = (tmp_x, tmp_y)

            if - WIDTH // 2 < tmp_x and tmp_x < WIDTH // 2 \
                    and - HEIGHT // 2 < tmp_y and tmp_y < HEIGHT // 2 \
                    and tmp_vertex not in FORBIDDEN \
                    and tmp_vertex != vertex:
                adjacent.add(tmp_vertex)

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


def seeker_pop(
        canvas: tk.Canvas,
        heap: List[Tuple[float, Vertex]],
        priorities: Dict[Vertex, Tuple[float, Vertex]],
        relative_target: Vertex
) -> Vertex:
    if relative_target == SOURCE:
        heap_colour = "#ffc72b"
        popped_colour = "#a87c00"
    else:
        heap_colour = "#0398fc"
        popped_colour = "#0062a8"

    priority, vertex = heapq.heappop(heap)
    travelled = priority - distance(vertex, relative_target)

    for adjacent in get_adjacent(vertex):
        alt_prio = travelled \
            + distance(vertex, adjacent) \
            + distance(adjacent, relative_target)

        if adjacent not in priorities or \
                alt_prio < priorities[adjacent][0]:
            draw_vertex(canvas, adjacent, heap_colour)
            draw_edge(canvas, vertex, adjacent)

            heapq.heappush(
                heap, (alt_prio, adjacent)
            )
            priorities[adjacent] = alt_prio, vertex

    draw_vertex(canvas, vertex, popped_colour)
    draw_vertex(canvas, SOURCE, COLOUR_SOURCE)

    return vertex


# THE PATHFINDING FUNCTION
def seeker(
        canvas: tk.Canvas,
        source: Vertex,
        target: Vertex,
        bidirectional: bool = False
) -> None:
    source_heap: List[Tuple[float, Vertex]] = list()
    target_heap: List[Tuple[float, Vertex]] = list()

    source_priorities: Dict[Vertex, Tuple[float, Vertex]] = dict()
    source_popped: Set[Vertex] = set()

    if bidirectional:
        target_priorities: Dict[Vertex, Tuple[float, Vertex]] = dict()
        target_popped: Set[Vertex] = set()

    heapq.heappush(
        source_heap, (distance(source, target), source)
    )
    heapq.heappush(
        target_heap, (distance(target, source), target)
    )

    while len(source_heap) > 0 and len(target_heap) > 0:
        pop_src = seeker_pop(canvas, source_heap, source_priorities, target)
        source_popped.add(pop_src)

        if bidirectional:
            pop_trg = seeker_pop(canvas, target_heap, target_priorities, source)
            target_popped.add(pop_trg)

            if pop_src in target_popped or pop_trg in source_popped:
                return

        elif pop_src == TARGET:
            draw_vertex(canvas, TARGET, COLOUR_HIT)
            return

        time.sleep(DELAY)

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

    forbid_area((-1, 2), (1, -2))

    # forbid_area((-1, 13), (1, -13))
    # forbid_area((-13, 7), (13, 5))
    # forbid_area((-13, -7), (13, -5))

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
        init_forbidden()

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
