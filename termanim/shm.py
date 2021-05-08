#!/usr/bin/env python3

from time import time, sleep
from itertools import count
from math import sin, cos, pi

from .ansi import ANSICodes
from .term import TermScreen, TermThings

"""
A demo of the TermScreen and TermThings classes, with an animation of a block
undergoing simple harmonic motion.
"""

def main():
    term = TermScreen()
    
    # Set the width and height of the block, as number of lines and columns occupied.
    width, height = 10, 5

    # Set the frame-rate.
    fps = 30
    period = 1 / fps

    # Calculate the parameters required to execute simple harmonic motion.
    left, right = 0, term.columns - width
    delta = right - left
    x_0 = delta / 2
    time_period = 10
    omega = 2 * pi / time_period
    
    # Start the animation loop.
    t_0 = time()
    for tick in count():
        # Calculate position and speed of the block.
        x = delta * (1 + sin(omega * tick / fps)) / 2
        speed = delta * omega / fps * cos(omega * tick / fps) / 2
        column = round(x)

        # Create the box object.
        box = list(TermThings.box(" ", range(0, height), range(column, column + width), bg="white"))
        # Create a text object indicating the current position and speed.
        indicator = TermThings.text(f"Box has x coordinate {x:.2f} and speed {speed:.2f}", height + 1, 0)
        # Create a "Hello World!" text object centered on the screen.
        hello = list(TermThings.text("Hello World!", height // 2, (term.columns - 12) // 2, bold=True))

        # Colour the "Hello World!" text bright red if it intersects with the box.
        intersection = TermThings.intersection(box, hello)
        if intersection:
            hello = TermThings.fg(hello, 'RED')    

        # Draw all objects to screen. The order is respected, so the "Hello World!" text is layered
        # over the block.
        term.draw_things(box, hello, indicator)
        term.draw_things(TermThings.text("Text and box intersect at " + str(len(intersection)) + " cells", height + 2, 0))
        # Refresh the screen.
        term.paint()
        
        # Update timings, sleep for just the right amount of time.
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
