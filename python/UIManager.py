import math
import sys

import pygame

from python import GameProperties, EnemiesManager
from python import Groups, Player
from python import Resources
from python.Player import PlayerProperties

pygame.init()


class Text(pygame.sprite.Sprite):
    def __init__(self, text, color, font, update_function=None, update_text=False, color_function=None, **kwargs):
        self.update_function = update_function
        self.color_function = color_function
        self.text = text
        self.color = color
        self.font = font
        self.update_text = update_text
        self.image = self.font.render(self.text, True, self.color).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, GameProperties.win_scale)
        self.spawn_tick = pygame.time.get_ticks()

        for key, value in kwargs.items():
            if "Text.image.get_width" in value:
                kwargs[key] = value.replace("Text.image.get_width", "self.image.get_width()")
            if "Text.image.get_height" in value:
                kwargs[key] = value.replace("Text.image.get_width", "self.image.get_width()")

            self.key = key
            self.value = str(kwargs[key])

        self.rect = self.image.get_rect(**{self.key: eval(self.value)})

        super().__init__(Groups.UIGroup)

    def update(self):
        if self.update_function:
            self.update_function(self)
            if self.update_text:
                self.image = self.font.render(self.text, True, self.color).convert_alpha()
                self.image = pygame.transform.scale_by(self.image, GameProperties.win_scale)
                self.rect = self.image.get_rect(**{self.key: eval(self.value)})
            if self.color_function:
                self.color = self.color_function()


class ShopText(Text):
    def __init__(self, upgrade_id, gems=False, **kwargs):
        self.upgrade_id = upgrade_id
        if not gems:
            super().__init__("Niv. " + str(GameProperties.coin_shop[self.upgrade_id]) + " / " + str(eval("GameProperties.get_" + self.upgrade_id + "_cost()")) + "$", (128, 0, 0),
                             Resources.UI.Fonts.arialblack_20, update_function=lambda self: setattr(self, "text", "Niv. " + str(GameProperties.coin_shop[self.upgrade_id]) + " / " + str(
                    eval("GameProperties.get_" + self.upgrade_id + "_cost()")) + "$"), update_text=True, color_function=lambda: self.get_upgrade_color(), **kwargs)
        else:

            super().__init__("Niv. " + str(GameProperties.gems_shop[self.upgrade_id]) + " / " + str(eval("GameProperties.get_" + self.upgrade_id + "_cost()")) + "$", (128, 0, 0),
                             Resources.UI.Fonts.arialblack_20, update_function=lambda self: setattr(self, "text", "Niv. " + str(GameProperties.gems_shop[self.upgrade_id]) + " / " + str(
                    eval("GameProperties.get_" + self.upgrade_id + "_cost()")) + "$"), update_text=True, color_function=lambda: self.get_upgrade_color(), **kwargs)

    def get_upgrade_color(self):
        if eval("GameProperties.get_" + self.upgrade_id + "_cost()") < GameProperties.coins:
            return 0, 128, 0
        else:
            return 128, 0, 0


class Button(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, image, function):
        super().__init__(Groups.UIGroup, Groups.ButtonGroup)
        self.image = pygame.transform.scale_by(pygame.transform.scale_by(image, GameProperties.button_scale), GameProperties.win_scale)
        self.rect = self.image.get_rect(center=pos)
        self.function = function
        super().__init__(Groups.UIGroup, Groups.ButtonGroup)

    def is_pressed(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update(self, **kwargs):
        is_button_group_update = kwargs.get("button_group_update", False)
        if is_button_group_update:
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] and self.is_pressed(mouse_pos):
                self.function()


class StartingScreen:

    @staticmethod
    def show_starting_screen():
        content_list.append(Text("Appuyez pour jouer", (255, 255, 255), Resources.UI.Fonts.arialblack_35,
                                 update_function=lambda self: self.image.set_alpha(int((math.sin(pygame.time.get_ticks() / 1000 * 1.5) + 1) * 123)),
                                 center=(GameProperties.win_size.x + GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * 0.9)))

        GameProperties.set_background(Resources.UI.Images.background_menu_img)
        GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)

    @staticmethod
    def update():
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if not keys[pygame.K_F11] and (any(keys) or any(mouse)):
            show_menu()


class Menu:

    @staticmethod
    def show_menu():
        hide_all()
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.paused = False

        Menu.create_show_game_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.20)

        Menu.create_show_shop_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.40)

        Menu.create_show_settings_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.60)

        Menu.create_leave_game_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.80)

    @staticmethod
    def hide_menu():
        for content in content_list:
            content.kill()

    @staticmethod
    def create_show_game_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_button_img, lambda: show_game()))

    @staticmethod
    def create_show_shop_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.shop_button_img, lambda: show_shop()))

    @staticmethod
    def create_show_settings_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.settings_button_img, lambda: show_settings()))

    @staticmethod
    def create_leave_game_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.quit_button_img, lambda: leave_game()))

    @staticmethod
    def create_show_menu_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_button_img, lambda: show_menu()))


