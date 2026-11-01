<p align="center">
  <img src="docs/screenshot.png" alt="Snake CLI running in a terminal window" width="840">
</p>

<h1 align="center">Snake Cli v 1.5py</h1>

<p align="center">
  A classic Snake game for the terminal — pure Python, zero dependencies, five levels and a persistent high score.
</p>

<p align="center">
  <a href="README.md"><b>English</b></a> •
  <a href="docs/README.pl.md">Polski</a>
</p>

<p align="center">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.8%2B-3776AB?style=flat-square&logo=python&logoColor=white">
  <img alt="Platform" src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-5C2D91?style=flat-square&logo=windows-terminal&logoColor=white">
  <img alt="Dependencies" src="https://img.shields.io/badge/Dependencies-none-0078D4?style=flat-square">
  <img alt="License" src="https://img.shields.io/badge/License-MIT-107C10?style=flat-square">
</p>

---

## Overview

**Snake Cli v 1.5py** is a lightweight, terminal-native take on the arcade classic. You steer a snake around a bordered arena,
eat berries to grow, dodge obstacles and your own tail, and chase a high score that is saved between sessions.

The game is written in plain Python on top of the standard `curses` library, so the whole project is a handful of
small, readable modules — easy to read, easy to modify, and no `pip install` required on a Python build that ships `_curses`.

## Features

| | Feature | Description |
|---|---|---|
| 🎮 | **Classic gameplay** | Arrow keys or WASD, no 180° turns, collision with walls, obstacles and the body ends the run. |
| 🧱 | **Five handcrafted levels** | Plain, Midwall, Pillars, Fortress and Maze — each with its own obstacle layout and speed. |
| ⏩ | **Progressive difficulty** | Every level is faster than the last; beyond level 5 the layout repeats and the speed keeps climbing. |
| 🏆 | **Persistent high score** | The best score is stored in `snake_game/highscore.txt` and shown in the menu and on the game-over screen. |
| ◉ | **Round, colourful graphics** | Snake, berry and walls are drawn with circular glyphs and colour-coded bands. |
| 🔤 | **Graceful fallback** | Terminals without colour or Unicode automatically get a readable ASCII rendering. |
| 🧩 | **Small, modular codebase** | Levels, scoring and configuration live in their own packages under `snake_game/`. |

## Requirements

- **Python 3.8 or newer.**
- The standard `curses` module.
  - **Linux / macOS** — included with CPython out of the box.
  - **Windows** — some official installers ship without the `_curses` C extension (seen on Python 3.13 and 3.15).
    Use a Python that includes it (e.g. `py -3.14`) or install the wheel:
    ```powershell
    pip install windows-curses
    ```
- A terminal at least **20 × 50** characters (larger is better — the arena scales with the window).

## Quick start

```powershell
# Clone the repository
git clone https://github.com/polsoft-its/Snake_Cli_The_Game.git
cd Snake_Cli_The_Game

# Run the game (pick a Python that has curses on Windows)
py -3.14 Snake.py
# or
python Snake.py
```

On Linux or macOS simply run:

```bash
python3 Snake.py
```

> [!TIP]
> On Windows, use **Windows Terminal** for the best-looking result. If you see `?` instead of `◉ ◎ ◍`, your console
> is not UTF-8 — run `chcp 65001` before starting the game (or keep the ASCII fallback, which is fully playable).

## Controls

| Key | Action |
|---|---|
| <kbd>↑</kbd> <kbd>↓</kbd> <kbd>←</kbd> <kbd>→</kbd> | Move the snake |
| <kbd>W</kbd> <kbd>A</kbd> <kbd>S</kbd> <kbd>D</kbd> | Move the snake (alternative) |
| <kbd>Enter</kbd> / <kbd>S</kbd> | Start the game from the main menu |
| <kbd>I</kbd> | Show instructions |
| <kbd>Q</kbd> / <kbd>Esc</kbd> | Quit |
| <kbd>R</kbd> | Restart after a game over |
| <kbd>Q</kbd> | Quit from the game-over screen |

## Gameplay

- The snake starts in the left half of the arena and moves to the right.
- Eating a berry adds **+1 point** and grows the snake by one segment.
- Reaching the target score advances you to the next level; the arena keeps its size and the snake keeps its length.
- The run ends when the head hits the outer border, an obstacle, or the snake's own body.

