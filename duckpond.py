#!/usr/bin/env python3
# from sys import argv, exit
import curses
from curses import wrapper
from random import choice

# window.addstr(y, x, str[, attr])


def curses_setup(stdscr):
    stdscr.clear()  # Clear the screen
    curses.noecho()  # Turn off echoing of keys
    curses.cbreak()  # Turn off normal tty line buffering
    stdscr.keypad(True)  # Enable keypad mode
    # curses.mousemask(True)  # Enable mouse event reporting
    curses.curs_set(0)  # Hide cursor
    curses.start_color()  # Enable colors if supported
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLUE)    # water
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLUE)   # beak
    curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)  # body
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLUE)  # beak
    stdscr.bkgd(" ", curses.color_pair(1))
    stdscr.refresh()


def left(y, x):
    return (
        [[y, x, ".", curses.color_pair(3)]]
        + [
            [y + yx[0], x + yx[1], " ", curses.color_pair(3)]
            for yx in ((0, 1), (1, 0), (1, 1), (1, 2), (1, 3))
        ]
        + [[y, x - 1, ">", curses.color_pair(4)]]
    )


def right(y, x):
    return (
        [[y, x, ".", curses.color_pair(3)]]
        + [
            [y + yx[0], x + yx[1], " ", curses.color_pair(3)]
            for yx in ((0, -1), (1, 0), (1, -1), (1, -2), (1, -3))
        ]
        + [[y, x + 1, "<", curses.color_pair(4)]]
    )


def draw_duck(y, x, stdscr):
    for k, j in [(0, 1), (1, 0), (1, 1), (1, 2), (1, 3)]:
        stdscr.addstr(y + k, x + j, " ", curses.color_pair(3))

    stdscr.addstr(y, x, "·", curses.color_pair(3))
    stdscr.addstr(y, x - 1, ">", curses.color_pair(4))
    # stdscr.addstr(y + 2, x + 1, "╛╛", curses.color_pair(4))


def draw(a):
    """Receives a list of [y, x, str, attribute]"""
    for item in a:
        stdscr.addstr(*item)


def get_input(c, head, direction):
    if c == curses.KEY_LEFT or c == ord("h"):
        head[1] = max( head[1] - 1, 2)
        return left
    elif c == curses.KEY_RIGHT or c == ord("l"):
        head[1] = min( head[1] + 1, curses.COLS - 3)
        return right
    elif c == curses.KEY_UP or c == ord("k"):
        head[0] = max( head[0] - 1, 0)
    elif c == curses.KEY_DOWN or c == ord("j"):
        head[0] = min( head[0] + 1, curses.LINES - 2)
    return direction


def main(stdscr):
    FPS = 30
    direction = right
    head = [curses.LINES // 2, curses.COLS // 2]
    curses_setup(stdscr)
    stdscr.clear()
    while True:
        for item in direction(*head):
            stdscr.addstr(*item)
        direction = get_input(stdscr.getch(), head, direction)
        curses.napms(int(1000 / FPS))
        stdscr.clear()


if __name__ == "__main__":
    try:
        wrapper(main)
    except KeyboardInterrupt:
        print("Thank you for visiting the pond.")
    except curses.error:
        print("Terminal not large enough, resize and try again.")
