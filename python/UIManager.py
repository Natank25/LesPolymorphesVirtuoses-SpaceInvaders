import math

import pygame

from python import GameProperties, EnemiesManager, DataManager, Utils, UIElements
from python import Groups, Player
from python import Resources
from python.Player import PlayerProperties
from python.Utils import Text, ShopText, Button, TextBox

pygame.init()


class StartingScreen:
    @staticmethod
    def show_starting_screen():
        """
        Displays the starting screen with a text message and a fading effect.
        """
        content_list.append(Text("Appuyez pour jouer", (255, 255, 255), Resources.UI.Fonts.arialblack_35,
                                 update_function=lambda self: self.image.set_alpha(int((math.sin(pygame.time.get_ticks() / 1000 * 1.5) + 1) * 123)),
                                 center=(GameProperties.win_size.x + GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * 0.9)))

        GameProperties.set_background(Resources.UI.Images.background_menu_img)
        GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)
        GameProperties.screen.blit(Resources.UI.Images.game_title_img, GameProperties.win_size.move(25, 100).topleft)

    @staticmethod
    def update():
        """
        Updates the starting screen based on user input.
        """
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()
        if not keys[pygame.K_F11] and (any(keys) or any(mouse)):
            show_menu()


class Menu:
    @staticmethod
    def show_menu():
        """
        Displays the main menu with buttons for various actions.

        This method hides all other content, sets the background, and creates buttons for playing the game,
        accessing the shop, adjusting settings, and leaving the game.
        """
        hide_all()
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.paused = False

        Menu.create_show_game_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.20)
        Menu.create_show_shop_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.40)
        Menu.create_show_settings_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.60)
        Menu.create_leave_game_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.80)
        Menu.create_login_button(GameProperties.win_size.x + GameProperties.win_size.width * 0.925, GameProperties.win_size.y + GameProperties.win_size.height * 0.05)

    """
    @staticmethod
    def hide_menu():
        ###
        Hides all menu-related content.
        ###
        for content in content_list:
            content.kill()
    """

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
    def create_login_button(x, y):
        if not GameProperties.logged_in:
            content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.login_icon, lambda: show_login()))
        else:
            content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.login_icon_green, lambda: show_login()))
            Login.create_logged_in_text(x - GameProperties.win_size.width * 0.3, y - (GameProperties.win_size.y + GameProperties.win_size.height * 0.03))

    @staticmethod
    def create_show_menu_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_button_img, lambda: show_menu()))


class Pause:
    @staticmethod
    def show_pause():
        """
        Displays the pause menu with buttons for resuming the game and going back to the main menu.

        This method hides all other content, sets the background, and creates buttons for resuming the game
        and going back to the main menu.
        """
        for content in content_list:
            content.kill()
        hide_all()
        GameProperties.set_background(Resources.UI.Images.background_menu_img)
        GameProperties.paused = True
        GameProperties.has_paused = True
        Pause.create_resume_game_button(GameProperties.win_size.x + GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * 0.45)
        Pause.create_back_menu_button(GameProperties.win_size.x + GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * 0.8)
        Resources.UI.Sons.ButtonClick8.play()
        Resources.UI.Sons.ButtonClick8.set_volume(0.10)

    @staticmethod
    def resume_game():
        """
        Resumes the game from the pause menu.

        Restores the hidden content, sets the background, and updates the game state to resume.
        """
        for content in content_list:
            Groups.UIGroup.add(content)
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.game_started = True
        Settings.show_coins()
        Resources.UI.Sons.ButtonClick8.play()
        Resources.UI.Sons.ButtonClick8.set_volume(0.10)

    @staticmethod
    def create_resume_game_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.resume_button_img, lambda: Pause.resume_game_button_click()))

    @staticmethod
    def resume_game_button_click():
        Pause.unpause_game()
        Resources.UI.Sons.ButtonClick1.play()
        Resources.UI.Sons.ButtonClick1.set_volume(0.10)

    @staticmethod
    def unpause_game():
        """
        Toggles the pause state of the game.
        """
        GameProperties.paused = not GameProperties.paused
        resume_game()

    @staticmethod
    def create_back_menu_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.leave_game_button_img, lambda: Pause.go_back()))

    @staticmethod
    def back_menu_button_click():
        Pause.go_back()

    @staticmethod
    def go_back():
        """
        Goes back to the main menu from the pause menu.

        Restores the initial game state, clears enemy and player sprites, and shows the main menu.
        """
        GameProperties.paused = False
        GameProperties.game_overed = False
        GameProperties.game_started = False
        GameProperties.playing = False
        EnemiesManager.next_spawns = []

        for players in Groups.PlayerGroup.sprites():
            players.kill()
        for invader in Groups.InvaderGroup.sprites():
            # noinspection PyArgumentList
            invader.kill(animation=False)  # Expected argument
        for bullet in Groups.BulletGroup.sprites():
            bullet.kill()
        EnemiesManager.next_spawns.clear()
        Menu.show_menu()


