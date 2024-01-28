import pygame
from typing import Literal

from Setup import Constants as c, Colours


class Powerup:
    def __init__(self, _type: Literal["l", "m", "c", "g", "e"], grid_pos: tuple[int, int]):
        self._type: Literal["l", "m", "c", "g", "e"] = _type
        self.grid_pos: tuple[int, int] = grid_pos

        self.nw_px_pos: tuple[float, float] = self.__init_nw_px_pos()
        self.colour: tuple[int, int, int] = Colours.PURPLE

        self.is_active: bool = False

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.nw_px_pos, c.POWERUP_SIZE)

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(
            screen,
            self.colour,
            self.rect,
            c.POWERUP_BORDER_WIDTH,
            c.POWERUP_BORDER_RAD
        )

    def __init_nw_px_pos(self) -> tuple[float, float]:
        return ((self.grid_pos[0]*c.BRICK_SIZE[0]) + ((c.BRICK_SIZE[0] - c.POWERUP_SIZE[0])/2),
                self.grid_pos[1]*c.BRICK_SIZE[1])
