#!/usr/bin/env python3

from time import time, sleep
from random import random, randint, choice
from math import cos, pi
from argparse import ArgumentParser

from .ansi import ANSICodes
from .term import TermScreenRGB, TermThings
from .anim import Effects

WHITE = (255, 255, 255)

def hex_to_rgb(h):
    return (h >> 16) % 256, (h >> 8) % 256, h % 256

def random_rgb():
    return int(256 * random()), int(256 * random()), int(256 * random())

def random_box():
    size = randint(4, 6)
    height, width = size, 2 * size + 1
    return TermThings.box(" ", range(0, height), range(0, width), bg=random_rgb(), alpha=0.0)

def fade_in_move(fps, alpha, delay, speed):
    fade_in = Effects.chain([
        Effects.static(fps, delay),
        Effects.alpha(fps, 1.0, alpha_final=alpha),
        Effects.forever(),
    ])
    def animate(thing):
        thing = list(thing)
        dy, dx = 0, 0
        for frame in fade_in(thing):
            dy += speed[0] / fps
            dx += speed[1] / fps
            yield TermThings.translate(frame, int(dy), int(dx))
    return animate

def pulse(fps, period, alpha_min=0.0, alpha_max=1.0):
    alphafunc = lambda t: alpha_min + (alpha_max - alpha_min) * (1 + cos(2 * pi * t)) * 0.5
    fade = Effects.alpha(fps, period, alphafunc=alphafunc)
    def animate(thing):
        thing = list(thing)
        while True:
            for frame in fade(thing):
                yield frame
    return animate

def main(fps, fg, bg, n_boxes, box_alpha, no_grad):
    term = TermScreenRGB(wrap=True, bg=bg)

    period = 1 / fps

    boxes = [TermThings.translate(random_box(), randint(0, term.lines - 5), randint(0, term.columns - 10)) for i in range(n_boxes)]
    if not no_grad:
        boxes = [TermThings.gradient(box, bg=random_rgb(), mixfunc=lambda y, x: 0.7 / ((1 - x)**2 + (1 - y)**2 + 1.0)) for box in boxes]
    directions = [choice([0, 1]) for i in range(n_boxes)]
    speeds = [(0.5 * randint(5, 15) * choice([-1, 1]) * a, randint(5, 15) * choice([-1, 1]) * (1 - a)) for a in directions]

    hello_text = "Hello World!"
    hello = TermThings.text(hello_text, term.lines // 2 - 1, (term.columns - len(hello_text)) // 2, fg=fg)
    
    fade_pulse = Effects.chain([
        Effects.alpha(fps, 1.0),
        pulse(fps, 2.0, alpha_min=0.5)
    ])

    frames = zip(
        *(fade_in_move(fps, box_alpha, 6 * random(), speed)(box) for box, speed in zip(boxes, speeds)),
        fade_pulse(hello)
    )

    # Start the animation loop.
    t_0 = time()
    for frame in frames:
        term.draw_things(*frame)
        term.paint()
        
        # Update timings, sleep for just the right amount of time.
        t = time()
        t_next = t_0 + period
        if t < t_next:
            sleep(t_next - t)
        t_0 = time()


if __name__ == '__main__':
    parser = ArgumentParser("Animations with python in the terminal")
    parser.add_argument("--fg", type=str, default="ffffff", help="foreground colour, e.g. 000000 for black, ffffff for white")
    parser.add_argument("--bg", type=str, default="000000", help="background colour")
    parser.add_argument("--fps", type=float, default=30, help="frames printed per second")
    parser.add_argument("--boxes", "-n", type=int, default=8, help="number of boxes")
    parser.add_argument("--box-alpha", type=float, default=0.9, help="opacity of boxes, between 0.0 and 1.0")
    parser.add_argument("--no-grad", action="store_true", help="do not put gradients on the boxes")
    args = parser.parse_args()
    fg = hex_to_rgb(int(args.fg, 16))
    bg = hex_to_rgb(int(args.bg, 16))
    n_boxes = max(args.boxes, 0)
    box_alpha = min(max(args.box_alpha, 0.0), 1.0)
    fps = max(args.fps, 0)
    try:
        print(ANSICodes.HIDE_CURSOR)
        main(fps, fg, bg, n_boxes, box_alpha, args.no_grad)
    except KeyboardInterrupt:
        pass
    finally:
        print(ANSICodes.CLEAR + ANSICodes.HOME + ANSICodes.SHOW_CURSOR, end="")
