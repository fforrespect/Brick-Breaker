import pygame
from typing import Literal

from Game import Player
from Setup import Constants as c, GlobalVars as gv, Colours


class Instance:
    def __init__(self, _type: Literal["l", "m", "c", "g", "e"], grid_pos: tuple[int, int]):
        self._type: Literal["l", "m", "c", "g", "e"] = _type
        self.grid_pos: tuple[int, int] = grid_pos

        self.nw_px_pos: list[float] = self.__init_nw_px_pos()
        self.colour: tuple[int, int, int] = Colours.PURPLE

        self.is_active: bool = False

        gv.all_objects.append(self)
        global all_powerups
        all_powerups.append(self)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.nw_px_pos, c.POWERUP_SIZE)

    def draw(self, screen: pygame.Surface) -> None:
        if self.is_active:
            pygame.draw.rect(
                screen,
                self.colour,
                self.rect,
                c.POWERUP_BORDER_WIDTH,
                c.POWERUP_BORDER_RAD
            )

    def process(self) -> None:
        self.__fall()
        self.__check_if_collected()

    def delete(self) -> None:
        global all_powerups
        all_powerups.remove(self)
        gv.all_objects.remove(self)

    def __fall(self) -> None:
        if self.is_active:
            self.nw_px_pos[1] += c.POWERUP_FALL_SPEED

    def __check_if_collected(self) -> None:
        if self.rect.colliderect(Player.active_paddle.rect):
            self.delete()

    def __init_nw_px_pos(self) -> list[float]:
        return [(self.grid_pos[0]*c.BRICK_SIZE[0]) + ((c.BRICK_SIZE[0] - c.POWERUP_SIZE[0])/2),
                self.grid_pos[1]*c.BRICK_SIZE[1]]


all_powerups: list[Instance] = []


def process_all() -> None:
    global all_powerups
    for powerup in all_powerups:
        powerup.process()
