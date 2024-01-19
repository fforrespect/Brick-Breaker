import pygame
from typing import Literal

from Setup import Constants as c, GlobalVars as gv, Colours


class Instance:
    def __init__(self, pos: list[int] | None = None, vel: list[int] | None = None, is_first: bool = False):
        self.rad: int = c.DEFAULT_BALL_RAD

        self.cent_pos: list[int] = pos if pos is not None else self.__get_pos_rel_to_paddle()
        self.vel: list[int] = vel if vel is not None else [0, 0]
        self.has_been_shot: bool = not is_first

        self.colour = Colours.RED

        gv.all_objects.append(self)
        gv.all_balls.append(self)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.colour, self.cent_pos, self.rad)

    def update(self, new_x: float = None, new_y: float = None) -> None:
        self.cent_pos = [new_x if new_x is not None else self.cent_pos[0],
                         new_y if new_y is not None else self.cent_pos[1]]

    def move(self, move_x: float = 0, move_y: float = 0) -> None:
        self.cent_pos[0] += move_x
        self.cent_pos[1] += move_y

    def move_by_vel(self) -> None:
        self.__check_for_bounce()
        self.cent_pos[0] += self.vel[0]
        self.cent_pos[1] += self.vel[1]

    def set_vel(self, x: float = None, y: float = None):
        self.vel = [x if x is not None else self.vel[0],
                    y if y is not None else self.vel[1]]

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

        self.move_by_vel()

    def __get_pos_rel_to_paddle(self) -> list[int]:
        return [gv.paddle.centre[0], gv.paddle.nw_pos[1] - self.rad]

    def __check_for_bounce(self) -> None:
        if not (0 < (self.cent_pos[0] + self.vel[0]) < c.SCREEN_SIZE[0]):
            self.bounce('side')
        if self.cent_pos[1] + self.vel[1] < 0:
            self.bounce('top')


def init_first_ball() -> Instance:
    return Instance(is_first=True)


def process_all() -> None:
    ball: Instance
    for ball in gv.all_balls:
        ball.process()
