import pygame
from pygame import Vector2

from python import Utils

pygame.init()


class Sprite(Utils.Sprite):
    """
    The base class of all UIElements
    Args:
        surface (pygame.Surface): The surface to be displayed
        pos (Vector2 | tuple[int, int] | list[int, int]): The center position of the image
    Attributes:
        pos (Vector2): The position of the center of the sprite
        self.set_pos(new_pos): The new center of the image
        self.move(delta_pos): Moves the image by the specified delta position
        self.set_surface(surface): Changes the surface to be displayed
    """

    def __init__(self, surface, pos, *groups):
        super().__init__(*groups)
        self.pos = Vector2(pos)
        self.image = surface
        self.rect = self.image.get_rect(center=self.pos)
        self.group = None

    def set_pos(self, new_pos):
        """
        Changes the center position of the sprite to *new_pos*
        Args:
            new_pos (tuple[int, int]| list[int, int] | Vector2): The new center of the sprite
        """
        self.rect.center = new_pos

    def move(self, delta_pos):
        """
        Moves the image by the specified delta position
        Args:
            delta_pos (tuple[int, int]| list[int, int] | Vector2): The amount of pixels to move the sprite
        """
        self.set_pos(Vector2(self.rect.center) - Vector2(delta_pos))

    def set_surface(self, surface):
        """
        Changes the surface to be displayed
        Args:
            surface (pygame.Surface): The surface to be displayed
        """
        self.image = surface
        self.rect = self.image.get_rect(center=self.pos)
        self.update_group()

    def set_alpha(self, alpha):
        """
        Changes the alpha of the sprite
        Args:
            alpha (int): The new alpha of the sprite, should be a value between 0 and 255. Values between 0 will do the same as 0, values above 255 will do the same as 255
        """
        self.image.set_alpha(alpha)

    def get_rect(self):
        """
        Returns the rect of the sprite
        Returns:
            pygame.rect.Rect: The rect of the sprite
        """
        return self.rect

    def set_group(self, new_group):
        """
        Sets the group of the sprite
        Args:
            new_group (Group | HorizontalGroup | VerticalGroup): The new group of the sprite
        """
        self.group = new_group

    def get_group(self):
        """
        Returns the group of the sprite
        Returns:
            (Group | HorizontalGroup | VerticalGroup): The group of the sprite
        """
        return self.group

    def update_group(self):
        """
        Updates the pos of the group of the sprite
        """
        if self.group:
            self.group.update_pos()


class Image(Sprite):
    """
    A class representing an image that can be displayed on screen
    Args:
        image (pygame.Surface): The image to be displayed
        pos (Vector2 | tuple[int, int] | list[int, int]): The center position of the image
        *groups (pygame.sprite.Group)

    Attributes:
        self.set_image(image): Sets the image while keeping its center at the same position as the previous one
    """

    def __init__(self, image, pos, *groups):
        super().__init__(image, pos, *groups)

    def set_image(self, image):
        """
        Changes the image of the sprite to *image*
        Args:
            image (pygame.Surface): The image to be set
        """
        self.set_surface(image)


