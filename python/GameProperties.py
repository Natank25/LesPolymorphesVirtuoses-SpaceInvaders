import pygame

print(100, pygame.time.get_ticks())
from python import Resources

print(101, pygame.time.get_ticks())
from python.DataManager import DataManager

print(102, pygame.time.get_ticks())

pygame.init()

win_size: pygame.Rect = pygame.Rect(0, 0, 1920, 1080)

difficulty = DataManager.get_diffculty()

deltatime = 0

default_win_size = [500, 800]

win_scale = 1

screen: pygame.surface.Surface = None

background = Resources.UI.Images.background_menu_img

group_background = Resources.UI.Images.background_menu_img

paused = False

game_started = False

current_wave = DataManager.get_current_waves()

has_paused = False

coins: int = DataManager.get_coins_player()

gems: int = DataManager.get_gems_player()

does_player_exists = False

game_overed = False

button_scale = 0.75

coin_shop = DataManager.get_coin_shop()

gems_shop = DataManager.get_gems_shop()


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
    if coins - get_damage_upgrade_cost() > 0:
        coin_shop[Upgrades.damage_upgrade] += 1
        coins -= get_damage_upgrade_cost()
        Upgrades.update_upgrades()
    else:
        print("t'as pas les thunes salope")


def atk_speed_upgrade():
    global coins
    if coins - get_atk_speed_upgrade_cost() > 0:
        coin_shop[Upgrades.atk_speed_upgrade] += 1
        coins -= get_atk_speed_upgrade_cost()
        Upgrades.update_upgrades()
    else:
        print('clochard')


def health_upgrade():
    global coins
    if coins - get_health_upgrade_cost() > 0:
        coin_shop[Upgrades.health_upgrade] += 1
        coins -= get_health_upgrade_cost()
        Upgrades.update_upgrades()
    else:
        print('pas de bras pas de chocolat')


def get_damage_upgrade_cost():
    return int(1 + coin_shop[Upgrades.damage_upgrade] ** 1.6)


def get_atk_speed_upgrade_cost():
    return int(100 + coin_shop[Upgrades.atk_speed_upgrade] ** 2.8)


def get_health_upgrade_cost():
    return int(20 + coin_shop[Upgrades.health_upgrade] ** 2)


def gems_10():
    global gems, coins
    if gems - get_gems_10_cost() > 0:
        gems -= 10
        coins *= 2
    else:
        print("t'es pauvre tafiolle")


def get_gems_10_cost():
    return 10


class Upgrades:
    @staticmethod
    def update_upgrades():
        from python.Player import PlayerProperties
        PlayerProperties.DAMAGE = int((coin_shop[Upgrades.damage_upgrade] + 1) ** (max(1.05, 1.2 - (difficulty / 100))))
        PlayerProperties.ATK_SPEED = int((coin_shop[Upgrades.atk_speed_upgrade] + 1) ** (max(1.05, 1.2 - (difficulty / 100))))
        PlayerProperties.MAX_HEALTH = int((coin_shop[Upgrades.health_upgrade] + 1) ** (max(1.1, 1.4 - (difficulty / 100))) + 2)

    damage_upgrade = "damage_upgrade"
    atk_speed_upgrade = "atk_speed_upgrade"
    health_upgrade = "health_upgrade"

    gems_10 = "gems_10"
