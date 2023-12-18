import pygame

from python import Resources

pygame.init()


win_size: pygame.Rect = pygame.Rect(0, 0, 1920, 1080)

difficulty = 1

deltatime = 0

default_win_size = [500, 800]

win_scale = 1

screen: pygame.surface.Surface = None

background = Resources.UI.Images.background_menu_img

group_background = Resources.UI.Images.background_menu_img

game_started = False

current_wave = 0

paused = False

coins = 0

gems = 0

does_player_exists = False

game_overed = False


def set_background(value):
    global group_background, screen, background
    value = pygame.transform.scale(value, (value.get_width() * win_scale, value.get_height() * win_scale))
    screen.blit(value, win_size.topleft)
    screen.fill("black")
    screen.blit(pygame.transform.scale(value, win_size.size), win_size.topleft)
    pygame.image.save(screen.copy(), "bg.png")
    group_background = pygame.image.load("bg.png")
    background = value


