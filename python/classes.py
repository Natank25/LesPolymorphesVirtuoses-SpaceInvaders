import os
import random
import sys
import threading
from enum import Enum

import pygame


class AllSpritesGroup(pygame.sprite.RenderClear):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def moveSprites(self, current_window: pygame.rect.Rect, prev_window: pygame.rect.Rect):
        scale_x = current_window.width / prev_window.width
        scale_y = current_window.height / prev_window.height

        GameProperties.win_scale = current_window.width / GameConstants.default_win_size[0]

        for sprite in self.sprites():

            if hasattr(sprite, 'image_path'):
                sprite.image = pygame.transform.scale(pygame.image.load(sprite.image_path), (int(scale_x * sprite.image.get_width()), int(scale_y * sprite.image.get_height())))
            else:
                sprite.image = pygame.transform.scale(sprite.image, (int(scale_x * sprite.image.get_width()), int(scale_y * sprite.image.get_height())))

            new_x = int((sprite.rect.x - prev_window.x) * scale_x + current_window.x)
            new_y = int((sprite.rect.y - prev_window.y) * scale_y + current_window.y)

            sprite.rect = sprite.image.get_rect(topleft=(new_x, new_y))


class UIGroup(AllSpritesGroup):
    def __init__(self, *sprites):
        super().__init__(*sprites)


class MetaClassGP(type):
    background = pygame.image.load(os.path.join("..", "img", "background_menu.png"))

    def __setattr__(self, key, value):
        if key == 'background':
            value = pygame.transform.scale(value, (value.get_width() * GameProperties.win_scale, value.get_height() * GameProperties.win_scale))
            GameProperties.screen.blit(value, GameProperties.win_size.topleft)
            GameProperties.screen.fill("black")
            GameProperties.screen.blit(pygame.transform.scale(value, GameProperties.win_size.size), GameProperties.win_size.topleft)
            pygame.image.save(GameProperties.screen.copy(), "bg.png")
            GameProperties.group_background = pygame.image.load("bg.png")

        super().__setattr__(key, value)


class GameProperties(metaclass=MetaClassGP):
    win_size: pygame.Rect = pygame.Rect(0, 0, 1920, 1080)

    difficulty = 1

    deltatime = 0

    win_scale = 1

    on_going_threads = []

    screen: pygame.surface.Surface = None

    screen_mask = None

    background = pygame.image.load(os.path.join("..", "img", "background_menu.png"))

    group_background = pygame.image.load(os.path.join("..", "img", "background_menu.png"))

    AllSprites: AllSpritesGroup = AllSpritesGroup()
    InvaderGroup: pygame.sprite.RenderClear = pygame.sprite.RenderClear()
    PlayerGroup: pygame.sprite.RenderClear = pygame.sprite.RenderClear()
    BulletGroup: pygame.sprite.RenderClear = pygame.sprite.RenderClear()
    ButtonGroup: pygame.sprite.RenderClear = pygame.sprite.RenderClear()
    UIGroup: UIGroup = UIGroup()


# region Enemies
class Invader(pygame.sprite.Sprite):
    def __init__(self, hauteur, speedx, speedy, health, img_name, shooter=False, ATKspeed=0, can_esquive=False, file_ext="png"):
        super().__init__(GameProperties.InvaderGroup, GameProperties.AllSprites)  # Run program and fix error
        self.speedx = speedx
        self.speedy = speedy
        self.depart = random.randint(0, GameProperties.win_size[0])
        self.hauteur = hauteur
        self.image_path = os.path.join("..", "img", img_name + "." + file_ext)
        self.image = pygame.image.load(self.image_path)
        self.health = health
        self.shooter = shooter
        self.ATKspeed = ATKspeed
        self.lastEsquive = pygame.time.get_ticks()
        self.nextEsquive = pygame.time.get_ticks() + random.randint(500, 5000)
        self.canEsquive = can_esquive
        self.rect = self.image.get_rect()
        self.rect.topleft = (random.randint(GameProperties.win_size.x + 10, GameProperties.win_size.width - self.rect.width - 10), GameProperties.win_size.y + 10)

    def apply_damage(self, amount):
        self.health -= amount

    def avancer(self):

        self.rect.y += self.speedy * GameProperties.deltatime * GameProperties.win_scale
        self.rect.x += self.speedx * GameProperties.deltatime * GameProperties.win_scale

        if self.rect.x < GameProperties.win_size.x or self.rect.x + self.rect.width > GameProperties.win_size.x + GameProperties.win_size.width:
            self.speedx = -self.speedx

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
        if self.health < 0:
            self.kill()


