import os
import random
from enum import Enum

import pygame
from pygame.sprite import AbstractGroup

class GameProperties:
    
    win_size: pygame.Rect = pygame.Rect(0,0,1920,1080)

    difficulty = 1


class GameConstants:

    class GameEvents(Enum):
        # common
        CommonInvader1SpawnEvent = pygame.USEREVENT + 1
        CommonInvader2SpawnEvent = pygame.USEREVENT + 2
        CommonInvader3SpawnEvent = pygame.USEREVENT + 3

        # speed
        SpeedInvader1SpawnEvent = pygame.USEREVENT + 4
        SpeedInvader2SpawnEvent = pygame.USEREVENT + 5
        SpeedInvader3SpawnEvent = pygame.USEREVENT + 6

        # tank
        TankInvader1SpawnEvent = pygame.USEREVENT + 7
        TankInvader2SpawnEvent = pygame.USEREVENT + 8
        TankInvader3SpawnEvent = pygame.USEREVENT + 9

        # shooter
        ShooterInvader1SpawnEvent = pygame.USEREVENT + 30
        ShooterInvader2SpawnEvent = pygame.USEREVENT + 31
        ShooterInvader3SpawnEvent = pygame.USEREVENT + 32

        # boss
        Boss1SpawnEvent = pygame.USEREVENT + 10
        Boss2SpawnEvent = pygame.USEREVENT + 11
        Boss3SpawnEvent = pygame.USEREVENT + 12
        Boss4SpawnEvent = pygame.USEREVENT + 13
        Boss5SpawnEvent = pygame.USEREVENT + 14
        Boss6SpawnEvent = pygame.USEREVENT + 15
        Boss7SpawnEvent = pygame.USEREVENT + 16
        Boss8SpawnEvent = pygame.USEREVENT + 17
        Boss9SpawnEvent = pygame.USEREVENT + 18
        Boss10SpawnEvent = pygame.USEREVENT + 19
        Boss11SpawnEvent = pygame.USEREVENT + 20
        Boss12SpawnEvent = pygame.USEREVENT + 21
        Boss13SpawnEvent = pygame.USEREVENT + 22
        Boss14SpawnEvent = pygame.USEREVENT + 23
        Boss15SpawnEvent = pygame.USEREVENT + 24
        Boss16SpawnEvent = pygame.USEREVENT + 25
        Boss17SpawnEvent = pygame.USEREVENT + 26
        Boss18SpawnEvent = pygame.USEREVENT + 27
        Boss19SpawnEvent = pygame.USEREVENT + 28
        Boss20SpawnEvent = pygame.USEREVENT + 29

    class PlayerSpeed(Enum):
        LEFT = -2
        STOP = 0
        RIGHT = 2

    class EnemyAttributes(Enum):
        # common
        CommonInvaders1DefaultHealth = 1
        CommonInvaders1DefaultSpeedx = 0.3
        CommonInvaders1DefaultSpeedy = 0.1

        CommonInvaders2DefaultHealth = 5
        CommonInvaders2DefaultSpeedx = 0.3
        CommonInvaders2DefaultSpeedy = 0.1

        CommonInvaders3DefaultHealth = 25
        CommonInvaders3DefaultSpeedx = 0.3
        CommonInvaders3DefaultSpeedy = 0.1

        # speed
        SpeedInvader1DefaultHealth = 1
        SpeedInvader1DefaultSpeedx = 0.4
        SpeedInvader1DefaultSpeedy = 0.3

        SpeedInvader2DefaultHealth = 3
        SpeedInvader2DefaultSpeedx = 0.5
        SpeedInvader2DefaultSpeedy = 0.4

        SpeedInvader3DefaultHealth = 15
        SpeedInvader3DefaultSpeedx = 0.5
        SpeedInvader3DefaultSpeedy = 0.4

        # tank
        TankInvader1DefaultHealth = 20
        TankInvader1DefaultSpeedx = 0.2
        TankInvader1DefaultSpeedy = 0.075

        TankInvader2DefaultHealth = 100
        TankInvader2DefaultSpeedx = 0.2
        TankInvader2DefaultSpeedy = 0.075

        TankInvader3DefaultHealth = 500
        TankInvader3DefaultSpeedx = 0.2
        TankInvader3DefaultSpeedy = 0.075

        # shooter
        ShooterInvader1DefaultHealth = 20
        ShooterInvader1DefaultSpeedx = 2
        ShooterInvader1DefaultSpeedy = 0.2
        ShooterInvader1DefaultSpeedATK = 1

        ShooterInvader2DefaultHealth = 50
        ShooterInvader2DefaultSpeedx = 2
        ShooterInvader2DefaultSpeedy = 0.2
        ShooterInvader2DefaultSpeedATK = 1.5

        ShooterInvader3DefaultHealth = 150
        ShooterInvader3DefaultSpeedx = 2
        ShooterInvader3DefaultSpeedy = 0.2
        ShooterInvader3DefaultSpeedATK = 2

        # Boss
        Boss1DefaultHealth = 150
        Boss1DefaultSpeedx = 2
        Boss1DefaultSpeedy = 0.2
        Boss1DefaultSpeedATK = 1

        Boss2DefaultHealth = 150
        Boss2DefaultSpeedx = 2
        Boss2DefaultSpeedy = 0.2
        Boss2DefaultSpeedATK = 1

        Boss3DefaultHealth = 150
        Boss3DefaultSpeedx = 2
        Boss3DefaultSpeedy = 0.2
        Boss3DefaultSpeedATK = 1

        Boss4DefaultHealth = 150
        Boss4DefaultSpeedx = 2
        Boss4DefaultSpeedy = 0.2
        Boss4DefaultSpeedATK = 1

        Boss5DefaultHealth = 150
        Boss5DefaultSpeedx = 2
        Boss5DefaultSpeedy = 0.2
        Boss5DefaultSpeedATK = 1

        Boss6DefaultHealth = 150
        Boss6DefaultSpeedx = 2
        Boss6DefaultSpeedy = 0.2
        Boss6DefaultSpeedATK = 1

        Boss7DefaultHealth = 150
        Boss7DefaultSpeedx = 2
        Boss7DefaultSpeedy = 0.2
        Boss7DefaultSpeedATK = 1

        Boss8DefaultHealth = 150
        Boss8DefaultSpeedx = 2
        Boss8DefaultSpeedy = 0.2
        Boss8DefaultSpeedATK = 1

        Boss9DefaultHealth = 150
        Boss9DefaultSpeedx = 2
        Boss9DefaultSpeedy = 0.2
        Boss9DefaultSpeedATK = 1

        Boss10DefaultHealth = 150
        Boss10DefaultSpeedx = 2
        Boss10DefaultSpeedy = 0.2
        Boss10DefaultSpeedATK = 1

        Boss11DefaultHealth = 150
        Boss11DefaultSpeedx = 2
        Boss11DefaultSpeedy = 0.2
        Boss11DefaultSpeedATK = 1

        Boss12DefaultHealth = 150
        Boss12DefaultSpeedx = 2
        Boss12DefaultSpeedy = 0.2
        Boss12DefaultSpeedATK = 1

        Boss13DefaultHealth = 150
        Boss13DefaultSpeedx = 2
        Boss13DefaultSpeedy = 0.2
        Boss13DefaultSpeedATK = 1

        Boss14DefaultHealth = 150
        Boss14DefaultSpeedx = 2
        Boss14DefaultSpeedy = 0.2
        Boss14DefaultSpeedATK = 1

        Boss15DefaultHealth = 150
        Boss15DefaultSpeedx = 2
        Boss15DefaultSpeedy = 0.2
        Boss15DefaultSpeedATK = 1

        Boss16DefaultHealth = 150
        Boss16DefaultSpeedx = 2
        Boss16DefaultSpeedy = 0.2
        Boss16DefaultSpeedATK = 1

        Boss17DefaultHealth = 150
        Boss17DefaultSpeedx = 2
        Boss17DefaultSpeedy = 0.2
        Boss17DefaultSpeedATK = 1

        Boss18DefaultHealth = 150
        Boss18DefaultSpeedx = 2
        Boss18DefaultSpeedy = 0.2
        Boss18DefaultSpeedATK = 1

        Boss19DefaultHealth = 150
        Boss19DefaultSpeedx = 2
        Boss19DefaultSpeedy = 0.2
        Boss19DefaultSpeedATK = 1

        Boss20DefaultHealth = 150
        Boss20DefaultSpeedx = 2
        Boss20DefaultSpeedy = 0.2
        Boss20DefaultSpeedATK = 1

    class EnemyType(Enum):
        # common
        COMMONINVADER1 = "CommonInvader1"
        COMMONINVADER2 = "CommonInvader2"
        COMMONINVADER3 = "CommonInvader3"

        # speed
        SPEEDINVADER1 = "SpeedInvader1"
        SPEEDINVADER2 = "SpeedInvader2"
        SPEEDINVADER3 = "SpeedInvader3"

        # tank
        TANKINVADER1 = "TankInvader1"
        TANKINVADER2 = "TankInvader2"
        TANKINVADER3 = "TankInvader3"

        # shooter
        SHOOTERINVADER1 = "ShooterInvader1"
        SHOOTERINVADER2 = "ShooterInvader2"
        SHOOTERINVADER3 = "ShooterInvader3"

        # Boss
        BOSS1 = "Boss1"
        BOSS2 = "Boss2"
        BOSS3 = "Boss3"
        BOSS4 = "Boss4"
        BOSS5 = "Boss5"
        BOSS6 = "Boss6"
        BOSS7 = "Boss7"
        BOSS8 = "Boss8"
        BOSS9 = "Boss9"
        BOSS10 = "Boss10"
        BOSS11 = "Boss11"
        BOSS12 = "Boss12"
        BOSS13 = "Boss13"
        BOSS14 = "Boss14"
        BOSS15 = "Boss15"
        BOSS16 = "Boss16"
        BOSS17 = "Boss17"
        BOSS18 = "Boss18"
        BOSS19 = "Boss19"
        BOSS20 = "Boss20"


