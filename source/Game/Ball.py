import pygame
from typing import Literal

from Game import Player, Brick
from Process import Vector
from Setup import Constants as c, GlobalVars as gv, Colours


class Instance:
    def __init__(self,
                 pos: list[int] | None = None,
                 vel: list[int] | None = None,
                 is_first: bool = False):
        self.radius: int = c.DEFAULT_BALL_RADIUS

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
        return pygame.Rect(nw_pos, (self.radius*2, self.radius*2))

    # Directional Properties #
    @property
    def left(self) -> float:
        return self.cent_pos[0] - self.radius

    @property
    def right(self) -> float:
        return self.cent_pos[0] + self.radius

    @property
    def top(self) -> float:
        return self.cent_pos[1] - self.radius

    @property
    def bottom(self) -> float:
        return self.cent_pos[1] + self.radius

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.circle(screen, self.colour, self.cent_pos, self.radius)

    def process(self):
        if not self.has_been_shot:
            self.update_cent(x=self.__get_coords_while_stuck()[0])

        self.move_by_vel()

    def delete(self) -> None:
        gv.all_objects.remove(self)
        global all_balls
        all_balls.remove(self)

    def update_cent(self, x: float = None, y: float = None) -> None:
        self.cent_pos = [x if x is not None else self.cent_pos[0],
                         y if y is not None else self.cent_pos[1]]

    def move(self, x: float = 0, y: float = 0) -> None:
        if self.should_move:
            self.cent_pos[0] += x
            self.cent_pos[1] += y

    def move_by_vel(self) -> None:
        self.__check_for_hit()
        self.__check_off_screen()
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

        # which part of the ball hit an object
        match point_hit:
            case 'left':
                self.update_cent(x=bounce_off + self.radius)
            case 'right':
                self.update_cent(x=bounce_off - self.radius)
            case 'top':
                self.update_cent(y=bounce_off + self.radius)
            case 'bottom':
                self.update_cent(y=bounce_off - self.radius)
            case _:
                raise ValueError("Invalid point hit")

    def __get_coords_while_stuck(self) -> list[int]:
        return [Player.active_paddle.centre[0], Player.active_paddle.nw_pos[1] - self.radius]

    def __get_normalised_angle_rel_to_paddle(self) -> float:
        # returns how far left or right the ball is on the paddle,
        # as a value from -1 to 1
        return (self.cent_pos[0] - Player.active_paddle.centre[0])/Player.active_paddle.size[0]

    def __check_for_hit(self) -> None:
        # By default, it should move
        # But, if it hits something, don't move for one frame
        self.should_move = True

        # hits the left wall
        if (self.left + self.vel[0]) < 0 and self.vel[0] < 0:
            self.bounce('x', 0, 'left')
            self.can_hit_paddle = True

        # hits the right wall
        elif (self.right + self.vel[0]) > c.SCREEN_SIZE[0] and self.vel[0] > 0:
            self.bounce('x', c.SCREEN_SIZE[0], 'right')
            self.can_hit_paddle = True

        # hits the roof
        if self.top + self.vel[1] < 0 and self.vel[1] < 0:
            self.bounce('y', 0, 'top')
            self.can_hit_paddle = True

        # hits the paddle
        elif self.rect.move(self.vel).colliderect(Player.active_paddle.rect):
            if self.can_hit_paddle:
                self.bounce('paddle', Player.active_paddle.rect.top, 'bottom')
            self.can_hit_paddle = False

        # hits a brick
        brick_hit_index: int = self.rect.collidelist(Brick.grid.all_brick_rects)
        if brick_hit_index != -1:
            brick_hit: Brick.Instance = Brick.all_bricks[brick_hit_index]

            i: int = 0
            for i, triangle in enumerate(brick_hit.collision_triangles):
                if triangle.point_inside(tuple[float, float](self.cent_pos)):
                    break

            bounce_parameters: dict[int, tuple[Literal['x', 'y'], Literal['left', 'right', 'top', 'bottom']]] = \
                {
                    0: ('x', 'left'),
                    1: ('x', 'right'),
                    2: ('y', 'top'),
                    3: ('y', 'bottom'),
                }

            # Retrieve parameters based on side_hit
            axis: Literal['x', 'y'] = bounce_parameters[i][0]
            side: float = getattr(brick_hit, bounce_parameters[i][1])
            # the function 'f(i) = -(i%2) + 2*(i//2) + 1' gets the opposite side without redefining it
            # i.e. f(0) = 1,
            #      f(1) = 0,
            #      f(2) = 3,
            #      f(3) = 2
            opposite_side: Literal['left', 'right', 'top', 'bottom'] = bounce_parameters[-(i%2) + 2*(i//2) + 1][1]

            # Call the bounce method with the parameters
            self.bounce(axis, side, opposite_side)

            brick_hit.gets_hit()
            self.can_hit_paddle = True

    def __check_off_screen(self) -> None:
        if len(all_balls) <= 1 and self.cent_pos[1] > c.SCREEN_SIZE[1]:
            gv.player_lives -= 1
            reset_all_balls()
            Player.active_paddle.reset_pos()


all_balls: list[Instance] = []


def init_first_ball() -> Instance:
    return Instance(is_first=True)


def reset_all_balls() -> None:
    ball: Instance
    global all_balls
    for ball in all_balls:
        ball.delete()

    all_balls = []
    Player.active_paddle.bound_ball = init_first_ball()


def process_all() -> None:
    ball: Instance
    global all_balls
    for ball in all_balls:
        ball.process()
