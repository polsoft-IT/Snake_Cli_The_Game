import random
import os
import sys
from pathlib import Path
from snake_game.config import HIGH_SCORE_FILE
from snake_game.levels.catalog import get_level
from snake_game.storage.scores import load_high_score, save_high_score

try:
    import curses
except ModuleNotFoundError as exc:
    raise SystemExit(
        "The 'curses' module is not available in this Python installation "
        f"({os.sys.executable}), so Snake Cli v 1.5py cannot start.\n"
        "On Windows the '_curses' C extension is missing from some builds "
        "(e.g. Python 3.13/3.15 installers). Run the game with a Python that "
        "ships it, for example:\n"
        "    py -3.14 Snake.py\n"
        "or install it into the current interpreter with:\n"
        "    pip install windows-curses\n"
        f"Original error: {exc}"
    ) from None

def load_high_score(file_path):
    """Loads the high score from a file."""
    if not os.path.exists(file_path):
        return 0
    try:
        with open(file_path, "r") as file:
            return int(file.read())
    except (IOError, ValueError):
        return 0

def save_high_score(file_path, score):
    """Saves the high score to a file."""
    try:
        with open(file_path, "w") as file:
            file.write(str(score))
    except IOError:
        pass # Fail silently if we can't save the score

def draw_centered(win, row, text, attributes=0):
    # Display centered text in the terminal.
    _, width = win.getmaxyx()
    x = max(0, (width - len(text)) // 2)
    win.addstr(row, x, text[:max(1, width - x - 1)], attributes)


HEAD_GLYPHS = {
    curses.KEY_UP: "\u25b2",
    curses.KEY_DOWN: "\u25bc",
    curses.KEY_LEFT: "\u25c0",
    curses.KEY_RIGHT: "\u25b6",
}
HEAD_FALLBACK_GLYPHS = {
    curses.KEY_UP: "^",
    curses.KEY_DOWN: "v",
    curses.KEY_LEFT: "<",
    curses.KEY_RIGHT: ">",
}

# Round glyphs only: no square/block characters anywhere on the snake.
HEAD_FACING_GLYPHS = {
    curses.KEY_UP: "\u25c9",
    curses.KEY_DOWN: "\u25c9",
    curses.KEY_LEFT: "\u25c9",
    curses.KEY_RIGHT: "\u25c9",
}
HEAD_FALLBACK_FACING_GLYPHS = {key: "@" for key in HEAD_GLYPHS}
BODY_GLYPHS = ("\u25c9", "\u25ce")
TAIL_GLYPHS = ("\u25cb", "\u25cc")
NECK_GLYPHS = ("\u25cd", "\u25c9")
FOOD_GLYPHS = ("\u25cf", "\u25c9")
WALL_GLYPHS = ("\u25cd", "\u25cd")


def _has_colors():
    """Return True when curses is initialised and the terminal supports color."""
    try:
        return curses.has_colors()
    except Exception:
        return False


def _supports_unicode():
    """Return True when the terminal can print the box-drawing glyphs."""
    encoding = (getattr(sys.stdout, "encoding", None) or "").lower()
    return "utf" in encoding


def _glyph(options, rank, plain_options):
    """Pick a glyph variant by rank, keeping ASCII when the terminal is plain."""
    if _has_colors() and _supports_unicode():
        try:
            options[rank].encode("ascii")
        except UnicodeError:
            return options[rank]
    return plain_options[rank]


def _shade_rank(index):
    """Banding pattern: bright right after the head, then short/dark zebra stripes."""
    if index <= 1:
        return 0
    return 0 if (index - 2) % 4 < 2 else 1


def tail_glyph():
    """Return the glyph used for the last segment of the snake."""
    return _glyph(TAIL_GLYPHS, 0, ("",))


def draw_snake(win, snake, key, colors):
    """Draw the whole snake: bright head, shaded banded body, tapering tail."""
    erase = [(row, col) for row, col in snake]
    length = len(snake)
    for index, (row, col) in enumerate(snake):
        row, col = int(row), int(col)
        if index == 0:
            if length > 1:
                char = _glyph(HEAD_FACING_GLYPHS, key, HEAD_FALLBACK_FACING_GLYPHS)
            else:
                char = _glyph(HEAD_GLYPHS, key, HEAD_FALLBACK_GLYPHS)
            attr = colors["snake_head"]
        elif index == length - 1:
            char, attr = _glyph(TAIL_GLYPHS, index % 2, ("", "")), colors["snake_tail"]
        elif index == 1 and length > 2:
            char, attr = _glyph(NECK_GLYPHS, 0, ("+",)), colors["snake_body"]
        else:
            rank = _shade_rank(index)
            char = _glyph(BODY_GLYPHS, rank, ("+", "#"))
            attr = colors["snake_body"] if rank == 0 else colors["snake_body_dim"]
        try:
            win.addch(row, col, char, attr)
        except curses.error:
            pass
    return erase


def draw_food(win, food, colors, scan=0):
    """Draw the collectible as a bright berry that gently shimmers."""
    if food is None:
        return
    rank = 0 if scan <= 0 else (scan + int(food[0]) + int(food[1])) % 4 // 2
    try:
        win.addch(int(food[0]), int(food[1]), _glyph(FOOD_GLYPHS, rank, ("o", "o")), colors["food"])
    except curses.error:
        pass


def draw_wall(win, wall, colors):
    """Draw an obstacle as a chiselled stone block."""
    rank = (int(wall[0]) + int(wall[1])) % 2
    try:
        win.addch(int(wall[0]), int(wall[1]), _glyph(WALL_GLYPHS, rank, ("#", "#")), colors["wall"])
    except curses.error:
        pass


def initialize_colors():
    'Set up color pairs, with a plain-text fallback for unsupported terminals.'
    colors = {
        "menu_border": 0,
        "menu_title": curses.A_BOLD,
        "menu_heading": curses.A_BOLD,
        "menu_option": 0,
        "menu_high_score": curses.A_BOLD,
        "game_over_border": 0,
        "game_over_title": curses.A_BOLD,
        "game_over_score": 0,
        "game_over_high_score": curses.A_BOLD,
        "game_over_prompt": 0,
        "snake_head": curses.A_BOLD,
        "snake_body": 0,
        "snake_body_dim": 0,
        "snake_tail": curses.A_DIM,
        "food": curses.A_BOLD,
        "wall": curses.A_DIM,
    }
    if not _has_colors():
        return colors
    curses.start_color()
    try:
        curses.use_default_colors()
    except curses.error:
        pass
    pairs = {
        "menu_border": (curses.COLOR_CYAN, -1),
        "menu_title": (curses.COLOR_GREEN, -1),
        "menu_heading": (curses.COLOR_YELLOW, -1),
        "menu_option": (curses.COLOR_WHITE, -1),
        "menu_high_score": (curses.COLOR_MAGENTA, -1),
        "game_over_border": (curses.COLOR_RED, -1),
        "game_over_title": (curses.COLOR_RED, -1),
        "game_over_score": (curses.COLOR_YELLOW, -1),
        "game_over_high_score": (curses.COLOR_GREEN, -1),
        "game_over_prompt": (curses.COLOR_CYAN, -1),
        "snake_head": (curses.COLOR_GREEN, -1),
        "snake_body": (curses.COLOR_GREEN, -1),
        "snake_body_dim": (curses.COLOR_CYAN, -1),
        "snake_tail": (curses.COLOR_GREEN, -1),
        "food": (curses.COLOR_RED, -1),
        "wall": (curses.COLOR_WHITE, -1),
    }
    for pair_number, (name, (foreground, background)) in enumerate(pairs.items(), start=1):
        curses.init_pair(pair_number, foreground, background)
        colors[name] = curses.color_pair(pair_number)
    colors["snake_head"] |= curses.A_BOLD
    colors["snake_body"] |= curses.A_BOLD
    colors["food"] |= curses.A_BOLD
    colors["snake_tail"] |= curses.A_DIM
    return colors

def show_menu(win, high_score, colors):
    # Show the start menu and return True when the player starts the game.
    win.nodelay(False)
    win.keypad(True)

    while True:
        height, _ = win.getmaxyx()
        win.clear()
        win.attrset(colors["menu_border"])
        win.border()
        draw_centered(win, max(1, height // 2 - 7), "S N A K E   C L I   v   1.5py", colors["menu_title"])
        draw_centered(win, max(2, height // 2 - 5), "MAIN MENU", colors["menu_heading"])
        draw_centered(win, max(3, height // 2 - 2), "[ENTER] Start Game", colors["menu_option"])
        draw_centered(win, max(4, height // 2), "[I] Instructions", colors["menu_option"])
        draw_centered(win, max(5, height // 2 + 2), "[Q] Quit", colors["menu_option"])
        draw_centered(win, max(6, height // 2 + 4), f"High Score: {high_score}", colors["menu_high_score"])
        win.refresh()

        choice = win.getch()
        if choice in (curses.KEY_ENTER, 10, 13, ord("s"), ord("S")):
            return True
        if choice in (ord("q"), ord("Q"), 27):
            return False
        if choice in (ord("i"), ord("I")):
            win.clear()
            win.attrset(colors["menu_border"])
            win.border()
            draw_centered(win, max(1, height // 2 - 5), "INSTRUCTIONS", colors["menu_heading"])
            draw_centered(win, max(2, height // 2 - 2), "Controls: arrow keys or WASD", colors["menu_option"])
            draw_centered(win, max(3, height // 2), "Eat the food, avoid the walls and your own tail.", colors["menu_option"])
            draw_centered(win, max(4, height // 2 + 2), "Press any key to return to the main menu.", colors["menu_option"])
            win.refresh()
            win.getch()


def main(stdscr):
    # Set up the screen
    curses.curs_set(0)
    colors = initialize_colors()
    sh, sw = stdscr.getmaxyx()
    win = curses.newwin(sh, sw, 0, 0)
    win.keypad(1)

    high_score = load_high_score(Path(HIGH_SCORE_FILE))

    if not show_menu(win, high_score, colors):
        return
    while True:  # Main loop for restarting the game
        level = get_level(1)
        win.timeout(level.speed_ms)
        # Initial snake and food
        snake_x = sw // 4
        snake_y = sh // 2
        snake = [
            [snake_y, snake_x],
            [snake_y, snake_x - 1],
            [snake_y, snake_x - 2]
        ]

        food = [sh // 2, sw // 2]

        # Game variables
        key = curses.KEY_RIGHT
        score = 0
        win.clear()
        win.border()
        for wall in level.walls:
            if 0 < wall[0] < sh - 1 and 0 < wall[1] < sw - 1:
                draw_wall(win, wall, colors)
        draw_snake(win, snake, key, colors)
        draw_food(win, food, colors)
        win.refresh()

        ticks = 0
        while True:  # Single game loop
            next_key = win.getch()
            if next_key in (ord("w"), ord("W")):
                next_key = curses.KEY_UP
            elif next_key in (ord("s"), ord("S")):
                next_key = curses.KEY_DOWN
            elif next_key in (ord("a"), ord("A")):
                next_key = curses.KEY_LEFT
            elif next_key in (ord("d"), ord("D")):
                next_key = curses.KEY_RIGHT
            if next_key != -1:
                # Prevent the snake from reversing
                if not ((key == curses.KEY_UP and next_key == curses.KEY_DOWN) or \
                        (key == curses.KEY_DOWN and next_key == curses.KEY_UP) or \
                        (key == curses.KEY_LEFT and next_key == curses.KEY_RIGHT) or \
                        (key == curses.KEY_RIGHT and next_key == curses.KEY_LEFT)):
                    key = next_key

            # Game over conditions
            if (snake[0][0] in [0, sh-1] or
                snake[0][1] in [0, sw-1] or
                tuple(snake[0]) in level.walls or
                snake[0] in snake[1:]):
                if score > high_score:
                    high_score = score
                    save_high_score(Path(HIGH_SCORE_FILE), score)

                win.clear()
                win.attrset(colors["game_over_border"])
                win.border()
                credit_text = "Sebastian Januchowski — polsoft.ITS™"
                win.addstr(1, (sw - len(credit_text)) // 2, credit_text, colors["game_over_prompt"])
                title_text = "Snake Cli v 1.5py"
                win.addstr(3, (sw - len(title_text)) // 2, title_text, colors["game_over_title"])
                game_over_msg = "Game Over!"
                score_msg = f"Your Score: {score}"
                high_score_msg = f"High Score: {high_score}"
                restart_msg = "Press 'r' to restart or 'q' to quit."
                win.addstr(sh // 2 - 2, (sw - len(game_over_msg)) // 2, game_over_msg, colors["game_over_title"])
                win.addstr(sh // 2 - 1, (sw - len(score_msg)) // 2, score_msg, colors["game_over_score"])
                win.addstr(sh // 2, (sw - len(high_score_msg)) // 2, high_score_msg, colors["game_over_high_score"])
                win.addstr(sh // 2 + 2, (sw - len(restart_msg)) // 2, restart_msg, colors["game_over_prompt"])

                win.timeout(-1) # Wait indefinitely for user input
                choice = -1
                while choice not in [ord('r'), ord('q')]:
                    choice = win.getch()

                if choice == ord('r'):
                    break  # Breaks the inner game loop, restarts the outer one
                elif choice == ord('q'):
                    return  # Exits the main function

            new_head = [snake[0][0], snake[0][1]]

            if key == curses.KEY_DOWN:
                new_head[0] += 1
            if key == curses.KEY_UP:
                new_head[0] -= 1
            if key == curses.KEY_LEFT:
                new_head[1] -= 1
            if key == curses.KEY_RIGHT:
                new_head[1] += 1

            snake.insert(0, new_head)

            # Check if snake eats the food
            if snake[0] == food:
                score += 1
                if score >= level.target_score:
                    level = get_level(level.number + 1)
                    win.timeout(level.speed_ms)
                food = None
                while food is None:
                    nf = [
                        random.randint(1, sh - 2),
                        random.randint(1, sw - 2)
                    ]
                    food = nf if (nf not in snake and tuple(nf) not in level.walls) else None
                draw_food(win, food, colors)
            else:
                tail = snake.pop()
                win.addch(int(tail[0]), int(tail[1]), ' ')
                # Reveal the new tail glyph on the segment that was drawn one deeper.
                if len(snake) > 1:
                    tail_row, tail_col = int(snake[-1][0]), int(snake[-1][1])
                    win.addch(tail_row, tail_col, tail_glyph(), colors["snake_tail"])

            draw_snake(win, snake, key, colors)
            ticks += 1
            draw_food(win, food, colors, ticks)

            # Display score
            win.border()
            score_text = f"Score: {score}"
            high_score_text = f"High Score: {high_score}"
            level_text = f"Level: {level.number} {level.name}"
            win.addstr(0, 2, score_text)
            win.addstr(0, max(2, (sw - len(level_text)) // 2), level_text)
            win.addstr(0, sw - len(high_score_text) - 2, high_score_text)
            win.refresh()


if __name__ == "__main__":
    curses.wrapper(main)