class Game:

    @staticmethod
    def show_game():
        """
        Displays the game screen.

        Initializes or resumes the game, sets the background, and displays information like coins and lives.
        """
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
        GameProperties.playing = True
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)
        Settings.show_coins()
        Game.show_gem_text_upleft()

    @staticmethod
    def show_gem_text_upleft():
        content_list.append(UIElements.HorizontalGroup(
            (GameProperties.win_size.x + GameProperties.win_size.width * 0.92, GameProperties.win_size.y + GameProperties.win_size.height * 0.06),
            [UIElements.Image(pygame.transform.scale(Resources.UI.Images.icon_gem, (22, 22)), (0, 0)), UIElements.Text(GameProperties.gems, Resources.UI.Fonts.fugaz_one_30, (0, 0))], spacing=10))

        """      
        Text("Gems : " + str(GameProperties.gems), (200, 6, 6), Resources.UI.Fonts.arialblack_20, update_function=lambda self: setattr(self, "text", "Gems : " + str(GameProperties.gems)),
        update_text=True,
        topleft="(GameProperties.win_size.x + GameProperties.win_size.width - Text.image.get_width - GameProperties.win_size.width * 0.005, GameProperties.win_size.y + GameProperties.win_size.height * 0.035)"))
        """

    @staticmethod
    def hide_game():
        """
        Hides the game screen by killing all invader sprites and other content.
        """
        for sprite in Groups.InvaderGroup.sprites():
            sprite.kill()
        for content in content_list:
            content.kill()

    @staticmethod
    def wave_color(self):
        """
        Determines the color of the wave text based on the elapsed time.

        Fades in and out the wave text during specific time intervals.

        Args:
            self: The Text sprite representing the wave text.
        """
        if self.spawn_tick + 2500 < pygame.time.get_ticks():
            content_list.remove(self)
            self.kill()
        elif self.spawn_tick + 1000 < pygame.time.get_ticks():
            self.image.set_alpha(int(-(math.sin((pygame.time.get_ticks() - self.spawn_tick - 1000) / 1000)) * 255) + 255)

    @staticmethod
    def waves_text():
        """
        Displays the wave text with fading effect on the game screen.
        """
        content_list.append(Text("WAVE " + str(GameProperties.current_wave), (255, 255, 255), font=Resources.UI.Fonts.arialblack_35, update_function=lambda self: Game.wave_color(self),
                                 center="(GameProperties.win_size.x + GameProperties.win_size.width- GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * 0.15)"))

    @staticmethod
    def lives_text():
        """
        Displays the lives text on the game screen.
        """
        content_list.append(Text("Vies: " + str(PlayerProperties.MAX_HEALTH), (255, 255, 255), Resources.UI.Fonts.arialblack_20,
                                 update_function=lambda self: setattr(self, "text", "Vies: " + str(PlayerProperties.MAX_HEALTH)), update_text=True, bottomleft=GameProperties.win_size.bottomleft))

    @staticmethod
    def update():
        """
        Updates the game state.

        Checks if the game is started, all invaders are defeated, and there are no pending enemy spawns.
        If conditions are met, it advances to the next wave.
        """
        if GameProperties.game_started and len(Groups.InvaderGroup.sprites()) == 0 and len(EnemiesManager.next_spawns) == 0:
            GameProperties.current_wave += 1
            EnemiesManager.send_waves_levels(GameProperties.current_wave)

    @staticmethod
    def show_coins_text(pos, coindrop):
        text = Text("+" + str(coindrop), (255, 255, 0), Resources.UI.Fonts.arialblack_20, update_function=lambda self: Game.coin_update(self), center=pos)
        Game.show_kill_text(pos, text)

    @staticmethod
    def show_gem_text(pos, gemdrop):
        text = Text("+" + str(gemdrop), (200, 6, 6), Resources.UI.Fonts.arialblack_20, update_function=lambda self: Game.gem_update(self), center=pos)
        Game.show_kill_text(pos, text)

    @staticmethod
    def show_kill_text(pos, text):
        img_text = text.image.copy()
        gem_icon = pygame.transform.scale(Resources.UI.Images.icon_coin, (text.image.get_height(), text.image.get_height()))
        text.image = pygame.Surface((text.image.get_width() + gem_icon.get_width() + 10, text.image.get_height()), pygame.SRCALPHA)
        text.image.blit(img_text, (0, 0))
        text.image.blit(gem_icon, (img_text.get_width() + 10, 0))
        text.rect = text.image.get_rect(center=pos)
        content_list.append(text)

    @staticmethod
    def coin_update(text):
        if text.image.get_alpha() == 0:
            text.kill()
        text.image.set_alpha(500 - (pygame.time.get_ticks() - text.spawn_tick) // 2)
        text.rect.move_ip(0, -1.5)

    @staticmethod
    def gem_update(text):
        if text.image.get_alpha() == 0:
            text.kill()
        text.image.set_alpha(800 - (pygame.time.get_ticks() - text.spawn_tick) // 2)
        text.rect.move_ip(0, -1)


class Shop:
    @staticmethod
    def show_shop():
        """
        Displays the shop screen with upgrade and purchase options.

        This method hides all other content, sets the background, and creates buttons for upgrading damage, attack speed,
        and health. It also provides options to buy gems and navigate between coin and gem shops.
        """
        hide_all()
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)
        Settings.show_coins()

        Shop.upgrade_dmg_button(GameProperties.win_size.width * 0.5 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.2)
        Shop.upgrade_speed_atk_button(GameProperties.win_size.width * 0.5 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.4)
        Shop.upgrade_health_button(GameProperties.win_size.width * 0.5 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.6)

        Shop.back_menu_button(GameProperties.win_size.width * 0.05 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.05)
        content_list.append(Button(pygame.Vector2(GameProperties.win_size.width * 0.95 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.5),
                                   pygame.transform.rotate(Resources.UI.Images.arrow_img, -90), lambda: Shop.gem_shop()))

    @staticmethod
    def gem_shop():
        """
        Displays the gem shop screen with gem purchase options.

        This method hides all other content, sets the background, and creates buttons for buying different quantities
        of gems. It also provides an option to go back to the main coin shop.
        """
        hide_all()
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)
        content_list.append(
            Text("Gems : " + str(GameProperties.gems), (200, 6, 6), Resources.UI.Fonts.arialblack_20, update_function=lambda self: setattr(self, "text", "Gems : " + str(GameProperties.gems)),
                 update_text=True,
                 topleft="(GameProperties.win_size.x + GameProperties.win_size.width - Text.image.get_width - GameProperties.win_size.width * 0.005, GameProperties.win_size.y + GameProperties.win_size.height * 0.005)"))
        Shop.back_menu_button(GameProperties.win_size.width * 0.05 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.05)
        content_list.append(Button(pygame.Vector2(GameProperties.win_size.width * 0.05 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.5),
                                   pygame.transform.rotate(Resources.UI.Images.arrow_img, 90), lambda: Shop.show_shop()))
        content_list.append(Button(pygame.Vector2(GameProperties.win_size.width * 0.95 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.5),
                                   pygame.transform.rotate(Resources.UI.Images.arrow_img, -90), lambda: Shop.skin_shop()))
        Shop.buy_10_button(GameProperties.win_size.width * 0.5 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.2)
        Shop.buy_25_button(GameProperties.win_size.width * 0.5 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.4)
        Shop.buy_50_button(GameProperties.win_size.width * 0.5 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.6)
        Shop.buy_100_button(GameProperties.win_size.width * 0.5 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.8)

    @staticmethod
    def skin_shop():
        hide_all()
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)
        content_list.append(
            Text("Gems : " + str(GameProperties.gems), (200, 6, 6), Resources.UI.Fonts.arialblack_20, update_function=lambda self: setattr(self, "text", "Gems : " + str(GameProperties.gems)),
                 update_text=True,
                 topleft="(GameProperties.win_size.x + GameProperties.win_size.width - Text.image.get_width - GameProperties.win_size.width * 0.005, GameProperties.win_size.y + GameProperties.win_size.height * 0.005)"))
        Shop.back_menu_button(GameProperties.win_size.width * 0.05 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.05)
        content_list.append(Button(pygame.Vector2(GameProperties.win_size.width * 0.05 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.5),
                                   pygame.transform.rotate(Resources.UI.Images.arrow_img, 90), lambda: Shop.gem_shop()))
        Shop.skin_red1_shop(GameProperties.win_size.width * 0.25, GameProperties.win_size.height * 0.3)
        Shop.skin_green1_shop(GameProperties.win_size.width * 0.5, GameProperties.win_size.height * 0.3)
        Shop.skin_blue1_shop(GameProperties.win_size.width * 0.75, GameProperties.win_size.height * 0.3)

    @staticmethod
    def skin_red1_shop(x, y):
        content_list.append(Utils.SpriteImage(Resources.UI.Images.red_skin1, center=(x, y - 75)))
        if GameProperties.red_skin1_locked:
            content_list.append(Utils.SpriteImage(Resources.UI.Images.lock, center=(x, y - 75)))
            content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_button_img, lambda: Shop.refresh_page(GameProperties.red_skin1)))
            content_list.append(ShopText(GameProperties.Upgrades.red1_skin, gems=True, center="(" + str(x) + "," + str(y) + ")"))
        else:
            if GameProperties.skin_name == 'red1':
                content_list.append(Text("Equipped", (255, 255, 255), Resources.UI.Fonts.arialblack_20, center=(x, y)))
            else:
                content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.leave_game_button_img, lambda: Shop.refresh_page(Shop.equip_red1)))

    @staticmethod
    def skin_green1_shop(x, y):
        content_list.append(Utils.SpriteImage(Resources.UI.Images.green_skin1, center=(x, y - 75)))
        if GameProperties.green_skin1_locked:
            content_list.append(Utils.SpriteImage(Resources.UI.Images.lock, center=(x, y - 75)))
            content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_button_img, lambda: Shop.refresh_page(GameProperties.green_skin1())))
            content_list.append(ShopText(GameProperties.Upgrades.green1_skin, gems=True, center="(" + str(x) + "," + str(y) + ")"))
        else:
            if GameProperties.skin_name == 'green1':
                content_list.append(Text("Equipped", (255, 255, 255), Resources.UI.Fonts.arialblack_20, center=(x, y)))
            else:
                content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.leave_game_button_img, lambda: Shop.refresh_page(Shop.equip_green1())))

    @staticmethod
    def skin_blue1_shop(x, y):
        content_list.append(Utils.SpriteImage(Resources.UI.Images.blue_skin1, center=(x, y - 75)))
        if GameProperties.blue_skin1_locked:
            content_list.append(Utils.SpriteImage(Resources.UI.Images.lock, center=(x, y - 75)))
            content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_button_img, lambda: Shop.refresh_page(GameProperties.blue_skin1())))
            content_list.append(ShopText(GameProperties.Upgrades.blue1_skin, gems=True, center="(" + str(x) + "," + str(y) + ")"))
        else:
            if GameProperties.skin_name == 'blue1':
                content_list.append(Text("Equipped", (255, 255, 255), Resources.UI.Fonts.arialblack_20, center=(x, y)))
            else:
                content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.leave_game_button_img, lambda: Shop.refresh_page(Shop.equip_blue1())))

    @staticmethod
    def refresh_page(other_function=None):
        if other_function is not None:
            other_function()

        Shop.skin_shop()

    @staticmethod
    def equip_red1():
        GameProperties.skin = Resources.UI.Images.red_skin1
        GameProperties.skin_name = 'red1'

    @staticmethod
    def equip_green1():
        GameProperties.skin = Resources.UI.Images.green_skin1
        GameProperties.skin_name = 'green1'

    @staticmethod
    def equip_blue1():
        GameProperties.skin = Resources.UI.Images.blue_skin1
        GameProperties.skin_name = 'blue1'

    @staticmethod
    def upgrade_dmg_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.damage_upg_img, lambda: GameProperties.damage_upgrade()))
        content_list.append(ShopText(GameProperties.Upgrades.damage_upgrade, center="(" + str(x) + "," + str(y) + ")"))

    @staticmethod
    def upgrade_speed_atk_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.fire_rate_upg_img, lambda: GameProperties.atk_speed_upgrade()))
        content_list.append(ShopText(GameProperties.Upgrades.atk_speed_upgrade, center="(" + str(x) + "," + str(y) + ")"))

    @staticmethod
    def upgrade_health_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.health_upg_img, lambda: GameProperties.health_upgrade()))
        content_list.append(ShopText(GameProperties.Upgrades.health_upgrade, center="(" + str(x) + "," + str(y) + ")"))

    @staticmethod
    def back_menu_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), pygame.transform.rotate(Resources.UI.Images.arrow_img, 90), lambda: Menu.show_menu()))

    @staticmethod
    def buy_10_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.gems_10, lambda: GameProperties.gems_10()))
        content_list.append(ShopText(GameProperties.Upgrades.gems_10, gems=True, center="(" + str(x) + "," + str(y) + ")"))

    @staticmethod
    def buy_25_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.gems_25, lambda: GameProperties.gems_25()))
        content_list.append(ShopText(GameProperties.Upgrades.gems_25, gems=True, center="(" + str(x) + "," + str(y) + ")"))

    @staticmethod
    def buy_50_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.gems_50, lambda: GameProperties.gems_50()))
        content_list.append(ShopText(GameProperties.Upgrades.gems_50, gems=True, center="(" + str(x) + "," + str(y) + ")"))

    @staticmethod
    def buy_100_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.gems_100, lambda: GameProperties.gems_100()))
        content_list.append(ShopText(GameProperties.Upgrades.gems_100, gems=True, center="(" + str(x) + "," + str(y) + ")"))


