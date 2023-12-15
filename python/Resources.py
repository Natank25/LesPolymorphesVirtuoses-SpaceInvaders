import pygame


pygame.init()
class UI:
    class Images:
        play_game_img = pygame.image.load("../img/UI/buttons/play_button.png")
        background_img = pygame.image.load("../img/background.png")
        background_menu_img = pygame.image.load("../img/background_menu.png")

    class Sons:
        pass


class Player:
    class Images:
        Vaisseau_Base = pygame.image.load("../img/vaisseau.png")
        Balle = pygame.image.load("../img/balle.png")

    class Sons:
        pass


class Ennemies:
    class Images:
        CommonInvader1 = pygame.image.load("../img/CommonInvader1.png")
        CommonInvader2 = pygame.image.load("../img/CommonInvader2.png")
        CommonInvader3 = pygame.image.load("../img/CommonInvader2.png")

        SpeedInvader1 = pygame.image.load("../img/SpeedInvader1.png")
        SpeedInvader2 = pygame.image.load("../img/SpeedInvader2.png")
        SpeedInvader3 = pygame.image.load("../img/SpeedInvader2.png")

        TankInvader1 = pygame.image.load("../img/Ships/UFO.png")
        TankInvader2 = pygame.image.load("../img/Ships/UFO.png")
        TankInvader3 = pygame.image.load("../img/Ships/UFO.png")

    class Sons:
        pass
