from random import randint

import pygame

from python import GameProperties
from python import Groups
from python import Resources, Utils


class PlayerProperties:
    SPEED = 0.3
    DAMAGE = 1
    ATK_SPEED = 1
    MAX_HEALTH = 3


GameProperties.Upgrades.update_upgrades()


class Balle(Utils.Sprite):
    def __init__(self, ship: pygame.rect.Rect, speed=0.3):
        super().__init__(Groups.BulletGroup)

        self.image = Resources.Player.Images.Balle
        self.image = pygame.transform.scale_by(self.image, GameProperties.win_scale)
        self.rect = self.image.get_rect()
        self.rect.center = ship.center
        self.speed = speed
        self.damage = PlayerProperties.DAMAGE

    def update(self):
        super().update()

        self.damage = PlayerProperties.DAMAGE

        if self.rect.bottom > 0:
            self.rect.y -= self.speed * GameProperties.deltatime * GameProperties.win_scale
        else:
            self.kill()
        collided_sprites = pygame.sprite.spritecollide(self, Groups.InvaderGroup, False)
        for invader in collided_sprites:
            invader.apply_damage(self.damage)
            self.kill()


# TODO: add lives/health
class Player(Utils.Sprite):
    def __init__(self):
        super().__init__(Groups.PlayerGroup)
        self.image = Resources.Player.Images.Vaisseau_Base
        self.image = pygame.transform.scale_by(self.image, GameProperties.win_scale)
        self.rect = self.image.get_rect()
        self.rect.x = randint(GameProperties.win_size.x,
                              GameProperties.win_size.x + GameProperties.win_size.width - self.rect.width)
        self.rect.y = GameProperties.win_size.height - 100 * GameProperties.win_scale
        self.timeLastShot = pygame.time.get_ticks()
        self.cooldown = 500 - PlayerProperties.ATK_SPEED

        self.health = PlayerProperties.MAX_HEALTH

        GameProperties.does_player_exists = True

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

    def apply_damage(self, damage):
        self.health -= damage

    def update(self):
        super().update()

        keys = pygame.key.get_pressed()
        self.controls(keys)

        if keys[pygame.K_SPACE] and pygame.time.get_ticks() > self.timeLastShot + self.cooldown:
            self.timeLastShot = pygame.time.get_ticks()
            self.tirer()

        collided_invaders = pygame.sprite.spritecollide(self, Groups.InvaderGroup, False)

        if len(collided_invaders) != 0:
            self.kill()  # TODO: Faire une EXPLOSION
            GameProperties.game_overed = True

        if self.health <= 0:
            self.kill()  # TODO: Faire une EXPLOSION
            GameProperties.game_overed = True

    def kill(self):
        GameProperties.does_player_exists = False
        super().kill()
