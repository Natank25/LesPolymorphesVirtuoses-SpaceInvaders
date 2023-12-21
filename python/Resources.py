import os

import pygame

pygame.init()
pygame.mixer.init()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("UI", pygame.time.get_ticks())


class UI:
    print("    Images", pygame.time.get_ticks())

    class Images:
        # Font : FUGAZ ONE; 72, all caps
        play_game_button_img = pygame.image.load("../img/UI/buttons/play_button.png")
        leave_game_button_img = pygame.image.load("../img/UI/buttons/leave_game_button.png")
        resume_button_img = pygame.image.load("../img/UI/buttons/resume_button.png")

        shop_button_img = pygame.image.load("../img/UI/buttons/shop_button.png")

        settings_button_img = pygame.image.load("../img/UI/buttons/settings_button.png")
        quit_button_img = pygame.image.load("../img/UI/buttons/quit_button.png")

        arrow_img = pygame.image.load("../img/UI/buttons/arrow.png")

        background_img = pygame.image.load("../img/background.png")
        background_menu_img = pygame.image.load("../img/background_menu.png")

    print("    Fonts", pygame.time.get_ticks())

    class Fonts:
        arialblack_20 = pygame.font.SysFont("arialblack", 20)
        arialblack_35 = pygame.font.SysFont("arialblack", 35, bold=True)

    print("    Sons", pygame.time.get_ticks())

    class Sons:
        pass


print("Player", pygame.time.get_ticks())


class Player:
    print("    Images", pygame.time.get_ticks())

    class Images:
        Vaisseau_Base = pygame.image.load("../img/vaisseau.png")
        Balle = pygame.image.load("../img/balle.png")

    print("    Sons", pygame.time.get_ticks())

    class Sons:
        pass


print("Ennemies", pygame.time.get_ticks())


class Ennemies:
    print("    Images", pygame.time.get_ticks())

    class Images:
        Balle = pygame.image.load("../img/balle.png")

        CommonInvader1 = pygame.image.load("../img/CommonInvader1.png")
        CommonInvader2 = pygame.image.load("../img/CommonInvader2.png")
        CommonInvader3 = pygame.image.load("../img/CommonInvader2.png")

        SpeedInvader1 = pygame.image.load("../img/SpeedInvader1.png")
        SpeedInvader2 = pygame.image.load("../img/SpeedInvader2.png")
        SpeedInvader3 = pygame.image.load("../img/SpeedInvader2.png")

        TankInvader1 = pygame.image.load("../img/Ships/UFO.png")
        TankInvader2 = pygame.image.load("../img/Ships/UFO.png")
        TankInvader3 = pygame.image.load("../img/Ships/UFO.png")

    print("    Sons", pygame.time.get_ticks())

    class Sons:
        BossSound = pygame.mixer.Sound("../sounds/BossSound.ogg")
        PlayerDeathSound = pygame.mixer.Sound("../sounds/PlayerDeathSound.ogg")
        InvaderDeathSound = pygame.mixer.Sound("../sounds/InvaderDeathSound.ogg")
