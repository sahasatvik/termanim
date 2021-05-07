#!/usr/bin/env python3

from time import time, sleep
from itertools import count
from math import sin, cos, pi

from .ansi import ANSICodes
from .term import TermScreen, TermThings

def main():
    term = TermScreen()
    
    width, height = 10, 5
    fps = 30
    period = 1 / fps

    t_0 = time()

    left, right = 0, term.columns - width
    delta = right - left
    x_0 = delta / 2
    time_period = 10
    omega = 2 * pi / time_period

    for tick in count():
        x = delta * (1 + sin(omega * tick / fps)) / 2
        speed = delta * omega / fps * cos(omega * tick / fps) / 2
        column = round(x)

        box = list(TermThings.box(" ", range(0, height), range(column, column + width), bg="white"))
        indicator = TermThings.text(f"Box has x coordinate {x:.2f} and speed {speed:.2f}", height + 1, 0)
        hello = list(TermThings.text("Hello World!", height // 2, (term.columns - 12) // 2, bold=True))

        intersection = TermThings.intersection(box, hello)
        if intersection:
            hello = TermThings.fg(hello, 'RED')    

        term.draw_things(box, hello, indicator)
        term.draw_things(TermThings.text("Text and box intersect at " + str(len(intersection)) + " cells", height + 2, 0))
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
