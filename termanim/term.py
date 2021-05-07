#!/usr/bin/env python3

from shutil import get_terminal_size
from .ansi import ANSICodes
from os import write

class TermScreen:
    def __init__(self, size=None, offset=(0, 0), wrap=False, bg=""):
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
        self.screen = {(i, j): (" ", "", self.bg, False) for i in range(self.lines) for j in range(self.columns)}

    def draw(self, char, line, column, fg="", bg="", bold=False, *args):
        if not self.wrap and (line, column) not in self.screen:
            return
        line = line % self.lines
        column = column % self.columns
        if not bg:
            bg = self.screen[line, column][2]
        self.screen[line, column] = (char, fg, bg, bold) 
        self.redraw.add((line, column))

    def draw_things(self, *things):
        for thing in things:
            for cell in thing:
                self.draw(*cell)

    def _get_redraw_chars(self):
        off_i, off_j = self.offset
        for (i, j) in sorted(self.redraw | self.redraw_past):
            char, fg, bg, bold = self.screen[i, j]
            fg_code = ANSICodes.FG_COLORS.get(fg, "")
            bg_code = ANSICodes.BG_COLORS.get(bg, "")
            bold_code = ANSICodes.BOLD if bold else ""
            yield ANSICodes.GOTO.format(1 + i + off_i, 1 + j + off_j) + \
                fg_code + bg_code + bold_code + char + ANSICodes.RESET

    def paint(self):
        output = "".join(self._get_redraw_chars())
        write(1, output.encode("ascii"))

        self._reset_screen()
        self.redraw_past = self.redraw
        self.redraw = set()


class TermScreenRGB(TermScreen):
    def __init__(self, size=None, offset=(0, 0), wrap=False, bg=(0, 0, 0)):
        super().__init__(size, offset, wrap, bg)

    def _mix_rgb(base, top, alpha):
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
        if not self.wrap and (line, column) not in self.screen:
            return
        line = line % self.lines
        column = column % self.columns
        char_, fg_, bg_, bold_ = self.screen[line, column]
        fg_new = TermRGB._mix_rgb(bg_, fg, alpha)
        bg_new = TermRGB._mix_rgb(bg_, bg, alpha)
        self.screen[line, column] = (char, fg_new, bg_new, bold)
        self.redraw.add((line, column))

    def _get_redraw_chars(self):
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
    def text(text, line, column, fg="", bg="", bold=False, alpha=1.0):
        for n, char in enumerate(text):
            yield char, line, column + n, fg, bg, bold, alpha

    def box(char, lines, columns, fg="", bg="", bold=False, alpha=1.0):
        for i in lines:
            for j in columns:
                yield char, i, j, fg, bg, bold, alpha

    def fg(thing, fg):
        for (char, i, j, _, bg, bold, alpha) in thing:
            yield char, i, j, fg, bg, bold, alpha

    def bg(thing, bg):
        for (char, i, j, fg, _, bold, alpha) in thing:
            yield char, i, j, fg, bg, bold, alpha

    def alpha(thing, alpha):
        for (char, i, j, fg, bg, bold, _) in thing:
            yield char, i, j, fg, bg, bold, alpha

    def intersection(*things):
        cells = {(i, j) for _, i, j, *_ in things[0]}
        for thing in things[1:]:
            cells &= {(i, j) for _, i, j, *_  in thing}
        return cells
