import pygame
from typing import Literal

from Game import Player, Brick
from Process import Vector
from Setup import Constants as c, GlobalVars as gv, Colours


class Instance:
    def __init__(self, pos: list[int] | None = None, vel: list[int] | None = None, is_first: bool = False):
        self.radius: int = c.DEFAULT_BALL_RAD

        self.cent_pos: list[int] = pos if pos is not None else self.__get_coords_while_stuck()
        self.vel: list[int] = vel if vel is not None else [0, 0]
        self.has_been_shot: bool = not is_first

        self.colour: tuple[int, int, int] = Colours.RED
        self.speed: int = c.BALL_SPEED
        self.can_be_hit: bool = False

        gv.all_objects.append(self)
        global all_balls
        all_balls.append(self)

    @property
    def rect(self) -> pygame.Rect:
        nw_pos: tuple[float, float] = (
            self.cent_pos[0] - self.radius,
            self.cent_pos[1] - self.radius
        )
        return pygame.Rect(nw_pos, [self.radius * 2] * 2)

    @property
    def nw_pos(self) -> tuple[float, float]:
        return (
            self.cent_pos[0] - self.radius,
            self.cent_pos[1] - self.radius
        )

    @property
    def se_pos(self) -> tuple[float, float]:
        return (
            self.cent_pos[0] + self.radius,
            self.cent_pos[1] + self.radius
        )

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.colour, self.cent_pos, self.radius)

    def update(self, new_x: float = None, new_y: float = None) -> None:
        self.cent_pos = [new_x if new_x is not None else self.cent_pos[0],
                         new_y if new_y is not None else self.cent_pos[1]]

    def move(self, move_x: float = 0, move_y: float = 0) -> None:
        self.cent_pos[0] += move_x
        self.cent_pos[1] += move_y

    def move_by_vel(self) -> None:
        self.__check_for_hit()
        self.cent_pos[0] += self.vel[0]
        self.cent_pos[1] += self.vel[1]

    def set_vel(self, x: float = None, y: float = None):
        self.vel = [x*self.speed if x is not None else self.vel[0],
                    y*self.speed if y is not None else self.vel[1]]

    def bounce(self, surface: Literal['paddle', 'brick', 'side', 'top']) -> None:
        match surface:
            case 'side':
                self.vel[0] *= -1
            case 'top':
                self.vel[1] *= -1
            case 'paddle':
                normalised_angle = self.__get_normalised_angle_rel_to_paddle()
                unit_vector = Vector.unit_vector_from_angle(normalised_angle)
                self.vel = [unit_vector[0]*self.speed, unit_vector[1]*self.speed]
            case 'brick':
                pass
            case _:
                raise ValueError("Invalid surface")

    def process(self):
        if not self.has_been_shot:
            self.update(new_x=self.__get_coords_while_stuck()[0])

        self.move_by_vel()

    def __get_coords_while_stuck(self) -> list[int]:
        return [Player.active_paddle.centre[0], Player.active_paddle.nw_pos[1] - self.radius]

    def __get_normalised_angle_rel_to_paddle(self) -> float:
        # returns how far left or right the ball is on the paddle,
        # as a value from -1 to 1
        return (self.cent_pos[0] - Player.active_paddle.centre[0])/Player.active_paddle.size[0]

    def __check_for_hit(self) -> None:
        if (self.nw_pos[0] + self.vel[0]) < 0 or (self.se_pos[0] + self.vel[0]) > c.SCREEN_SIZE[0]:
            self.bounce('side')
            self.can_be_hit = True

        if self.nw_pos[1] + self.vel[1] < 0:
            self.bounce('top')
            self.can_be_hit = True

        if self.rect.colliderect(Player.active_paddle.rect):
            if self.can_be_hit:
                self.bounce('paddle')
            self.can_be_hit = False

        brick_hit: int = self.rect.collidelist(Brick.all_bricks)
        if brick_hit != -1:
            Brick.all_bricks[brick_hit].gets_hit()
            self.can_be_hit = True


all_balls: list[Instance] = []


def init_first_ball() -> Instance:
    return Instance(is_first=True)


def process_all() -> None:
    ball: Instance
    for ball in all_balls:
        ball.process()
