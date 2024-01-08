import math
import random

import pygame
import pygame.sprite
from pygame import Vector2

from python import GameProperties, Resources
from python import Groups


class Sprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        if Groups.UIGroup in groups:
            super().__init__(*groups, Groups.UIGroup)
        else:
            super().__init__(*groups, Groups.AllSpritesGroup)

    def update(self, *args, **kwargs):
        if self.rect.top > GameProperties.win_size.height + GameProperties.win_size.y:
            self.kill()

    def kill(self):
        super().kill()
        del self


class AnimatedSprite(Sprite):

    def __init__(self, pos, animation_img, total_frames: int, frame_time=150, kill_when_done=False, rotable=False, *groups):

        self.rotable = rotable
        self.total_frames = total_frames
        self.frame_time = frame_time
        self.current_frame = 0
        self.current_time = 0
        self.animation_img = animation_img.convert_alpha()
        self.frames = [pygame.surface.Surface((self.animation_img.get_height(), self.animation_img.get_height()), pygame.SRCALPHA).convert_alpha() for _ in range(total_frames)]
        self.kill_when_done = kill_when_done

        rotation = random.randint(-180, 180)

        for index in range(self.total_frames):
            self.frames[index].blit(self.animation_img, (0, 0), ((self.animation_img.get_width() // self.total_frames) * index, 0, self.animation_img.get_height(), self.animation_img.get_height()))
            if self.rotable:
                self.frames[index] = pygame.transform.rotozoom(self.frames[index], rotation, 1)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=pos)
        super().__init__(*groups)

    def update(self, *args, **kwargs):
        super().update(args=args, kwargs=kwargs)
        self.update_frame()

    def update_frame(self):
        self.current_time += GameProperties.deltatime
        if self.current_time >= self.frame_time:
            self.current_time = 0
            self.current_frame = (self.current_frame + 1) % self.total_frames
            if self.current_frame + 1 == self.total_frames:
                self.kill()
            self.image = self.frames[self.current_frame]


class PivotSprite(Sprite):

    def __init__(self, pos, pivot_point, image, *groups, speed=20):
        super().__init__(*groups)
        self.speed = speed
        self.image = image
        # A reference to the original image to preserve the quality.
        self.orig_image = self.image
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)  # .rotate(180) # The original center position/pivot point.
        self.pivot_point = -Vector2(pivot_point)

        self.angle = -1
        self.target_angle = self.angle
        self.easing = False
        self.start_angle = self.angle
        self.start_rot_time = 0
        self.duration = 0
        self.set_rotation(0)

    def update(self):
        self.smooth_rotate()

    def smooth_rotate(self):
        if self.easing:
            # Calculate the eased position based on time elapsed
            elapsed_time = pygame.time.get_ticks() - self.start_rot_time
            progress = elapsed_time / self.duration
            if progress > 1:
                progress = 1

            eased_progress = Easings.easeInOutSine(progress)
            next_pos = round(self.start_angle + eased_progress * (self.target_angle - self.start_angle))

            # Rotate the image.
            self.image = pygame.transform.rotozoom(self.orig_image, -next_pos, 1)
            # Rotate the pivot_point vector.
            offset_rotated = self.pivot_point.rotate(next_pos)
            # Create a new rect with the center of the sprite + the pivot_point.
            self.rect = self.image.get_rect(center=self.pos + offset_rotated)

            self.angle = next_pos

            if progress == 1:
                self.easing = False

    def rotate(self, angle):
        if not self.easing:
            self.target_angle += angle
            self.update_target_angle()

    def set_rotation(self, angle):
        if not self.easing:
            self.target_angle = fastest_angle(self.angle, angle)
            self.update_target_angle()

    def update_target_angle(self):
        self.start_angle = self.angle
        distance = abs(self.target_angle - self.start_angle)
        self.duration = distance / self.speed * 1000  # Calculate duration based on speed
        if self.duration == 0:
            self.duration = 1
        self.start_rot_time = pygame.time.get_ticks()
        self.easing = True

    def move(self, x, y):
        self.rect.move_ip(x, y)
        self.pos += Vector2(x, y)


class Body:
    def __init__(self):
        self.childs = []

    def move(self, x, y):
        for child in self.childs:
            child.move_ip(x, y)


class Bone:
    def __init__(self, parent):
        self.parent = parent
        self.childs = []

    def move_ip(self, x, y):
        for child in self.childs:
            child.move_ip(x, y)


class Easings:
    @staticmethod
    def easeInOutSine(t):
        return -(math.cos(math.pi * t) - 1) / 2

    @staticmethod
    def ease_out_elastic(x):
        c4 = (2 * math.pi) / 3

        if x == 0:
            return 0
        elif x == 1:
            return 1
        else:
            return math.pow(2, -20 * x) * math.sin((x * 10 - 0.75) * c4) + 1

    @staticmethod
    def ease_in_out_back(x):
        c1 = 1.70158
        c2 = c1 * 1.525

        if x < 0.5:
            return (pow(2 * x, 2) * ((c2 + 1) * 2 * x - c2)) / 2
        else:
            return (pow(2 * x - 2, 2) * ((c2 + 1) * (x * 2 - 2) + c2) + 2) / 2

    @staticmethod
    def ease_in_out_cubic(x):
        return 4 * x ** 3 if x < 0.5 else 1 - ((-2 * x + 2) ** 3) / 2


def fastest_angle(prev_angle, new_angle):
    # Ensure both angles are within the range [0, 360)
    prev_angle %= 360
    new_angle %= 360

    # Calculate the absolute angular difference
    angle_diff = (new_angle - prev_angle + 180) % 360 - 180

    return angle_diff


def show_coins_text(pos, coindrop):
    from python import UIManager
    UIManager.Game.show_coins_text(pos, coindrop)


def show_gem_text(pos, coindrop):
    from python import UIManager
    UIManager.Game.show_gem_text(pos, coindrop)


class Text(pygame.sprite.Sprite):
    """
            A versatile pygame sprite for rendering text with optional dynamic updates.

            Args:
                text (str): The initial text to be displayed.
                color (tuple): RGB values representing the text color.
                font (pygame.font.Font): The font used for rendering the text.
                update_function (callable, optional): A function that can dynamically update the text sprite.
                update_text (bool, optional): Flag indicating whether to update the text dynamically.
                color_function (callable, optional): A function to dynamically update the text color.
                **kwargs: Additional keyword arguments for customizing the sprite's rect.

            Attributes:
                update_function (callable): A function that can dynamically update the text sprite.
                color_function (callable): A function to dynamically update the text color.
                text (str): The current text being displayed.
                color (tuple): RGB values representing the text color.
                font (pygame.font.Font): The font used for rendering the text.
                update_text (bool): Flag indicating whether to update the text dynamically.
                image (pygame.Surface): The rendered text surface.
                rect (pygame.Rect): The rectangular area that encloses the text sprite.
                spawn_tick (int): The timestamp when the text sprite was created.
            """

    def __init__(self, text, color, font, background_color=None, update_function=None, update_text=False, color_function=None, **kwargs):
        self.background_color = background_color
        self.update_function = update_function
        self.color_function = color_function
        self.text = text
        self.color = color
        self.font = font
        self.update_text = update_text
        self.image = self.font.render(self.text, True, self.color, self.background_color).convert_alpha()
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
                self.set_text()
            if self.color_function:
                self.color = self.color_function()

    def set_text(self, new_text=None):
        if new_text is not None:
            self.text = new_text

        self.image = self.font.render(self.text, True, self.color, self.background_color).convert_alpha()
        self.image = pygame.transform.scale_by(self.image, GameProperties.win_scale)
        self.rect = self.image.get_rect(**{self.key: eval(self.value)})


class ShopText(Text):
    def __init__(self, upgrade_id, gems=False, **kwargs):
        """
        A specialized Text class for displaying upgrade information in a shop.

        Args:
            upgrade_id (str): The identifier for the upgrade.
            gems (bool, optional): Flag indicating whether the upgrade uses gems instead of coins.
            **kwargs: Additional keyword arguments for customizing the sprite's rect.

        Attributes:
            upgrade_id (str): The identifier for the upgrade.
            gems (bool): Flag indicating whether the upgrade uses gems instead of coins.
        """
        self.upgrade_id = upgrade_id
        self.gems = gems

        if not self.gems:
            super().__init__("Niv. " + str(GameProperties.coin_shop[self.upgrade_id]) + " / " + str(GameProperties.format_int(eval("GameProperties.get_" + self.upgrade_id + "_cost()"))) + "$",
                             (128, 0, 0), Resources.UI.Fonts.fugaz_one_30, update_function=lambda self: setattr(self, "text", "Niv. " + str(GameProperties.coin_shop[self.upgrade_id]) + " / " + str(
                    GameProperties.format_int(eval("GameProperties.get_" + self.upgrade_id + "_cost()"))) + "$"), update_text=True, color_function=lambda: self.get_upgrade_color(), **kwargs)
        else:
            super().__init__("Niv. " + str(GameProperties.gem_shop[self.upgrade_id]) + " / " + str(GameProperties.format_int(eval("GameProperties.get_" + self.upgrade_id + "_cost()"))) + "$",
                             (128, 0, 0), Resources.UI.Fonts.fugaz_one_30, update_function=lambda self: setattr(self, "text", "N°. " + str(GameProperties.gem_shop[self.upgrade_id]) + " / " + str(
                    GameProperties.format_int(eval("GameProperties.get_" + self.upgrade_id + "_cost()"))) + "$"), update_text=True, color_function=lambda: self.get_upgrade_color(), **kwargs)

    def get_upgrade_color(self):
        """
        Determines the color of the text based on the affordability of the upgrade.

        Returns:
            tuple: RGB values representing the color.
        """
        if self.gems:
            if eval("GameProperties.get_" + self.upgrade_id + "_cost()") <= GameProperties.gems:
                return 0, 128, 0  # Green color for affordable gems upgrade
            else:
                return 128, 0, 0  # Red color for unaffordable gems upgrade
        else:
            if eval("GameProperties.get_" + self.upgrade_id + "_cost()") <= GameProperties.coins:
                return 0, 128, 0  # Green color for affordable coins upgrade
            else:
                return 128, 0, 0  # Red color for unaffordable coins upgrade


class Button(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, image, function):
        """
        A pygame sprite representing a clickable button.

        Args:
            pos (pygame.Vector2): The position of the button's center.
            image: The image used for the button.
            function (callable): The function to be executed when the button is clicked.
        """
        super().__init__(Groups.UIGroup, Groups.ButtonGroup)
        self.image = pygame.transform.scale_by(pygame.transform.scale_by(image, GameProperties.button_scale), GameProperties.win_scale)
        self.rect = self.image.get_rect(center=pos)
        self.function = function
        super().__init__(Groups.UIGroup, Groups.ButtonGroup)

    def is_pressed(self, mouse_pos):
        """
        Checks if the button is pressed based on the mouse position.

        Args:
            mouse_pos (tuple): The current mouse position (x, y).

        Returns:
            bool: True if the button is pressed, False otherwise.
        """
        return self.rect.collidepoint(mouse_pos)

    def update(self, **kwargs):
        """
        Updates the button's state and executes the associated function if clicked.

        Args:
            **kwargs: Additional keyword arguments.
                button_group_update (bool, optional): Flag indicating whether the update is part of a button group update.
        """
        is_button_group_update = kwargs.get("button_group_update", False)
        if is_button_group_update:
            mouse_pos = pygame.mouse.get_pos()
            if pygame.mouse.get_pressed()[0] and self.is_pressed(mouse_pos):
                self.function()


class TextBox(pygame.sprite.Sprite):
    def __init__(self, x, y, return_function, other_box=None, password=False, active=False):
        """
        A pygame sprite representing a text input box.

        Args:
            x (int): The x-coordinate of the center of the text box.
            y (int): The y-coordinate of the center of the text box.
            return_function (callable): The function to be executed when the Enter key is pressed.
            active (bool, optional): Flag indicating whether the text box is currently active.
        """
        super().__init__(Groups.UIGroup)
        self.active = active
        self.other_box = other_box
        self.color_passive = Resources.UI.Colors.color_passive
        self.color_active = Resources.UI.Colors.color_active
        self.color = self.color_passive
        self.font = Resources.UI.Fonts.arialblack_20
        self.text = ""
        self.displayed_text = ""
        self.password = password
        self.image = pygame.surface.Surface((200, 30), pygame.SRCALPHA)
        self.rect = self.image.get_rect(center=(x, y))
        self.image.fill(self.color)
        self.return_function = return_function

    def update(self):
        """
        Updates the state of the text box based on user input and triggers associated actions.
        """
        for event in GameProperties.events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = True
                else:
                    self.active = False
            if self.active and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.displayed_text = self.displayed_text[:-1]
                    self.text = self.text[:-1]

                elif event.key == pygame.K_TAB:
                    GameProperties.events.remove(event)
                    self.active = not self.active
                    self.other_box.active = not self.other_box.active

                elif self.active and event.key == pygame.K_RETURN:
                    self.return_function()

                else:
                    if self.password:
                        self.displayed_text += "*"
                    else:
                        self.displayed_text += event.unicode
                    self.text += event.unicode
        if self.active:
            self.color = self.color_active
        else:
            self.color = self.color_passive

        self.draw_text()

    def draw_text(self):
        """
        Draws the text on the text box surface.
        """
        self.image.fill(self.color)
        text_surface = self.font.render(self.displayed_text, True, (255, 255, 255))
        self.image.blit(text_surface, (5, 0))
