import pygame

from python import Resources
from python.DataManager import DataManager

pygame.init()

win_size: pygame.Rect = pygame.Rect(0, 0, 1920, 1080)

difficulty = DataManager.get_diffculty()

deltatime = 0

default_win_size = [500, 800]

win_scale = 1

screen: pygame.surface.Surface = None

background = Resources.UI.Images.background_menu_img

group_background = Resources.UI.Images.background_menu_img

game_started = False

current_wave = DataManager.get_current_waves()

paused = False

coins = DataManager.get_coins_player()

gems = DataManager.get_gems_player()

does_player_exists = False

game_overed = False

coin_shop = DataManager.get_coin_shop()



gems_shop = DataManager.get_gems_shop()


def set_background(value):
    global group_background, screen, background
    value = pygame.transform.scale(value, (value.get_width() * win_scale, value.get_height() * win_scale))
    screen.blit(value, win_size.topleft)
    screen.fill("black")
    screen.blit(pygame.transform.scale(value, win_size.size), win_size.topleft)
    pygame.image.save(screen.copy(), "bg.png")
    group_background = pygame.image.load("bg.png")
    background = value


def damage_upgrade():
    global coins
    coin_shop["damage_upgrade"] += 1
    coins -= coin_shop["damage_upgrade"]**1.5
