#!/usr/bin/env python3

from shutil import get_terminal_size
from .ansi import ANSICodes
from os import write

class TermScreen:
    def __init__(self, size=None, offset=(0, 0), wrap=False):
        if size is not None:
            self.lines, self.columns = size
        else:
            self.columns, self.lines = get_terminal_size()
        self.offset = offset
        self.wrap = wrap
        self.screen = {(i, j): (" ", "", "", False) for i in range(self.lines) for j in range(self.columns)}
        self.redraw = {(i, j) for i in range(self.lines) for j in range(self.columns)}
        self.redraw_past = set()

    def draw(self, char, line, column, fg="", bg="", bold=False):
        if not self.wrap and (line, column) not in self.screen:
            return
        line = line % self.lines
        column = column % self.columns
        if not bg:
            _, _, bg_, _ = self.screen[line, column]
            bg = bg_
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

        self.screen = {(i, j): (" ", "", "", False) for i in range(self.lines) for j in range(self.columns)}
        self.redraw_past = self.redraw
        self.redraw = set()


class TermThings:
    def text(text, line, column, fg="", bg="", bold=False):
        for n, char in enumerate(text):
            yield char, line, column + n, fg, bg, bold

    def box(char, lines, columns, fg="", bg="", bold=False):
        for i in lines:
            for j in columns:
                yield char, i, j, fg, bg, bold

    def fg(thing, fg):
        for (char, i, j, _, bg, bold) in thing:
            yield char, i, j, fg, bg, bold

    def bg(thing, bg):
        for (char, i, j, fg, _, bold) in thing:
            yield char, i, j, fg, bg, bold

    def intersection(*things):
        cells = {(i, j) for _, i, j, _, _, _ in things[0]}
        for thing in things[1:]:
            cells &= {(i, j) for _, i, j, _, _, _ in thing}
        return cells

