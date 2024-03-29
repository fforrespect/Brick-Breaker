import pygame

from Display import Window, Lives
from Event import GameOver
from Game import Player, Ball, Brick, Powerup
from Setup import Constants as c

pygame.init()

screen: pygame.Surface = pygame.display.set_mode(c.SCREEN_SIZE)
clock: pygame.time.Clock = pygame.time.Clock()
pygame.display.set_caption("Brick Breaker")

Player.init()
Brick.init_grid()
Lives.Lives()

while True:
    clock.tick(c.FPS)
    GameOver.quit_pressed(pygame.event.get())

    Player.active_paddle.process()
    Ball.process_all()
    Brick.grid.check_for_new_level()
    Lives.check_exceeded_max_lives()
    Powerup.process_all()

    Window.display(screen)
