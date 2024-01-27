
from Setup import Constants as c

_levels: dict[int, tuple[str, ...]] = {}


def _decode(level: int) -> tuple[str, ...]:
    with open(f"{c.LEVELS_FP}{level}.txt", 'r') as file:
        lines: list[str] = file.read().split("\n")

    # remove the first line - it will always be irrelevant
    lines = lines[1:]

    # -- Format each of the lines correctly -- #
    # line[1:]                        : remove the first char in every line - it will also always be irrelevant
    # .replace(".", " ")              : replace all '.'s with spaces, since they are only in the level files as a guide
    # .ljust(c.NUM_OF_BRICKS[0], " ") : make every line the same length
    lines = list(map(
        lambda line:
            line[1:].replace(".", " ").ljust(c.NUM_OF_BRICKS[0], " "),
        lines)
    )

    # remove any trailing empty lines, for efficiency
    for line_i in reversed(range(len(lines))):
        if lines[line_i] == " "*c.NUM_OF_BRICKS[0]:
            del lines[line_i]
        else:
            break

    # add the new level to the _levels dictionary
    _levels[level] = tuple(lines)

    return tuple(lines)


def get(level: int | str) -> tuple[str, ...]:
    level = int(level)
    if level in _levels:
        return _levels[level]
    else:
        return _decode(level)
