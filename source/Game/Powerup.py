import pygame
import time
from typing import Literal

from Game import Player
from Setup import Constants as c, GlobalVars as gv, Colours


class Instance:
    def __init__(self, power: Literal["l", "m", "c", "g", "e"], grid_pos: tuple[int, int]):
        self.power: Literal["l", "m", "c", "g", "e"] = power
        self.grid_pos: tuple[int, int] = grid_pos

        self.nw_px_pos: list[float] = self.__init_nw_px_pos()
        self.colour: tuple[int, int, int] = Colours.PURPLE

        self.is_falling: bool = False
        self.is_active: bool = False

        self.time_active: float | None = None

        gv.all_objects.append(self)
        global all_powerups
        all_powerups.append(self)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.nw_px_pos, c.POWERUP_SIZE)

    def draw(self, screen: pygame.Surface) -> None:
        if self.is_falling:
            pygame.draw.rect(
                screen,
                self.colour,
                self.rect,
                c.POWERUP_BORDER_WIDTH,
                c.POWERUP_BORDER_RAD
            )

    def process(self) -> None:
        if self.is_falling:
            self.__fall()
            self.__check_if_collected()

        if self.is_active and self.time_active is not None:
            if (time.time() - self.time_active) >= c.POWERUP_ACTIVE_TIME:
                self.deactivate()

    def stop_drawing(self) -> None:
        gv.all_objects.remove(self)

    def delete(self) -> None:
        global all_powerups
        all_powerups.remove(self)
        if self in gv.all_objects:
            gv.all_objects.remove(self)

    def __fall(self) -> None:
        self.nw_px_pos[1] += c.POWERUP_FALL_SPEED

    def __check_if_collected(self) -> None:
        if self.rect.colliderect(Player.active_paddle.rect):
            self.stop_drawing()
            self.is_falling = False
            self.activate()

    def activate(self):
        self.is_active = True

        match self.power:
            # Extra Life
            case "l":
                gv.player_lives += 1
            # Multi ball
            case "m":
                pass
            # Catch
            case "c":
                pass
            # Gun
            case "g":
                pass
            # Extend paddle
            case "e":
                self.time_active = time.time()
                Player.active_paddle.extend_paddle_size()
            case _:
                raise ValueError(f"Invalid powerup type \"{self.power}\"")

    def deactivate(self):
        self.is_active = False

        match self.power:
            # Catch
            case "c":
                pass
            # Gun
            case "g":
                pass
            # Extend paddle
            case "e":
                Player.active_paddle.reset_paddle_size()
            case _:
                raise ValueError(f"Invalid powerup type \"{self.power}\"")

        self.delete()

    def __init_nw_px_pos(self) -> list[float]:
        return [(self.grid_pos[0]*c.BRICK_SIZE[0]) + ((c.BRICK_SIZE[0] - c.POWERUP_SIZE[0])/2),
                self.grid_pos[1]*c.BRICK_SIZE[1]]


all_powerups: list[Instance] = []


def process_all() -> None:
    global all_powerups
    for powerup in all_powerups:
        powerup.process()
