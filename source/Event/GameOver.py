import sys

import pygame


def quit_all() -> None:
    pygame.quit()
    sys.exit()


def quit_pressed(events: list[pygame.event.Event]) -> None:
    for event in events:
        if event.type == pygame.QUIT:
            quit_all()
