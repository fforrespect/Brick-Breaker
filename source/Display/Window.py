import pygame

from Setup import Colours


def display(screen: pygame.Surface) -> None:
    # Background
    screen.fill(Colours.D_GRAY)

    # # Iterate through the objects, and draw them one by one
    # for item in gv.all_objects + gv.all_overlays:
    #     item.draw(screen)

    pygame.display.update()
