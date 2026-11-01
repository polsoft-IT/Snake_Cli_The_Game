"""Game-wide configuration values."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
PACKAGE_ROOT = Path(__file__).resolve().parent
HIGH_SCORE_FILE = PACKAGE_ROOT / "highscore.txt"
