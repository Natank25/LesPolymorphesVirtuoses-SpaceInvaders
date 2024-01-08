import os

import pygame

pygame.init()
pygame.mixer.init()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

print("UI", pygame.time.get_ticks())


class UI:
    print("    Images", pygame.time.get_ticks())

    class Images:
        # Font: FUGAZ ONE; 72, all caps
        play_game_button_img = pygame.image.load("../img/UI/buttons/play_button.png")
        leave_game_button_img = pygame.image.load("../img/UI/buttons/leave_game_button.png")
        resume_button_img = pygame.image.load("../img/UI/buttons/resume_button.png")
        shop_button_img = pygame.image.load("../img/UI/buttons/shop_button.png")
        settings_button_img = pygame.image.load("../img/UI/buttons/settings_button.png")
        quit_button_img = pygame.image.load("../img/UI/buttons/quit_button.png")
        arrow_img = pygame.image.load("../img/UI/buttons/arrow.png")
        background_img = pygame.image.load("../img/background.png")
        background_menu_img = pygame.image.load("../img/background_menu.png")
        game_title_img = pygame.image.load("../img/title.png")
        login_icon = pygame.image.load("../img/UI/buttons/login.png")
        game_over_text = pygame.image.load("../img/UI/game_over.png")
        big_numbers_image = pygame.image.load("../img/UI/buttons/settings/big_numbers.png")
        scientific_numbers_image = pygame.image.load("../img/UI/buttons/settings/scientific.png")
        damage_upg_img = pygame.image.load("../img/UI/buttons/shops/damage_upgrade.png")
        fire_rate_upg_img = pygame.image.load("../img/UI/buttons/shops/fire_rate_upgrade.png")
        health_upg_img = pygame.image.load("../img/UI/buttons/shops/health_upgrade.png")
        gems_10 = pygame.image.load("../img/UI/buttons/shops/gems_10.png")
        gems_25 = pygame.image.load("../img/UI/buttons/shops/gems_25.png")
        gems_50 = pygame.image.load("../img/UI/buttons/shops/gems_50.png")
        gems_100 = pygame.image.load("../img/UI/buttons/shops/gems_100.png")

    class Colors:
        color_passive = pygame.Color(100, 100, 100, 100)
        color_active = pygame.Color(100, 100, 100, 175)

    print("    Fonts", pygame.time.get_ticks())

    class Fonts:
        arialblack_20 = pygame.font.SysFont("arialblack", 20)
        arialblack_35 = pygame.font.SysFont("arialblack", 35, bold=True)
        fugaz_one_30 = pygame.font.SysFont("fugazone", 30)

    print("    Sons", pygame.time.get_ticks())

    class Sons:
        ButtonClick1 = pygame.mixer.Sound("../sounds/buttons/click_button.ogg")
        ButtonClick1.set_volume(0.5)
        ButtonClick2 = pygame.mixer.Sound("../sounds/buttons/click_button2.ogg")
        ButtonClick1.set_volume(0.5)
        ButtonClick3 = pygame.mixer.Sound("../sounds/buttons/click_button3.ogg")
        ButtonClick1.set_volume(0.5)
        ButtonClick4 = pygame.mixer.Sound("../sounds/buttons/click_button4.ogg")
        ButtonClick1.set_volume(0.5)
        ButtonClick5 = pygame.mixer.Sound("../sounds/buttons/click_button5.ogg")
        ButtonClick1.set_volume(0.5)
        ButtonClick6 = pygame.mixer.Sound("../sounds/buttons/click_button6.ogg")
        ButtonClick1.set_volume(0.5)
        ButtonClick7 = pygame.mixer.Sound("../sounds/buttons/click_button7.ogg")
        ButtonClick1.set_volume(0.5)
        ButtonClick8 = pygame.mixer.Sound("../sounds/buttons/click_button8.ogg")
        ButtonClick1.set_volume(0.5)
        ButtonClick9 = pygame.mixer.Sound("../sounds/buttons/click_button9.ogg")
        ButtonClick1.set_volume(0.5)


print("Player", pygame.time.get_ticks())


class Player:
    print("    Images", pygame.time.get_ticks())

    class Images:
        Vaisseau_Base = pygame.image.load("../img/vaisseau.png")
        Balle = pygame.image.load("../img/balle.png")

    print("    Sounds", pygame.time.get_ticks())

    class Sons:
        pass


print("Ennemies", pygame.time.get_ticks())


class Game:
    class Sons:
        BackgroundSound = pygame.mixer.Sound("../sounds/intro.ogg")
        BackgroundSound.set_volume(0.1)


class Ennemies:
    print("    Images", pygame.time.get_ticks())

    class Images:
        Balle = pygame.image.load("../img/balle.png")
        CommonInvader1 = pygame.image.load("../img/Invaders/CommonInvader1.png")
        CommonInvader2 = pygame.image.load("../img/Invaders/CommonInvader2.png")
        CommonInvader3 = pygame.image.load("../img/Invaders/CommonInvader3.png")
        SpeedInvader1 = pygame.image.load("../img/Invaders/SpeedInvader1.png")
        SpeedInvader2 = pygame.image.load("../img/Invaders/SpeedInvader2.png")
        SpeedInvader3 = pygame.image.load("../img/Invaders/SpeedInvader3.png")
        TankInvader1 = pygame.image.load("../img/Ships/UFO.png")
        TankInvader2 = pygame.image.load("../img/Ships/UFO.png")
        TankInvader3 = pygame.image.load("../img/Ships/UFO.png")
        LightningAnimated = pygame.image.load("../img/Ships/Lightning.png")
        Explosion = pygame.image.load("../img/Ships/explosions/explosion_01_strip13.png")
        Explosion_pink = pygame.image.load("../img/Ships/explosions/explosion_02_strip13.png")
        Explosion_purple = pygame.image.load("../img/Ships/explosions/explosion_03_strip13.png")

    print("    Sounds", pygame.time.get_ticks())

    class Sons:
        PlayerDeathSound = pygame.mixer.Sound("../sounds/PlayerDeathSound.ogg")
        InvaderDeathSound = pygame.mixer.Sound("../sounds/InvaderDeathSound.ogg")
        BulletSound = pygame.mixer.Sound("../sounds/alienshoot1.ogg")


class Bosses:
    class Images:
        Boss5Body = pygame.image.load("../img/Invaders/Bosses/5/body.png")
        Boss5UpperArm = pygame.image.load("../img/Invaders/Bosses/5/upper_arm.png")
        Boss5LowerArm = pygame.image.load("../img/Invaders/Bosses/5/upper_arm.png")

    class Sons:
        Boss5Sound = pygame.mixer.Sound("../sounds/BossSound.ogg")
