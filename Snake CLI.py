# Python on Windows only has curses after `pip install windows-curses`.
# Without it the import dies with "No module named '_curses'" - explain that instead.
import sys

try:
    import curses
except ImportError as exc:
    raise SystemExit(
        f"The 'curses' module is not available in this Python interpreter ({sys.executable}).\n"
        "On Windows install it with:  python -m pip install windows-curses\n"
        "or start the game with:      .\\run_snake.ps1"
    ) from exc

import random
from pathlib import Path

# Not part of the standard project layout; fall back to a file next to this script.
try:
    from snake_game.config import HIGH_SCORE_FILE
    from snake_game.levels.catalog import get_level
    from snake_game.storage.scores import load_high_score, save_high_score
except ImportError:
    HIGH_SCORE_FILE = Path(__file__).with_name("high_score.txt")

    class _Level:
        number = 1
        name = "Classic"
        speed_ms = 150
        target_score = 10**9
        walls = ()

    def get_level(_number):
        return _Level()

    def load_high_score(file_path):
        """Loads the high score from a file."""
        try:
            with open(file_path, "r") as file:
                return int(file.read())
        except (OSError, ValueError):
            return 0

    def save_high_score(file_path, score):
        """Saves the high score to a file."""
        try:
            with open(file_path, "w") as file:
                file.write(str(score))
        except OSError:
            pass  # Fail silently if we can't save the score

# Windows curses (PDCurses) has no ACS_* glyph constants; fall back to ASCII art.
WALL_CHAR = getattr(curses, "ACS_CKBOARD", "#")
FOOD_CHAR = getattr(curses, "ACS_PI", "*")
SNAKE_CHAR = getattr(curses, "ACS_CKBOARD", "o")


def draw_centered(win, row, text, attributes=0):
    # Display centered text in the terminal.
    _, width = win.getmaxyx()
    x = max(0, (width - len(text)) // 2)
    win.addstr(row, x, text[:max(1, width - x - 1)], attributes)


def show_menu(win, high_score):
    # Show the start menu and return True when the player starts the game.
    win.nodelay(False)
    win.keypad(True)

    while True:
        height, _ = win.getmaxyx()
        win.clear()
        win.border()
        draw_centered(win, max(1, height // 2 - 7), "S N A K E   C L I", curses.A_BOLD)
        draw_centered(win, max(2, height // 2 - 5), "MAIN MENU")
        draw_centered(win, max(3, height // 2 - 2), "[ENTER] Start Game")
        draw_centered(win, max(4, height // 2), "[I] Instructions")
        draw_centered(win, max(5, height // 2 + 2), "[Q] Quit")
        draw_centered(win, max(6, height // 2 + 4), f"High Score: {high_score}")
        win.refresh()

        choice = win.getch()
        if choice in (curses.KEY_ENTER, 10, 13, ord("s"), ord("S")):
            return True
        if choice in (ord("q"), ord("Q"), 27):
            return False
        if choice in (ord("i"), ord("I")):
            win.clear()
            win.border()
            draw_centered(win, max(1, height // 2 - 5), "INSTRUCTIONS", curses.A_BOLD)
            draw_centered(win, max(2, height // 2 - 2), "Controls: arrow keys or WASD")
            draw_centered(win, max(3, height // 2), "Eat the food, avoid the walls and your own tail.")
            draw_centered(win, max(4, height // 2 + 2), "Press any key to return to the main menu.")
            win.refresh()
            win.getch()


def main(stdscr):
    # Set up the screen
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    win = curses.newwin(sh, sw, 0, 0)
    win.keypad(1)

    high_score = load_high_score(HIGH_SCORE_FILE)

    if not show_menu(win, high_score):
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
                win.addch(wall[0], wall[1], WALL_CHAR)
        win.addch(int(food[0]), int(food[1]), FOOD_CHAR)


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
                    save_high_score(HIGH_SCORE_FILE, score)

                win.clear()
                win.border()
                credit_text = "Sebastian Januchowski — polsoft.ITS™"
                win.addstr(1, (sw - len(credit_text)) // 2, credit_text)
                title_text = "Snake CLI"
                win.addstr(3, (sw - len(title_text)) // 2, title_text)
                game_over_msg = "Game Over!"
                score_msg = f"Your Score: {score}"
                high_score_msg = f"High Score: {high_score}"
                restart_msg = "Press 'r' to restart or 'q' to quit."
                win.addstr(sh // 2 - 2, (sw - len(game_over_msg)) // 2, game_over_msg)
                win.addstr(sh // 2 - 1, (sw - len(score_msg)) // 2, score_msg)
                win.addstr(sh // 2, (sw - len(high_score_msg)) // 2, high_score_msg)
                win.addstr(sh // 2 + 2, (sw - len(restart_msg)) // 2, restart_msg)
                win.refresh()

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
                    food = nf if nf not in snake else None
                win.addch(food[0], food[1], FOOD_CHAR)
            else:
                tail = snake.pop()
                win.addch(int(tail[0]), int(tail[1]), ' ')

            win.addch(int(snake[0][0]), int(snake[0][1]), SNAKE_CHAR)

            # Display score
            win.border()
            score_text = f"Score: {score}"
            high_score_text = f"High Score: {high_score}"
            level_text = f"Level: {level.number} {level.name}"
            win.addstr(0, 2, score_text)
            win.addstr(0, max(2, (sw - len(level_text)) // 2), level_text)
            win.addstr(0, sw - len(high_score_text) - 2, high_score_text)


if __name__ == "__main__":
    curses.wrapper(main)