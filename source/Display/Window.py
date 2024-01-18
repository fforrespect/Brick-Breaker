import pygame

from Setup import GlobalVars as gv, Colours


def display(screen: pygame.Surface) -> None:
    # Background
    screen.fill(Colours.D_GRAY)

    # Iterate through the objects, and draw them one by one
    for item in gv.all_objects:
        item.draw(screen)

    pygame.display.update()
