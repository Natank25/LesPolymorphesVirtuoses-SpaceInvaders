import os
import sys

import pygame

from EnemiesSpawner import EnemiesManager
from Groups import Groups
from Player import Player
from python.GameProperties import GameProperties


class UI_Manager:

    @staticmethod
    def hide_all():
        UI_Manager.Menu.hide_menu()
        UI_Manager.Game.hide_game()
        GameProperties.screen.blit(GameProperties.background, (0, 0))

    @staticmethod
    def show_menu():
        UI_Manager.hide_all()
        UI_Manager.Menu.show_menu()

    @staticmethod
    def show_game():
        UI_Manager.hide_all()
        UI_Manager.Game.show_game()

        EnemiesManager.send_waves_levels(1)

    @staticmethod
    def show_shop():
        UI_Manager.hide_all()
        UI_Manager.Game.show_shop()

    @staticmethod
    def show_settings():
        UI_Manager.hide_all()
        UI_Manager.Game.show_settings()

    @staticmethod
    def leave_game():
        pygame.quit()
        sys.exit()

    @staticmethod
    def create_show_game_button(x, y):
        UI_Manager.Menu.content_list.append(
            UI_Manager.Button(pygame.Vector2(x * GameProperties.win_scale, y * GameProperties.win_scale),
                              lambda: UI_Manager.show_game()))

    @staticmethod
    def create_show_shop_button(x, y):
        UI_Manager.Menu.content_list.append(
            UI_Manager.Button(pygame.Vector2(x * GameProperties.win_scale, y * GameProperties.win_scale),
                              lambda: UI_Manager.show_shop()))

    @staticmethod
    def create_show_settings_button(x, y):
        UI_Manager.Menu.content_list.append(
            UI_Manager.Button(pygame.Vector2(x * GameProperties.win_scale, y * GameProperties.win_scale),
                              lambda: UI_Manager.show_settings()))

    @staticmethod
    def create_leave_game_button(x, y):
        UI_Manager.Menu.content_list.append(
            UI_Manager.Button(pygame.Vector2(x * GameProperties.win_scale, y * GameProperties.win_scale),
                              lambda: UI_Manager.leave_game()))

    class Button(pygame.sprite.Sprite):
        def __init__(self, pos: pygame.Vector2, function):
            super().__init__(Groups.UIGroup, Groups.ButtonGroup)
            self.image_path = os.path.join("img", "UI", "buttons")
            self.image = pygame.image.load(self.image_path).convert_alpha()
            self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * GameProperties.win_scale),
                                                             int(self.image.get_height() * GameProperties.win_scale)))
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
            GameProperties.background = pygame.image.load(os.path.join("img", "background_menu.png"))

            UI_Manager.create_show_game_button(GameProperties.win_size.x + GameProperties.win_size.width / 2,
                                               GameProperties.win_size.y + GameProperties.win_size.height * 0.20)

            UI_Manager.create_show_shop_button(GameProperties.win_size.x + GameProperties.win_size.width / 2,
                                               GameProperties.win_size.y + GameProperties.win_size.height * 0.40)

            UI_Manager.create_show_settings_button(GameProperties.win_size.x + GameProperties.win_size.width / 2,
                                                   GameProperties.win_size.y + GameProperties.win_size.height * 0.60)

            UI_Manager.create_leave_game_button(GameProperties.win_size.x + GameProperties.win_size.width / 2,
                                                GameProperties.win_size.y + GameProperties.win_size.height * 0.80)

        @staticmethod
        def hide_menu():
            for content in UI_Manager.Menu.content_list:
                content.kill()

    class Game:
        content_list: list = []

        @staticmethod
        def show_game():
            UI_Manager.Game.content_list.append(Player())
            GameProperties.background = pygame.image.load(os.path.join("img", "background.png"))
            GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)

        @staticmethod
        def show_shop():
            GameProperties.background = pygame.image.load(os.path.join("img", "background.png"))
            GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)

        @staticmethod
        def show_settings():
            GameProperties.background = pygame.image.load(os.path.join("img", "background.png"))
            GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)

        @staticmethod
        def hide_game():
            for sprite in Groups.InvaderGroup.sprites():
                sprite.kill()
            for on_going_thread in GameProperties.on_going_threads:
                on_going_thread.cancel()
            for content in UI_Manager.Game.content_list:
                content.kill()
