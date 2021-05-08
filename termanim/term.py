#!/usr/bin/env python3

from shutil import get_terminal_size
from .ansi import ANSICodes
from os import write

class TermScreen:
    """
    An interface for creating simple ASCII graphics on the terminal.
    """

    def __init__(self, size=None, offset=(0, 0), wrap=False, bg=""):
        """
        Sets the size and location of the drawing space on screen.
        Also allows screen wrapping, and a custom background colour.
        """

        if size is not None:
            self.lines, self.columns = size
        else:
            self.columns, self.lines = get_terminal_size()
        self.offset = offset
        self.wrap = wrap
        self.bg = bg
        self._reset_screen()
        self.redraw = {(i, j) for i in range(self.lines) for j in range(self.columns)}
        self.redraw_past = set()

    def _reset_screen(self):
        """
        Reset the screenbuffer.
        """

        self.screen = {(i, j): (" ", "", self.bg, False) for i in range(self.lines) for j in range(self.columns)}

    def draw(self, char, line, column, fg="", bg="", bold=False, *args):
        """
        Draw an object onto the screenbuffer.

        A drawable object is a list of tuples of the form (char, line, column, fg, bg, bold).
        Each tuple represents a single character on screen, at location (line, column).
        The foreground and background colours must be a valid key from the ANSICodes.FG_COLORS
        and ANSICodes.BG_COLORS dictionaries, such as "red" or "BLUE" (capitals denote the bright
        variant of the colour). The bold parameter determined whether the characters are printed
        in bold.

        For cells drawn onto pre-existing cell entries, the old character and foreground colour
        are overwritten. The background colour is also overwritten if non-empty. This means that
        new text can be layered onto old backgrounds.

        Cells out of bounds of the screen are simply ignored, unless the wrap option was set in which
        case the coordinates are wrapped around.
        """

        if not self.wrap and (line, column) not in self.screen:
            return
        line = line % self.lines
        column = column % self.columns
        if not bg:
            bg = self.screen[line, column][2]
        self.screen[line, column] = (char, fg, bg, bold) 
        self.redraw.add((line, column))

    def draw_things(self, *things):
        """
        Draws the supplied objects onto the screenbuffer, in order.
        """

        for thing in things:
            for cell in thing:
                self.draw(*cell)

    def _get_redraw_chars(self):
        """
        Converts the screenbuffer contents to proper ANSI codes, and streams them in order.
        Only the characters which need to be redrawn, i.e. those which differ from the previous
        buffer are supplied.
        """

        off_i, off_j = self.offset
        for (i, j) in sorted(self.redraw | self.redraw_past):
            char, fg, bg, bold = self.screen[i, j]
            fg_code = ANSICodes.FG_COLORS.get(fg, "")
            bg_code = ANSICodes.BG_COLORS.get(bg, "")
            bold_code = ANSICodes.BOLD if bold else ""
            yield ANSICodes.GOTO.format(1 + i + off_i, 1 + j + off_j) + \
                fg_code + bg_code + bold_code + char + ANSICodes.RESET

    def paint(self):
        """
        Flushes the screenbuffer to the terminal.
        """

        output = "".join(self._get_redraw_chars())
        write(1, output.encode("ascii"))

        self._reset_screen()
        self.redraw_past = self.redraw
        self.redraw = set()


