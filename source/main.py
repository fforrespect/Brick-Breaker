import pygame

from Display import Window
from Event import GameOver
from Game import Player, Ball
from Setup import Constants as c

pygame.init()

screen: pygame.Surface = pygame.display.set_mode(c.SCREEN_SIZE)
clock: pygame.time.Clock = pygame.time.Clock()

Player.init()
Ball.init()

while True:
    clock.tick(c.FPS)

    GameOver.quit_pressed(pygame.event.get())

    Window.display(screen)
