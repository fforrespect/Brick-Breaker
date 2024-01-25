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
        left_point: tuple[float, float],
        right_point: tuple[float, float],
        direction: Literal['top', 'bottom', 'left', 'right']) -> Instance:

    x_l, y_lr = left_point
    x_r = right_point[0]

    height = c.DEFAULT_BALL_RADIUS*2

    p1 = (x_l - height, y_lr - height)
    p2 = (x_r + height, y_lr - height)

    midpoint = (x_r + x_l)/2
    p3 = (midpoint, y_lr - midpoint)

    return Instance((p1, p2, p3))
