import os
from random import randint

from python import Resources
from python.Groups import *


class PlayerProperties:
    SPEED = 0.3

class Balle(pygame.sprite.Sprite):
    def __init__(self, ship: pygame.rect.Rect, speed=0.3, damage=1, fire_speed=1):
        super().__init__(Groups.BulletGroup, Groups.AllSprites)

        self.image = Resources.Player.Images.Balle
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * GameProperties.win_scale),
                                                         int(self.image.get_height() * GameProperties.win_scale)))
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
        collided_sprites = pygame.sprite.groupcollide(Groups.BulletGroup, Groups.InvaderGroup, True,
                                                      False)
        for bullet in collided_sprites:
            for invader in collided_sprites[bullet]:
                invader.apply_damage(bullet.damage)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__(Groups.PlayerGroup, Groups.AllSprites)
        self.image = Resources.Player.Images.Vaisseau_Base
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * GameProperties.win_scale),
                                                         int(self.image.get_height() * GameProperties.win_scale)))
        self.rect = self.image.get_rect()
        self.rect.x = randint(GameProperties.win_size.x,
                                     GameProperties.win_size.x + GameProperties.win_size.width - self.rect.width)
        self.rect.y = GameProperties.win_size.height - 100 * GameProperties.win_scale
        self.timeLastShot = pygame.time.get_ticks()
        self.cooldown = 500

    def controls(self, keys):
        speed = PlayerProperties.SPEED * GameProperties.win_scale * GameProperties.deltatime
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