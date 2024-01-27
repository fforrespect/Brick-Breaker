import pygame

from Setup import GlobalVars as gv, Constants as c


class Life:
    def __init__(self, number):
        self.number = number

        self.x: float = c.LIVES_START_X - (number * c.LIVES_SPACING)
        self.y: float = c.LIVES_PADDING

        self.image: pygame.image = pygame.image.load(f"{c.IMAGES_FP}life.png")
        self.image = pygame.transform.scale(self.image, (c.LIVES_SIZE, c.LIVES_SIZE))

    def draw(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, (self.x, self.y))


class Lives:
    def __init__(self):
        self.life_objects: list[Life] = []

        gv.all_objects.append(self)

    def draw(self, screen: pygame.Surface):
        for life in self.life_objects:
            if life.number < gv.player_lives:
                life.draw(screen)


lives_object: Lives | None = None


def init() -> None:
    global lives_object
    lives_object = Lives()

    for i in range(c.MAX_LIVES):
        lives_object.life_objects.append(Life(i))


def check_exceeded_max_lives():
    if gv.player_lives > c.MAX_LIVES:
        gv.player_lives = c.MAX_LIVES
