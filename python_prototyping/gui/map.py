import tkinter as tk

from typing import Dict, Tuple


Placement = Tuple[int, int, int, int]  # x, y, width, height


class Map:
    def __init__(
            self,
            window: tk.Tk,
            width:  int,
            height: int
    ) -> None:
        window.title("Map")

        self.window = window
        self.width  = width
        self.height = height

        self.margin = width / 50
        self.gap    = self.margin / 2
        self.a      = self.margin * 2
        self.vertical_boost = 0
        self.separator      = self.a * (1 / 8)

        self.zoom_indicator = None
        self.switches: Dict[str, Tuple[bool, Tuple[Placement, tk.Frame]]] = dict()

        self.init_frames()
        self.draw_default()
        self.draw_switches()

    def init_frames(
            self
    ) -> None:
        self.switches["ne"] = (True, self.ne_frame())
        self.switches["ce"] = (True, self.ce_frame())
        self.switches["se"] = (True, self.se_frame())
        self.switches["nw"] = (True, self.nw_frame())
        self.switches["cw"] = (True, self.cw_frame())
        self.switches["sw"] = (True, self.sw_frame())

    def draw_default(
            self
    ) -> None:
        for is_displayed, subject in self.switches.values():
            if is_displayed:
                placement, frame = subject
                x, y, w, h = placement

                frame.place(x=x, y=y, width=w, height=h)

    def switch(
            self,
            switch_id: str
    ) -> None:
        is_displayed, (placement, frame) = self.switches[switch_id]

        if is_displayed:
            frame.place_forget()
        else:
            x, y, w, h = placement
            frame.place(x=x, y=y, width=w, height=h)

        self.switches[switch_id] = not is_displayed, (placement, frame)

    def draw_switches(
            self
    ) -> None:
        a_s = self.a / 3

        ne = tk.Button(self.window, bg="gray", command=lambda: self.switch("ne")) \
            .place(
                x=self.width-a_s, y=self.margin+self.vertical_boost+a_s,
                width=a_s, height=a_s
            )

        ce = tk.Button(self.window, bg="gray", command=lambda: self.switch("ce")) \
            .place(
                x=self.width-a_s, y=self.height/2-a_s/2,
                width=a_s, height=a_s
            )

        se = tk.Button(self.window, bg="gray", command=lambda: self.switch("se")) \
            .place(
                x=self.width-a_s, y=self.height-self.margin-self.vertical_boost-2*a_s,
                width=a_s, height=a_s
            )

        nw = tk.Button(self.window, bg="gray", command=lambda: self.switch("nw")) \
            .place(
                x=0, y=self.margin+self.vertical_boost+a_s,
                width=a_s, height=a_s
            )

        cw = tk.Button(self.window, bg="gray", command=lambda: self.switch("cw")) \
            .place(
                x=0, y=self.height/2-a_s/2,
                width=a_s, height=a_s
            )

        sw = tk.Button(self.window, bg="gray", command=lambda: self.switch("sw")) \
            .place(
                x=0, y=self.height-self.margin-self.vertical_boost-2*a_s,
                width=a_s, height=a_s
            )

    def ne_frame(
            self
    ) -> Tuple[Placement, tk.Frame]:
        frame = tk.Frame(self.window)

        tk.Button(frame, bg="gray", command=lambda: print("Focus on: pin")) \
            .place(x=0, y=self.separator, width=self.a, height=self.a)

        tk.Button(frame, bg="gray", command=lambda: print("Focus on: quest")) \
            .place(x=self.a+self.gap, y=self.separator, width=self.a, height=self.a)

        tk.Button(frame, bg="gray", command=lambda: print("Focus on: me")) \
            .place(x=2*(self.a+self.gap), y=self.separator, width=self.a, height=self.a)

        tk.Button(frame, bg="silver", state="disabled") \
            .place(x=3*(self.a+self.gap), y=0, width=self.separator, height=self.a+2*self.separator)

        tk.Button(frame, bg="gray", command=lambda: print("Map filter")) \
            .place(x=3*(self.a+self.gap)+self.gap+self.separator, y=self.separator, width=self.a, height=self.a)

        tk.Button(frame, bg="gray", command=lambda: print("Show map legend")) \
            .place(x=4*(self.a+self.gap)+self.gap+self.separator, y=self.separator, width=self.a, height=self.a)

        frame_width = 5 * (self.a + self.gap) + self.separator

        return (
            self.width - frame_width - self.margin, self.margin + self.vertical_boost - self.separator,
            frame_width, self.a + 2 * self.separator
        ), frame

    def ce_frame(
            self
    ) -> Tuple[Placement, tk.Frame]:
        
        def zoom_in() -> None:
            print("Zoom [+]")
            self.zoom_indicator.place(y=self.scroll_check(self.zoom_indicator.winfo_y() - 2 * self.separator))

        def zoom_out() -> None:
            print("Zoom [-]")
            self.zoom_indicator.place(y=self.scroll_check(self.zoom_indicator.winfo_y() + 2 * self.separator))

        frame = tk.Frame(self.window)

        tmp_a = self.a * (1 / 2)
        bar_len = (self.height - 2 * tmp_a - 2 * self.separator) * (2 / 5)

        tk.Button(frame, bg="gray", command=lambda: zoom_in()) \
            .place(x=0, y=0, width=tmp_a, height=tmp_a)

        zoom_bar = tk.Button(frame, bg="gray", state="disabled")
        zoom_bar.place(x=1.5*self.separator, y=tmp_a+self.separator, width=self.separator, height=bar_len)

        tk.Button(frame, bg="gray", command=lambda: zoom_out()) \
            .place(x=0, y=tmp_a+2*self.separator+bar_len, width=tmp_a, height=tmp_a)

        zoom_indicator = tk.Button(frame, bg="silver", state="disabled")
        zoom_indicator.place(x=0.5*self.separator, y=50, width=self.separator*3, height=self.separator)
        self.zoom_indicator = zoom_indicator

        zoom_bar.bind("<Enter>", lambda _: self.window.bind_all("<MouseWheel>", self.scroll))
        zoom_bar.bind("<Leave>", lambda _: self.window.unbind_all("<MouseWheel>"))

        frame_width = tmp_a
        frame_height = 2 * tmp_a + 2 * self.separator + bar_len

        return (
            self.width - frame_width - self.a * (1 / 4) - self.margin, self.height/2 - frame_height/2,
            frame_width, frame_height
        ), frame

    def se_frame(
            self
    ) -> Tuple[Placement, tk.Frame]:
        frame = tk.Frame(self.window)

        tk.Button(frame, bg="gray", command=lambda: print("Put down the map")) \
            .place(x=0, y=0, width=self.a, height=self.a)

        tk.Button(frame, bg="gray", command=lambda: print("Menu")) \
            .place(x=self.a+self.gap, y=0, width=self.a, height=self.a)

        frame_width = 2 * self.a + self.gap

        return (
            self.width - frame_width - self.margin, self.height - self.margin - self.vertical_boost - self.a,
            frame_width, self.a
        ), frame

    def nw_frame(
            self
    ) -> Tuple[Placement, tk.Frame]:
        frame = tk.Frame(self.window, bg="red")

        return (
            self.margin, self.margin,
            200, 200
        ), frame

    def cw_frame(
            self
    ) -> Tuple[Placement, tk.Frame]:
        frame = tk.Frame(self.window, bg="lime")

        frame_height = self.a + 2 * self.separator + (self.height - self.a - 2 * self.separator) * (2 / 5)

        return (
            self.margin, self.height / 2 - frame_height / 2,
            50, frame_height
        ), frame

    def sw_frame(
            self
    ) -> Tuple[Placement, tk.Frame]:
        frame = tk.Frame(self.window, bg="blue")

        return (
            self.margin, self.height - self.margin - 200,
            200, 200
        ), frame

    def scroll_check(
            self,
            y: int
    ) -> int:
        if y < (1 / 2) * self.a + self.separator:
            return (1 / 2) * self.a + self.separator
        elif (2 / 5) * self.height < y:
            return (2 / 5) * self.height 
        return y

    def scroll(
            self,
            event: tk.Event
    ) -> None:
        polarity = -event.delta // 120
        new_y = self.zoom_indicator.winfo_y() + 2 * self.separator * polarity
        self.zoom_indicator.place(y=self.scroll_check(new_y))
