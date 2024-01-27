
from Setup import Constants as c

_levels: dict[int, tuple[tuple[str, ...], ...]] = {}


def _decode(level: int) -> tuple[tuple[str, ...], ...]:
    with open(f"{c.LEVELS_FP}{level}.txt", 'r') as file:
        lines: list[str] = file.read().split("\n")

    # remove the first line - it will always be irrelevant
    lines = lines[1:]

    # -- Format each of the lines correctly -- #
    # line[1:]                          : remove the first char in every line - it will also always be irrelevant
    # .replace(".", " ")                : replace all '.'s with spaces,
    #                                     since they are only in the level files as a guide
    # .ljust(c.NUM_OF_BRICKS[0]*2, " ") : make every line the same length
    lines = list(map(
        lambda line:
            line[1:].replace(".", " ").ljust(c.NUM_OF_BRICKS[0]*2, " "),
        lines)
    )

    # remove any trailing empty lines, for efficiency
    for line_i in reversed(range(len(lines))):
        if lines[line_i] == " "*c.NUM_OF_BRICKS[0]*2:
            del lines[line_i]
        else:
            break

    # split the line into
    lines_list: list[tuple[str, ...]] = []
    for line_content in lines:
        lines_list.append(tuple([line_content[i:i+2] for i in range(0, len(line_content), 2)]))

    # add the new level to the _levels dictionary
    _levels[level] = tuple(lines_list)

    print(_levels[level])

    return tuple(lines_list)


def get(level: int | str) -> tuple[tuple[str, ...], ...]:
    level = int(level)
    if level in _levels:
        return _levels[level]
    else:
        return _decode(level)
