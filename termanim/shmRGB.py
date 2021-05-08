#!/usr/bin/env python3

from time import time, sleep
from itertools import count
from math import sin, cos, pi

from .ansi import ANSICodes
from .term import TermScreenRGB, TermThings

"""
A demo of the TermScreenRGB class, with 24 bit colour objects displayed on the terminal.
"""

WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def main():
    term = TermScreenRGB()

    # Set the width and height of the large gradient box.
    size = min(term.columns // 2, term.lines) - 10
    width, height = size * 2 + 1, size
    
    # Create a large box centered on the screen, coloured red.
    box = TermThings.box(
        " ",
        range((term.lines - height) // 2, (term.lines + height) // 2), 
        range((term.columns - width) // 2, (term.columns + width) // 2),
        bg=RED
    )
    # Apply a linear gradient from left (red) to right (blue).
    box = TermThings.gradient_right(box, bg=BLUE)
    # Apply a linear gradient from top (pre-existing red/blue) to bottom (green).
    # The mix value of 0.8 indicates that the green is toned down.
    box = TermThings.gradient_down(box, bg=GREEN, mix=0.8)
    # Apply a radial(ish) gradient on the bottom right corner (yellow).
    # The mixfunc indicates the strength of the yellow colour, which is maximum at the (1.0, 1.0)
    # coordinate and fades away with distance.
    box = TermThings.gradient(box, bg=(255, 255, 0), mixfunc=lambda y, x: 0.2 / ((1 - x)**2 + (1 - y)**2 + 0.2))
    box = list(box)

    # Create a "Hello World!" text object centered on the screen.
    hello = TermThings.text(
        "Hello World!",
        term.lines // 2 - 1,
        (term.columns - 12) // 2,
        fg=WHITE
    )
    hello = list(hello)

    # Create an oscillating block/slider, bluish in colour and slightly transparent.
    slider_width, slider_height = 10, 5
    slider = TermThings.box(
        " ",
        range((term.lines - slider_height) // 2, (term.lines + slider_height) // 2),
        range(0, slider_width),
        bg=(128, 128, 255),
        alpha=0.5
    )
    slider = list(slider)
    
    # Set the frame-rate.
    fps = 30
    period = 1 / fps

    # Parameters for simple harmonic motion.
    time_period = 2
    omega = 2 * pi / time_period

    # Start the animation loop.
    t_0 = time()
    for tick in count():
        # The "Hello World!" text pulses periodically (2 seconds), by having its
        # alpha transparency vary sinusoidally between 0.33 and 1.0
        alpha = (2 + cos(omega * tick / fps)) / 3
        # The sliding block also oscillates periodically (10 seconds) from left right.
        x = (term.columns - slider_width) * (1 - sin(omega / 5 * tick / fps)) / 2

        # Draw the gradient box.
        term.draw_things(box)
        # Draw the sliding box at the appropriate location.
        term.draw_things(TermThings.translate(slider, 0, round(x)))
        # Draw the "Hello World!" text with the appropriate transparency.
        term.draw_things(TermThings.alpha(hello, alpha))
        # Draw a text indicator on the top right, denoting the position of the sliding box.
        term.draw_things(TermThings.text(f"{x:.2f}", 0, 0, fg=WHITE))
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
