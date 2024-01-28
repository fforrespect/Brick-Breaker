import pygame
from typing import Literal

from Game import Ball, Player, Powerup
from Process import Level, Triangle
from Setup import Constants as c, GlobalVars as gv, Colours


class Instance:
    def __init__(self,
                 strength: str,
                 powerup: Literal[" ", "x", "l", "m", "c", "g", "e"],
                 grid_pos: tuple[int, int]):
        self.strength: int = int(strength)
        self.grid_pos: tuple[int, int] = grid_pos
        self.powerup: Powerup.Instance | None = None if powerup in (" ", "x") \
            else (
            Powerup.Instance(
                powerup,
                self.grid_pos
            )
        )

        self.is_unbreakable: bool = self.strength == 0

        self.px_size: tuple[float, float] = (c.BRICK_SIZE[0] - (c.BRICK_SPACER*2),
                                             c.BRICK_SIZE[1] - (c.BRICK_SPACER*2))

        dir_: Literal['left', 'right', 'top', 'bottom']
        self.collision_triangles: list[Triangle.Instance] = [
            Triangle.create_collision_triangle(self, dir_)
            for dir_ in ('left', 'right', 'top', 'bottom')
        ]

        global all_bricks
        all_bricks.append(self)

    @property
    def colour(self) -> tuple[int, int, int]:
        return Colours.STRENGTH[self.strength]

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.nw_px_pos, self.px_size)

    @property
    def nw_px_pos(self) -> tuple[float, float]:
        return ((self.grid_pos[0]*c.BRICK_SIZE[0]) + c.BRICK_SPACER,
                (self.grid_pos[1]*c.BRICK_SIZE[1]) + c.BRICK_SPACER)

    # Directional Properties #
    @property
    def left(self) -> float:
        return self.nw_px_pos[0]

    @property
    def right(self) -> float:
        return self.nw_px_pos[0] + c.BRICK_SIZE[0]

    @property
    def top(self) -> float:
        return self.nw_px_pos[1]

    @property
    def bottom(self) -> float:
        return self.nw_px_pos[1] + c.BRICK_SIZE[1]

    @property
    def is_destroyed(self) -> bool:
        return self.strength <= 0

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.colour, self.rect, border_radius=c.BRICK_BORDER_RAD)
        pygame.draw.rect(screen, Colours.BACKGROUND, self.rect, 2, c.BRICK_BORDER_RAD)

    def gets_hit(self):
        if not self.is_unbreakable:
            self.strength -= 1
            self.__check_for_destruction()

            if self.powerup is not None:
                self.powerup.is_active = True
                self.powerup = None

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
        level_strings: tuple[tuple[tuple[str, str], ...], ...] = Level.get(level)

        row: int; col: int
        for row, row_string in enumerate(level_strings):
            for col, brick_val in enumerate(row_string):
                if brick_val != (" ", " "):
                    Instance(brick_val[0], brick_val[1], (col, row))

    def check_for_new_level(self) -> None:
        if len(all_bricks) <= 0:
            gv.current_level += 1
            self.set_level(gv.current_level)
            Ball.reset_all_balls()
            Player.active_paddle.reset_pos()


grid: Grid | None = None


def init_grid():
    Grid()
    global grid
    grid.set_level(gv.current_level)