class TermScreenRGB(TermScreen):
    """
    An extension of TermScreenRGB, supporting 24 bit colours (if supported by your terminal).
    """

    def __init__(self, size=None, offset=(0, 0), wrap=False, bg=(0, 0, 0)):
        super().__init__(size, offset, wrap, bg)

    def _mix_rgb(base, top, alpha):
        """
        Mix two RGB colours, according to a given alpha transparency value.
        """

        if not base and not top:
            return ""
        if not base:
            return top
        if not top:
            return base
        r1, g1, b1 = base
        r2, g2, b2 = top
        return r1 + (r2 - r1) * alpha, g1 + (g2 - g1) * alpha, b1 + (b2 - b1) * alpha

    def draw(self, char, line, column, fg="", bg="", bold=False, alpha=1.0, *args):
        """
        Foreground and background colours are now tuples of bytes, in an RGB format.
        For example, (0, 0, 0) denotes black, (255, 0, 0) denotes red and (255, 255, 255)
        denotes white. Drawable objects now have an additional alpha parameter, denoting transparency.

        New text characters overwrite previously present ones at the same coordinates.
        Foreground and background colours drawn are blended in with old ones as per the supplied
        alpha transparency.
        """

        if not self.wrap and (line, column) not in self.screen:
            return
        line = line % self.lines
        column = column % self.columns
        char_, fg_, bg_, bold_ = self.screen[line, column]
        fg_new = TermScreenRGB._mix_rgb(bg_, fg, alpha)
        bg_new = TermScreenRGB._mix_rgb(bg_, bg, alpha)
        self.screen[line, column] = (char, fg_new, bg_new, bold)
        self.redraw.add((line, column))

    def _get_redraw_chars(self):
        """
        Converts the screenbuffer contents to proper ANSI codes, and streams them in order.
        Only the characters which need to be redrawn, i.e. those which differ from the previous
        buffer are supplied.
        """

        off_i, off_j = self.offset
        for (i, j) in sorted(self.redraw | self.redraw_past):
            char, fg, bg, bold = self.screen[i, j]
            fg_code, bg_code = "", ""
            if fg:
                r, g, b = fg
            if bg:
                R, G, B = bg
            fg_code = ANSICodes.FG_RGB.format(int(r), int(g), int(b)) if fg else ""
            bg_code = ANSICodes.BG_RGB.format(int(R), int(G), int(B)) if bg else ""
            bold_code = ANSICodes.BOLD if bold else ""
            yield ANSICodes.GOTO.format(1 + i + off_i, 1 + j + off_j) + \
                fg_code + bg_code + bold_code + char + ANSICodes.RESET


