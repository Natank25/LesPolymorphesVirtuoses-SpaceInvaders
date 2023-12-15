import math
import random
import sys

import pygame

from EnemiesSpawner import EnemiesManager
from Groups import Groups
from Groups import AllSpritesGroup
from Player import Player
from python import Resources
from python.GameProperties import GameProperties

pygame.init()


class UIManager:


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
            if self.is_pressed(mouse_pos):
                self.function()

    class StartingScreen:

        class StartGameText():

            def __init__(self):
                font = pygame.font.SysFont('arialblack', 35, bold=True)
                self.image = font.render("Appuyez pour jouer", True, (255, 255, 255)).convert_alpha()
                self.rect = self.image.get_rect(center=(GameProperties.win_size.x + GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * 0.9))
                self.function = lambda: self.update_alpha()

            def update_alpha(self):
                GameProperties.screen.blit(GameProperties.group_background, self.rect, self.rect)
                self.image.set_alpha(int((math.sin(pygame.time.get_ticks() / 1000 * 1.5) + 1) * 123))
                GameProperties.screen.blit(self.image, self.rect)


        @staticmethod
        def show_starting_screen():
            text = UIManager.StartingScreen.StartGameText()
            UIManager.content_list.update({text: True})

        @staticmethod
        def update():
            keys = pygame.key.get_pressed()
            mouse = pygame.mouse.get_pressed()
            if any(keys) or any(mouse):
                UIManager.show_game()

    class Menu:

        @staticmethod
        def show_menu():
            GameProperties.background = Resources.UI.Images.background_menu_img

            UIManager.Menu.create_show_game_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.20)

            UIManager.Menu.create_show_shop_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.40)

            UIManager.Menu.create_show_settings_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.60)

            UIManager.Menu.create_leave_game_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.80)

        @staticmethod
        def hide_menu():
            for content in UIManager.content_list:
                content.kill()

        @staticmethod
        def create_show_game_button(x, y):
            UIManager.content_list.update({UIManager.Button(pygame.Vector2(x * GameProperties.win_scale, y * GameProperties.win_scale), lambda: UIManager.show_game()): False})

        @staticmethod
        def create_show_shop_button(x, y):
            UIManager.content_list.update({UIManager.Button(pygame.Vector2(x * GameProperties.win_scale, y * GameProperties.win_scale), lambda: UIManager.show_shop()): False})

        @staticmethod
        def create_show_settings_button(x, y):
            UIManager.content_list.update({UIManager.Button(pygame.Vector2(x * GameProperties.win_scale, y * GameProperties.win_scale), lambda: UIManager.show_settings()): False})

        @staticmethod
        def create_leave_game_button(x, y):
            UIManager.content_list.update({UIManager.Button(pygame.Vector2(x * GameProperties.win_scale, y * GameProperties.win_scale), lambda: UIManager.leave_game()): False})

    class Game:

        @staticmethod
        def show_game():
            UIManager.content_list.update({Player(): False})
            GameProperties.background = Resources.UI.Images.background_img
            GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)

        @staticmethod
        def hide_game():
            for sprite in Groups.InvaderGroup.sprites():
                sprite.kill()
            for on_going_thread in GameProperties.on_going_threads:
                on_going_thread.cancel()
            for content in UIManager.content_list:
                content.kill()

    class Shop:
        @staticmethod
        def show_shop():
            GameProperties.background = Resources.UI.Images.background_img
            GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)

    class Settings:
        @staticmethod
        def show_settings():
            GameProperties.background = Resources.UI.Images.background_img
            GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)

    content_list = {}

    shown_screen: object = StartingScreen

    @staticmethod
    def hide_all():
        for content in UIManager.content_list:
            if hasattr(content, "kill") and callable(getattr(content, "kill")):
                content.kill()
        UIManager.content_list.clear()
        GameProperties.screen.blit(GameProperties.background, (0, 0))

    @staticmethod
    def update():
        if hasattr(UIManager.shown_screen, "update") and callable(getattr(UIManager.shown_screen, "update")):
            UIManager.shown_screen.update()

        for content, does_have_function in UIManager.content_list.items():
            if does_have_function:
                content.function()

    @staticmethod
    def show_menu():
        UIManager.hide_all()
        UIManager.Menu.show_menu()
        UIManager.shown_screen = UIManager.Menu

    @staticmethod
    def show_game():
        UIManager.hide_all()
        UIManager.Game.show_game()
        UIManager.shown_screen = UIManager.Game

        EnemiesManager.send_waves_levels(1)

    @staticmethod
    def show_shop():
        UIManager.hide_all()
        UIManager.Shop.show_shop()
        UIManager.shown_screen = UIManager.Shop

    @staticmethod
    def show_settings():
        UIManager.hide_all()
        UIManager.Settings.show_settings()
        UIManager.shown_screen = UIManager.Settings

    @staticmethod
    def leave_game():
        pygame.quit()
        sys.exit()

    @staticmethod
    def show_starting_screen():
        UIManager.hide_all()
        UIManager.StartingScreen.show_starting_screen()