class Settings:
    @staticmethod
    def show_settings():
        """
        Displays the settings screen.

        This method sets the background, adds a placeholder message for settings, and creates a button to go back to the main menu.
        """
        GameProperties.set_background(Resources.UI.Images.background_img)
        GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)
        Settings.back_menu_button(GameProperties.win_size.width * 0.05 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.05)
        content_list.append(Text("Change coins", (255, 255, 255), Resources.UI.Fonts.arialblack_20,
                                 center=(GameProperties.win_size.width * 0.2 + GameProperties.win_size.x, GameProperties.win_size.height * 0.3 + GameProperties.win_size.y)))
        content_list.append(Text("display : ", (255, 255, 255), Resources.UI.Fonts.arialblack_20,
                                 center=(GameProperties.win_size.width * 0.2225 + GameProperties.win_size.x, GameProperties.win_size.height * 0.3275 + GameProperties.win_size.y)))
        Settings.change_coins_type_button(GameProperties.win_size.width * 0.675 + GameProperties.win_size.x, GameProperties.win_size.y + GameProperties.win_size.height * 0.3175)

    @staticmethod
    def back_menu_button(x, y):
        content_list.append(Button(pygame.Vector2(x, y), pygame.transform.rotate(Resources.UI.Images.arrow_img, 90), lambda: Menu.show_menu()))

    @staticmethod
    def change_coins_type_button(x, y):
        if GameProperties.settings.get("coins_type") == 'exponent':
            content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.scientific_numbers_image, lambda: Settings.change_coins_type()))
        else:
            content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.big_numbers_image, lambda: Settings.change_coins_type()))

    @staticmethod
    def change_coins_type():
        coins_type = GameProperties.settings.get("coins_type")
        if coins_type == 'exponent':
            GameProperties.settings["coins_type"] = 'big_numbers'
        else:
            GameProperties.settings["coins_type"] = 'exponent'
        show_settings()

    @staticmethod
    def show_coins():
        content_list.append(Text("Coins : " + str(GameProperties.format_int(GameProperties.coins)), (255, 255, 0), Resources.UI.Fonts.arialblack_20,
                                 update_function=lambda self: setattr(self, "text", "Coins : " + str(GameProperties.format_int(GameProperties.coins))), update_text=True,
                                 topleft="(GameProperties.win_size.x + GameProperties.win_size.width - Text.image.get_width - GameProperties.win_size.width * 0.005, GameProperties.win_size.y + GameProperties.win_size.height * 0.005)"))