class Pause:
    @staticmethod
    def show_pause():
        for content in content_list:
            content.kill()
        hide_all()
        GameProperties.set_background(Resources.UI.Images.background_menu_img)
        GameProperties.paused = True
        GameProperties.has_paused = True
        Pause.create_resume_game_button(GameProperties.win_size.x + GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * 0.45)
        Pause.create_back_menu_button(GameProperties.win_size.x + GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * 0.8)

    @staticmethod
    def resume_game():
        for content in content_list:
            Groups.UIGroup.add(content)
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.game_started = True
        content_list.append(
            Text("Coins : " + str(GameProperties.coins), (255, 255, 255), Resources.UI.Fonts.arialblack_20, update_function=lambda self: setattr(self, "text", "Coins : " + str(GameProperties.coins)),
                 update_text=True,
                 topleft="(GameProperties.win_size.x + GameProperties.win_size.width - Text.image.get_width - GameProperties.win_size.width * 0.005, GameProperties.win_size.y + GameProperties.win_size.height * 0.005)"))

    @staticmethod
    def create_resume_game_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.resume_button_img, lambda: Pause.unpause_game()))

    @staticmethod
    def unpause_game():
        GameProperties.paused = not GameProperties.paused
        resume_game()

    @staticmethod
    def create_back_menu_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.leave_game_button_img, lambda: Pause.go_back()))

    @staticmethod
    def go_back():
        GameProperties.paused = False
        GameProperties.game_overed = False
        GameProperties.game_started = False
        EnemiesManager.next_spawns = []

        for players in Groups.PlayerGroup.sprites():
            players.kill()
        for invader in Groups.InvaderGroup.sprites():
            invader.kill()
        for bullet in Groups.BulletGroup.sprites():
            bullet.kill()
        EnemiesManager.next_spawns.clear()
        Menu.show_menu()


class Game:

    @staticmethod
    def show_game():
        GameProperties.game_overed = False
        GameProperties.game_started = True
        EnemiesManager.next_spawns = []
        for invader in Groups.InvaderGroup.sprites():
            invader.kill()
        EnemiesManager.next_spawns.clear()
        if not GameProperties.has_paused:
            GameProperties.current_wave = 0
        else:
            GameProperties.current_wave -= 1
        Player.Player()
        GameProperties.has_paused = False
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)
        content_list.append(
            Text("Coins : " + str(GameProperties.coins), (255, 255, 255), Resources.UI.Fonts.arialblack_20, update_function=lambda self: setattr(self, "text", "Coins : " + str(GameProperties.coins)),
                 update_text=True,
                 topleft="(GameProperties.win_size.x + GameProperties.win_size.width - Text.image.get_width - GameProperties.win_size.width * 0.005, GameProperties.win_size.y + GameProperties.win_size.height * 0.005)"))
        Game.lives_text()

    @staticmethod
    def hide_game():
        for sprite in Groups.InvaderGroup.sprites():
            sprite.kill()
        for content in content_list:
            content.kill()

    @staticmethod
    def wave_color(self):
        if self.spawn_tick + 2500 < pygame.time.get_ticks():
            content_list.remove(self)
            self.kill()
        elif self.spawn_tick + 1000 < pygame.time.get_ticks():
            self.image.set_alpha(int(-(math.sin((pygame.time.get_ticks() - self.spawn_tick - 1000) / 1000)) * 255) + 255)

    @staticmethod
    def waves_text():
        content_list.append(Text("WAVE " + str(GameProperties.current_wave), (255, 255, 255), font=Resources.UI.Fonts.arialblack_35, update_function=lambda self: Game.wave_color(self),
                                 center="(GameProperties.win_size.x + GameProperties.win_size.width- GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * 0.15)"))

    @staticmethod
    def lives_text():
        content_list.append(Text("Vies: " + str(PlayerProperties.MAX_HEALTH), (255, 255, 255), Resources.UI.Fonts.arialblack_20,
                                 update_function=lambda self: setattr(self, "text", "Vies: " + str(PlayerProperties.MAX_HEALTH)), update_text=True, bottomleft=GameProperties.win_size.bottomleft))

    @staticmethod
    def update():
        if GameProperties.game_started and len(Groups.InvaderGroup.sprites()) == 0 and len(EnemiesManager.next_spawns) == 0:
            GameProperties.current_wave += 1
            EnemiesManager.send_waves_levels(GameProperties.current_wave)


