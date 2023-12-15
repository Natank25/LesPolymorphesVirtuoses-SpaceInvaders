import pygame

from python.GameProperties import GameProperties

pygame.init()


class AllSpritesGroup(pygame.sprite.RenderClear):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def moveSprites(self, current_window: pygame.rect.Rect, prev_window: pygame.rect.Rect):
        scale_x = current_window.width / prev_window.width
        scale_y = current_window.height / prev_window.height

        GameProperties.win_scale = current_window.width / GameProperties.default_win_size[0]

        for sprite in self.sprites():

            if hasattr(sprite, 'image_path'):
                sprite.image = pygame.transform.scale(pygame.image.load(sprite.image_path), (
                    int(scale_x * sprite.image.get_width()), int(scale_y * sprite.image.get_height())))
            else:
                sprite.image = pygame.transform.scale(sprite.image, (
                    int(scale_x * sprite.image.get_width()), int(scale_y * sprite.image.get_height())))

            new_x = int((sprite.rect.x - prev_window.x) * scale_x + current_window.x)
            new_y = int((sprite.rect.y - prev_window.y) * scale_y + current_window.y)

            sprite.rect = sprite.image.get_rect(topleft=(new_x, new_y))


class UIGroup(AllSpritesGroup):
    def __init__(self, *sprites):
        super().__init__(*sprites)


class Groups:

    AllSprites: AllSpritesGroup = AllSpritesGroup()
    InvaderGroup: pygame.sprite.RenderClear = pygame.sprite.RenderClear()
    PlayerGroup: pygame.sprite.RenderClear = pygame.sprite.RenderClear()
    BulletGroup: pygame.sprite.RenderClear = pygame.sprite.RenderClear()
    ButtonGroup: pygame.sprite.RenderClear = pygame.sprite.RenderClear()
    UIGroup: UIGroup = UIGroup()