class GameOver:
    @staticmethod
    def show_game_over():
        """
        Displays the game over screen.

        This method sets the background and creates a button to go back to the main menu.
        """

        for invader in Groups.InvaderGroup.sprites():
            invader.kill()

        EnemiesManager.next_spawns.clear()
        content_list.append(GameOver.show_defeat_wave_text())
        GameProperties.current_wave = 0
        GameProperties.set_background(Resources.UI.Images.background_menu_img)
        Pause.create_back_menu_button(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.85)
        content_list.append(Resources.UI.Images.game_over_text)

        content_list.append(GameOver.GameOverImage())

    class GameOverImage(Utils.Sprite):
        def __init__(self):
            super().__init__(Groups.UIGroup)
            self.image = Resources.UI.Images.game_over_text
            self.rect = self.image.get_rect(midtop=(GameProperties.win_size.x + GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * 0.09))

    @staticmethod
    def show_defeat_wave_text():
        return Text("Defeated at wave : " + str(GameProperties.current_wave), (255, 255, 255), Resources.UI.Fonts.arialblack_35,
                    center="(GameProperties.win_size.x + GameProperties.win_size.width * 0.50, GameProperties.win_size.y + GameProperties.win_size.height * 0.70)")


class Login:
    loginPopUp: Utils.PopUp = None
    inputBox: TextBox = None
    passwordBox: TextBox = None

    @staticmethod
    def show_login_menu():
        """
        Displays the login menu.

        This method creates text boxes for username and password entry, and a button to attempt login.
        """
        global inputBox, passwordBox
        Login.show_login_text(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.26)
        inputBox = TextBox(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.30, lambda: Login.try_login())
        Login.show_password_text(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.56)
        passwordBox = TextBox(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.60, lambda: Login.try_login(),
                              password=True)

        inputBox.other_box = passwordBox
        passwordBox.other_box = inputBox

        content_list.append(inputBox)
        content_list.append(passwordBox)
        Login.verify_login_password(GameProperties.win_size.x + GameProperties.win_size.width / 2, GameProperties.win_size.y + GameProperties.win_size.height * 0.80)
        Resources.UI.Sons.ButtonClick8.play()
        Resources.UI.Sons.ButtonClick8.set_volume(0.10)

    @staticmethod
    def show_login_text(x, y):
        content_list.append(Text("Username : ", (255, 255, 255), Resources.UI.Fonts.arialblack_20, center=(x, y)))
        Resources.UI.Sons.ButtonClick8.play()
        Resources.UI.Sons.ButtonClick8.set_volume(0.10)

    @staticmethod
    def show_password_text(x, y):
        content_list.append(Text("Password : ", (255, 255, 255), Resources.UI.Fonts.arialblack_20, center=(x, y)))
        Resources.UI.Sons.ButtonClick8.play()
        Resources.UI.Sons.ButtonClick8.set_volume(0.10)

    @staticmethod
    def try_login():
        """
        Attempts login using the provided username and password.

        If both the username and password are provided and a successful login is verified, the game is loaded.
        Otherwise, the default user is loaded.
        """
        if inputBox.text != "" and passwordBox.text != "":
            if DataManager.DataManager.verify_successful_login(inputBox.text, passwordBox.text):
                Login.loginPopUp = Utils.PopUp("Vous allez vous connecter au compte :  " + inputBox.text, "white", Resources.UI.Fonts.arialblack_20, "blue4",
                                               [Login.accept_login_button(GameProperties.win_size.x + GameProperties.win_size.width * 0.35,
                                                                          GameProperties.win_size.y + GameProperties.win_size.height * 0.55),
                                                Login.cancel_button(GameProperties.win_size.x + GameProperties.win_size.width * 0.75,
                                                                    GameProperties.win_size.y + GameProperties.win_size.height * 0.55)],
                                               (25 + (GameProperties.win_size.width - 50) * 0.8, GameProperties.win_size.height * 0.1), content_list,
                                               midtop=[GameProperties.win_size.x + GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * 0.4])

            elif len(passwordBox.text) < 3:
                Login.loginPopUp = Utils.PopUp("Password is too short", "white", Resources.UI.Fonts.arialblack_20, "blue4",
                                               [Login.ok_button(GameProperties.win_size.x + GameProperties.win_size.width * 0.5,
                                                                GameProperties.win_size.y + GameProperties.win_size.height * 0.55)],
                                               (25 + (GameProperties.win_size.width - 50) * 0.8, GameProperties.win_size.height * 0.1), content_list,
                                               midtop=[GameProperties.win_size.x + GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * 0.4])
            else:
                Login.loginPopUp = Utils.PopUp("Vous allez créer un nouveau compte " + inputBox.text, "white", Resources.UI.Fonts.arialblack_20, "blue4",
                                               [Login.accept_create_button(GameProperties.win_size.x + GameProperties.win_size.width * 0.35,
                                                                           GameProperties.win_size.y + GameProperties.win_size.height * 0.55),
                                                Login.cancel_button(GameProperties.win_size.x + GameProperties.win_size.width * 0.75,
                                                                    GameProperties.win_size.y + GameProperties.win_size.height * 0.55)],
                                               (25 + (GameProperties.win_size.width - 50) * 0.8, GameProperties.win_size.height * 0.1), content_list,
                                               midtop=[GameProperties.win_size.x + GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * 0.4])

        elif inputBox.text == "":
            Login.loginPopUp = Utils.PopUp("veuillez rentrer un username cohérent", "white", Resources.UI.Fonts.arialblack_20, "blue4",
                                           [Login.ok_button(GameProperties.win_size.x + GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * 0.55)],
                                           (25 + (GameProperties.win_size.width - 50) * 0.8, GameProperties.win_size.height * 0.1), content_list,
                                           midtop=[GameProperties.win_size.x + GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * 0.4])
        elif passwordBox.text == "":
            Login.loginPopUp = Utils.PopUp("Votre mot de passe est vide", "white", Resources.UI.Fonts.arialblack_20, "blue4",
                                           [Login.ok_button(GameProperties.win_size.x + GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * 0.55)],
                                           (25 + (GameProperties.win_size.width - 50) * 0.8, GameProperties.win_size.height * 0.1), content_list,
                                           midtop=[GameProperties.win_size.x + GameProperties.win_size.width * 0.5, GameProperties.win_size.y + GameProperties.win_size.height * 0.4])
            content_list.append(Login.loginPopUp)
            # Login.LoginPopUp1('empty_password', center=(GameProperties.win_size.x + GameProperties.win_size.width*0.5, GameProperties.win_size.y + GameProperties.win_size.height*0.4))

    @staticmethod
    def ok_button(x, y):
        btn = Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_button_img, lambda: Login.del_pop_up())
        content_list.append(btn)
        Resources.UI.Sons.ButtonClick8.play()
        Resources.UI.Sons.ButtonClick8.set_volume(0.10)
        return btn

    @staticmethod
    def cancel_button(x, y):
        btn = Button(pygame.Vector2(x, y), Resources.UI.Images.leave_game_button_img, lambda: Login.del_pop_up())
        content_list.append(btn)
        Resources.UI.Sons.ButtonClick8.play()
        Resources.UI.Sons.ButtonClick8.set_volume(0.10)
        return btn

    @staticmethod
    def accept_create_button(x, y):
        btn = Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_button_img, lambda: Login.del_pop_up_create())
        content_list.append(btn)
        Resources.UI.Sons.ButtonClick8.play()
        Resources.UI.Sons.ButtonClick8.set_volume(0.10)
        return btn

    @staticmethod
    def accept_login_button(x, y):
        btn = Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_button_img, lambda: Login.del_pop_up_login())
        content_list.append(btn)
        Resources.UI.Sons.ButtonClick8.play()
        Resources.UI.Sons.ButtonClick8.set_volume(0.10)
        return btn

    @staticmethod
    def del_pop_up():
        Login.loginPopUp.kill()
        pass

    @staticmethod
    def del_pop_up_login():
        DataManager.DataManager.load_game(username=inputBox.text)
        GameProperties.logged_in = True
        show_menu()
        Login.loginPopUp.kill()
        pass

    @staticmethod
    def del_pop_up_create():
        DataManager.DataManager.add_user(inputBox.text, passwordBox.text)
        DataManager.DataManager.load_game(username=inputBox.text)
        GameProperties.logged_in = True
        show_menu()
        Login.loginPopUp.kill()
        pass

    @staticmethod
    def create_logged_in_text(x, y):
        if len(inputBox.text) > 5:
            for i in range(len(inputBox.text) - 5):
                x -= 9
        content_list.append(Text("Logged In as : " + inputBox.text, (255, 255, 255), Resources.UI.Fonts.arialblack_20, center=(x, y)))

    class LoginPopUp1(Text):
        def __init__(self, message_type, color='white', **kwargs):
            super().__init__("Lorem ipsum", color, Resources.UI.Fonts.arialblack_20, "blue4", **kwargs)
            # self.rect.size = ()
            self.message_type = message_type
            self.show_pop_up()

        def show_pop_up(self):
            if self.message_type == 'empty_password':
                self.set_text(" Vous n'avez pas entrez de MDP ")
                print('le password est vide')

    @staticmethod
    def verify_login_password(x, y):
        content_list.append(Button(pygame.Vector2(x, y), Resources.UI.Images.play_game_button_img, lambda: Login.try_login()))


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
    Resources.UI.Sons.ButtonClick8.play()
    Resources.UI.Sons.ButtonClick8.set_volume(0.10)


