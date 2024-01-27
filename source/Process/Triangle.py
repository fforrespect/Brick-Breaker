from typing import Literal

from Setup import Constants as c


class Instance:
    def __init__(self, points: tuple[tuple[float, float], tuple[float, float], tuple[float, float]]):
        self.points: tuple[tuple[float, float], tuple[float, float], tuple[float, float]] = points

    # Method created with GPT-4 #
    def point_inside(self, point: tuple[float, float]) -> bool:
        """
        Check if a given point is inside the triangle.

        :param point: A tuple (x, y) representing the point to check.
        :type point: tuple[float, float]

        :return: True if the point is inside the triangle, False otherwise.
        :rtype: bool
        """
        def sign(p1: tuple[float, float], p2: tuple[float, float], p3: tuple[float, float]) -> float:
            return (p1[0] - p3[0]) * (p2[1] - p3[1]) - (p2[0] - p3[0]) * (p1[1] - p3[1])

        b1: bool = sign(point, self.points[0], self.points[1]) < 0.0
        b2: bool = sign(point, self.points[1], self.points[2]) < 0.0
        b3: bool = sign(point, self.points[2], self.points[0]) < 0.0

        return (b1 == b2) and (b2 == b3)


def create_collision_triangle(
        brick,
        direction: Literal['left', 'right', 'top', 'bottom']) -> Instance:

    ball_size: int = c.DEFAULT_BALL_RADIUS*2

    p1: tuple[float, float]
    p2: tuple[float, float]
    p3: tuple[float, float]

    match direction:
        case 'left':
            y_t: float = brick.top
            y_b: float = brick.bottom
            x_tb: float = brick.left

            p1 = (x_tb - ball_size, y_t - ball_size)
            p2 = (x_tb - ball_size, y_b + ball_size)

            dist = abs(y_t - y_b)/2
            p3 = (x_tb + dist, y_t + dist)

        case 'right':
            y_t: float = brick.top
            y_b: float = brick.bottom
            x_tb: float = brick.right

            p1 = (x_tb + ball_size, y_t - ball_size)
            p2 = (x_tb + ball_size, y_b + ball_size)

            dist = abs(y_t - y_b)/2
            p3 = (x_tb - dist, y_b - dist)

        case 'top':
            x_l: float = brick.left
            x_r: float = brick.right
            y_lr: float = brick.top

            p1 = (x_l - ball_size, y_lr - ball_size)
            p2 = (x_r + ball_size, y_lr - ball_size)

            dist = abs(x_r - x_l)/2
            p3 = (x_l + dist, y_lr + dist)

        case 'bottom':
            x_l: float = brick.left
            x_r: float = brick.right
            y_lr: float = brick.bottom

            p1 = (x_l - ball_size, y_lr + ball_size)
            p2 = (x_r + ball_size, y_lr + ball_size)

            dist = (x_r - x_l)/2
            p3 = (x_l + dist, y_lr - dist)

        case _:
            raise ValueError("Invalid direction")

    return Instance((p1, p2, p3))
