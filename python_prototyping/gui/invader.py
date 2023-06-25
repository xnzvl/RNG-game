import tkinter as tk

from typing import List, Tuple


INVADER: List[List[int]] = [
    [3, 1, 6, 1],
    [4, 2, 2, 2],
    [0, 1, 3, 1, 4, 1, 3, 1],
    [1, 2, 2, 4, 2, 2],
    [3, 8],
    [1, 1, 1, 1, 1, 3, 1, 2, 1, 1],
    [2, 10],
    [2, 3, 1, 2, 1, 3],
    [2, 1, 1, 1, 4, 1, 1, 1],
    [2, 1, 2, 1, 2, 1, 2, 1],
    [3, 1, 1, 1, 2, 1, 1, 1],
    [5, 1, 2, 1],
    [5, 1, 2, 1],
    [5, 1, 2, 1]
]


def create_invader(
        master: tk.Tk,
        unit: int
) -> Tuple[tk.Frame, int, int]:
    frame = tk.Frame(master, bg="#DDDDDD")

    for row, line in enumerate(INVADER):
        frame_line(frame, unit, line, row)

    return frame, max([sum(l) for l in INVADER]) * unit, len(INVADER) * unit


def frame_line(
        master: tk.Frame,
        unit: int,
        steps: List[int],
        line: int
) -> None:
    black = False
    x = 0

    for step in steps:
        if black:
            tk.Frame(master, bg="#abe062") \
                .place(x=x*unit, y=line*unit, width=step*unit, height=unit)

        x += step
        black = not black
