import pygame

from Setup import Constants as c, GlobalVars as gv, Colours


class Paddle:
    def __init__(self) -> None:
        self.nw_pos: list[int] = list(c.INITIAL_PADDLE_POSITION)
        self.colour: tuple[int, int, int] = Colours.WHITE
        self.size: list[int] = list(c.PADDLE_SIZE)

        gv.all_objects.append(self)
        gv.paddle = self

    @property
    def centre(self) -> tuple[int, int]:
        return tuple[int, int]([self.nw_pos[0] + self.size[0] // 2, self.nw_pos[1] + self.size[1] // 2])

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.nw_pos, self.size)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.colour,  self.rect, border_radius=c.PADDLE_BORDER_RAD)

    def update(self, new_pos: tuple[int, int]) -> None:
        self.nw_pos = new_pos

    def move(self, x: int, y: int):
        self.nw_pos[0] += x
        self.nw_pos[1] += y

    def process(self):
        pass
