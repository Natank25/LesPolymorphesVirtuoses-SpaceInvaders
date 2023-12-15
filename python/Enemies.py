import os
from enum import Enum
from random import randint

import pygame

from python.GameProperties import GameProperties
from python.Groups import Groups
from python.Resources import Ennemies

pygame.init()


class Balle(pygame.sprite.Sprite):
    def __init__(self, pos, speed=0.3, damage=1):

        self.image = Ennemies.Images.Balle
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * GameProperties.win_scale),
                                                         int(self.image.get_height() * GameProperties.win_scale)))
        self.rect = self.image.get_rect(center=pos)
        self.speed = speed
        self.damage = damage
        super().__init__(Groups.BulletGroup, Groups.AllSprites)

    def update(self):
        self.rect.move_ip(0,50)

class Invader(pygame.sprite.Sprite):
    def __init__(self, speedx, speedy, health, image, shooter=False, ATKspeed=0.05, can_esquive=False):
        self.image = image
        self.speedx = speedx
        self.speedy = speedy
        self.health = health
        self.shooter = shooter
        self.next_shot = pygame.time.get_ticks() + 1 / ATKspeed
        self.last_shot = pygame.time.get_ticks()
        self.lastEsquive = pygame.time.get_ticks()
        self.nextEsquive = pygame.time.get_ticks() + randint(500, 5000)
        self.canEsquive = can_esquive
        self.ATKspeed = ATKspeed
        self.rect = self.image.get_rect(topleft=(
            randint(GameProperties.win_size.x + 10, GameProperties.win_size.width - self.image.get_width() - 10),
            GameProperties.win_size.y + 10))
        super().__init__(Groups.InvaderGroup, Groups.AllSprites)

    def apply_damage(self, amount):
        self.health -= amount

    def avancer(self):

        self.rect.move_ip(self.speedx * GameProperties.deltatime * GameProperties.win_scale,
                          self.speedy * GameProperties.deltatime * GameProperties.win_scale)

        if self.rect.x < GameProperties.win_size.x or self.rect.x + self.rect.width > GameProperties.win_size.x + GameProperties.win_size.width:
            self.speedx = -self.speedx

    def tirer(self):
        if self.shooter:
            Balle(self.rect.center)

    def esquive(self):
        self.speedy = -self.speedy

    def update(self, *args, **kwargs):
        if self.canEsquive and pygame.time.get_ticks() >= self.nextEsquive:
            self.esquive()
            self.lastEsquive = pygame.time.get_ticks()
            self.nextEsquive = pygame.time.get_ticks() + randint(500, 5000)
        self.avancer()

        if self.health < 0:
            self.kill()

        if self.shooter and pygame.time.get_ticks() >= self.last_shot:
            self.tirer()
            self.last_shot = pygame.time.get_ticks()
            self.next_shot = pygame.time.get_ticks() + 1 / self.ATKspeed


class CommonInvader1(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.CommonInvaders1DefaultSpeedx.value * GameProperties.difficulty,
                         EnemyAttributes.CommonInvaders1DefaultSpeedy.value * GameProperties.difficulty / 2,
                         EnemyAttributes.CommonInvaders1DefaultHealth.value * (1 + GameProperties.difficulty),
                         Ennemies.Images.CommonInvader1)


class CommonInvader2(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.CommonInvaders2DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.CommonInvaders2DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.CommonInvaders2DefaultHealth.value * (1 + GameProperties.difficulty),
                         Ennemies.Images.CommonInvader2)


class CommonInvader3(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.CommonInvaders3DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.CommonInvaders3DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.CommonInvaders3DefaultHealth.value * (1 + GameProperties.difficulty),
                         Ennemies.Images.CommonInvader3)


class SpeedInvader1(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.SpeedInvader1DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.SpeedInvader1DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.SpeedInvader2DefaultHealth.value * (1 + GameProperties.difficulty),
                         Ennemies.Images.SpeedInvader1)


class SpeedInvader2(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.SpeedInvader2DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.SpeedInvader2DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.SpeedInvader2DefaultHealth.value * (1 + GameProperties.difficulty),
                         Ennemies.Images.SpeedInvader2)


class SpeedInvader3(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.SpeedInvader2DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.SpeedInvader2DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.SpeedInvader2DefaultHealth.value * (1 + GameProperties.difficulty),
                         Ennemies.Images.SpeedInvader3)


class TankInvader1(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.TankInvader1DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.TankInvader1DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.TankInvader1DefaultHealth.value * (1 + GameProperties.difficulty),
                         Ennemies.Images.TankInvader1)


class TankInvader2(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.TankInvader2DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.TankInvader2DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.TankInvader2DefaultHealth.value * (1 + GameProperties.difficulty),
                         TankInvader2)


class TankInvader3(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.TankInvader3DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.TankInvader3DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.TankInvader3DefaultHealth.value * (1 + GameProperties.difficulty),
                         TankInvader3)


class ShooterInvader1(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.ShooterInvader1DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.ShooterInvader1DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.ShooterInvader1DefaultHealth.value * (1 + GameProperties.difficulty),
                         Ennemies.Images.SpeedInvader1, shooter=True)