class Text(Sprite):
    """
    A class representing a text that can be displayed on screen

    The alpha for the text will use the alpha of *color*
    Args:
        text (str | MutableObject): The text to display, if is an instance of the MutableObject (or any subclass) the text will update automatically
        font (pygame.font.Font | pygame.font.SysFont): The font used to render the text
        pos (Vector2 | tuple[int, int] | list[int, int]): The center position of the text
        color (tuple[int, int, int] | tuple[int, int, int, int] | list[int, int, int] | list[int, int, int, int] | pygame.color.Color): The color of the text (r,g,b,a)
        background_color (tuple[int, int, int]| list[int, int, int] | pygame.color.Color): The color of the background of the text (r,g,b)

    """

    def __init__(self, text, font, pos, color=(255, 255, 255, 255), background_color=None, *groups):
        super().__init__(font.render(str(text), True, color, background_color), pos, *groups)
        self.set_alpha(pygame.color.Color(color).a)
        self.text = text
        self.str_text = str(self.text)
        self.font: pygame.font.Font = font
        self.color = color
        self.background_color = background_color
        self.pos = pos

    def set_text(self, text):
        """
        Changes the displayed text
        Args:
        text (str | MutableObject): The new text to display, if is an instance of the MutableObject (or any subclass) the text will update automatically
        """
        self.text = text
        self.str_text = str(self.text)
        self.set_surface(self.font.render(str(self.text), True, self.color, self.background_color))

    def set_colors(self, color=(255, 255, 255, 255), background_color=None):
        """
        Changes the colors of the text. Both colors can be changed at the same time,or only the text's color or only the background color
        Args:
            color (tuple[int, int, int] | tuple[int, int, int, int] | list[int, int, int] | list[int, int, int, int] | pygame.color.Color): The color of the text (r,g,b,a)
            background_color (tuple[int, int, int]| list[int, int, int] | pygame.color.Color): The color of the background of the text (r,g,b)

        Returns:

        """
        self.set_surface(self.font.render(self.text, True, color, background_color))
        self.set_alpha(pygame.color.Color(color).a)
        self.color = color
        self.background_color = background_color

    def update(self):
        if self.str_text != str(self.text):
            self.set_text(self.text)


class Rectangle(Sprite):
    """
    A class representing a rectangle that can be displayed on screen
    Args:
        pos (Vector2 | tuple[int, int] | list[int, int]): The center position of the rectangle
        size (Vector2 | tuple[int, int] | list[int, int]): The size of the rectangle (w*h)
        inside_color (tuple[int, int, int] | tuple[int, int, int, int] | list[int, int, int] | list[int, int, int, int] | pygame.color.Color): The color of the inside of the rectangle (r,g,b,a)
        outline_color (tuple[int, int, int] | tuple[int, int, int, int] | list[int, int, int] | list[int, int, int, int] | pygame.color.Color): The color of the outline of the rectangle (r,g,b,a)
        outline_width (int) : The width of the outline
    Raises:
        pygame.error: If a coordinate of the size is below 0
    """

    def __init__(self, pos, size, inside_color=(255, 255, 255, 0), outline_color=(255, 255, 255, 0), outline_width=1, *groups):
        super().__init__(pygame.Surface(size, pygame.SRCALPHA), pos, *groups)
        self.size = size
        self.pos = pos
        self.inside_color = inside_color
        self.outline_color = outline_color
        self.outline_width = outline_width
        pygame.draw.rect(self.image, inside_color, pygame.Rect((0, 0), size), max(size[0], size[1]) * 2)
        pygame.draw.rect(self.image, outline_color, pygame.Rect((0, 0), size), outline_width)

    def set_size(self, size):
        """
        Set the size of the rectangle
        Args:
            size (Vector2 | tuple[int, int] | list [int, int]): The size of the rectangle
        Raises:
            pygame.error: If a coordinate of the size is below 0
        """
        self.size = size
        self.image = pygame.Surface(self.size, pygame.SRCALPHA)
        pygame.draw.rect(self.image, self.inside_color, pygame.Rect((0, 0), size), max(size[0], size[1]) * 2)
        pygame.draw.rect(self.image, self.outline_color, pygame.Rect((0, 0), size), self.outline_width)
        self.rect = self.image.get_rect(center=self.pos)
        self.update_group()

    def set_colors(self, inside_color, outline_color, outline_width=1):
        """
        Set the colors of the rectangle
        Args:
            inside_color (tuple[int, int, int] | tuple[int, int, int, int] | list[int, int, int] | list[int, int, int, int] | pygame.color.Color): The new color of the inside of the rectangle (r,g,b,a)
            outline_color (tuple[int, int, int] | tuple[int, int, int, int] | list[int, int, int] | list[int, int, int, int] | pygame.color.Color): The new color of the outline of the rectangle (r,g,b,a)
            outline_width (int) : The new width of the outline
        """
        self.inside_color = inside_color
        self.outline_color = outline_color
        self.outline_width = outline_width

        pygame.draw.rect(self.image, self.inside_color, pygame.Rect((0, 0), self.size), max(self.size[0], self.size[1]) * 2)
        pygame.draw.rect(self.image, self.outline_color, pygame.Rect((0, 0), self.size), self.outline_width)


