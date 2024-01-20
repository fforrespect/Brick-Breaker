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
        nw_pos: tuple[float, float] = (
            self.cent_pos[0] - self.radius,
            self.cent_pos[1] - self.radius
        )
        return pygame.Rect(nw_pos, [self.radius * 2] * 2)

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

    def update(self, new_x: float = None, new_y: float = None) -> None:
        self.cent_pos = [new_x if new_x is not None else self.cent_pos[0],
                         new_y if new_y is not None else self.cent_pos[1]]

    def move(self, move_x: float = 0, move_y: float = 0) -> None:
        self.__check_for_hit()
        self.cent_pos[0] += move_x
        self.cent_pos[1] += move_y

    def move_by_vel(self) -> None:
        self.move(*self.vel)

    def set_vel(self, x: float = None, y: float = None):
        self.vel = [x*self.speed if x is not None else self.vel[0],
                    y*self.speed if y is not None else self.vel[1]]

    def bounce(self, surface: Literal['paddle', 'x', 'y']) -> None:
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
        if (self.left + self.vel[0]) < 0 or (self.right + self.vel[0]) > c.SCREEN_SIZE[0]:
            self.bounce('x')
            self.can_hit_paddle = True

        if self.top + self.vel[1] < 0:
            self.bounce('y')
            self.can_hit_paddle = True

        if self.rect.colliderect(Player.active_paddle.rect):
            if self.can_hit_paddle:
                self.bounce('paddle')
            self.can_hit_paddle = False

        brick_hit_index: int = self.rect.collidelist(Brick.grid.all_brick_rects)
        if brick_hit_index != -1:
            brick_hit: Brick.Instance = Brick.all_bricks[brick_hit_index]

            # Determine the side of collision
            hit_side: Literal['x', 'y'] | None = None
            if self.rect.collidepoint(brick_hit.rect.midtop) or self.rect.collidepoint(brick_hit.rect.midbottom):
                hit_side = 'y'
            elif self.rect.collidepoint(brick_hit.rect.midleft) or self.rect.collidepoint(brick_hit.rect.midright):
                hit_side = 'x'

            # Handle corner collisions
            if hit_side is None:
                if self.vel[0] > 0:  # Moving right
                    if self.vel[1] > 0:  # Moving down
                        hit_side = 'y' if brick_hit.rect.collidepoint(self.left, self.bottom) else 'x'
                    else:  # Moving up
                        hit_side = 'y' if brick_hit.rect.collidepoint(self.left, self.top) else 'x'
                else:  # Moving left
                    if self.vel[1] > 0:  # Moving down
                        hit_side = 'y' if brick_hit.rect.collidepoint(self.right, self.bottom) else 'x'
                    else:  # Moving up
                        hit_side = 'y' if brick_hit.rect.collidepoint(self.right, self.top) else 'x'

            if hit_side is not None:
                self.bounce(hit_side)
            brick_hit.gets_hit()
            self.can_hit_paddle = True


all_balls: list[Instance] = []


def init_first_ball() -> Instance:
    return Instance(is_first=True)


def process_all() -> None:
    ball: Instance
    for ball in all_balls:
        ball.process()