class Shop:

    @staticmethod
    def show_shop():
        hide_all()
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)
        content_list.append(
            Text("Coins : " + str(GameProperties.coins), (255, 255, 255), Resources.UI.Fonts.arialblack_20, update_function=lambda self: setattr(self, "text", "Coins : " + str(GameProperties.coins)),
                 update_text=True,
                 topleft="(GameProperties.win_size.x + GameProperties.win_size.width - Text.image.get_width - GameProperties.win_size.width * 0.005, GameProperties.win_size.y + GameProperties.win_size.height * 0.005)"))

        Shop.upgrade_dmg_button(GameProperties.win_size.width * 0.2 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.2)
        Shop.upgrade_speed_atk_button(GameProperties.win_size.width * 0.2 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.4)
        Shop.upgrade_health_button(GameProperties.win_size.width * 0.2 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.6)

        Shop.back_menu_button(GameProperties.win_size.width * 0.05 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.05)
        content_list.append(
            Button(pygame.Vector2(GameProperties.win_size.width * 0.95 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.5),
                   pygame.transform.rotate(Resources.UI.Images.arrow_img, -90),
                   lambda: Shop.gem_shop()))

    @staticmethod
    def gem_shop():
        hide_all()
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)
        content_list.append(
            Text("Gems : " + str(GameProperties.gems), (255, 255, 255), Resources.UI.Fonts.arialblack_20, update_function=lambda self: setattr(self, "text", "Gems : " + str(GameProperties.gems)),
                 update_text=True,
                 topleft="(GameProperties.win_size.x + GameProperties.win_size.width - Text.image.get_width - GameProperties.win_size.width * 0.005, GameProperties.win_size.y + GameProperties.win_size.height * 0.005)"))
        Shop.back_menu_button(GameProperties.win_size.width * 0.05 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.05)
        content_list.append(Button(pygame.Vector2(GameProperties.win_size.width * 0.05 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.5),
                                   pygame.transform.rotate(Resources.UI.Images.arrow_img, 90), lambda: Shop.show_shop()))
        Shop.buy_10_button(GameProperties.win_size.width * 0.2 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.2)

    @staticmethod
    def upgrade_dmg_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_button_img, lambda: GameProperties.damage_upgrade()))
        content_list.append(ShopText(GameProperties.Upgrades.damage_upgrade, center="(" + str(x) + "," + str(y) + ")"))

    @staticmethod
    def upgrade_speed_atk_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_button_img, lambda: GameProperties.atk_speed_upgrade()))
        content_list.append(ShopText(GameProperties.Upgrades.atk_speed_upgrade, center="(" + str(x) + "," + str(y) + ")"))

    @staticmethod
    def upgrade_health_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_button_img, lambda: GameProperties.health_upgrade()))
        content_list.append(ShopText(GameProperties.Upgrades.health_upgrade, center="(" + str(x) + "," + str(y) + ")"))

    @staticmethod
    def back_menu_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), pygame.transform.rotate(Resources.UI.Images.arrow_img, 90), lambda: Menu.show_menu()))

    @staticmethod
    def buy_10_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_button_img, lambda: Shop.buy_10()))
        content_list.append(ShopText(GameProperties.Upgrades.gems_10, gems=True, center="(" + str(x) + "," + str(y) + ")"))

    @staticmethod
    def buy_10():
        if GameProperties.gems - 10 > 0:
            GameProperties.gems -= 10
            GameProperties.coins *= 2
        else:
            print("t'es pauvre tafiolle")


class Settings:
    @staticmethod
    def show_settings():
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)
        Settings.back_menu_button(GameProperties.win_size.width * 0.05 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.05)
        content_list.append(Text("Sorry, settings are yet to be implemented", (255, 255, 255), Resources.UI.Fonts.arialblack_20,
                                 center=(GameProperties.win_size.width * 0.5 + GameProperties.win_size.x, GameProperties.win_size.height * 0.5 + GameProperties.win_size.y)))

    @staticmethod
    def back_menu_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), pygame.transform.rotate(Resources.UI.Images.arrow_img, 90), lambda: Menu.show_menu()))


class GameOver:
    @staticmethod
    def show_game_over():
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)
        Menu.create_show_menu_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.45)


content_list = []

shown_screen: object = StartingScreen


def hide_all():
    for content in content_list:
        if hasattr(content, "kill") and callable(getattr(content, "kill")):
            content.kill()
    content_list.clear()
    GameProperties.screen.blit(GameProperties.background, (0, 0))


def update():
    if hasattr(shown_screen, "update") and callable(getattr(shown_screen, "update")):
        shown_screen.update()


def show_menu():
    global shown_screen
    hide_all()
    Menu.show_menu()
    shown_screen = Menu


def show_game():
    global shown_screen
    hide_all()
    Game.show_game()
    shown_screen = Game


def show_shop():
    global shown_screen
    hide_all()
    Shop.show_shop()
    shown_screen = Shop


def show_settings():
    global shown_screen
    hide_all()
    Settings.show_settings()
    shown_screen = Settings


def leave_game():
    global shown_screen
    pygame.quit()
    sys.exit()


def show_starting_screen():
    global shown_screen
    hide_all()
    StartingScreen.show_starting_screen()
    shown_screen = StartingScreen


def show_game_over():
    global shown_screen
    hide_all()
    GameOver.show_game_over()
    shown_screen = GameOver


def show_pause():
    Pause.show_pause()


def resume_game():
    hide_all()
    Pause.resume_game()


def reset_game(new_wave=0):
    GameProperties.game_overed = False
    GameProperties.game_started = False
    EnemiesManager.next_spawns = []
    for invader in Groups.InvaderGroup.sprites():
        invader.kill()
    EnemiesManager.next_spawns.clear()
    GameProperties.current_wave = new_wave
