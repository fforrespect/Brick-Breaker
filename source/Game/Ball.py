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
        self.can_hit_paddle: bool = False

        gv.all_objects.append(self)
        global all_balls
        all_balls.append(self)

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.nw_pos, [self.radius * 2] * 2)

    @property
    def nw_pos(self) -> tuple[float, float]:
        return (
            self.cent_pos[0] - self.radius,
            self.cent_pos[1] - self.radius
        )

    @nw_pos.setter
    def nw_pos(self, value: tuple[float, float]) -> None:
        self.cent_pos = [value[0] + self.radius, value[1] + self.radius]

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

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.colour, self.cent_pos, self.radius)

    def update_cent(self, x: float = None, y: float = None) -> None:
        self.cent_pos = [x if x is not None else self.cent_pos[0],
                         y if y is not None else self.cent_pos[1]]

    def update_nw(self, x: float = None, y: float = None) -> None:
        self.nw_pos = [x if x is not None else self.nw_pos[0],
                       y if y is not None else self.nw_pos[1]]

    def move(self, x: float = 0, y: float = 0) -> None:
        self.__check_for_hit()
        self.cent_pos[0] += x
        self.cent_pos[1] += y

    def move_by_vel(self) -> None:
        self.move(*self.vel)

    def set_vel(self, x: float = None, y: float = None):
        self.vel = [x*self.speed if x is not None else self.vel[0],
                    y*self.speed if y is not None else self.vel[1]]

    def bounce(self,
               surface: Literal['paddle', 'x', 'y'],
               bounce_off: float | None,
               point_hit: Literal['top', 'bottom', 'left', 'right'] | None) -> None:
        match surface:
            case 'x':
                self.vel[0] *= -1
            case 'y':
                self.vel[1] *= -1
            case 'paddle':
                normalised_angle = self.__get_normalised_angle_rel_to_paddle()
                unit_vector = Vector.unit_vector_from_angle(normalised_angle)
                self.vel = [unit_vector[0]*self.speed, unit_vector[1]*self.speed]
            case _:
                raise ValueError("Invalid surface")

        match point_hit:
            case 'top':
                self.update_cent(y=bounce_off + self.radius)
            case 'bottom':
                self.update_cent(y=bounce_off - self.radius)
            case 'left':
                self.update_cent(x=bounce_off + self.radius)
            case 'right':
                self.update_cent(x=bounce_off - self.radius)
            case _:
                raise ValueError("Invalid point hit")

    def process(self):
        if not self.has_been_shot:
            self.update_cent(x=self.__get_coords_while_stuck()[0])

        self.move_by_vel()

    def __get_coords_while_stuck(self) -> list[int]:
        return [Player.active_paddle.centre[0], Player.active_paddle.nw_pos[1] - self.radius]

    def __get_normalised_angle_rel_to_paddle(self) -> float:
        # returns how far left or right the ball is on the paddle,
        # as a value from -1 to 1
        return (self.cent_pos[0] - Player.active_paddle.centre[0])/Player.active_paddle.size[0]

    def __check_for_hit(self) -> None:
        # hits the left wall
        if (self.left + self.vel[0]) < 0:
            self.bounce('x', 0, 'left')
            self.can_hit_paddle = True

        # hits the right wall
        if (self.right + self.vel[0]) > c.SCREEN_SIZE[0]:
            self.bounce('x', c.SCREEN_SIZE[0], 'right')
            self.can_hit_paddle = True

        # hits the roof
        if self.top + self.vel[1] < 0:
            self.bounce('y', 0, 'top')
            self.can_hit_paddle = True

        # hits the paddle
        if self.rect.move(self.vel).colliderect(Player.active_paddle.rect):
            if self.can_hit_paddle:
                self.bounce('paddle', Player.active_paddle.rect.top, 'bottom')
                print(self.bottom)
                print(Player.active_paddle.rect.top)
                print()
            self.can_hit_paddle = False

        # hits a brick
        brick_hit_index: int = self.rect.collidelist(Brick.grid.all_brick_rects)
        if brick_hit_index != -1:
            brick_hit: Brick.Instance = Brick.all_bricks[brick_hit_index]

            # if it hits the brick on the...
            # ...left
            if (self.right + self.vel[0]) < brick_hit.left:
                self.bounce('x', brick_hit.left, 'right')
            # ...right
            elif (self.left + self.vel[0]) > brick_hit.right:
                self.bounce('x', brick_hit.right, 'left')
            # ...top
            elif (self.bottom + self.vel[1]) > brick_hit.top:
                self.bounce('y', brick_hit.top, 'bottom')
            # ...bottom
            elif (self.top + self.vel[1]) < brick_hit.bottom:
                self.bounce('y', brick_hit.bottom, 'top')

            brick_hit.gets_hit()
            self.can_hit_paddle = True


all_balls: list[Instance] = []


def init_first_ball() -> Instance:
    return Instance(is_first=True)


def process_all() -> None:
    ball: Instance
    for ball in all_balls:
        ball.process()
