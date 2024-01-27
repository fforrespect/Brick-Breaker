import pygame

from Setup import GlobalVars as gv, Constants as c


def display():
    # How many lives the player has
    lives = gv.player_lives

    for i in range(lives):
        Life(i)


class Life:
    def __init__(self, number):
        self.x = c.LIVES_START_X - (number * c.LIVES_SPACING)
        self.y = c.LIVES_PADDING

        self.image = pygame.image.load(f"{c.IMAGES_FP}life.png")
        self.image = pygame.transform.scale(self.image, (50, 50))

        gv.all_objects.append(self)

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))