class Group:
    """
    The base class of all Groups
    Args:
        elements (tuple[Image | Text | Rectangle, ...]): The list of UIElements present in the group
    Attributes:
        pos (Vector2 | tuple[int, int] | list[int, int]): The position of the center of the group
    """

    def __init__(self, pos, elements, *groups, set_pos=True):
        self.elements: list[Image | Text | Rectangle] = list(elements)
        self.pos = Vector2(pos)
        self.group = None

        self.total_width = 0
        self.total_height = 0
        self.elements_heights = [elem.rect.h for elem in self.elements]
        self.elements_widths = [elem.rect.w for elem in self.elements]
        for elem in self.elements:
            elem.add(*groups)
            self.total_width += elem.get_rect().width
            self.total_height += elem.get_rect().height
            elem.set_group(self)

        self.rect: pygame.Rect = pygame.Rect(pos, (max(self.elements_widths), max(self.elements_heights)))

        if set_pos:
            for element in self.elements:
                element.set_pos(self.pos)

        self.image = pygame.surface.Surface(self.get_rect().size, pygame.SRCALPHA)
        for elem in self.elements:
            self.image.blit(elem.image, elem.pos)

    def move(self, delta_pos):
        """
        Move each element of the group by *delta_pos*
        Args:
            delta_pos (tuple[int, int]| list[int, int] | Vector2): The amount of pixels to move the sprite
        """
        for element in self.elements:
            element.move(delta_pos)

    def set_pos(self, new_pos):
        """
        Changes the center position of the group to *new_pos*
        Args:
            new_pos (tuple[int, int]| list[int, int] | Vector2): The new center of the group
        """
        delta_pos = Vector2(self.pos) - Vector2(new_pos)
        for element in self.elements:
            element.move(delta_pos)

    def set_alpha(self, alpha):
        """
        Changes the alpha of each element of the group
        Args:
            alpha (int): The new alpha of the sprite, should be a value between 0 and 255. Values between 0 will do the same as 0, values above 255 will do the same as 255
        """
        for element in self.elements:
            element.set_alpha(alpha)

    def add(self, *groups):
        """
        Adds each element of the group to *groups*
        Args:
            *groups (): The list of groups that the elements will be added to
        """
        for element in self.elements:
            element.add(*groups)

    def get_rect(self):
        """
        Returns the rect of the group
        Returns:
            (pygame.Rect) The rect
        """
        return self.rect

    def kill(self):
        """
        Kills each element of the group and thus kills the group
        """
        for element in self.elements:
            element.kill()

    def set_group(self, new_group):
        """
        Sets the group of the group and of all the elements of it to *new_group*
        Args:
            new_group (Group | HorizontalGroup | VerticalGroup): The new group
        """
        self.group = new_group
        for element in self.elements:
            element.set_group(self.group)

    def get_group(self):
        """
        Returns the group of the group
        Returns:
            (Group | HorizontalGroup | VerticalGroup): The group of the group. Returns *None* if the group isn't in any group
        """
        return self.group

    def update_pos(self):
        """
        Updates the position of the group, which allows to resize the rect of the group if the size of an element has changed
        """
        self.set_pos(self.pos)


class HorizontalGroup(Group):
    """
    A class representing a Horizontal Group which can be used to show elements in a horizontal way, stacked next to each other
    Args:
        pos (Vector2 | tuple[int, int] | list[int, int]): The position of the center of the group
        elements (tuple[Image | Text | Rectangle, ...]): The list of UIElements present in the group
        *groups (list[pygame.sprite.Group,...]): The list of all the groups that each element will belong to
        spacing (int): The spacing between each element, default is *0*
    """
    def __init__(self, pos, elements, *groups, spacing=0):
        self.num_elem = len(elements)
        self.spacing = spacing
        super().__init__(pos, elements, *groups, set_pos=False)

        self.total_width = 0
        self.rects_widths = []
        for elem in self.elements:
            elem.add(*groups)
            self.total_width += elem.get_rect().width
            self.rects_widths.append(elem.get_rect().width)

        self.total_width += (self.num_elem - 1) * self.spacing
        self.get_rect().width = self.total_width
        self.update_elements()

    def set_pos(self, new_pos):
        self.pos = Vector2(new_pos)

        self.update_elements()

    def update_pos(self):
        self.total_width = 0
        self.total_height = 0
        self.rects_widths = []
        for elem in self.elements:
            self.total_width += elem.get_rect().width
            self.total_height += elem.get_rect().height
            self.rects_widths.append(elem.get_rect().width)
            if hasattr(elem, "update_pos"):
                elem.update_pos()

        self.total_width += (self.num_elem - 1) * self.spacing

        self.rect: pygame.Rect = pygame.Rect(self.pos, (self.total_width, self.total_height))

        self.update_elements()

    def update_elements(self):
        """
        Moves each element of the group accordingly to their size
        """
        start_x = self.pos.x - self.total_width / 2
        for i_element in range(self.num_elem):
            self.elements[i_element].set_pos((int(start_x + sum(self.rects_widths[:i_element]) + i_element * self.spacing + self.elements[i_element].get_rect().width / 2), int(self.pos.y)))


