import os

import pygame

from python import Resources

pygame.init()

class MetaClassGP(type):
    background = Resources.UI.Images.background_menu_img

    def __setattr__(self, key, value):
        if key == 'background':
            value = pygame.transform.scale(value, (
            value.get_width() * GameProperties.win_scale, value.get_height() * GameProperties.win_scale))
            GameProperties.screen.blit(value, GameProperties.win_size.topleft)
            GameProperties.screen.fill("black")
            GameProperties.screen.blit(pygame.transform.scale(value, GameProperties.win_size.size),
                                       GameProperties.win_size.topleft)
            pygame.image.save(GameProperties.screen.copy(), "bg.png")
            GameProperties.group_background = pygame.image.load("bg.png")

        super().__setattr__(key, value)


class GameProperties(metaclass=MetaClassGP):
    win_size: pygame.Rect = pygame.Rect(0, 0, 1920, 1080)

    difficulty = 1

    deltatime = 0


    default_win_size = [500, 800]

    win_scale = 1

    on_going_threads = []

    screen: pygame.surface.Surface = None

    screen_mask = None

    background = Resources.UI.Images.background_menu_img

    group_background = Resources.UI.Images.background_menu_img