class CommonInvader1(Invader):
    def __init__(self):
        super().__init__(0, GameConstants.EnemyAttributes.CommonInvaders1DefaultSpeedx.value * GameProperties.difficulty,
                         GameConstants.EnemyAttributes.CommonInvaders1DefaultSpeedy.value * GameProperties.difficulty / 2,
                         GameConstants.EnemyAttributes.CommonInvaders1DefaultHealth.value * (1 + GameProperties.difficulty), "CommonInvader1")


class CommonInvader2(Invader):
    def __init__(self):
        super().__init__(0, GameConstants.EnemyAttributes.CommonInvaders2DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.CommonInvaders2DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.CommonInvaders2DefaultHealth.value * (1 + GameProperties.difficulty), "CommonInvader2")


class CommonInvader3(Invader):
    def __init__(self):
        super().__init__(0, GameConstants.EnemyAttributes.CommonInvaders3DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.CommonInvaders3DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.CommonInvaders3DefaultHealth.value * (1 + GameProperties.difficulty), "CommonInvader2")


class SpeedInvader1(Invader):
    def __init__(self):
        super().__init__(0, GameConstants.EnemyAttributes.SpeedInvader1DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.SpeedInvader1DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.SpeedInvader2DefaultHealth.value * (1 + GameProperties.difficulty), "SpeedInvader1")


class SpeedInvader2(Invader):
    def __init__(self):
        super().__init__(0, GameConstants.EnemyAttributes.SpeedInvader2DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.SpeedInvader2DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.SpeedInvader2DefaultHealth.value * (1 + GameProperties.difficulty), "SpeedInvader2")


class SpeedInvader3(Invader):
    def __init__(self):
        super().__init__(0, GameConstants.EnemyAttributes.SpeedInvader2DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.SpeedInvader2DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.SpeedInvader2DefaultHealth.value * (1 + GameProperties.difficulty), "SpeedInvader2")


class TankInvader1(Invader):
    def __init__(self):
        super().__init__(0, GameConstants.EnemyAttributes.TankInvader1DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.TankInvader1DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.TankInvader1DefaultHealth.value * (1 + GameProperties.difficulty), "SpeedInvader1")


class TankInvader2(Invader):
    def __init__(self):
        super().__init__(0, GameConstants.EnemyAttributes.TankInvader2DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.TankInvader2DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.TankInvader2DefaultHealth.value * (1 + GameProperties.difficulty), "SpeedInvader1")


class TankInvader3(Invader):
    def __init__(self):
        super().__init__(0, GameConstants.EnemyAttributes.TankInvader3DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.TankInvader3DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.TankInvader3DefaultHealth.value * (1 + GameProperties.difficulty), "SpeedInvader1")


class ShooterInvader1(Invader):
    def __init__(self):
        super().__init__(0, GameConstants.EnemyAttributes.ShooterInvader1DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.ShooterInvader1DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.ShooterInvader1DefaultHealth.value * (1 + GameProperties.difficulty), 'SpeedInvader1', shooter=True,
                         ATKspeed=GameConstants.EnemyAttributes.ShooterInvader1DefaultSpeedATK.value)


class ShooterInvader2(Invader):
    def __init__(self):
        super().__init__(0, GameConstants.EnemyAttributes.ShooterInvader2DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.ShooterInvader2DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.ShooterInvader2DefaultHealth.value * (1 + GameProperties.difficulty), 'SpeedInvader1', shooter=True,
                         ATKspeed=GameConstants.EnemyAttributes.ShooterInvader2DefaultSpeedATK.value)


class ShooterInvader3(Invader):
    def __init__(self):
        super().__init__(0, GameConstants.EnemyAttributes.ShooterInvader3DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.ShooterInvader3DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.ShooterInvader3DefaultHealth.value * (1 + GameProperties.difficulty), 'SpeedInvader1', shooter=True,
                         ATKspeed=GameConstants.EnemyAttributes.ShooterInvader3DefaultSpeedATK.value)