class VerticalGroup(Group):
    """
    A class representing a Vertical Group which can be used to show elements in a vertical way, stacked on top of each other
    Args:
        pos (Vector2 | tuple[int, int] | list[int, int]): The position of the center of the group
        elements (tuple[Image | Text | Rectangle, ...]): The list of UIElements present in the group
        *groups (list[pygame.sprite.Group,...]): The list of all the groups that each element will belong to
        spacing (int): The spacing between each element, default is *0*
    """
    def __init__(self, pos, elements, *groups, spacing=0):
        self.num_elem = len(elements)
        self.spacing = spacing
        super().__init__(pos, elements, *groups, set_pos=False)

        self.total_height = 0
        self.rects_heights = []
        for elem in self.elements:
            elem.add(*groups)
            self.total_height += elem.get_rect().height
            self.rects_heights.append(elem.get_rect().height)
            if hasattr(elem, "update_pos"):
                elem.update_pos()

        self.total_height += (self.num_elem - 1) * self.spacing

        self.get_rect().height = self.total_height

        self.update_elements()

    def set_pos(self, new_pos):
        self.pos = Vector2(new_pos)

        self.update_elements()

    def update_pos(self):
        self.total_height = 0
        self.total_width = 0
        self.rects_heights = []
        for elem in self.elements:
            self.total_height += elem.get_rect().height
            self.total_width += elem.get_rect().width
            self.rects_heights.append(elem.get_rect().height)

        self.total_height += (self.num_elem - 1) * self.spacing

        self.rect: pygame.Rect = pygame.Rect(self.pos, (self.total_width, self.total_height))

        self.update_elements()

    def update_elements(self):
        """
        Moves each element of the group accordingly to their size
        """
        start_y = self.pos.y - self.total_height / 2
        for i_element in range(self.num_elem):
            self.elements[i_element].set_pos((int(self.pos.x), int(start_y + sum(self.rects_heights[:i_element]) + i_element * self.spacing + self.elements[i_element].get_rect().height / 2)))


class Button(Sprite):
    """
    A class that represents a button
    Args:
        pos (Vector2, tuple[int, int], list[int, int]): The center position of the button
        element (Sprite..., Group...): The element that is used as the button
        click_function (callable): The function that will be called when the button is clicked
        *groups (list[pygame.sprite.Group], ...): The groups that this button will belong to
    """
    def __init__(self, pos, element, click_function, *groups):
        super().__init__(element.image, pos, *groups)
        self.element = element
        self.click_function = click_function
        self.rect = self.element.rect
        self.rect.center = pos

    def is_clicked(self):
        """
        Checks if the button is clicked
        Returns:
            True if the cursor of the mouse is in the rect of the button
            False otherwise
        """
        return self.rect.collidepoint(pygame.mouse.get_pos())

    def update(self, **kwargs):
        """
        The update function of the button, it is used to test if the button is clicked if and only if the kwargs contains *click_update=False*
        It must be called if it is overriden by the user
        """
        if kwargs.get("click_update", False):
            if self.is_clicked():
                self.click_function(self)

    def move(self, delta_pos):
        super().move(delta_pos)
        self.element.move(delta_pos)
