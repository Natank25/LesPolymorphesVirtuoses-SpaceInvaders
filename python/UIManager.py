import math
import sys

import pygame

from python import Groups, Player
from python import Resources
from python import GameProperties

pygame.init()


class Text(pygame.sprite.Sprite):
    def __init__(self, text, color, font, update_function=None, update_text=False, **kwargs):
        self.update_function = update_function
        self.text = text
        self.color = color
        self.font = font
        self.update_text = update_text
        self.image = self.font.render(self.text, True, self.color).convert_alpha()

        for key,value in kwargs.items():
            if "Text.image.get_width" in value:
                kwargs[key] = eval(value.replace("Text.image.get_width", "self.image.get_width()"))

        self.rect = self.image.get_rect(**kwargs)
        self.kwargs = kwargs

        super().__init__(Groups.UIGroup)

    #TODO: correctly move the text when updated
    def update(self):
        if self.update_function:
            self.update_function(self)
            if self.update_text:
                self.image = self.font.render(self.text, True, self.color).convert_alpha()
                self.rect = self.image.get_rect(**self.kwargs)


class Button(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, function):
        super().__init__(Groups.UIGroup, Groups.ButtonGroup)
        self.image = Resources.UI.Images.play_game_img
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * GameProperties.win_scale), int(self.image.get_height() * GameProperties.win_scale)))
        self.rect = self.image.get_rect(center=pos)
        self.function = function

    def is_pressed(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and self.is_pressed(mouse_pos):
            self.function()


class CoinsText(pygame.sprite.Sprite):
    def __init__(self):
        self.text = "Coins : " + str(GameProperties.coins)
        self.font = pygame.font.SysFont("arialblack", 20)
        self.image = self.font.render(self.text, True, (255, 255, 255)).convert_alpha()
        self.pos = (
            GameProperties.win_size.x + GameProperties.win_size.width - self.image.get_width() - GameProperties.win_size.width * 0.005,
            GameProperties.win_size.y + GameProperties.win_size.height * 0.005)
        self.rect = self.image.get_rect(topleft=self.pos)
        super().__init__(Groups.UIGroup)

    def update(self):
        self.text = "Coins : " + str(GameProperties.coins)
        self.image = self.font.render(self.text, True, (255, 255, 255)).convert_alpha()
        self.pos = (
            GameProperties.win_size.x + GameProperties.win_size.width - self.image.get_width() - GameProperties.win_size.width * 0.005,
            GameProperties.win_size.y + GameProperties.win_size.height * 0.005)
        self.rect = self.image.get_rect(topleft=self.pos)


class GemText(pygame.sprite.Sprite):
    def __init__(self):
        self.text = "Gems : " + str(GameProperties.gems)
        self.font = pygame.font.SysFont("arialblack", 20)
        self.image = self.font.render(self.text, True, (255, 255, 255)).convert_alpha()
        self.pos = (
            GameProperties.win_size.x + GameProperties.win_size.width - self.image.get_width() - GameProperties.win_size.width * 0.005,
            GameProperties.win_size.y + GameProperties.win_size.height * 0.005)
        self.rect = self.image.get_rect(topleft=self.pos)
        super().__init__(Groups.UIGroup)

    def update(self):
        self.text = "Gems : " + str(GameProperties.gems)
        self.image = self.font.render(self.text, True, (255, 255, 255)).convert_alpha()
        self.pos = (
            GameProperties.win_size.x + GameProperties.win_size.width - self.image.get_width() - GameProperties.win_size.width * 0.005,
            GameProperties.win_size.y + GameProperties.win_size.height * 0.005)
        self.rect = self.image.get_rect(topleft=self.pos)


class StartingScreen:

    @staticmethod
    def show_starting_screen():
        content_list.append(Text("Appuyez pour jouer", (255, 255, 255), pygame.font.SysFont("arialblack", 35, bold=True),
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
        GameProperties.set_background(Resources.UI.Images.background_img)

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
        content_list.append(Button(pygame.Vector2(x, y), lambda: show_game()))

    @staticmethod
    def create_show_shop_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), lambda: show_shop()))

    @staticmethod
    def create_show_settings_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), lambda: show_settings()))

    @staticmethod
    def create_leave_game_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), lambda: leave_game()))

    @staticmethod
    def create_show_menu_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), lambda: show_menu()))


class Pause:
    @staticmethod
    def show_pause():
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)
        Pause.create_resume_game_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.45)

    @staticmethod
    def resume_game():
        GameProperties.paused = not GameProperties.paused

    @staticmethod
    def create_resume_game_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), lambda: resume_game()))


class Game:

    @staticmethod
    def show_game():
        for sprite in Groups.InvaderGroup.sprites():
            sprite.kill()
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)
        GameProperties.game_started = True
        content_list.append(Text("Coins : " + str(GameProperties.coins), (255,255,255), pygame.font.SysFont("arialblack",20), update_function= lambda self: setattr(self, "text", "Coins : " + str(GameProperties.coins)), update_text=True, topleft="(GameProperties.win_size.x + GameProperties.win_size.width - Text.image.get_width - GameProperties.win_size.width * 0.005, GameProperties.win_size.y + GameProperties.win_size.height * 0.005)"))

    @staticmethod
    def hide_game():
        for sprite in Groups.InvaderGroup.sprites():
            sprite.kill()
        for content in content_list:
            content.kill()


class Shop:
    @staticmethod
    def show_shop():
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)
        content_list.append(GemText())

    @staticmethod
    def upgrade_dmg_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y),
                                   lambda: setattr(Player.PlayerProperties, 'DAMAGE',
                                                   Player.PlayerProperties.DAMAGE + Player.PlayerProperties.DAMAGE_UPGRADE(x ^ (1.4 - (GameProperties.difficulty / 100))))))


class Settings:
    @staticmethod
    def show_settings():
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)


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
        if type(content) != Player.Player and hasattr(content, "kill") and callable(getattr(content, "kill")):
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
    GameProperties.game_started = False
    GameProperties.current_wave = 0


def show_pause():
    Pause.show_pause()


def resume_game():
    hide_all()
    Pause.resume_game()
