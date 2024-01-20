import pygame

from Process import Level
from Setup import Constants as c, GlobalVars as gv, Colours


class Instance:
    def __init__(self, strength, grid_pos: tuple[int, int]):
        self.strength: int = int(strength)
        self.grid_pos: tuple[int, int] = grid_pos

        self.px_size: tuple[float, float] = c.BRICK_SIZE

        global all_bricks
        all_bricks.append(self)

    @property
    def colour(self) -> tuple[int, int, int]:
        return Colours.STRENGTH[self.strength]

    @property
    def rect(self) -> pygame.Rect:
        nw_px: tuple[float, float] = self.grid_pos[0]*c.BRICK_SIZE[0], self.grid_pos[1]*c.BRICK_SIZE[1]
        return pygame.Rect(nw_px, self.px_size)

    @property
    def top(self) -> float:
        return self.rect.top

    @property
    def bottom(self) -> float:
        return self.rect.bottom

    @property
    def left(self) -> float:
        return self.rect.left

    @property
    def right(self) -> float:
        return self.rect.right

    @property
    def is_destroyed(self) -> bool:
        return self.strength <= 0

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.colour, self.rect, border_radius=c.BRICK_BORDER_RAD)
        pygame.draw.rect(screen, Colours.BACKGROUND, self.rect, 2, c.BRICK_BORDER_RAD)

    def gets_hit(self):
        self.strength -= 1
        self.__check_for_destruction()

    def __check_for_destruction(self) -> bool:
        """
        :return: has been removed?
        """
        if self.is_destroyed:
            all_bricks.remove(self)
            return True
        return False


all_bricks: list[Instance] = []


class Grid:
    def __init__(self):
        self.size: tuple[int, int] = c.NUM_OF_BRICKS

        gv.all_objects.append(self)
        global grid
        grid = self

    @property
    def bricks_left(self) -> int:
        return len(all_bricks)

    @property
    def all_brick_rects(self) -> list[pygame.Rect]:
        return list(map(lambda brick: brick.rect, all_bricks))

    @staticmethod
    def draw(screen: pygame.Surface) -> None:
        for brick in all_bricks:
            brick.draw(screen)

    @staticmethod
    def set_level(level: int | str):
        level_strings: tuple[str, ...] = Level.get(level)

        for row, row_string in enumerate(level_strings):
            for col, brick_val in enumerate(row_string):
                if brick_val != " ":
                    Instance(brick_val, (col, row))


grid: Grid | None = None


def init_grid():
    Grid()
    global grid
    grid.set_level(0)
