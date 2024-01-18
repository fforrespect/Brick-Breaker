import pygame

from Setup import Constants as c, GlobalVars as gv, Colours


class Paddle:
    def __init__(self) -> None:
        self.pos: tuple[int, int] = c.INITIAL_PADDLE_POSITION
        self.colour: tuple[int, int, int] = Colours.WHITE
        self.size: tuple[int, int] = c.PADDLE_SIZE

        gv.all_objects.append(self)

    @property
    def centre(self) -> tuple[int, int]:
        return tuple[int, int]([list(self.pos)[0] - self.size[0]//2, self.pos[1]])

    @property
    def rect(self) -> pygame.Rect:
        return pygame.Rect(self.pos, self.size)

    def draw(self, screen: pygame.Surface) -> None:
        pygame.draw.rect(screen, self.colour,  self.rect, border_radius=c.PADDLE_BORDER_RAD)

    def update(self, new_pos: list[int]) -> None:
        self.pos = new_pos

    def move(self, x: int, y: int):
        self.pos[0] += x
        self.pos[1] += y

    def process(self):
        pass
