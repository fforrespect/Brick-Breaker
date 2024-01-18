import pygame
from typing import Literal

from Setup import Constants as c, GlobalVars as gv, Colours


def process_all():
    for ball in gv.all_balls:
        ball.process()


class Instance:
    def __init__(self, pos: list[int] | None = None, vel: list[int] | None = None):
        self.rad: int = c.DEFAULT_BALL_RAD

        self.cent_pos: list[int] = pos if pos is not None else self.__get_pos_rel_to_paddle()
        self.vel: list[int] = vel if vel is not None else [0, 0]

        self.colour = Colours.RED
        self.has_been_shot: bool = False

        gv.all_objects.append(self)
        gv.all_balls.append(self)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.colour, self.cent_pos, self.rad)

    def update(self, new_x: int = None, new_y: int = None) -> None:
        self.cent_pos = (new_x if new_x is not None else self.cent_pos[0],
                       new_y if new_y is not None else self.cent_pos[1])

    def move(self, move_x: int = 0, move_y: int = 0) -> None:
        self.cent_pos[0] += move_x
        self.cent_pos[1] += move_y

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
        if not self.has_been_shot:
            self.update(new_x=self.__get_pos_rel_to_paddle()[0])

    def __get_pos_rel_to_paddle(self) -> tuple[int, int]:
        return gv.paddle.centre[0], gv.paddle.nw_pos[1] - self.rad


def init() -> None:
    Instance()
