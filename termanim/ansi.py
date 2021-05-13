#!/usr/bin/env python3

class ANSICodes:
    """
    An enumeration of commonly used ANSI codes.
    """

    # Basic control characters.
    RESET = "\033[0m"
    CLEAR = "\033[2J"
    HOME  = "\033[H"
    GOTO = "\033[{};{}H"                # lines, columns
    BOLD = "\033[1m"
    UNBOLD = "\033[2m"
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"

    # 24 bit colour code formats
    FG_RGB = "\033[38;2;{};{};{}m"      # red, green, blue
    BG_RGB = "\033[48;2;{};{};{}m"      # red, green, blue

    # Basic console foreground colours
    FG_BLACK   = "\033[30m"
    FG_RED     = "\033[31m"
    FG_GREEN   = "\033[32m"
    FG_YELLOW  = "\033[33m"
    FG_BLUE    = "\033[34m"
    FG_MAGENTA = "\033[35m"
    FG_CYAN    = "\033[36m"
    FG_WHITE   = "\033[37m"
    
    # Basic console background colours
    BG_BLACK   = "\033[40m"
    BG_RED     = "\033[41m"
    BG_GREEN   = "\033[42m"
    BG_YELLOW  = "\033[43m"
    BG_BLUE    = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN    = "\033[46m"
    BG_WHITE   = "\033[47m"

    # Bright variants
    FG_BLACK_BRIGHT   = "\033[90m"
    FG_RED_BRIGHT     = "\033[91m"
    FG_GREEN_BRIGHT   = "\033[92m"
    FG_YELLOW_BRIGHT  = "\033[93m"
    FG_BLUE_BRIGHT    = "\033[94m"
    FG_MAGENTA_BRIGHT = "\033[95m"
    FG_CYAN_BRIGHT    = "\033[96m"
    FG_WHITE_BRIGHT   = "\033[97m"
    
    # Bright variants
    BG_BLACK_BRIGHT   = "\033[100m"
    BG_RED_BRIGHT     = "\033[101m"
    BG_GREEN_BRIGHT   = "\033[102m"
    BG_YELLOW_BRIGHT  = "\033[103m"
    BG_BLUE_BRIGHT    = "\033[104m"
    BG_MAGENTA_BRIGHT = "\033[105m"
    BG_CYAN_BRIGHT    = "\033[106m"
    BG_WHITE_BRIGHT   = "\033[107m"

    # A dictionary of foreground colours
    FG_COLORS = {
        'black'   : FG_BLACK,
        'red'     : FG_RED,
        'green'   : FG_GREEN,
        'yellow'  : FG_YELLOW,
        'blue'    : FG_BLUE,
        'magenta' : FG_MAGENTA,
        'cyan'    : FG_CYAN,
        'white'   : FG_WHITE,
        'BLACK'   : FG_BLACK_BRIGHT,
        'RED'     : FG_RED_BRIGHT,
        'GREEN'   : FG_GREEN_BRIGHT,
        'YELLOW'  : FG_YELLOW_BRIGHT,
        'BLUE'    : FG_BLUE_BRIGHT,
        'MAGENTA' : FG_MAGENTA_BRIGHT,
        'CYAN'    : FG_CYAN_BRIGHT,
        'WHITE'   : FG_WHITE_BRIGHT
    }
    
    # A dictionary of background colours
    BG_COLORS = {
        'black'   : BG_BLACK,
        'red'     : BG_RED,
        'green'   : BG_GREEN,
        'yellow'  : BG_YELLOW,
        'blue'    : BG_BLUE,
        'magenta' : BG_MAGENTA,
        'cyan'    : BG_CYAN,
        'white'   : BG_WHITE,
        'BLACK'   : BG_BLACK_BRIGHT,
        'RED'     : BG_RED_BRIGHT,
        'GREEN'   : BG_GREEN_BRIGHT,
        'YELLOW'  : BG_YELLOW_BRIGHT,
        'BLUE'    : BG_BLUE_BRIGHT,
        'MAGENTA' : BG_MAGENTA_BRIGHT,
        'CYAN'    : BG_CYAN_BRIGHT,
        'WHITE'   : BG_WHITE_BRIGHT
    }
    

# A simple colour test, which prints all combinations of foreground and background
# colours to the terminal.
if __name__ == '__main__':
    for i, fg in ANSICodes.FG_COLORS.items():
        for j, bg in ANSICodes.BG_COLORS.items():
            print(f"{fg}{bg} {i:8s} {ANSICodes.RESET}", end="")
        print()
