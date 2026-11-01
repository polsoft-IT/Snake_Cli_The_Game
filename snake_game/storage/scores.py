"""High score persistence."""

import os


def load_high_score(file_path):
    """Load the high score from a file, returning 0 when unavailable or invalid."""
    if not os.path.exists(file_path):
        return 0
    try:
        with open(file_path, "r") as file:
            return int(file.read())
    except (IOError, ValueError):
        return 0


def save_high_score(file_path, score):
    """Save the high score to a file."""
    try:
        with open(file_path, "w") as file:
            file.write(str(score))
    except IOError:
        pass  # Fail silently if we can't save the score
