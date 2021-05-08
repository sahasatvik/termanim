#!/usr/bin/env python3

from time import time, sleep
from itertools import count
from math import sin, cos, pi

from .ansi import ANSICodes
from .term import TermScreenRGB, TermThings


WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def main():
    term = TermScreenRGB()

    size = min(term.columns // 2, term.lines) - 10
    width, height = size * 2 + 1, size
    
    box = TermThings.box(
        " ",
        range((term.lines - height) // 2, (term.lines + height) // 2), 
        range((term.columns - width) // 2, (term.columns + width) // 2),
        bg=RED
    )
    box = TermThings.gradient_right(box, bg=BLUE)
    box = TermThings.gradient_down(box, bg=GREEN, mix=0.8)
    box = list(box)

    hello = TermThings.text(
        "Hello World!",
        term.lines // 2 - 1,
        (term.columns - 12) // 2,
        fg=WHITE
    )
    hello = list(hello)

    slider_width, slider_height = 10, 5
    slider = TermThings.box(
        " ",
        range((term.lines - slider_height) // 2, (term.lines + slider_height) // 2),
        range(0, slider_width),
        bg=(128, 128, 255),
        alpha=0.5
    )
    slider = list(slider)
    
    fps = 30
    period = 1 / fps


    time_period = 2
    omega = 2 * pi / time_period

    t_0 = time()

    for tick in count():
        alpha = (2 + cos(omega * tick / fps)) / 3
        x = (term.columns - slider_width) * (1 - sin(omega / 5 * tick / fps)) / 2

        term.draw_things(box)
        term.draw_things(TermThings.translate(slider, 0, round(x)))
        term.draw_things(TermThings.alpha(hello, alpha))
        term.draw_things(TermThings.text(f"{x:.2f}", 0, 0, fg=WHITE))
        term.paint()
        
        t = time()
        t_next = t_0 + period
        if t < t_next:
            sleep(t_next - t)
        t_0 = time()


if __name__ == '__main__':
    try:
        print(ANSICodes.HIDE_CURSOR)
        main()
    except KeyboardInterrupt:
        pass
    finally:
        print(ANSICodes.SHOW_CURSOR)