class Boss(pygame.sprite.Sprite):
    def __init__(self, hauteur, speedx, speedy, health, ATKspeed, img_name, file_ext="png", *groups):
        super().__init__(*groups, GameProperties.AllSprites)
        self.hauteur = hauteur
        self.speedx = speedx
        self.speedy = speedy
        self.health = health
        self.ATKspeed = ATKspeed
        self.image_path = os.path.join("..", "img", img_name + "." + file_ext)
        self.image = pygame.image.load(self.image_path)


# region Bosses

class Boss1(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss1DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss1DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss1DefaultHealth.value * (1 + GameProperties.difficulty), GameConstants.EnemyAttributes.Boss1DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss2(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss2DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss2DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss2DefaultHealth.value * (1 + GameProperties.difficulty), GameConstants.EnemyAttributes.Boss2DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss3(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss3DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss3DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss3DefaultHealth.value * (1 + GameProperties.difficulty), GameConstants.EnemyAttributes.Boss3DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss4(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss4DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss4DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss4DefaultHealth.value * (1 + GameProperties.difficulty), GameConstants.EnemyAttributes.Boss4DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss5(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss5DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss5DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss5DefaultHealth.value * (1 + GameProperties.difficulty), GameConstants.EnemyAttributes.Boss5DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss6(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss6DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss6DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss6DefaultHealth.value * (1 + GameProperties.difficulty), GameConstants.EnemyAttributes.Boss6DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss7(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss7DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss7DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss7DefaultHealth.value * (1 + GameProperties.difficulty), GameConstants.EnemyAttributes.Boss7DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss8(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss8DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss8DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss8DefaultHealth.value * (1 + GameProperties.difficulty), GameConstants.EnemyAttributes.Boss8DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss9(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss9DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss9DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss9DefaultHealth.value * (1 + GameProperties.difficulty), GameConstants.EnemyAttributes.Boss9DefaultSpeedATK.value + GameProperties.difficulty,
                         img_name="CommonInvader1")


class Boss10(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss10DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss10DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss10DefaultHealth.value * (1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss10DefaultSpeedATK.value + GameProperties.difficulty, img_name="CommonInvader1")


class Boss11(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss11DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss11DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss11DefaultHealth.value * (1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss11DefaultSpeedATK.value + GameProperties.difficulty, img_name="CommonInvader1")


class Boss12(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss12DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss12DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss12DefaultHealth.value * (1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss12DefaultSpeedATK.value + GameProperties.difficulty, img_name="CommonInvader1")


class Boss13(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss13DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss13DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss13DefaultHealth.value * (1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss13DefaultSpeedATK.value + GameProperties.difficulty, img_name="CommonInvader1")


class Boss14(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss14DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss14DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss14DefaultHealth.value * (1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss14DefaultSpeedATK.value + GameProperties.difficulty, img_name="CommonInvader1")


class Boss15(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss15DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss15DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss15DefaultHealth.value * (1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss15DefaultSpeedATK.value + GameProperties.difficulty, img_name="CommonInvader1")


class Boss16(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss16DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss16DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss16DefaultHealth.value * (1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss16DefaultSpeedATK.value + GameProperties.difficulty, img_name="CommonInvader1")


class Boss17(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss17DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss17DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss17DefaultHealth.value * (1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss17DefaultSpeedATK.value + GameProperties.difficulty, img_name="CommonInvader1")


class Boss18(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss18DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss18DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss18DefaultHealth.value * (1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss18DefaultSpeedATK.value + GameProperties.difficulty, img_name="CommonInvader1")


class Boss19(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss19DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss19DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss19DefaultHealth.value * (1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss19DefaultSpeedATK.value + GameProperties.difficulty, img_name="CommonInvader1")


class Boss20(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, GameConstants.EnemyAttributes.Boss20DefaultSpeedx.value + (GameProperties.difficulty / 10),
                         GameConstants.EnemyAttributes.Boss20DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         GameConstants.EnemyAttributes.Boss20DefaultHealth.value * (1 + GameProperties.difficulty),
                         GameConstants.EnemyAttributes.Boss20DefaultSpeedATK.value + GameProperties.difficulty, img_name="CommonInvader1")


# endregion

# endregion


class GameConstants:
    default_win_size = [500, 800]

    class UI:
        play_game_img = pygame.image.load(os.path.join("..", "img", "UI", "buttons", "play_button.png"))

    class PlayerProperties:
        SPEED = 0.3

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
        SHOOTERINVADER1 = "ShooterInvader1", SpeedInvader1
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


class Balle(pygame.sprite.Sprite):
    def __init__(self, ship: pygame.rect.Rect, speed=0.3, damage=1, fire_speed=1):
        super().__init__(GameProperties.BulletGroup, GameProperties.AllSprites)

        self.image_path = os.path.join('..', "img", "balle.png")
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * GameProperties.win_scale), int(self.image.get_height() * GameProperties.win_scale)))
        self.rect = self.image.get_rect()
        self.rect.center = ship.center
        self.speed = speed
        self.damage = damage
        self.fire_speed = fire_speed

    def update(self):
        if self.rect.bottom > 0:
            self.rect.y -= self.speed * GameProperties.deltatime * GameProperties.win_scale
        else:
            self.kill()
        collided_sprites = pygame.sprite.groupcollide(GameProperties.BulletGroup, GameProperties.InvaderGroup, True, False)
        for bullet in collided_sprites:
            for invader in collided_sprites[bullet]:
                invader.apply_damage(bullet.damage)

class Player(pygame.sprite.Sprite):
    def __init__(self, img_name, file_ext="png"):
        super().__init__(GameProperties.PlayerGroup, GameProperties.AllSprites)
        self.image_path = os.path.join("..", "img", img_name + "." + file_ext)
        self.image = pygame.image.load(self.image_path)
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * GameProperties.win_scale), int(self.image.get_height() * GameProperties.win_scale)))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(GameProperties.win_size.x, GameProperties.win_size.x + GameProperties.win_size.width - self.rect.width)
        self.rect.y = GameProperties.win_size.height - 100 * GameProperties.win_scale
        self.timeLastShot = pygame.time.get_ticks()
        self.cooldown = 100

    def controls(self, keys):
        speed = GameConstants.PlayerProperties.SPEED * GameProperties.win_scale * GameProperties.deltatime
        dist_x = 0
        dist_y = 0
        if keys[pygame.K_z]:
            dist_y -= speed
        if keys[pygame.K_s]:
            dist_y += speed
        if keys[pygame.K_q]:
            dist_x -= speed
        if keys[pygame.K_d]:
            dist_x += speed

        if dist_x != 0 and dist_y != 0:
            length = (dist_x ** 2 + dist_y ** 2) ** 0.5

            dist_x = (dist_x / length) * speed
            dist_y = (dist_y / length) * speed

        if self.rect.x + dist_x > GameProperties.win_size.x and self.rect.x + dist_x + self.rect.width < GameProperties.win_size.width + GameProperties.win_size.x:
            self.rect.move_ip(dist_x, 0)
        if self.rect.y + dist_y > GameProperties.win_size.y and self.rect.y + dist_y + self.rect.height < GameProperties.win_size.height + GameProperties.win_size.y:
            self.rect.move_ip(0, dist_y)

    def tirer(self):
        Balle(self.rect)

    def update(self):
        keys = pygame.key.get_pressed()
        self.controls(keys)

        if keys[pygame.K_SPACE] and pygame.time.get_ticks() > self.timeLastShot + self.cooldown:
            self.timeLastShot = pygame.time.get_ticks()
            self.tirer()


class EnemiesManager:
    list_enemies = []

    @staticmethod
    def update():
        pass

    @staticmethod
    def send_waves_endless(difficulty: int):
        for i in range(difficulty * 3):
            pass

    @staticmethod
    def send_waves_levels(num_lvl: int):
        match num_lvl:
            case 1:
                for i in range(3 + GameProperties.difficulty):
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.COMMONINVADER1, 1500 * i)

            case 2:
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.COMMONINVADER1, 1500 * i)
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.SPEEDINVADER1, 3000 * i)

            case 3:
                for i in range(4 + GameProperties.difficulty):
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.COMMONINVADER1, 1500 * i)
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.SPEEDINVADER1, 3000 * i)

            case 4:
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.COMMONINVADER1, 1500 * i)
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.SPEEDINVADER1, 3000 * i)
            case 5:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS1)
            case 6:
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.COMMONINVADER1, 1500 * i)
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.SPEEDINVADER1, 3000 * i)
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.SPEEDINVADER2, 4500 * i)
            case 7:
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.COMMONINVADER1, 1500 * i)
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.SPEEDINVADER1, 3000 * i)
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.SPEEDINVADER2, 4500 * i)
            case 8:
                for i in range(4 + GameProperties.difficulty):
                    for j in range(2 + GameProperties.difficulty):
                        EnemiesManager.spawnEnemy(GameConstants.EnemyType.COMMONINVADER2, 1500 * i * j)
                        EnemiesManager.spawnEnemy(GameConstants.EnemyType.SPEEDINVADER2, 3000 * i * j)
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.TANKINVADER1, 4500 * i)
            case 9:
                for i in range(2 + GameProperties.difficulty):
                    for j in range(3 + GameProperties.difficulty):
                        EnemiesManager.spawnEnemy(GameConstants.EnemyType.COMMONINVADER2, 1500 * i * j)
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.SPEEDINVADER2, 3000 * i)
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.TANKINVADER1, 4500 * i)
            case 10:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS2)
            case 11:
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.SPEEDINVADER2, 1500 * i)
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.TANKINVADER1, 3000 * i)
                    for j in range(3 + GameProperties.difficulty):
                        EnemiesManager.spawnEnemy(GameConstants.EnemyType.COMMONINVADER2, 1500 * i * j)
            case 12:
                for i in range(3 + GameProperties.difficulty):
                    for j in range(3 + GameProperties.difficulty):
                        EnemiesManager.spawnEnemy(GameConstants.EnemyType.SPEEDINVADER2, 1500 * i * j)
                        EnemiesManager.spawnEnemy(GameConstants.EnemyType.TANKINVADER1, 3000 * i * j)
                    EnemiesManager.spawnEnemy(GameConstants.EnemyType.SPEEDINVADER2, 1500 * i)
            case 13:
                pass
            case 14:
                pass
            case 15:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS3)
            case 16:
                pass
            case 17:
                pass
            case 18:
                pass
            case 19:
                pass
            case 20:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS4)
            case 21:
                pass
            case 22:
                pass
            case 23:
                pass
            case 24:
                pass
            case 25:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS5)
            case 26:
                pass
            case 27:
                pass
            case 28:
                pass
            case 29:
                pass
            case 30:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS6)
            case 31:
                pass
            case 32:
                pass
            case 33:
                pass
            case 34:
                pass
            case 35:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS7)
            case 36:
                pass
            case 37:
                pass
            case 39:
                pass
            case 40:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS8)
            case 41:
                pass
            case 42:
                pass
            case 43:
                pass
            case 44:
                pass
            case 45:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS9)
            case 46:
                pass
            case 47:
                pass
            case 48:
                pass
            case 49:
                pass
            case 50:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS10)
            case 51:
                pass
            case 52:
                pass
            case 53:
                pass
            case 54:
                pass
            case 55:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS11)
            case 56:
                pass
            case 57:
                pass
            case 58:
                pass
            case 59:
                pass
            case 60:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS12)
            case 61:
                pass
            case 62:
                pass
            case 63:
                pass
            case 64:
                pass
            case 65:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS13)
            case 66:
                pass
            case 67:
                pass
            case 68:
                pass
            case 69:
                pass
            case 70:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS14)
            case 71:
                pass
            case 72:
                pass
            case 73:
                pass
            case 74:
                pass
            case 75:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS15)
            case 76:
                pass
            case 77:
                pass
            case 78:
                pass
            case 79:
                pass
            case 80:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS16)
            case 81:
                pass
            case 82:
                pass
            case 83:
                pass
            case 84:
                pass
            case 85:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS17)
            case 86:
                pass
            case 87:
                pass
            case 88:
                pass
            case 89:
                pass
            case 90:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS18)
            case 91:
                pass
            case 92:
                pass
            case 93:
                pass
            case 94:
                pass
            case 95:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS19)
            case 96:
                pass
            case 97:
                pass
            case 98:
                pass
            case 99:
                pass
            case 100:
                EnemiesManager.spawnEnemy(GameConstants.EnemyType.BOSS20)

    @staticmethod
    def spawnEnemy(enemy_type: GameConstants.EnemyType, delay: float = None):
        if delay is None:
            EnemiesManager.list_enemies.append(enemy_type.enemy_class())
        else:
            thread = threading.Timer(delay / 1000, lambda: EnemiesManager.spawnEnemy(enemy_type))
            GameProperties.on_going_threads.append(thread)
            thread.start()


