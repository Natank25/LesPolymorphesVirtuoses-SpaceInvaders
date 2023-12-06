import os
import random
from enum import Enum

import pygame
from pygame.sprite import AbstractGroup


class GameConstants:
    win_size = []

    difficulty = 1

    class GameEvents(Enum):
        # common
        CommonInvader1SpawnEvent = pygame.USEREVENT + 1
        CommonInvader2SpawnEvent = pygame.USEREVENT + 2

        # speed
        SpeedInvader1SpawnEvent = pygame.USEREVENT + 3
        SpeedInvader2SpawnEvent = pygame.USEREVENT + 4

        # tank
        TankInvader1SpawnEvent = pygame.USEREVENT + 5

        # boss
        Boss1SpawnEvent = pygame.USEREVENT + 6

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

        # speed
        SpeedInvader1DefaultHealth = 1
        SpeedInvader1DefaultSpeedx = 0.4
        SpeedInvader1DefaultSpeedy = 0.3

        SpeedInvader2DefaultHealth = 3
        SpeedInvader2DefaultSpeedx = 0.5
        SpeedInvader2DefaultSpeedy = 0.4

        # tank
        TankInvader1DefaultHealth = 20
        TankInvader1DefaultSpeedx = 0.2
        TankInvader1DefaultSpeedy = 0.075

        # Boss
        Boss1DefaultHealth = 150
        Boss1DefaultSpeedx = 2
        Boss1DefaultSpeedy = 0.2
        Boss1DefaultSpeedATK = 1

    class EnemyType(Enum):
        # common
        COMMONINVADER1 = "CommonInvader1"
        COMMONINVADER2 = "CommonInvader2"

        # speed
        SPEEDINVADER1 = "SpeedInvader1"
        SPEEDINVADER2 = "SpeedInvader2"

        # tank
        TANKINVADER1 = "TankInvader1"

        # Boss
        BOSS1 = "Boss1"

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
    def __init__(self, hauteur, speedx, speedy, health, ATKspeed, img_name, file_ext="png", *groups: AbstractGroup):
        super().__init__(*groups)
        self.hauteur = hauteur
        self.speedx = speedx
        self.speedy = speedy
        self.health = health
        self.ATKspeed = ATKspeed
        self.img_name = pygame.image.load(os.path.join('..', "img", img_name +
                                                       "." + file_ext))


