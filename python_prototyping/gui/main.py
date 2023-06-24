import tkinter as tk

import map

from enum import Enum


WINDOW_RATIO = 3 / 5


class Context(Enum):
    DESTROY = -1

    MAP = 0


class Window:
    def __init__(
            self,
            init: Context
    ) -> None:
        self.width  = int(1920 * WINDOW_RATIO)
        self.height = int(1080 * WINDOW_RATIO)

        self.root = tk.Tk()
        self.root.geometry("%dx%d" % (self.width, self.height))
        self.root.resizable(False, False)

        self.change_context(init)

        self.root.mainloop()

    def change_context(
            self,
            context: Context
    ) -> None:
        for widget in self.root.slaves():
            widget.destroy()

        match context:
            case Context.DESTROY:
                self.root.destroy()
            case Context.MAP:
                map.Map(self.root, self.width, self.height)


def main() -> None:
    Window(Context.MAP)


if __name__ == "__main__":
    main()
