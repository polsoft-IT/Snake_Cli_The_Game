"""Level catalog: speed, obstacles and target score for each level."""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Level:
    number: int
    name: str
    speed_ms: int
    target_score: int
    walls: tuple = field(default_factory=tuple)


_BASE_LEVELS = (
    Level(number=1, name="Plain", speed_ms=150, target_score=10),
    Level(number=2, name="Midwall", speed_ms=130, target_score=20),
    Level(
        number=3,
        name="Pillars",
        speed_ms=110,
        target_score=30,
        walls=((5, 10), (5, 11), (5, 12), (5, 13), (5, 14)),
    ),
    Level(
        number=4,
        name="Fortress",
        speed_ms=95,
        target_score=40,
        walls=(
            (7, 10), (7, 11), (7, 12), (7, 13), (7, 14),
            (8, 10), (8, 14),
            (9, 10), (9, 14),
            (10, 10), (10, 11), (10, 12), (10, 13), (10, 14),
        ),
    ),
    Level(
        number=5,
        name="Maze",
        speed_ms=80,
        target_score=50,
        walls=(
            (4, 6), (6, 6), (8, 6), (10, 6),
            (4, 16), (6, 16), (8, 16), (10, 16),
            (12, 6), (12, 10), (12, 14), (12, 16),
        ),
    ),
)


def get_level(number):
    """Return the level with the given number, looping the catalog endlessly."""
    if number < 1:
        number = 1
    index = (number - 1) % len(_BASE_LEVELS)
    base = _BASE_LEVELS[index]
    if number > len(_BASE_LEVELS):
        # Beyond the catalog: keep the last layout but make it faster.
        extra = number - len(_BASE_LEVELS)
        return Level(
            number=number,
            name=base.name,
            speed_ms=max(40, base.speed_ms - extra * 5),
            target_score=base.target_score + extra * 10,
            walls=base.walls,
        )
    return base