### Levels

| Level | Name | Speed | Target score | Obstacles |
|:---:|---|---:|---:|---|
| 1 | Plain | 150 ms/tick | 10 | none |
| 2 | Midwall | 130 ms/tick | 20 | none |
| 3 | Pillars | 110 ms/tick | 30 | horizontal wall |
| 4 | Fortress | 95 ms/tick | 40 | hollow square |
| 5 | Maze | 80 ms/tick | 50 | scattered pillars |
| 6+ | Last layout, faster | −5 ms per level (min 40 ms) | +10 per level | same as level 5 |

## Project structure

```text
Snake_Cli_The_Game/
├── Snake.py                     # Entry point: curses UI, game loop, drawing
├── snake_game/
│   ├── config.py                # Project paths and the high-score file location
│   ├── highscore.txt            # Created/updated automatically after a run
│   ├── levels/
│   │   └── catalog.py           # Level definitions (speed, target score, walls)
│   └── storage/
│       └── scores.py            # Loading and saving the high score
├── docs/
│   ├── screenshot.png           # Screenshot used in this README
│   ├── README.pl.md             # Polish version of this document
│   └── ReadMeP.txt              # 350-character quick description
└── README.md                    # This file
```

### How it fits together

- **`Snake.py`** owns the `curses` window, the main menu, the game loop and all drawing helpers
  (`draw_snake`, `draw_food`, `draw_wall`, `initialize_colors`).
- **`snake_game/levels/catalog.py`** is pure data plus `get_level(number)`, which loops the level list endlessly
  and makes later levels faster.
- **`snake_game/storage/scores.py`** reads and writes the single integer stored in `snake_game/highscore.txt`;
  failures are handled silently so the game never crashes over a filesystem problem.
- **`snake_game/config.py`** builds absolute paths from the package location, so the high-score file is always found
  inside `snake_game/` regardless of the working directory.

## Configuration

Most tuning is a one-line change:

| What | Where |
|---|---|
| Level speed, target score, obstacles | `snake_game/levels/catalog.py` — the `Level(...)` entries |
| High-score file location | `snake_game/config.py` — `HIGH_SCORE_FILE` |
| Colours of snake, food and walls | `Snake.py` — `initialize_colors()` |
| Glyphs used for snake, food and walls | `Snake.py` — `HEAD_*`, `BODY_GLYPHS`, `TAIL_GLYPHS`, `FOOD_GLYPHS`, `WALL_GLYPHS` |

## Troubleshooting

<details>
<summary><b>"The 'curses' module is not available in this Python installation"</b></summary>

Your Python build is missing the `_curses` C extension. Run the game with a Python that ships it
(for example `py -3.14 Snake.py`) or install `windows-curses`:

```powershell
pip install windows-curses
```
</details>

<details>
<summary><b>I only see <code>?</code> or ASCII letters instead of round glyphs</b></summary>

The console is not using a UTF-8 code page or has no colour support, so the game intentionally switches to its
ASCII fallback. Run `chcp 65001` (Windows) or use a UTF-8 terminal such as Windows Terminal.
</details>

<details>
<summary><b>The board looks cramped or does not fit</b></summary>

The arena fills the current terminal window. Enlarge the window before starting, or use a font with a smaller
line height. A minimum of 20 × 50 characters is required.
</details>

<details>
<summary><b>The high score did not change</b></summary>

The score is only written when it beats the stored value, and into `snake_game/highscore.txt`.
If that folder is read-only, saving fails silently by design.
</details>

## Contributing

1. Fork the repository and create a feature branch (`git checkout -b feature/my-idea`).
2. Keep changes small and focused; follow the existing module layout.
3. Test by running the game on a terminal both with and without colour/UTF-8 support.
4. Open a pull request describing what you changed and why.

Ideas that fit the project well: new level layouts, more collectible types, a pause key, or an
on-screen legend for the glyphs.

## License

Released under the **MIT License** — see the repository for details.

---

<p align="center">
  <sub><b>Snake Cli v 1.5py</b> — built with Python and curses · <a href="docs/README.pl.md">Polski</a> · <a href="#snake-cli">Back to top</a></sub>
</p>
