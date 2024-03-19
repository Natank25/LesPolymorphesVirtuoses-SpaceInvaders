import random
from enum import Enum
from random import randint

import pygame
from pygame import Vector2

from python import GameProperties
from python import Groups, Resources
from python import Utils
from python.Resources import Ennemies

pygame.init()


class Balle(Utils.Sprite):
    def __init__(self, pos, speed=3, damage=1, angle=0):
        self.speed = speed
        self.damage = damage
        self.angle = angle

        self.image = Ennemies.Images.Balle
        self.image = pygame.transform.scale_by(self.image, GameProperties.win_scale)
        self.image = pygame.transform.rotate(self.image, self.angle - 180)
        self.rect = self.image.get_rect(center=pos)
        super().__init__(Groups.EnemiesBulletGroup)

    def update(self):
        super().update()
        self.rect.move_ip(Vector2(0, self.speed).rotate(self.angle))
        if self.rect.top > GameProperties.win_size.height + GameProperties.win_size.y:
            self.kill()

        collided_sprites = pygame.sprite.spritecollide(self, Groups.PlayerGroup, False)
        for player in collided_sprites:
            player.apply_damage(self.damage)
            self.kill()


class Invader(Utils.AnimatedSprite):
    def __init__(self, speedx, speedy, health, image, atk_speed: float = 0, shooter=False, can_esquive=False):

        super().__init__(
            (randint(GameProperties.win_size.x + (image.get_width() // 2) + 15,
                     GameProperties.win_size.x + GameProperties.win_size.width - (image.get_width() // 2) - 15), GameProperties.win_size.y + 10), image,
            Groups.InvaderGroup)

        self.speedx = random.choice([speedx * GameProperties.difficulty, -speedx * GameProperties.difficulty])
        self.speedy = speedy * GameProperties.difficulty / 3
        self.shooter = shooter
        self.atk_speed = atk_speed * 1000

        self.health = health * GameProperties.difficulty
        self.coin_drop = health * GameProperties.difficulty
        self.gem_drop = 1

        self.lastEsquive = pygame.time.get_ticks()
        self.nextEsquive = pygame.time.get_ticks() + randint(500, 5000)
        self.canEsquive = can_esquive

        for invader in Groups.InvaderGroup.sprites():
            while self.rect.colliderect(invader.rect) and not self.rect.colliderect(GameProperties.win_size):
                self.rect.x += random.randint(-self.image.get_width() - 10, self.image.get_width() + 10)

        self.next_shot = pygame.time.get_ticks() + self.atk_speed

    def apply_damage(self, amount):
        self.health -= amount

    def avancer(self):
        self.rect.move_ip(self.speedx * GameProperties.deltatime * GameProperties.win_scale, self.speedy * GameProperties.deltatime * GameProperties.win_scale)
        if self.rect.x < GameProperties.win_size.x or self.rect.x + self.rect.width + self.speedx > GameProperties.win_size.x + GameProperties.win_size.width + self.speedx:
            self.speedx = -self.speedx

    def tirer(self):
        if self.shooter:
            if self.next_shot < pygame.time.get_ticks():
                Balle(self.rect.center)
                self.next_shot = pygame.time.get_ticks() + self.atk_speed

    def esquive(self):
        self.speedy = -self.speedy

    def update(self):
        super().update()
        if GameProperties.paused:
            self.next_shot += int(GameProperties.deltatime)

        if self.canEsquive and pygame.time.get_ticks() >= self.nextEsquive:
            self.esquive()
            self.lastEsquive = pygame.time.get_ticks()
            self.nextEsquive = pygame.time.get_ticks() + randint(500, 5000)
        self.avancer()
        self.tirer()

        if self.health < 0:
            self.kill()

        if GameProperties.does_player_exists and self.rect.center[1] > GameProperties.win_size.height + GameProperties.win_size.y:
            GameProperties.game_overed = True
            self.kill()

    def kill(self, animation=True):
        if not GameProperties.game_overed and animation:
            Resources.Ennemies.Sons.InvaderDeathSound.play()
            if self.gem_drop == random.randint(0, 100):
                GameProperties.gems += 1 + GameProperties.difficulty
                Utils.show_gem_text(self.rect.move(0, 20).center, 1)

            GameProperties.coins += self.coin_drop
            Utils.show_coins_text(self.rect.center, self.coin_drop)

            img_explosion = random.choice([Resources.Ennemies.Images.Explosion, Resources.Ennemies.Images.Explosion_pink, Resources.Ennemies.Images.Explosion_purple])
            Utils.AnimatedSprite(self.rect.center, img_explosion, Groups.AllSpritesGroup, frame_time=50, kill_when_done=True, rotable=True)

        super().kill()


# region Invaders
class CommonInvader1(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.CommonInvaders1DefaultSpeedx.value, EnemyAttributes.CommonInvaders1DefaultSpeedy.value, EnemyAttributes.CommonInvaders1DefaultHealth.value,
                         Ennemies.Images.CommonInvader1)


class CommonInvader2(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.CommonInvaders2DefaultSpeedx.value, EnemyAttributes.CommonInvaders2DefaultSpeedy.value, EnemyAttributes.CommonInvaders2DefaultHealth.value,
                         Ennemies.Images.CommonInvader2)


class CommonInvader3(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.CommonInvaders3DefaultSpeedx.value, EnemyAttributes.CommonInvaders3DefaultSpeedy.value, EnemyAttributes.CommonInvaders3DefaultHealth.value,
                         Ennemies.Images.CommonInvader3)


class SpeedInvader1(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.SpeedInvader1DefaultSpeedx.value, EnemyAttributes.SpeedInvader1DefaultSpeedy.value, EnemyAttributes.SpeedInvader1DefaultHealth.value,
                         Ennemies.Images.SpeedInvader1)


class SpeedInvader2(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.SpeedInvader2DefaultSpeedx.value, EnemyAttributes.SpeedInvader2DefaultSpeedy.value, EnemyAttributes.SpeedInvader2DefaultHealth.value,
                         Ennemies.Images.SpeedInvader2)


class SpeedInvader3(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.SpeedInvader3DefaultSpeedx.value, EnemyAttributes.SpeedInvader3DefaultSpeedy.value, EnemyAttributes.SpeedInvader3DefaultHealth.value,
                         Ennemies.Images.SpeedInvader3)


class TankInvader1(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.TankInvader1DefaultSpeedx.value, EnemyAttributes.TankInvader1DefaultSpeedy.value, EnemyAttributes.TankInvader1DefaultHealth.value,
                         Ennemies.Images.TankInvader1)


class TankInvader2(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.TankInvader2DefaultSpeedx.value, EnemyAttributes.TankInvader2DefaultSpeedy.value, EnemyAttributes.TankInvader2DefaultHealth.value,
                         Ennemies.Images.TankInvader2)


class TankInvader3(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.TankInvader3DefaultSpeedx.value, EnemyAttributes.TankInvader3DefaultSpeedy.value, EnemyAttributes.TankInvader3DefaultHealth.value,
                         Ennemies.Images.TankInvader3)


class ShooterInvader1(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.ShooterInvader1DefaultSpeedx.value, EnemyAttributes.ShooterInvader1DefaultSpeedy.value, EnemyAttributes.ShooterInvader1DefaultHealth.value,
                         Ennemies.Images.SpeedInvader1, shooter=True, atk_speed=2.5)


class ShooterInvader2(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.ShooterInvader2DefaultSpeedx.value, EnemyAttributes.ShooterInvader2DefaultSpeedy.value, EnemyAttributes.ShooterInvader2DefaultHealth.value,
                         Ennemies.Images.SpeedInvader1, shooter=True, atk_speed=3.5)


class ShooterInvader3(Invader):
    def __init__(self):
        super().__init__(EnemyAttributes.ShooterInvader3DefaultSpeedx.value, EnemyAttributes.ShooterInvader3DefaultSpeedy.value, EnemyAttributes.ShooterInvader3DefaultHealth.value,
                         Ennemies.Images.SpeedInvader1, shooter=True, atk_speed=4.5)


# endregion

class Boss(Utils.Body):

    def __init__(self, speedx, speedy, health, boss_name, cooldown_attack=5000, cooldown_bullet=1500, shooter_arm_id=1):
        # self.next_shot = pygame.time.get_ticks() + atk_speed + GameProperties.difficulty

        self.speedy = speedy + (GameProperties.difficulty / 20)
        self.health = health * (1 + GameProperties.difficulty)

        self.image = eval("Resources.Bosses.Images.Boss" + boss_name + "Body")
        self.rect: pygame.rect.Rect = self.image.get_rect(topleft=(GameProperties.win_size.x + GameProperties.win_size.width * 0.5 - self.image.get_width() // 2, 25))

        self.upper_arm_image = eval("Resources.Bosses.Images.Boss" + boss_name + "UpperArm")
        self.lower_arm_image = eval("Resources.Bosses.Images.Boss" + boss_name + "LowerArm")

        self.coin_drop = health * GameProperties.difficulty
        self.gem_drop = 1

        self.next_move = pygame.time.get_ticks() + randint(1000, 5000)

        self.cooldown_attacks = cooldown_attack
        self.next_attack = pygame.time.get_ticks() + self.cooldown_attacks

        self.cooldown_bullet = cooldown_bullet
        self.next_shot = pygame.time.get_ticks() + self.cooldown_bullet

        self.sound = Resources.Ennemies.Sons.InvaderDeathSound

        super().__init__(self.image, Groups.InvaderGroup, topleft=(GameProperties.win_size.x + GameProperties.win_size.width * 0.5 - self.image.get_width() // 2, 25))
        self.arms = []

        # Right arm
        self.upper_right_arm = Utils.Bone(self, (115, 11), (0, 41), self.upper_arm_image, True)
        self.arms.append(self.upper_right_arm)

        self.lower_right_arm = Utils.Bone(self.upper_right_arm, (0, 40), (0, 41), self.lower_arm_image, True)
        self.arms.append(self.lower_right_arm)

        # Left arm
        self.upper_left_arm = Utils.Bone(self, (-115, 11), (0, 41), self.upper_arm_image, True)
        self.arms.append(self.upper_left_arm)

        self.lower_left_arm = Utils.Bone(self.upper_left_arm, (0, 40), (0, 41), self.lower_arm_image, True)
        self.arms.append(self.lower_left_arm)

        self.shooter_arm = self.arms[shooter_arm_id]

    def update(self):
        super().update()

        if self.health < 0:
            self.kill()
            GameProperties.coins += self.coin_drop
            if self.gem_drop == random.randint(0, 100):
                GameProperties.gems += 1 + GameProperties.difficulty

        if GameProperties.does_player_exists and self.rect.center[1] > GameProperties.win_size.height + GameProperties.win_size.y:
            self.kill()
            GameProperties.game_overed = True

        if not GameProperties.paused:
            if self.next_move < pygame.time.get_ticks():
                self.move_to(Vector2(GameProperties.win_size.x + randint(self.image.get_width() // 2, GameProperties.win_size.width - self.image.get_width() // 2), self.rect.centery))
                self.next_move = pygame.time.get_ticks() + randint(1000, 5000)

            if randint(0, 50) == 0:
                arm = random.randint(0, 3)
                if arm == 0:
                    self.arms[arm].set_rotation(randint(-130, 45))
                elif arm == 1:
                    angle = 1
                    self.arms[arm].set_rotation(randint(-60, 30))
                elif arm == 2:
                    self.arms[arm].set_rotation(randint(-45, 130))
                elif arm == 3:
                    self.arms[arm].set_rotation(randint(-30, 60))

                # TODO: set_rotation -> 0 is from parent

        self.try_attack()

    def try_attack(self):
        if self.next_attack < pygame.time.get_ticks():
            self.next_attack = pygame.time.get_ticks() + self.cooldown_attacks + random.randint(-2000, 2000)
            attack = random.randint(0, 5)
            if attack == 0:
                Attack1Rect(3000, 5, 250, [GameProperties.win_size.x + GameProperties.win_size.width * 0.42, GameProperties.win_size.height * 0.8], midtop=self.rect.move(0, 20).midbottom)
            elif attack == 1 or attack == 2:
                random_space = random.randint(5, 10) / 100
                Attack2Rect(3500, 5, 250, [GameProperties.win_size.x + GameProperties.win_size.width * 0.1, GameProperties.win_size.height + GameProperties.win_size.y],
                            midtop=(GameProperties.win_size.x + GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * (0.275 + random_space)),
                            space_between=GameProperties.win_size.height * (0.15 + random_space * 0.7))
            else:
                for i in range(random.randint(7, 10)):
                    Attack1Circle(random.randrange(0, GameProperties.win_size.width), random.randrange(GameProperties.win_size.height * 0.4, GameProperties.win_size.height), 5)
        if self.next_shot < pygame.time.get_ticks():
            self.next_shot = pygame.time.get_ticks() + self.cooldown_bullet + randint(-500, 1500)
            shoot_pos = self.shooter_arm.pos + Vector2(0, 100).rotate(self.shooter_arm.angle)
            Balle(shoot_pos, angle=Utils.calculate_angle(shoot_pos, Groups.PlayerGroup.sprites()[0].rect.center) - 90)

    def apply_damage(self, damage):
        self.health -= damage

    def kill(self, **kwargs):
        self.sound.stop()
        for arm in self.arms:
            arm.kill()
        super().kill()


class Attack1Rect(Utils.Sprite):
    def __init__(self, fade_in, damage, fade_out, size, color=(255, 0, 0, 255), rotation=0, **kwargs):
        super().__init__()
        self.color = color
        self.fade_out = fade_out
        self.damage = damage
        self.fade_in = fade_in
        self.surf = pygame.transform.rotate(pygame.surface.Surface(size, pygame.SRCALPHA), rotation)
        pygame.draw.rect(self.surf, self.color, self.surf.get_rect(), 5)
        self.image = self.surf
        self.image.set_alpha(0)
        self.rect = self.image.get_rect(**kwargs)
        self.spawn_tick = pygame.time.get_ticks()
        self.has_attacked = False

    def update(self):
        if self.spawn_tick + self.fade_in > pygame.time.get_ticks():
            progress = Utils.Easings.easeInOutSine((pygame.time.get_ticks() - self.spawn_tick) / self.fade_in)
            self.image.set_alpha(round(progress * 200))

        elif self.spawn_tick + self.fade_in + self.fade_out > pygame.time.get_ticks():
            if not self.has_attacked:
                self.surf.fill(self.color)
                for player in Groups.PlayerGroup.sprites():
                    if self.rect.colliderect(player.rect):
                        player.apply_damage(self.damage)
                self.has_attacked = True

            progress = Utils.Easings.easeInOutSine((pygame.time.get_ticks() - self.spawn_tick - self.fade_in) / self.fade_out)
            self.image.set_alpha(round(200 + progress * (-200)))

        elif self.image.get_alpha() < 50:
            self.kill()


class Attack1Circle(Utils.Sprite):
    def __init__(self, x, y, damage):
        super().__init__()
        self.size = random.randint(50, 200)
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.radius = self.size // 2
        self.rect = self.image.get_rect(center=(x, y))
        self.fade = 0
        self.border_fade = 0
        self.fade_out_start = pygame.time.get_ticks() + 4000
        self.damage = damage
        self.has_attacked = False

    def update(self):
        if self.fade_out_start - 1400 <= pygame.time.get_ticks():
            if not self.has_attacked:
                for player in Groups.PlayerGroup.sprites():
                    if pygame.sprite.collide_circle(self, player):
                        player.apply_damage(self.damage)
                self.has_attacked = True

            self.fade -= 30
            self.border_fade -= 30
            if self.fade <= 0:
                self.fade = 0
                self.border_fade = 0
                self.kill()
        else:
            self.border_fade += 1.75
            if self.border_fade >= 255 or self.fade >= 255:
                self.fade = 255
                self.border_fade = 255
        self.image.fill((0, 0, 0, 0))
        pygame.draw.circle(self.image, (255, 0, 0, self.fade), (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, (255, 0, 0, self.border_fade), (self.radius, self.radius), self.radius, 4)


class Attack2Rect:
    def __init__(self, fade_in, damage, fade_out, size, color=(255, 0, 0, 255), space_between=150, **kwargs):
        pos = kwargs.get("midtop")
        Attack1Rect(fade_in, damage, fade_out, (size[0] + 25, size[1]), color, rotation=0, center=(GameProperties.win_size.width * 0.33, GameProperties.win_size.height * 0.7))
        Attack1Rect(fade_in, damage, fade_out, (size[0] + 25, size[1]), color, rotation=0, center=(GameProperties.win_size.width * 0.67, GameProperties.win_size.height * 0.7))
        for i in range(0, 4):
            Attack1Rect(fade_in, damage, fade_out, size, color, rotation=90, midtop=(pos[0], pos[1] + space_between * i))


# region Bosses


class Boss1(Boss):
    def __init__(self):
        super().__init__(EnemyAttributes.Boss1DefaultSpeedx.value, EnemyAttributes.Boss1DefaultSpeedy.value, EnemyAttributes.Boss1DefaultHealth.value, "5", EnemyAttributes.Boss1DefaultSpeedATK.value)
        pygame.mixer.music.load("../sounds/BossSound.ogg")
        pygame.mixer.music.play()

    def main_attack(self):
        pass


class Boss2(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss2DefaultSpeedx.value, EnemyAttributes.Boss2DefaultSpeedy.value, EnemyAttributes.Boss2DefaultHealth.value, Ennemies.Images.CommonInvader1,
                         EnemyAttributes.Boss2DefaultSpeedATK.value)


class Boss3(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss3DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss3DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss3DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss3DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


class Boss4(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss4DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss4DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss4DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss4DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


class Boss5(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss5DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss5DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss5DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss5DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


class Boss6(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss6DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss6DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss6DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss6DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


class Boss7(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss7DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss7DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss7DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss7DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


class Boss8(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss8DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss8DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss8DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss8DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


class Boss9(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss9DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss9DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss9DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss9DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


class Boss10(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss10DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss10DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss10DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss10DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


class Boss11(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss11DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss11DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss11DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss11DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


class Boss12(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss12DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss12DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss12DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss12DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


class Boss13(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss13DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss13DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss13DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss13DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


class Boss14(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss14DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss14DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss14DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss14DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


class Boss15(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss15DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss15DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss15DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss15DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


class Boss16(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss16DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss16DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss16DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss16DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


class Boss17(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss17DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss17DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss17DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss17DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


class Boss18(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss18DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss18DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss18DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss18DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


class Boss19(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss19DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss19DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss19DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss19DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


class Boss20(Boss):
    def __init__(self, hauteur=25):
        super().__init__(hauteur, EnemyAttributes.Boss20DefaultSpeedx.value + (GameProperties.difficulty / 10), EnemyAttributes.Boss20DefaultSpeedy.value + (GameProperties.difficulty / 20),
                         EnemyAttributes.Boss20DefaultHealth.value * (1 + GameProperties.difficulty), EnemyAttributes.Boss20DefaultSpeedATK.value + GameProperties.difficulty,
                         Ennemies.Images.CommonInvader1)


# endregion

class EnemyAttributes(Enum):
    # common
    CommonInvaders1DefaultHealth = 2
    CommonInvaders1DefaultSpeedx = 0.1
    CommonInvaders1DefaultSpeedy = 0.2

    CommonInvaders2DefaultHealth = 25
    CommonInvaders2DefaultSpeedx = 0.1
    CommonInvaders2DefaultSpeedy = 0.2

    CommonInvaders3DefaultHealth = 100
    CommonInvaders3DefaultSpeedx = 0.1
    CommonInvaders3DefaultSpeedy = 0.2

    # speed
    SpeedInvader1DefaultHealth = 2
    SpeedInvader1DefaultSpeedx = 0.15
    SpeedInvader1DefaultSpeedy = 0.45

    SpeedInvader2DefaultHealth = 10
    SpeedInvader2DefaultSpeedx = 0.2
    SpeedInvader2DefaultSpeedy = 0.5

    SpeedInvader3DefaultHealth = 25
    SpeedInvader3DefaultSpeedx = 0.25
    SpeedInvader3DefaultSpeedy = 0.55

    # tank
    TankInvader1DefaultHealth = 25
    TankInvader1DefaultSpeedx = 0.075
    TankInvader1DefaultSpeedy = 0.1

    TankInvader2DefaultHealth = 200
    TankInvader2DefaultSpeedx = 0.075
    TankInvader2DefaultSpeedy = 0.1

    TankInvader3DefaultHealth = 500
    TankInvader3DefaultSpeedx = 0.2
    TankInvader3DefaultSpeedy = 0.075

    # shooter
    ShooterInvader1DefaultHealth = 2
    ShooterInvader1DefaultSpeedx = 0.1
    ShooterInvader1DefaultSpeedy = 0.2
    ShooterInvader1DefaultSpeedATK = 1

    ShooterInvader2DefaultHealth = 25
    ShooterInvader2DefaultSpeedx = 0.1
    ShooterInvader2DefaultSpeedy = 0.1
    ShooterInvader2DefaultSpeedATK = 1.5

    ShooterInvader3DefaultHealth = 100
    ShooterInvader3DefaultSpeedx = 0.15
    ShooterInvader3DefaultSpeedy = 0.1
    ShooterInvader3DefaultSpeedATK = 2

    # Boss
    Boss1DefaultHealth = 200
    Boss1DefaultSpeedx = 0.01
    Boss1DefaultSpeedy = 0.01
    Boss1DefaultSpeedATK = 7000

    Boss2DefaultHealth = 250
    Boss2DefaultSpeedx = 0.01
    Boss2DefaultSpeedy = 0.01
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
