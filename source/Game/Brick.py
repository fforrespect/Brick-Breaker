import pygame

from Setup import Constants as c, Colours


class Instance:
    def __init__(self, strength, grid_pos: tuple[int, int]):
        self.strength: int = strength
        self.grid_pos: tuple[int, int] = grid_pos

        all_bricks.append(self)

    @property
    def colour(self) -> tuple[int, int, int]:
        return Colours.strength[self.strength]

    @property
    def nw_px_pos(self) -> tuple[float, float]:
        return self.grid_pos[0]*c.BRICK_SIZE[0], self.grid_pos[1]*c.BRICK_SIZE[1]

    def draw(self, screen: pygame.Surface) -> None:
        pass

    def process(self) -> None:
        # Processing logic

        self.__check_for_destruction()

    def __check_for_destruction(self) -> bool:
        """
        :return: has been removed?
        """
        if self.strength <= 0:
            all_bricks.remove(self)
            return True
        return False


all_bricks: list[Instance] = []
