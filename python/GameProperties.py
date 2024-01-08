import sys

import pygame

print(100, pygame.time.get_ticks())
from python import Resources

print(101, pygame.time.get_ticks())
from python.DataManager import DataManager

print(102, pygame.time.get_ticks())

pygame.init()

username = "guest"

password = "None"


def set_username(_username: str):
    if _username == "":
        _username = "guest"
    global username
    username = _username
    DataManager.load_game(_username)


def add_username(_username: str):
    if _username == "":
        _username = "guest"
    global username
    username = _username
    DataManager.add_user(_username, "none")
    DataManager.save_game(_username)


win_size: pygame.Rect = pygame.Rect(0, 0, 1920, 1080)

difficulty = DataManager.get_difficulty(username)

deltatime = 0

default_win_size = [500, 800]

win_scale = 1

screen: pygame.surface.Surface = None

background = Resources.UI.Images.background_menu_img

group_background = Resources.UI.Images.background_menu_img

paused = False

game_started = False

current_wave = DataManager.get_current_waves(username)

has_paused = False

coins: int = DataManager.get_coins_player(username)

gems: int = DataManager.get_gems_player(username)

does_player_exists = False

game_overed = False

button_scale = 0.75

coin_shop = DataManager.get_coin_shop(username)

gem_shop = DataManager.get_gems_shop(username)

DataManager.load_game(username)

events = pygame.event.get()

settings = {"coins_type": 'big_number'}

playing = False


def big_number_format(cash):
    cash = float('{:.3g}'.format(cash))
    magnitude = 0
    while abs(cash) >= 1000:
        magnitude += 1
        cash /= 1000.0
    return '{}{}'.format('{:f}'.format(cash).rstrip('0').rstrip('.'),
                         ['', ' K', ' M', ' B', ' T', ' Qa', ' Qi', ' Sx', ' Sp', ' Oc', ' No', ' Dc', ' Ud', ' Dd', ' Td', ' Qad', ' Qid', ' Sxd', ' Spd', ' Ocd', ' Nod', ' Vg', ' Uvg', ' Dvg',
                          ' Tvg'][magnitude])


def exponent_format(cash):
    return "{:.2e}".format(cash)


def format_int(cash):
    if settings.get("coins_type") == "exponent":
        return exponent_format(cash)
    return big_number_format(cash)


def set_background(value):
    global group_background, screen, background
    value = pygame.transform.scale_by(value, win_scale)
    screen.blit(value, win_size.topleft)
    screen.fill("black")
    scaled_img = pygame.transform.scale(value, win_size.size)
    screen.blit(scaled_img, win_size.topleft)
    pygame.image.save(screen.copy(), "bg.png")
    group_background = pygame.image.load("bg.png")
    background = value


def damage_upgrade():
    global coins
    if get_damage_upgrade_cost() <= coins:
        coins -= get_damage_upgrade_cost()
        coin_shop[Upgrades.damage_upgrade] += 1
        Upgrades.update_upgrades()


def atk_speed_upgrade():
    global coins
    if get_atk_speed_upgrade_cost() <= coins:
        coins -= get_atk_speed_upgrade_cost()
        coin_shop[Upgrades.atk_speed_upgrade] += 1
        Upgrades.update_upgrades()


def health_upgrade():
    global coins
    if get_health_upgrade_cost() <= coins:
        coins -= get_health_upgrade_cost()
        coin_shop[Upgrades.health_upgrade] += 1
        Upgrades.update_upgrades()


def get_damage_upgrade_cost():
    return 25 + coin_shop[Upgrades.damage_upgrade] ** 2.5


def get_atk_speed_upgrade_cost():
    return 100 + coin_shop[Upgrades.atk_speed_upgrade] ** 5


def get_health_upgrade_cost():
    return 20 + coin_shop[Upgrades.health_upgrade] ** 3


def gems_10():
    global gems, coins
    if get_gems_10_cost() <= gems:
        gems -= get_gems_10_cost()
        gem_shop[Upgrades.gems_10] += 1
        coins *= 2


def gems_25():
    global gems, coins
    if get_gems_25_cost() <= gems:
        gems -= get_gems_25_cost()
        gem_shop[Upgrades.gems_25] += 1
        coins *= 5


def gems_50():
    global gems, coins
    if get_gems_25_cost() <= gems:
        gems -= get_gems_50_cost()
        gem_shop[Upgrades.gems_50] += 1
        coins *= 25


def gems_100():
    global gems, coins
    if get_gems_100_cost() <= gems:
        gems -= get_gems_100_cost()
        gem_shop[Upgrades.gems_100] += 1
        coins *= 100


def get_gems_10_cost():
    return 10


def get_gems_25_cost():
    return 25


def get_gems_50_cost():
    return 50


def get_gems_100_cost():
    return 100


class Upgrades:
    @staticmethod
    def update_upgrades():
        from python.Player import PlayerProperties
        PlayerProperties.DAMAGE = int((coin_shop[Upgrades.damage_upgrade] + 1) ** (max(1.05, 1.15 - (difficulty / 100))))
        PlayerProperties.ATK_SPEED = int((coin_shop[Upgrades.atk_speed_upgrade] + 1) ** (max(1.05, 1.2 - (difficulty / 100))))
        PlayerProperties.MAX_HEALTH = int((coin_shop[Upgrades.health_upgrade] + 1) ** (max(1.1, 1.2 - (difficulty / 100))) + 2)

    damage_upgrade = "damage_upgrade"
    atk_speed_upgrade = "atk_speed_upgrade"
    health_upgrade = "health_upgrade"

    gems_10 = "gems_10"
    gems_25 = "gems_25"
    gems_50 = "gems_50"
    gems_100 = "gems_100"


def leave_game():
    print(username)
    DataManager.save_game(username)

    pygame.quit()
    sys.exit()


def get_all_usernames():
    return DataManager.get_all_usernames()