class Boss1(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur,
                         GameConstants.EnemyAttributes.Boss1DefaultSpeedx.value + (
                                 GameConstants.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss1DefaultSpeedy.value + (
                                 GameConstants.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss1DefaultHealth.value * (
                                 1 + GameConstants.difficulty),
                         GameConstants.EnemyAttributes.Boss1DefaultSpeedATK.value + GameConstants.difficulty,
                         img_name="CommonInvader1")


class Invader(pygame.sprite.Sprite):
    def __init__(self, hauteur, speedx, speedy, health, img_name, file_ext="png", *groups: AbstractGroup):
        super().__init__(*groups)
        self.speedx = speedx
        self.speedy = speedy
        self.depart = random.randint(0, GameConstants.win_size[0])
        self.hauteur = hauteur
        self.image = pygame.image.load(os.path.join('..', "img", img_name +
                                                    "." + file_ext))
        self.health = health

    def avancer(self):
        self.hauteur += self.speedx
        if (self.depart < 0 or self.depart >
                pygame.display.get_window_size()[0]):
            self.speedy = -self.speedy

        self.depart += self.speedy


class CommonInvader1(Invader):
    def __init__(self):
        super().__init__(0,
                         GameConstants.EnemyAttributes.CommonInvaders1DefaultSpeedx.value + (
                                 GameConstants.difficulty / 10),
                         GameConstants.EnemyAttributes.CommonInvaders1DefaultSpeedy.value + (
                                 GameConstants.difficulty / 20),
                         GameConstants.EnemyAttributes.CommonInvaders1DefaultHealth.value * (
                                 1 + GameConstants.difficulty),
                         "CommonInvader1")


class CommonInvader2(Invader):
    def __init__(self):
        super().__init__(0,
                         GameConstants.EnemyAttributes.CommonInvaders2DefaultSpeedx.value + (
                                 GameConstants.difficulty / 10),
                         GameConstants.EnemyAttributes.CommonInvaders2DefaultSpeedy.value + (
                                 GameConstants.difficulty / 20),
                         GameConstants.EnemyAttributes.CommonInvaders2DefaultHealth.value * (
                                 1 + GameConstants.difficulty),
                         "CommonInvader2")


class SpeedInvader1(Invader):
    def __init__(self):
        super().__init__(0,
                         GameConstants.EnemyAttributes.SpeedInvader1DefaultSpeedx.value + (
                                 GameConstants.difficulty / 10),
                         GameConstants.EnemyAttributes.SpeedInvader1DefaultSpeedy.value + (
                                 GameConstants.difficulty / 20),
                         GameConstants.EnemyAttributes.SpeedInvader2DefaultHealth.value * (
                                 1 + GameConstants.difficulty),
                         "SpeedInvader1")


class SpeedInvader2(Invader):
    def __init__(self):
        super().__init__(0,
                         GameConstants.EnemyAttributes.SpeedInvader2DefaultSpeedx.value + (
                                 GameConstants.difficulty / 10),
                         GameConstants.EnemyAttributes.SpeedInvader2DefaultSpeedy.value + (
                                 GameConstants.difficulty / 20),
                         GameConstants.EnemyAttributes.SpeedInvader2DefaultHealth.value * (
                                 1 + GameConstants.difficulty),
                         "SpeedInvader2")


class TankInvader1(Invader):
    def __init__(self):
        super().__init__(0,
                         GameConstants.EnemyAttributes.TankInvader1DefaultSpeedx.value + (
                                 GameConstants.difficulty / 10),
                         GameConstants.EnemyAttributes.TankInvader1DefaultSpeedy.value + (
                                 GameConstants.difficulty / 20),
                         GameConstants.EnemyAttributes.TankInvader1DefaultHealth.value * (
                                 1 + GameConstants.difficulty),
                         "SpeedInvader1")


class EnemiesManager:
    list_enemies = []

    @staticmethod
    def send_waves_endless(difficulty: int):
        for i in range(difficulty * 3):
            pass

    @staticmethod
    def send_waves_levels(num_lvl: int):
        match num_lvl:
            case 1:
                pygame.time.set_timer(
                    GameConstants.GameEvents.CommonInvader1SpawnEvent.value,
                    1500, 3)

            case 2:
                for i in range(2):
                    pygame.time.set_timer(
                        GameConstants.GameEvents.CommonInvader1SpawnEvent.value,
                        1500)
                    pygame.time.set_timer(
                        GameConstants.GameEvents.SpeedInvader1SpawnEvent.value,
                        3000)
            case 3:
                pygame.time.set_timer(
                    GameConstants.GameEvents.CommonInvader1SpawnEvent.value,
                    1500, 4)
                pygame.time.set_timer(
                    GameConstants.GameEvents.SpeedInvader1SpawnEvent.value,
                    3000, 2)
            case 4:
                for i in range(3):
                    pygame.time.set_timer(
                        GameConstants.GameEvents.CommonInvader1SpawnEvent.value,
                        1500, 2)
                    pygame.time.set_timer(
                        GameConstants.GameEvents.SpeedInvader1SpawnEvent.value,
                        3000)
            case 5:
                pygame.time.set_timer(
                    GameConstants.GameEvents.Boss1SpawnEvent.value, 0)
            case 6:
                for i in range(3):
                    pygame.time.set_timer(
                        GameConstants.GameEvents.CommonInvader1SpawnEvent.value,
                        1500, 2)
                    pygame.time.set_timer(
                        GameConstants.GameEvents.SpeedInvader1SpawnEvent.value,
                        3000)
                    pygame.time.set_timer(
                        GameConstants.GameEvents.CommonInvader2SpawnEvent.value,
                        4500)
            case 7:
                for i in range(3):
                    pygame.time.set_timer(
                        GameConstants.GameEvents.CommonInvader2SpawnEvent.value,
                        1500, 2)
                    pygame.time.set_timer(
                        GameConstants.GameEvents.SpeedInvader1SpawnEvent.value,
                        3000)
                    pygame.time.set_timer(
                        GameConstants.GameEvents.SpeedInvader2SpawnEvent.value,
                        4500)
            case 8:
                for i in range(5):
                    pygame.time.set_timer(
                        GameConstants.GameEvents.CommonInvader2SpawnEvent.value,
                        1500, 2)
                    pygame.time.set_timer(
                        GameConstants.GameEvents.SpeedInvader2SpawnEvent.value,
                        3000, 2)
                pygame.time.set_timer(
                    GameConstants.GameEvents.TankInvader1SpawnEvent.value,
                    4500)
            case 9:
                for i in range(3):
                    pygame.time.set_timer(
                        GameConstants.GameEvents.CommonInvader2SpawnEvent.value,
                        1500, 4)
                    pygame.time.set_timer(
                        GameConstants.GameEvents.SpeedInvader2SpawnEvent.value,
                        3000, 2)
                    pygame.time.set_timer(
                        GameConstants.GameEvents.TankInvader1SpawnEvent.value,
                        4500)
            case 10:
                pass

    @staticmethod
    def spawnEnemy(type: GameConstants.EnemyType):

        # common
        if type == GameConstants.EnemyType.COMMONINVADER1:
            EnemiesManager.list_enemies.append(CommonInvader1())

        elif type == GameConstants.EnemyType.COMMONINVADER2:
            EnemiesManager.list_enemies.append(CommonInvader2())

        # speed
        elif type == GameConstants.EnemyType.SPEEDINVADER1:
            EnemiesManager.list_enemies.append(CommonInvader1())

        elif type == GameConstants.EnemyType.SPEEDINVADER2:
            EnemiesManager.list_enemies.append(SpeedInvader2())

        # tank
        elif type == GameConstants.EnemyType.TANKINVADER1:
            EnemiesManager.list_enemies.append(TankInvader1())

        # Boss
        elif type == GameConstants.EnemyType.BOSS1:
            EnemiesManager.list_enemies.append(Boss1())
