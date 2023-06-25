import tkinter as tk

from invader import create_invader
from typing import Dict, Tuple

Placement = Tuple[int, int, int, int]  # x, y, width, height


ZOOM_RANGE = 1 / 4
FONT = "system"


class Map:
    def __init__(
            self,
            window: tk.Tk,
            width:  int,
            height: int
    ) -> None:
        window.title("PROTOTYPE:Map")

        self.window = window
        self.width  = width
        self.height = height

        self.margin = width / 50
        self.gap    = self.margin / 2
        self.a      = self.margin * 2
        self.vertical_boost = 0
        self.separator      = self.a * (1 / 8)

        self.display = None

        self.zoom_indicator = None
        self.switches: Dict[str, Tuple[bool, Tuple[Placement, tk.Frame]]] = dict()

        self.min_scroll = (1 / 2) * self.a + self.separator
        self.max_scroll = (2 / 5) * self.height

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

        self.window.update()

        self.update_display()

    def draw_default(
            self
    ) -> None:
        for is_displayed, subject in self.switches.values():
            if is_displayed:
                placement, frame = subject
                x, y, w, h = placement

                frame.place(x=x, y=y, width=w, height=h)

    def update_display(
            self
    ) -> None:
        zoom = self.zoom_percentage()

        if self.display is not None:
            old_display, _, _ = self.display
            old_display.destroy()

        self.display = create_invader(self.window, int((self.a / 2) * zoom))
        display_frame, width, height = self.display

        display_frame.place(
            x=self.width/2-width/2, y=self.height/2-height/2,
            width=width, height=height
        )

        self.window.update()

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

        tk.Button(self.window, bg="gray", command=lambda: self.switch("ne")) \
            .place(
                x=self.width-a_s, y=self.margin+self.vertical_boost+a_s,
                width=a_s, height=a_s
            )

        tk.Button(self.window, bg="gray", command=lambda: self.switch("ce")) \
            .place(
                x=self.width-a_s, y=self.height/2-a_s/2,
                width=a_s, height=a_s
            )

        tk.Button(self.window, bg="gray", command=lambda: self.switch("se")) \
            .place(
                x=self.width-a_s, y=self.height-self.margin-self.vertical_boost-2*a_s,
                width=a_s, height=a_s
            )

        tk.Button(self.window, bg="gray", command=lambda: self.switch("nw")) \
            .place(
                x=0, y=self.margin+self.vertical_boost+a_s,
                width=a_s, height=a_s
            )

        tk.Button(self.window, bg="gray", command=lambda: self.switch("cw")) \
            .place(
                x=0, y=self.height/2-a_s/2,
                width=a_s, height=a_s
            )

        tk.Button(self.window, bg="gray", command=lambda: self.switch("sw")) \
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
        
        def bind_zoom(
                widget: tk.Widget
        ) -> None:
            widget.bind("<Enter>", lambda _: self.window.bind_all("<MouseWheel>", lambda e: self.scroll(e.delta // 120)))
            widget.bind("<Leave>", lambda _: self.window.unbind_all("<MouseWheel>"))

        def zoom_in() -> None:
            print("Zoom [+]")
            self.scroll(1)

        def zoom_out() -> None:
            print("Zoom [-]")
            self.scroll(-1)

        frame = tk.Frame(self.window)

        tmp_a = self.a * (1 / 2)
        bar_len = (self.height - 2 * tmp_a - 2 * self.separator) * (2 / 5)

        tk.Button(frame, bg="gray", command=lambda: zoom_in()) \
            .place(x=0, y=0, width=tmp_a, height=tmp_a)

        tk.Button(frame, bg="gray", command=lambda: zoom_out()) \
            .place(x=0, y=tmp_a+2*self.separator+bar_len, width=tmp_a, height=tmp_a)

        zoom_tolerance = tk.Frame(frame)
        zoom_tolerance.place(x=0, y=tmp_a+self.separator, width=tmp_a, height=bar_len)

        zoom_bar = tk.Button(frame, bg="gray", state="disabled")
        zoom_bar.place(x=1.5*self.separator, y=tmp_a+self.separator, width=self.separator, height=bar_len)

        zoom_indicator = tk.Button(frame, bg="silver", state="disabled")
        zoom_indicator.place(
            x=0.5*self.separator, y=tmp_a+self.separator/2+bar_len/2,
            width=self.separator*3, height=self.separator
        )
        self.zoom_indicator = zoom_indicator

        bind_zoom(zoom_tolerance)
        bind_zoom(zoom_bar)
        bind_zoom(zoom_indicator)

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
        frame = tk.Frame(self.window)

        frame_width = self.width * (1 / 2)
        frame_height = self.height * (1 / 5)
        unit = frame_height * (1 / 10)

        area_h = 7 * unit
        area = tk.Frame(frame)
        area.place(x=unit, y=unit, width=frame_width-self.margin/2, height=area_h)
        tk.Label(area, text="Overworld", font=(FONT, -int(area_h))) \
            .place(x=0, y=0, height=area_h)

        view_h = 2 * unit
        view = tk.Frame(frame)
        view.place(
            x=unit*3, y=frame_height-view_h,
            width=frame_width-self.margin, height=view_h
        )
        tk.Label(view, text="View level: whole map", font=(FONT, -int(view_h))) \
            .place(x=0, y=0, height=view_h)

        return (
            self.margin, self.margin,
            frame_width, self.height * (1 / 5)
        ), frame

    def cw_frame(
            self
    ) -> Tuple[Placement, tk.Frame]:
        frame = tk.Frame(self.window)

        frame_width = self.width / 4
        frame_height = self.a + 2 * self.separator + (self.height - self.a - 2 * self.separator) * (2 / 5)

        txt = tk.Label(
            frame,
            text="""Overworld\n"""
            """├ School\n"""
            """│ ├ 1st floor\n"""
            """│ │ └ A018\n"""
            """│ └ 2nd floor\n"""
            """│   ├ A118\n"""
            """│   └ B124\n"""
            """├ Track\n"""
            """│ ├ Football cage\n"""
            """│ ├ Basketball cage\n"""
            """│ ├ Volleyball court\n"""
            """│ ├ Football field\n"""
            """│ └ Athletics track\n"""
            """└ Outside\n"""
            """  ├ Armillary sphere\n"""
            """  ├ Park\n"""
            """  └ Jewish memorial""",
            font=(FONT, -int(self.a/3)),
            justify="left"
        )
        txt.place(x=self.a/5, y=(frame_height-txt.winfo_reqheight())/2)

        return (
            self.margin, self.height / 2 - frame_height / 2,
            frame_width, frame_height
        ), frame

    def sw_frame(
            self
    ) -> Tuple[Placement, tk.Frame]:
        frame = tk.Frame(self.window)

        frame_width = self.width * (1 / 2)
        frame_height = self.height * (1 / 5)
        unit = frame_height / 12
        indent = 5 * unit

        header_h = 3 * unit
        header = tk.Frame(frame)
        header.place(x=0, y=0, width=frame_width, height=header_h)
        tk.Label(header, text="Location of:", font=(FONT, -int(header_h))) \
            .place(x=unit, y=0, height=header_h)

        location_h = 2 * unit
        location_me = tk.Frame(frame)
        location_me.place(x=indent, y=unit*3.5, width=frame_width-unit, height=location_h)
        tk.Label(location_me, text="me:\tSchool, A018", font=(FONT, -int(location_h))) \
            .place(x=0, y=0, height=location_h)

        location_quest = tk.Frame(frame)
        location_quest.place(x=indent, y=unit*6, width=frame_width-unit, height=location_h)
        tk.Label(location_quest, text="quest:\tOutside, Armillary sphere", font=(FONT, -int(location_h))) \
            .place(x=0, y=0, height=location_h)

        location_pin = tk.Frame(frame)
        location_pin.place(x=indent, y=unit*8.5, width=frame_width-unit, height=location_h)
        tk.Label(location_pin, text="pin:\tTrack, Football cage", font=(FONT, -int(location_h))) \
            .place(x=0, y=0, height=location_h)

        return (
            self.margin, self.height - self.margin - frame_height,
            frame_width, frame_height
        ), frame

    def zoom_percentage(
            self
    ) -> float:
        range_min = 2 - ZOOM_RANGE
        range_max = ZOOM_RANGE

        return round(
            ((range_max - range_min) * (self.zoom_indicator.winfo_y() - self.min_scroll))
            / (self.max_scroll - self.min_scroll)
            + range_min, 2
        )

    def boundary_check(
            self,
            y: float
    ) -> float:
        if y < self.min_scroll:
            return self.min_scroll
        elif self.max_scroll < y:
            return self.max_scroll 
        return y

    def scroll(
            self,
            polarity: int
    ) -> None:
        new_y = self.zoom_indicator.winfo_y() + (-2) * polarity * self.separator
        self.zoom_indicator.place(y=self.boundary_check(new_y))
        self.window.update()
        self.update_display()