class Balle:
    def __init__(self):
        self.image = os.path.join('..', "img", "balle.png")


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, img_name, file_ext="png", *groups: AbstractGroup):
        super().__init__(*groups)
        self.image = pygame.image.load(os.path.join('..', "img", img_name +
                                                    "." + file_ext))
        self.pos = pos
        self.speed = GameConstants.PlayerSpeed.STOP

    def bouger(self):
        self.pos[0] += self.speed.value

    def setSpeed(self, speed: GameConstants.PlayerSpeed):
        self.speed = speed

    def tirer(self):
        pygame.image.load(os.path.join('..', "img", "balle.png"))


class Boss(pygame.sprite.Sprite):
    def __init__(self, hauteur, speedx, speedy, health, ATKspeed, img_name,
                 file_ext="png", *groups: AbstractGroup):
        super().__init__(*groups)
        self.hauteur = hauteur
        self.speedx = speedx
        self.speedy = speedy
        self.health = health
        self.ATKspeed = ATKspeed
        self.img_name = pygame.image.load(os.path.join('..', "img", img_name +
                                                       "." + file_ext))


# region Bosses

class Boss1(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss1DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss1DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss1DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss1DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss2(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss2DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss2DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss2DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss2DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss3(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss3DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss3DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss3DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss3DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss4(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss4DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss4DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss4DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss4DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss5(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss5DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss5DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss5DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss5DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss6(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss6DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss6DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss6DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss6DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss7(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss7DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss7DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss7DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss7DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss8(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss8DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss8DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss8DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss8DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss9(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss9DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss9DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss9DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss9DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss10(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss10DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss10DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss10DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss10DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss11(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss11DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss11DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss11DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss11DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss12(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss12DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss12DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss12DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss12DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss13(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss13DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss13DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss13DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss13DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss14(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss14DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss14DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss14DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss14DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss15(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss15DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss15DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss15DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss15DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss16(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss16DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss16DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss16DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss16DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss17(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss17DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss17DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss17DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss17DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss18(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss18DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss18DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss18DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss18DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss19(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss19DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss19DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss19DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss19DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss20(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss20DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss20DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss20DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss20DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


# endregion


class Invader(pygame.sprite.Sprite):
    def __init__(self, hauteur, speedx, speedy, health, img_name,
                 shooter=False, ATKspeed=0, can_esquive=False, file_ext="png",
                 *groups: AbstractGroup):
        super().__init__(*groups)
        self.speedx = speedx
        self.speedy = speedy
        self.depart = random.randint(0, GameProperties.win_size[0])
        self.hauteur = hauteur
        self.image = pygame.image.load(os.path.join('..', "img", img_name +
                                                    "." + file_ext))
        self.health = health
        self.shooter = shooter
        self.ATKspeed = ATKspeed
        self.lastEsquive = pygame.time.get_ticks()
        self.nextEsquive = pygame.time.get_ticks() + random.randint(500, 5000)
        self.canEsquive = can_esquive

    def avancer(self):
        self.hauteur += self.speedx
        if (self.depart < GameProperties.win_size.x or self.depart >
                GameProperties.win_size.y + GameProperties.win_size.width):
            self.speedy = -self.speedy

        self.depart += self.speedy

    def tier(self):
        if self.shooter:
            print("Pew pew !")

    def esquive(self):
        self.speedy = -self.speedy

    def update(self, *args, **kwargs):
        if self.canEsquive and pygame.time.get_ticks() >= self.nextEsquive:
            self.esquive()
            self.lastEsquive = pygame.time.get_ticks()
            self.nextEsquive = pygame.time.get_ticks() + random.randint(500, 5000)

        self.avancer()


# region Enemies

class CommonInvader1(Invader):
    def __init__(self):
        super().__init__(0,
                         GameConstants.EnemyAttributes.CommonInvaders1DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.CommonInvaders1DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.CommonInvaders1DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         "CommonInvader1")


class CommonInvader2(Invader):
    def __init__(self):
        super().__init__(0,
                         GameConstants.EnemyAttributes.CommonInvaders2DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.CommonInvaders2DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.CommonInvaders2DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         "CommonInvader2")


class CommonInvader3(Invader):
    def __init__(self):
        super().__init__(0,
                         GameConstants.EnemyAttributes.CommonInvaders3DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.CommonInvaders3DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.CommonInvaders3DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         "CommonInvader2")


class SpeedInvader1(Invader):
    def __init__(self):
        super().__init__(0,
                         GameConstants.EnemyAttributes.SpeedInvader1DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.SpeedInvader1DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.SpeedInvader2DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         "SpeedInvader1")


class SpeedInvader2(Invader):
    def __init__(self):
        super().__init__(0,
                         GameConstants.EnemyAttributes.SpeedInvader2DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.SpeedInvader2DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.SpeedInvader2DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         "SpeedInvader2")


class SpeedInvader3(Invader):
    def __init__(self):
        super().__init__(0,
                         GameConstants.EnemyAttributes.SpeedInvader2DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.SpeedInvader2DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.SpeedInvader2DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         "SpeedInvader2")


class TankInvader1(Invader):
    def __init__(self):
        super().__init__(0,
                         GameConstants.EnemyAttributes.TankInvader1DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.TankInvader1DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.TankInvader1DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         "SpeedInvader1")


class TankInvader2(Invader):
    def __init__(self):
        super().__init__(0,
                         GameConstants.EnemyAttributes.TankInvader2DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.TankInvader2DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.TankInvader2DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         "SpeedInvader1")


class TankInvader3(Invader):
    def __init__(self):
        super().__init__(0,
                         GameConstants.EnemyAttributes.TankInvader3DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.TankInvader3DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.TankInvader3DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         "SpeedInvader1")


class ShooterInvader1(Invader):
    def __init__(self):
        super().__init__(0,
                         GameConstants.EnemyAttributes.ShooterInvader1DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.ShooterInvader1DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.ShooterInvader1DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         'SpeedInvader1', shooter=True,
                         ATKspeed=GameConstants.EnemyAttributes.ShooterInvader1DefaultSpeedATK.value)


class ShooterInvader2(Invader):
    def __init__(self):
        super().__init__(0,
                         GameConstants.EnemyAttributes.ShooterInvader2DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.ShooterInvader2DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.ShooterInvader2DefaultHealth.value * (
                                 1 + GameProperties.difficulty),
                         'SpeedInvader1', shooter=True,
                         ATKspeed=GameConstants.EnemyAttributes.ShooterInvader2DefaultSpeedATK.value)


class ShooterInvader3(Invader):
    def __init__(self):
        super().__init__(0,
                         GameConstants.EnemyAttributes.ShooterInvader3DefaultSpeedx.value + (
                                 GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.ShooterInvader3DefaultSpeedy.value + (
                                 GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.ShooterInvader3DefaultHealth.value * (1 + GameProperties.difficulty),'SpeedInvader1', shooter=True, ATKspeed=GameConstants.EnemyAttributes.ShooterInvader3DefaultSpeedATK.value)


# endregion

class EnemiesManager:
    list_enemies = []

    next_events: dict = {}  # {"name_event":time_when_executed}

    @staticmethod
    def update():
        current_time = pygame.time.get_ticks()
        for event in EnemiesManager.next_events:
            if event == "CommonInvader1SpawnEvent" and EnemiesManager.next_events[event] == current_time:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.COMMONINVADER1)

    @staticmethod
    def send_waves_endless(difficulty: int):
        for i in range(difficulty * 3):
            pass

    @staticmethod
    def send_waves_levels(num_lvl: int):
        match num_lvl:
            case 1:
                for i in range(3 + GameProperties.difficulty):
                    EnemiesManager.next_events.update({"CommonInvader1SpawnEvent": (1500 * i) + pygame.time.get_ticks()})

            case 2:
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.next_events.update({"CommonInvader1SpawnEvent": (1500 * i) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader1SpawnEvent": (3000 * i) + pygame.time.get_ticks()})
            case 3:
                for i in range(4 + GameProperties.difficulty):
                    EnemiesManager.next_events.update({"CommonInvader1SpawnEvent": (1500 * i) + pygame.time.get_ticks()})
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.next_events.update({"SpeedInvader1SpawnEvent": (3000 * i) + pygame.time.get_ticks()})
            case 4:
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.next_events.update({"CommonInvader1SpawnEvent": (1500 * i) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader1SpawnEvent": (3000 * i) + pygame.time.get_ticks()})
            case 5:
                EnemiesManager.next_events.update({"Boss1SpawnEvent": 0 + pygame.time.get_ticks()})
            case 6:
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.next_events.update({"CommonInvader1SpawnEvent": (1500 * i) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader1SpawnEvent": (3000 * i) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (4500 * i) + pygame.time.get_ticks()})
            case 7:
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.next_events.update({"CommonInvader1SpawnEvent": (1500 * i) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader1SpawnEvent": (3000 * i) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (4500 * i) + pygame.time.get_ticks()})
            case 8:
                for i in range(4 + GameProperties.difficulty):
                    for j in range(2 + GameProperties.difficulty):
                        EnemiesManager.next_events.update({"CommonInvader2SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (3000 * i * j) + pygame.time.get_ticks()})
                    EnemiesManager.next_events += {"TankInvader1SpawnEvent": (4500 * i) + pygame.time.get_ticks()}
            case 9:
                for i in range(2 + GameProperties.difficulty):
                    for j in range(3 + GameProperties.difficulty):
                        EnemiesManager.next_events.update({"CommonInvader2SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (3000 * i) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"TankInvader1SpawnEvent": (4500 * i) + pygame.time.get_ticks()})
            case 10:
                EnemiesManager.next_events += {"Boss2SpawnEvent": 0}
            case 11:
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (1500*i) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"TankInvader1SpawnEvent": (3000 * i) + pygame.time.get_ticks()})
                    for j in range(3 + GameProperties.difficulty):
                        EnemiesManager.next_events.update({"CommonInvader2SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
            case 12:
                for i in range(3 + GameProperties.difficulty):
                    for j in range(3 + GameProperties.difficulty):
                        EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"TankInvader1SpawnEvent": (3000 * i * j) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (2000 * i) + pygame.time.get_ticks()})
            case 13:
                for i in range(4 + GameProperties.difficulty):
                    for j in range(3 + GameProperties.difficulty):
                        EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"TankInvader1SpawnEvent": (3000 * i * j) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (2000 * i) + pygame.time.get_ticks()})
            case 14:
                for i in range(5 + GameProperties.difficulty):
                    for j in range(3 + GameProperties.difficulty):
                        EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"TankInvader1SpawnEvent": (3000 * i * j) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (2000 * i) + pygame.time.get_ticks()})
            case 15:
                EnemiesManager.next_events += {"Boss3SpawnEvent": 0}
            case 16:
                for i in range(3):
                    for j in range(3):
                        EnemiesManager.next_events.update({"SpeedInvaderSpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"TankInvader2SpawnEvent": (3000 * i * j) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (2000 * i) + pygame.time.get_ticks()})
            case 17:
                for i in range(3):
                    for j in range(3):
                        EnemiesManager.next_events.update({"SpeedInvader3SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"TankInvader2SpawnEvent": (3000 * i * j) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (2000 * i) + pygame.time.get_ticks()})
            case 18:
                for i in range(3):
                    for j in range(3):
                        EnemiesManager.next_events.update({"SpeedInvader3SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"TankInvader2SpawnEvent": (3000 * i * j) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (2000 * i) + pygame.time.get_ticks()})
            case 19:
                for i in range(5):
                    for j in range(3):
                        EnemiesManager.next_events.update({"SpeedInvader3SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"TankInvader2SpawnEvent": (3000 * i * j) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (2000 * i) + pygame.time.get_ticks()})
            case 20:
                EnemiesManager.next_events += {"Boss4SpawnEvent": 0}
            case 21:
                for i in range(3):
                    for j in range(3):
                        EnemiesManager.next_events.update({"SpeedInvader3SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"TankInvader2SpawnEvent": (3000 * i * j) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (2000 * i) + pygame.time.get_ticks()})
            case 22:
                for i in range(3):
                    for j in range(3):
                        EnemiesManager.next_events.update({"SpeedInvader3SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"TankInvader2SpawnEvent": (3000 * i * j) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (2000 * i) + pygame.time.get_ticks()})
            case 23:
                for i in range(3):
                    for j in range(3):
                        EnemiesManager.next_events.update({"SpeedInvader3SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"TankInvader2SpawnEvent": (3000 * i * j) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (2000 * i) + pygame.time.get_ticks()})
            case 24:
                for i in range(3):
                    for j in range(3):
                        EnemiesManager.next_events.update({"SpeedInvader3SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"TankInvader2SpawnEvent": (3000 * i * j) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (2000 * i) + pygame.time.get_ticks()})
            case 25:
                EnemiesManager.next_events += {"Boss5SpawnEvent": 0}
            case 26:
                for i in range(3):
                    for j in range(3):
                        EnemiesManager.next_events.update({"SpeedInvader3SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"TankInvader1SpawnEvent": (3000 * i * j) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (2000 * i) + pygame.time.get_ticks()})
            case 27:
                for i in range(3):
                    for j in range(3):
                        EnemiesManager.next_events.update({"SpeedInvader3SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"TankInvader1SpawnEvent": (3000 * i * j) + pygame.time.get_ticks()})
                    EnemiesManager.next_events += {"SpeedInvader2SpawnEvent": (2000 * i) + pygame.time.get_ticks()}
            case 28:
                for i in range(3):
                    for j in range(3):
                        EnemiesManager.next_events.update({"SpeedInvader3SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})
                        EnemiesManager.next_events.update({"TankInvader1SpawnEvent": (3000 * i * j) + pygame.time.get_ticks()})
                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (2000 * i) + pygame.time.get_ticks()})
            case 29:
                pass
            case 30:
                EnemiesManager.next_events.update({"Boss6SpawnEvent": 0})
            case 31:
                pass
            case 32:
                pass
            case 33:
                pass
            case 34:
                pass
            case 35:
                EnemiesManager.next_events.update({"Boss7SpawnEvent": 0})
            case 36:
                pass
            case 37:
                pass
            case 39:
                pass
            case 40:
                EnemiesManager.next_events.update({"Boss8SpawnEvent": 0})
            case 41:
                pass
            case 42:
                pass
            case 43:
                pass
            case 44:
                pass
            case 45:
                EnemiesManager.next_events.update({"Boss9SpawnEvent": 0})
            case 46:
                pass
            case 47:
                pass
            case 48:
                pass
            case 49:
                pass
            case 50:
                EnemiesManager.next_events.update({"Boss10SpawnEvent": 0})
            case 51:
                for i in range(3):
                    for j in range(3):
                        EnemiesManager.next_events.update({"SpeedInvader3SpawnEvent": (1500 * i * j) + pygame.time.get_ticks()})

                    EnemiesManager.next_events.update({"SpeedInvader2SpawnEvent": (2000 * i) + pygame.time.get_ticks()})
            case 52:
                pass
            case 53:
                pass
            case 54:
                pass
            case 55:
                EnemiesManager.next_events.update({"Boss11SpawnEvent": 0})
            case 56:
                pass
            case 57:
                pass
            case 58:
                pass
            case 59:
                pass
            case 60:
                EnemiesManager.next_events.update({"Boss12SpawnEvent": 0})
            case 61:
                pass
            case 62:
                pass
            case 63:
                pass
            case 64:
                pass
            case 65:
                EnemiesManager.next_events.update({"Boss13SpawnEvent": 0})
            case 66:
                pass
            case 67:
                pass
            case 68:
                pass
            case 69:
                pass
            case 70:
                EnemiesManager.next_events.update({"Boss14SpawnEvent": 0})
            case 71:
                pass
            case 72:
                pass
            case 73:
                pass
            case 74:
                pass
            case 75:
                EnemiesManager.next_events.update({"Boss15SpawnEvent": 0})
            case 76:
                pass
            case 77:
                pass
            case 78:
                pass
            case 79:
                pass
            case 80:
                EnemiesManager.next_events.update({"Boss16SpawnEvent": 0})
            case 81:
                pass
            case 82:
                pass
            case 83:
                pass
            case 84:
                pass
            case 85:
                EnemiesManager.next_events.update({"Boss17SpawnEvent": 0})
            case 86:
                pass
            case 87:
                pass
            case 88:
                pass
            case 89:
                pass
            case 90:
                EnemiesManager.next_events.update({"Boss18SpawnEvent": 0})
            case 91:
                pass
            case 92:
                pass
            case 93:
                pass
            case 94:
                pass
            case 95:
                EnemiesManager.next_events.update({"Boss19SpawnEvent": 0})
            case 96:
                pass
            case 97:
                pass
            case 98:
                pass
            case 99:
                pass
            case 100:
                EnemiesManager.next_events.update({"Boss20SpawnEvent": 0})

    @staticmethod
    def spawnEnemy(type: GameConstants.EnemyType):

        # common
        if type == GameConstants.EnemyType.COMMONINVADER1:
            EnemiesManager.list_enemies.append(CommonInvader1())

        elif type == GameConstants.EnemyType.COMMONINVADER2:
            EnemiesManager.list_enemies.append(CommonInvader2())

        elif type == GameConstants.EnemyType.COMMONINVADER3:
            EnemiesManager.list_enemies.append(CommonInvader3())

        # speed
        elif type == GameConstants.EnemyType.SPEEDINVADER1:
            EnemiesManager.list_enemies.append(CommonInvader1())

        elif type == GameConstants.EnemyType.SPEEDINVADER2:
            EnemiesManager.list_enemies.append(SpeedInvader2())

        elif type == GameConstants.EnemyType.SPEEDINVADER3:
            EnemiesManager.list_enemies.append(SpeedInvader3())

        # tank
        elif type == GameConstants.EnemyType.TANKINVADER1:
            EnemiesManager.list_enemies.append(TankInvader1())

        elif type == GameConstants.EnemyType.TANKINVADER2:
            EnemiesManager.list_enemies.append(TankInvader2())

        elif type == GameConstants.EnemyType.TANKINVADER3:
            EnemiesManager.list_enemies.append(TankInvader3())

        # shooter

        elif type == GameConstants.EnemyType.SHOOTERINVADER1:
            EnemiesManager.list_enemies.append(ShooterInvader1())

        elif type == GameConstants.EnemyType.SHOOTERINVADER2:
            EnemiesManager.list_enemies.append(ShooterInvader2())

        elif type == GameConstants.EnemyType.SHOOTERINVADER3:
            EnemiesManager.list_enemies.append(ShooterInvader3())

        # Boss

        elif type == GameConstants.EnemyType.BOSS1:
            EnemiesManager.list_enemies.append(Boss1())

        elif type == GameConstants.EnemyType.BOSS2:
            EnemiesManager.list_enemies.append(Boss2())

        elif type == GameConstants.EnemyType.BOSS3:
            EnemiesManager.list_enemies.append(Boss3())

        elif type == GameConstants.EnemyType.BOSS4:
            EnemiesManager.list_enemies.append(Boss4())

        elif type == GameConstants.EnemyType.BOSS5:
            EnemiesManager.list_enemies.append(Boss5())

        elif type == GameConstants.EnemyType.BOSS6:
            EnemiesManager.list_enemies.append(Boss6())

        elif type == GameConstants.EnemyType.BOSS7:
            EnemiesManager.list_enemies.append(Boss7())

        elif type == GameConstants.EnemyType.BOSS8:
            EnemiesManager.list_enemies.append(Boss8())

        elif type == GameConstants.EnemyType.BOSS9:
            EnemiesManager.list_enemies.append(Boss9())

        elif type == GameConstants.EnemyType.BOSS10:
            EnemiesManager.list_enemies.append(Boss10())

        elif type == GameConstants.EnemyType.BOSS11:
            EnemiesManager.list_enemies.append(Boss11())

        elif type == GameConstants.EnemyType.BOSS12:
            EnemiesManager.list_enemies.append(Boss12())

        elif type == GameConstants.EnemyType.BOSS13:
            EnemiesManager.list_enemies.append(Boss13())

        elif type == GameConstants.EnemyType.BOSS14:
            EnemiesManager.list_enemies.append(Boss14())

        elif type == GameConstants.EnemyType.BOSS15:
            EnemiesManager.list_enemies.append(Boss15())

        elif type == GameConstants.EnemyType.BOSS16:
            EnemiesManager.list_enemies.append(Boss16())

        elif type == GameConstants.EnemyType.BOSS17:
            EnemiesManager.list_enemies.append(Boss17())

        elif type == GameConstants.EnemyType.BOSS18:
            EnemiesManager.list_enemies.append(Boss18())

        elif type == GameConstants.EnemyType.BOSS19:
            EnemiesManager.list_enemies.append(Boss19())

        elif type == GameConstants.EnemyType.BOSS20:
            EnemiesManager.list_enemies.append(Boss20())
