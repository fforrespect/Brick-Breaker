
from Setup import Constants as c

_levels: dict[int, tuple[str, ...]] = {}


def _decode(level: int) -> tuple[str, ...]:
    with open(f"{c.LEVELS_FP}{level}.txt", 'r') as file:
        lines: list[str] = file.read().split("\n")

    lines = lines[1:]
    lines = list(map(
        lambda line:
            line[1:].replace(".", " ").ljust(c.NUM_OF_BRICKS[0], " "),
        lines)
    )

    for line_i in reversed(range(len(lines))):
        if lines[line_i] == " "*c.NUM_OF_BRICKS[0]:
            del lines[line_i]
        else:
            break

    _levels[level] = tuple(lines)

    return tuple(lines)


def get(level: int | str) -> tuple[str, ...]:
    level = int(level)
    if level in _levels:
        return _levels[level]
    else:
        return _decode(level)