class TermThings:
    """
    A collection of methods for generating drawable objects, and modifying their properties.

    Drawable objects are created as generators of tuples instead of lists. Note that most
    methods consume these generated tuples, so it is advised to list them if you need to modify
    the objects multiple times.

    Parameters such as the foreground and background colour will be strings if you intend
    to use the TermScreen class, or tuples if you intend to use the TermScreenRGB class.
    """

    def text(text, line, column, fg="", bg="", bold=False, alpha=1.0):
        """
        Generates a drawable text object, with supplied foreground colour, background colour and
        alpha transparency.
        """

        for n, char in enumerate(text):
            yield char, line, column + n, fg, bg, bold, alpha

    def box(char, lines, columns, fg="", bg="", bold=False, alpha=1.0):
        """
        Generates a drawable box, which is filled with the supplied character and is drawn
        with the supplied background colour and alpha transparency. The lines and columns
        are lists of the line and column coordinates to use. This means that you could generate
        a grid or hollow box with a boundary by simply passing lists of integers with missing values.
        """

        for i in lines:
            for j in columns:
                yield char, i, j, fg, bg, bold, alpha

    def fg(thing, fg):
        """
        Takes a drawable object and generates an identical one with the supplied foreground colour.
        """

        for (char, i, j, _, bg, bold, alpha) in thing:
            yield char, i, j, fg, bg, bold, alpha

    def bg(thing, bg):
        """
        Takes a drawable object and generates an identical one with the supplied background colour.
        """

        for (char, i, j, fg, _, bold, alpha) in thing:
            yield char, i, j, fg, bg, bold, alpha

    def alpha(thing, alpha):
        """
        Takes a drawable object and generates an identical one with the supplied alpha transparency.
        """

        for (char, i, j, fg, bg, bold, _) in thing:
            yield char, i, j, fg, bg, bold, alpha

    def gradient_right(thing, fg="", bg="", mix=1.0):
        """
        Takes a drawable object and generates an identical one with a foreground and background colour
        linear gradient from left to right. The existing colours are on the left, with the new colours
        fading in towards the right. The mix parameter determined the maximum mixing alpha transparency
        of the supplied colours, used while mixing the colours. Lower the mix, the fainter the colour 
        on the right.
        """

        thing = list(thing)
        columns = {j for _, _, j, *_ in thing}
        left, right = min(columns), max(columns)
        delta = right - left
        for (char, i, j, fg_left, bg_left, bold, alpha) in thing:
            alpha_mix = (j - left) / delta * mix
            fg_new = TermScreenRGB._mix_rgb(fg_left, fg, alpha_mix)
            bg_new = TermScreenRGB._mix_rgb(bg_left, bg, alpha_mix)
            yield char, i, j, fg_new, bg_new, bold, alpha

    def gradient_down(thing, fg="", bg="", mix=1.0):
        """
        Takes a drawable object and generates an identical one with a foreground and background colour
        linear gradient from top to bottom. The existing colours are on the top, with the new colours
        fading in towards the bottom. The mix parameter determined the maximum mixing alpha transparency
        of the supplied colours, used while mixing the colours. Lower the mix, the fainter the colour 
        on the bottom.
        """

        thing = list(thing)
        rows = {i for _, i, _, *_ in thing}
        top, bottom = min(rows), max(rows)
        delta = bottom - top
        for (char, i, j, fg_top, bg_top, bold, alpha) in thing:
            alpha_mix = (i - top) / delta * mix
            fg_new = TermScreenRGB._mix_rgb(fg_top, fg, alpha_mix)
            bg_new = TermScreenRGB._mix_rgb(bg_top, bg, alpha_mix)
            yield char, i, j, fg_new, bg_new, bold, alpha

    def gradient(thing, fg="", bg="", mixfunc=lambda y, x: 1.0):
        """
        Takes a drawable object and generates an identical one with a foreground and background colour
        gradient. The nature of the gradient is determined by the mixfunc, which maps coordinates
        (y, x) to mix strength values (between 0.0 and 1.0) of the new layer. Note that the coordinates
        y (top to bottom) and x (left to right) are each between 0.0 and 1.0 as well, representing fractions
        of the height and width. The origin (0, 0) is at the top left of the drawable object.

        For example, a linear gradient from left to right would be represented by a mixfunc of (y, x) -> x.
        A radial gradient would be of the form (y, x) -> a / ((0.5 - x)**2 + (0.5 - y)**2 + a), where the
        constant 'a' determines how steeply the new colour drops off from the center.
        """

        thing = list(thing)
        rows = {i for _, i, _, *_ in thing}
        columns = {j for _, _, j, *_ in thing}
        left, right = min(columns), max(columns)
        top, bottom = min(rows), max(rows)
        height, width = bottom - top, right - left
        for (char, i, j, fg_top, bg_top, bold, alpha) in thing:
            y, x = (i - top) / height, (j - left) / width
            alpha_mix = mixfunc(y, x)
            fg_new = TermScreenRGB._mix_rgb(fg_top, fg, alpha_mix)
            bg_new = TermScreenRGB._mix_rgb(bg_top, bg, alpha_mix)
            yield char, i, j, fg_new, bg_new, bold, alpha

    def translate(thing, lines, columns):
        """
        Takes a drawable object and generates an identical one with the coordinates translated by the
        supplied offsets.
        """

        for (char, i, j, fg, bg, bold, alpha) in thing:
            yield char, i + lines, j + columns, fg, bg, bold, alpha

    def intersection(*things):
        """
        Takes a number of drawable objects and returns a set of their intersecting coordinates.
        """

        things = [list(thing) for thing in things]
        cells = {(i, j) for _, i, j, *_ in things[0]}
        for thing in things[1:]:
            cells &= {(i, j) for _, i, j, *_  in thing}
        return cells
