import pygame
from typing import Literal

from Setup import Constants as c, GlobalVars as gv, Colours


def init():
    Instance()


class Instance:
    def __init__(self, pos: list[int] | None = None, vel: list[int] | None = None):
        self.rad: int = c.DEFAULT_BALL_RAD

        self.cent_pos: list[int] = pos if pos is not None else [gv.paddle.centre[0], gv.paddle.nw_pos[1] - self.rad]
        self.vel: list[int] = vel if vel is not None else [0, 0]

        self.colour = Colours.RED

        gv.all_objects.append(self)
        gv.all_balls.append(self)

    def draw(self, screen: pygame.Surface):
        pygame.draw.circle(screen, self.colour, self.cent_pos, self.rad)

    def update(self, new_pos: tuple[int, int]) -> None:
        self.cent_pos = new_pos

    def move(self, x: int, y: int):
        self.cent_pos[0] += x
        self.cent_pos[1] += y

    def bounce(self, surface: Literal['paddle', 'side', 'top']) -> None:
        match surface:
            case "side":
                self.vel[0] *= -1
            case "top":
                self.vel[1] *= -1
            case "paddle":
                # Implement paddle bouncing logic here
                pass
            case _:
                raise ValueError("Invalid surface")

    def process(self):
        pass