# region UI

class UI:

    @staticmethod
    def hide_all():
        UI.Menu.hide_menu()
        UI.Game.hide_game()
        GameProperties.screen.blit(GameProperties.background, (0, 0))

    @staticmethod
    def show_menu():
        UI.hide_all()
        UI.Menu.show_menu()

    @staticmethod
    def show_game():
        UI.hide_all()
        UI.Game.show_game()

        EnemiesManager.spawnEnemy(GameConstants.EnemyType.COMMONINVADER1)

    @staticmethod
    def show_shop():
        UI.hide_all()
        UI.Game.show_shop()

    @staticmethod
    def show_settings():
        UI.hide_all()
        UI.Game.show_settings()

    @staticmethod
    def leave_game():
        pygame.quit()
        sys.exit()

    @staticmethod
    def create_show_game_button(x, y):
        UI.Menu.content_list.append(UI.Button(pygame.Vector2(x * GameProperties.win_scale, y * GameProperties.win_scale), "play_button", lambda: UI.show_game()))

    @staticmethod
    def create_show_shop_button(x, y):
        UI.Menu.content_list.append(UI.Button(pygame.Vector2(x * GameProperties.win_scale, y * GameProperties.win_scale), "play_button", lambda: UI.show_shop()))

    @staticmethod
    def create_show_settings_button(x, y):
        UI.Menu.content_list.append(UI.Button(pygame.Vector2(x * GameProperties.win_scale, y * GameProperties.win_scale), "play_button", lambda: UI.show_settings()))

    @staticmethod
    def create_leave_game_button(x, y):
        UI.Menu.content_list.append(UI.Button(pygame.Vector2(x * GameProperties.win_scale, y * GameProperties.win_scale), "play_button", lambda: UI.leave_game()))

    class Button(pygame.sprite.Sprite):
        def __init__(self, pos: pygame.Vector2, image_name: str, function, file_ext: str = "png"):
            super().__init__(GameProperties.UIGroup, GameProperties.ButtonGroup)
            self.image_path = os.path.join("..", "img", "UI", "buttons", image_name + "." + file_ext)
            self.image = pygame.image.load(self.image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * GameProperties.win_scale), int(self.image.get_height() * GameProperties.win_scale)))
            self.rect = self.image.get_rect(center=pos)
            self.function = function

        def is_pressed(self, mouse_pos):
            return self.rect.collidepoint(mouse_pos)

        def update(self):
            mouse_pos = pygame.mouse.get_pos()
            if self.is_pressed(mouse_pos):
                self.function()

    class Menu:
        content_list: list = []

        @staticmethod
        def show_menu():
            GameProperties.background = pygame.image.load(os.path.join("..", "img", "background_menu.png"))

            UI.create_show_game_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.20)

            UI.create_show_shop_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.40)

            UI.create_show_settings_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.60)

            UI.create_show_settings_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.80)

        @staticmethod
        def hide_menu():
            for content in UI.Menu.content_list:
                content.kill()

    class Game:
        content_list: list = []

        @staticmethod
        def show_game():
            UI.Game.content_list.append(Player("vaisseau"))
            GameProperties.background = pygame.image.load(os.path.join("..", "img", "background.png"))
            GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)

        @staticmethod
        def show_shop():
            GameProperties.background = pygame.image.load(os.path.join("..", "img", "background.png"))
            GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)

        @staticmethod
        def show_settings():
            GameProperties.background = pygame.image.load(os.path.join("..", "img", "background.png"))
            GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)

        @staticmethod
        def hide_game():
            for content in UI.Game.content_list:
                content.kill()

# endregion
