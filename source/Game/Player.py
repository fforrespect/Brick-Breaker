import pygame

from Game import Ball
from Process import Vector
from Setup import Constants as c, GlobalVars as gv, Colours


def _get_mouse_x() -> int:
    return pygame.mouse.get_pos()[0]


class Paddle:
    def __init__(self) -> None:
        self.nw_pos: list[int] = list(c.INITIAL_PADDLE_POSITION)
        self.colour: tuple[int, int, int] = Colours.WHITE
        self.size: list[int] = list(c.PADDLE_SIZE)

        gv.all_objects.append(self)
        gv.paddle = self

        self.bound_ball: Ball.Instance | None = Ball.init_first_ball()

    @property
    def centre(self) -> tuple[int, int]:
        return tuple[int, int]([self.nw_pos[0] + self.size[0] // 2, self.nw_pos[1] + self.size[1] // 2])

    @centre.setter
    def centre(self, value: list[int]) -> None:
        self.nw_pos = [value[0] - self.size[0] // 2, value[1] - self.size[1] // 2]

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.nw_pos, self.size)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.colour, self.rect, border_radius=c.PADDLE_BORDER_RAD)

    def update(self, new_x: int = None, new_y: int = None) -> None:
        self.nw_pos = (new_x if new_x is not None else self.nw_pos[0],
                       new_y if new_y is not None else self.nw_pos[1])

    def move(self, move_x: int = 0, move_y: int = 0) -> None:
        self.nw_pos[0] += move_x
        self.nw_pos[1] += move_y

    def shoot(self):
        if self.bound_ball is None:
            return

        shoot_direction: list[float] = list(Vector.unit_vector(pygame.mouse.get_pos(), self.centre))
        self.bound_ball.set_vel(shoot_direction[0]*c.BALL_SPEED, shoot_direction[1]*c.BALL_SPEED)

        self.bound_ball.has_been_shot = True
        self.bound_ball = None

    def process(self):
        self.centre = [_get_mouse_x(), self.centre[1]]

        if pygame.mouse.get_pressed(num_buttons=3)[0]:
            self.shoot()


def init() -> Paddle:
    return Paddle()