class ShooterInvader2(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.ShooterInvader2DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.ShooterInvader2DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.ShooterInvader2DefaultHealth.value * (1 + GameProperties.difficulty),
                         'SpeedInvader1', shooter=True, ATKspeed=EnemyAttributes.ShooterInvader2DefaultSpeedATK.value)


class ShooterInvader3(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.ShooterInvader3DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.ShooterInvader3DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.ShooterInvader3DefaultHealth.value * (1 + GameProperties.difficulty),
                         'SpeedInvader1', shooter=True, ATKspeed=EnemyAttributes.ShooterInvader3DefaultSpeedATK.value)


class Boss(pygame.sprite.Sprite):
    def __init__(self, hauteur, speedx, speedy, health, ATKspeed, img_name, file_ext="png", *groups):
        self.hauteur = hauteur
        self.speedx = speedx
        self.speedy = speedy
        self.health = health
        self.ATKspeed = ATKspeed
        self.image_path = os.path.join("img", img_name + "." + file_ext)
        self.image = pygame.image.load(self.image_path)
        super().__init__(*groups, Groups.AllSprites)


# region Bosses

class Boss1(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss1DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss1DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss1DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss1DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss2(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss2DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss2DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss2DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss2DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss3(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss3DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss3DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss3DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss3DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss4(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss4DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss4DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss4DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss4DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss5(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss5DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss5DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss5DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss5DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss6(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss6DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss6DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss6DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss6DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss7(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss7DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss7DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss7DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss7DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss8(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss8DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss8DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss8DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss8DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss9(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss9DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss9DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss9DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss9DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss10(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss10DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss10DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss10DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss10DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss11(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss11DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss11DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss11DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss11DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss12(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss12DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss12DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss12DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss12DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss13(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss13DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss13DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss13DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss13DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss14(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss14DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss14DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss14DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss14DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss15(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss15DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss15DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss15DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss15DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss16(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss16DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss16DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss16DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss16DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss17(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss17DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss17DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss17DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss17DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss18(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss18DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss18DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss18DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss18DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss19(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss19DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss19DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss19DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss19DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss20(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss20DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         EnemyAttributes.Boss20DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss20DefaultHealth.value * (1 + GameProperties.difficulty),
                         EnemyAttributes.Boss20DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class EnemyAttributes(Enum):
    # common
    CommonInvaders1DefaultHealth = 1
    CommonInvaders1DefaultSpeedx = 0.1
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
    ShooterInvader1DefaultSpeedx = 0.2
    ShooterInvader1DefaultSpeedy = 0.2
    ShooterInvader1DefaultSpeedATK = 0.05

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

    def __init__(self, enemy_name, enemy_class):
        self.enemy_name = enemy_name
        self.enemy_class = enemy_class
        self.spawn_event_name = self.enemy_name + "SpawnEvent"

    # common
    COMMONINVADER1 = "CommonInvader1", CommonInvader1
    COMMONINVADER2 = "CommonInvader2", CommonInvader2
    COMMONINVADER3 = "CommonInvader3", CommonInvader3

    # speed
    SPEEDINVADER1 = "SpeedInvader1", SpeedInvader1
    SPEEDINVADER2 = "SpeedInvader2", SpeedInvader2
    SPEEDINVADER3 = "SpeedInvader3", SpeedInvader3

    # tank
    TANKINVADER1 = "TankInvader1", TankInvader1
    TANKINVADER2 = "TankInvader2", TankInvader2
    TANKINVADER3 = "TankInvader3", TankInvader3

    # shooter
    SHOOTERINVADER1 = "ShooterInvader1", ShooterInvader1
    SHOOTERINVADER2 = "ShooterInvader2", ShooterInvader2
    SHOOTERINVADER3 = "ShooterInvader3", ShooterInvader3

    # Boss
    BOSS1 = "Boss1", Boss1
    BOSS2 = "Boss2", Boss2
    BOSS3 = "Boss3", Boss3
    BOSS4 = "Boss4", Boss4
    BOSS5 = "Boss5", Boss5
    BOSS6 = "Boss6", Boss6
    BOSS7 = "Boss7", Boss7
    BOSS8 = "Boss8", Boss8
    BOSS9 = "Boss9", Boss9
    BOSS10 = "Boss10", Boss10
    BOSS11 = "Boss11", Boss11
    BOSS12 = "Boss12", Boss12
    BOSS13 = "Boss13", Boss13
    BOSS14 = "Boss14", Boss14
    BOSS15 = "Boss15", Boss15
    BOSS16 = "Boss16", Boss16
    BOSS17 = "Boss17", Boss17
    BOSS18 = "Boss18", Boss18
    BOSS19 = "Boss19", Boss19
    BOSS20 = "Boss20", Boss20