def show_game():
    global shown_screen
    hide_all()
    Game.show_game()
    shown_screen = Game
    Resources.UI.Sons.ButtonClick8.play()
    Resources.UI.Sons.ButtonClick8.set_volume(0.10)


def show_shop():
    global shown_screen
    hide_all()
    Shop.show_shop()
    shown_screen = Shop
    Resources.UI.Sons.ButtonClick8.play()
    Resources.UI.Sons.ButtonClick8.set_volume(0.10)


def show_login():
    global shown_screen
    hide_all()
    Login.show_login_menu()
    shown_screen = Login
    Resources.UI.Sons.ButtonClick8.play()
    Resources.UI.Sons.ButtonClick8.set_volume(0.10)


def show_settings():
    global shown_screen
    hide_all()
    Settings.show_settings()
    Resources.UI.Sons.ButtonClick8.play()
    Resources.UI.Sons.ButtonClick8.set_volume(0.10)
    shown_screen = Settings
    Resources.UI.Sons.ButtonClick8.play()
    Resources.UI.Sons.ButtonClick8.set_volume(0.10)


def leave_game():
    global shown_screen
    GameProperties.leave_game()
    Resources.UI.Sons.ButtonClick8.play()
    Resources.UI.Sons.ButtonClick8.set_volume(0.10)


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
    Resources.UI.Sons.ButtonClick8.play()
    Resources.UI.Sons.ButtonClick8.set_volume(0.10)


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
