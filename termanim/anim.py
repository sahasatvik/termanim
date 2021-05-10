#!/usr/bin/env python3

from .term import TermThings, TermScreenRGB

class Animate:
    """
    A collection of methods for animating drawable objects.

    Each method accepts timing information such as the frame-rate, duration, and nature of
    the animation, and returns an effect. An effect is just a method which accepts a drawable object
    and yields a series of frames.

    Animating an object is intended to be of the following form.
    >>> from termanim.term import *
    >>> from termanim.anim import *
    >>> from itertools import zip_longest
    >>> from time import sleep

    >>> term = TermScreenRGB((2, 8))
    >>> fps = 30

    >>> hello = TermThings.text("Hello", 0, 0, fg=(255, 255, 255))
    >>> world = TermThings.text("World", 1, 2, fg=(255, 255, 255), alpha=0.0)

    >>> effect_hello = Animate.chain([
    >>>     Animate.alpha(fps, 1.0),
    >>>     Animate.forever()
    >>> ])
    >>> effect_world = Animate.chain([
    >>>     Animate.static(fps, 0.5),
    >>>     Animate.alpha(fps, 1.0),
    >>>     Animate.forever()
    >>> ])
    >>> frames = zip(effect_hello(hello), effect_world(world))

    >>> for frame in frames:
    >>>     term.draw_things(*frame)
    >>>     term.paint()
    >>>     sleep(1 / fps)

    Note that this animation will not stop until it is interrupted.
    """

    def chain(effects):
        """
        Chains together a list of effects, creating a new effect which is to act on 
        the same object.

        The last frame produced by one effect is passed into the next effect. For example, if the effects
        include a colour change (red -> blue) followed by a fade, the fade effect acts on the latest
        frame, which ought to be blue.
        """

        def animate(thing):
            thing = list(thing)
            for effect in effects:
                for frame in effect(thing):
                    thing = list(frame)
                    yield thing
        return animate

    def static(fps, duration):
        """
        Creates an effect which produces static, identical frames, useful for padding.
        """

        frames = int(duration * fps)
        def animate(thing):
            thing = list(thing)
            for i in range(frames):
                yield thing
        return animate
    
    def forever():
        """
        Creates an effect which produces identical frames forever.
        """

        def animate(thing):
            thing = list(thing)
            while True:
                yield thing
        return animate

    def alpha(fps, duration, alpha_init=0.0, alpha_final=1.0, alphafunc=None):
        """
        Creates an effect which fades the transparency between two values.

        The default is to fade in from 0.0 -> 1.0 linearly. The alpha_init and alpha_final can
        be set individually. An alphafunc can be supplied, which maps the fraction of the time
        elapsed (0.0 to 1.0) to an alpha transparency. For example, a fade out can be achieved with
        an alphafunc of the form t -> 1.0 - t.
        """

        if not alphafunc:
            alphafunc = lambda t: alpha_init + (alpha_final - alpha_init) * t
        frames = int(duration * fps)
        def animate(thing):
            thing = list(thing)
            for i in range(frames):
                yield TermThings.alpha(thing, alphafunc(i / frames))
        return animate
    
    def fg(fps, duration, fg_init="", fg_final="", fgfunc=None):
        """
        Creates an effect which fades the foreground colour between two values.

        The default is to fade between the given values linearly. An fgfunc can be supplied, which maps
        the fraction of the time elapsed (0.0 to 1.0) to a colour.
        """

        if not fgfunc:
            fgfunc = lambda t: TermScreenRGB._mix_rgb(fg_init, fg_final, t)
        frames = int(duration * fps)
        def animate(thing):
            thing = list(thing)
            for i in range(frames):
                yield TermThings.fg(thing, fgfunc(i / frames))
        return animate
    
    def bg(fps, duration, bg_init="", bg_final="", bgfunc=None):
        """
        Creates an effect which fades the background colour between two values.

        The default is to fade between the given values linearly. A bgfunc can be supplied, which maps
        the fraction of the time elapsed (0.0 to 1.0) to a colour.
        """

        if not bgfunc:
            bgfunc = lambda t: TermScreenRGB._mix_rgb(bg_init, bg_final, t)
        frames = int(duration * fps)
        def animate(thing):
            thing = list(thing)
            for i in range(frames):
                yield TermThings.bg(thing, bgfunc(i / frames))
        return animate


if __name__ == '__main__':
    from .term import *
    from time import time, sleep
    from itertools import zip_longest

    fps = 30
    period = 1 / 30
    
    term = TermScreenRGB(size=(8, 32))

    hello = TermThings.text("Hello World!", 2, 4, fg=(255, 255, 255))
    text  = TermThings.text("This is animation", 4, 8, fg=(255, 255, 255), alpha=0.0)
    
    fade_fg = Animate.chain([
        Animate.alpha(fps, 1.0),
        Animate.fg(fps, 1.0, (255, 255, 255), (255, 128, 0)),
        Animate.static(fps, 1.0),
        Animate.alpha(fps, 1.5, alpha_init=1.0, alpha_final=0.0),
        Animate.static(fps, 1.0),
    ])
    fade_bg = Animate.chain([
        Animate.static(fps, 0.5),
        Animate.alpha(fps, 1.0),
        Animate.bg(fps, 1.0, (0, 0, 0), (0, 128, 255)),
        Animate.static(fps, 0.5),
        Animate.alpha(fps, 1.5, alpha_init=1.0, alpha_final=0.0),
        Animate.static(fps, 0.5),
    ])

    frames = zip_longest(fade_fg(hello), fade_bg(text), fillvalue=[])
    
    t_0 = time()
    for frame in frames:
        term.draw_things(*frame)
        term.paint()

        t = time()
        t_next = t_0 + period
        if t < t_next:
            sleep(t_next - t)
        t_0 = time()
