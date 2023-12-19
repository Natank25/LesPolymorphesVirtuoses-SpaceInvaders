import math
import sys

import pygame

from python import GameProperties
from python import Groups, Player
from python import Resources

pygame.init()


class Text(pygame.sprite.Sprite):
    def __init__(self, text, color, font, update_function=None, update_text=False, **kwargs):
        self.update_function = update_function
        self.text = text
        self.color = color
        self.font = font
        self.update_text = update_text
        self.image = self.font.render(self.text, True, self.color).convert_alpha()

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
                self.rect = self.image.get_rect(**{self.key: eval(self.value)})


class Button(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, image, function):
        super().__init__(Groups.UIGroup, Groups.ButtonGroup)
        self.image = pygame.transform.scale(image, (
            int(image.get_width() * GameProperties.win_scale), int(image.get_height() * GameProperties.win_scale)))
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


class GemText(pygame.sprite.Sprite):
    def __init__(self):
        self.text = "Gems : " + str(GameProperties.gems)
        self.font = Resources.UI.Fonts.arialblack_20
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
        content_list.append(Text("Appuyez pour jouer", (255, 255, 255), Resources.UI.Fonts.click_to_play,
                                 update_function=lambda self: self.image.set_alpha(
                                     int((math.sin(pygame.time.get_ticks() / 1000 * 1.5) + 1) * 123)), center=(
                GameProperties.win_size.x + GameProperties.win_size.width * 0.5,
                GameProperties.win_size.y + GameProperties.win_size.height * 0.9)))

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

        Menu.create_show_game_button(GameProperties.win_size.x + GameProperties.win_size.width / 2,
                                     GameProperties.win_size.y + GameProperties.win_size.height * 0.20)

        Menu.create_show_shop_button(GameProperties.win_size.x + GameProperties.win_size.width / 2,
                                     GameProperties.win_size.y + GameProperties.win_size.height * 0.40)

        Menu.create_show_settings_button(GameProperties.win_size.x + GameProperties.win_size.width / 2,
                                         GameProperties.win_size.y + GameProperties.win_size.height * 0.60)

        Menu.create_leave_game_button(GameProperties.win_size.x + GameProperties.win_size.width / 2,
                                      GameProperties.win_size.y + GameProperties.win_size.height * 0.80)

    @staticmethod
    def hide_menu():
        for content in content_list:
            content.kill()

    @staticmethod
    def create_show_game_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_img, lambda: show_game()))

    @staticmethod
    def create_show_shop_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_img, lambda: show_shop()))

    @staticmethod
    def create_show_settings_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_img, lambda: show_settings()))

    @staticmethod
    def create_leave_game_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.quit_button_img, lambda: leave_game()))

    @staticmethod
    def create_show_menu_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_img, lambda: show_menu()))


class Pause:
    @staticmethod
    def show_pause():
        for content in content_list:
            if type(content) is not Player.Player:
                content.kill()
        hide_all()
        GameProperties.set_background(Resources.UI.Images.background_menu_img)
        Pause.create_resume_game_button(GameProperties.win_size.x + GameProperties.win_size.width * 0.5,
                                        GameProperties.win_size.y + GameProperties.win_size.height * 0.45)
        Pause.create_back_menu_button(GameProperties.win_size.x + GameProperties.win_size.width * 0.5,
                                        GameProperties.win_size.y + GameProperties.win_size.height * 0.8)


    @staticmethod
    def resume_game():
        for content in content_list:
            Groups.UIGroup.add(content)
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.game_started = True
        content_list.append(
            Text("Coins : " + str(GameProperties.coins), (255, 255, 255), Resources.UI.Fonts.arialblack_20,
                 update_function=lambda self: setattr(self, "text", "Coins : " + str(GameProperties.coins)),
                 update_text=True,
                 topleft="(GameProperties.win_size.x + GameProperties.win_size.width - Text.image.get_width - GameProperties.win_size.width * 0.005, GameProperties.win_size.y + GameProperties.win_size.height * 0.005)"))

    @staticmethod
    def create_resume_game_button(x, y):
        content_list.append(
            Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_img, lambda: Pause.unpause_game()))

    @staticmethod
    def unpause_game():
        GameProperties.paused = not GameProperties.paused
        resume_game()


    @staticmethod
    def create_back_menu_button(x, y):
        content_list.append(
            Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_img, lambda: Menu.show_menu()))

class Game:

    @staticmethod
    def show_game():
        for sprite in Groups.InvaderGroup.sprites():
            sprite.kill()
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)
        GameProperties.game_started = True
        content_list.append(
            Text("Coins : " + str(GameProperties.coins), (255, 255, 255), Resources.UI.Fonts.arialblack_20,
                 update_function=lambda self: setattr(self, "text", "Coins : " + str(GameProperties.coins)),
                 update_text=True,
                 topleft="(GameProperties.win_size.x + GameProperties.win_size.width - Text.image.get_width - GameProperties.win_size.width * 0.005, GameProperties.win_size.y + GameProperties.win_size.height * 0.005)"))

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
        content_list.append(
            Text("Gems : " + str(GameProperties.gems), (255, 255, 255), Resources.UI.Fonts.arialblack_20,
                 update_function=lambda self: setattr(self, "text", "Gems : " + str(GameProperties.gems)),
                 update_text=True,
                 topleft="(GameProperties.win_size.x + GameProperties.win_size.width - Text.image.get_width - GameProperties.win_size.width * 0.005, GameProperties.win_size.y + GameProperties.win_size.height * 0.005)"))

        content_list.append(GemText())
        Shop.upgrade_dmg_button(GameProperties.win_size.width * 0.2,
                                GameProperties.win_size.y + GameProperties.win_size.height * 0.2)

    @staticmethod
    def upgrade_dmg_button(x, y):
        content_list.append(
            Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_img, lambda: GameProperties.damage_upgrade()))
        content_list.append(Text("Coute : " + str(GameProperties.get_damage_upgrade_cost()), (255, 255, 255),
                                 Resources.UI.Fonts.arialblack_20, update_function=lambda self: setattr(self, "text",
                                                                                                        "Coute : " + str(
                                                                                                            GameProperties.get_damage_upgrade_cost())),
                                 update_text=True,
                                 center="(" + str(x) + "," + str(y) + ")"))


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
        Menu.create_show_menu_button(GameProperties.win_size.x + GameProperties.win_size.width / 2,
                                     GameProperties.win_size.y + GameProperties.win_size.height * 0.45)


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
