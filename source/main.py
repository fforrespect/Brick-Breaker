import pygame

from Display import Window
from Setup import Constants as c, GlobalVars as gv
from Event import GameOver

pygame.init()

screen: pygame.Surface = pygame.display.set_mode(c.SCREEN_SIZE)
clock: pygame.time.Clock = pygame.time.Clock()

while True:
    clock.tick(c.FPS)

    GameOver.quit_pressed(pygame.event.get())

    Window.display(screen)
