# File: smoke_test_curses.py
"""Headless smoke test for "Snake CLI.py" using the real curses (windows-curses).

Loads the game, draws the menu and a game frame in a virtual window, and checks
that nothing raises. Run with the interpreter that has windows-curses installed.
"""
import importlib.util
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
GAME = os.path.join(os.path.dirname(HERE), "Snake CLI.py")
LOG = os.path.join(HERE, "smoke_out.txt")
os.environ.setdefault("TERM", "xterm")

import curses  # noqa: E402

# curses needs a console; keep results in a file so the check works from a pipe.
LOG_FILE = open(LOG, "w")
sys.stdout = sys.stderr = LOG_FILE

spec = importlib.util.spec_from_file_location("snakecli", GAME)
game = importlib.util.module_from_spec(spec)
spec.loader.exec_module(game)


def run(stdscr):
    win = curses.newwin(24, 80, 0, 0)
    win.keypad(True)
    win.nodelay(True)
    game.show_menu(win, 0)
    win.clear()
    win.border()
    for wall in game.get_level(1).walls:
        win.addch(wall[0], wall[1], game.WALL_CHAR)
    win.addch(10, 40, game.FOOD_CHAR)
    win.addch(12, 20, game.SNAKE_CHAR)
    win.addstr(0, 2, "Score: 0")
    win.addstr(0, 70, "High Score: 0")
    win.refresh()


try:
    curses.wrapper(run)
except Exception:
    traceback.print_exc()
    raise
else:
    print(f"smoke test OK: {sys.executable}")
finally:
    LOG_FILE.flush()
    LOG_FILE.close()
