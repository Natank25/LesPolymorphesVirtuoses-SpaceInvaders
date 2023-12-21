import pygame

print(27, pygame.time.get_ticks())
from python import GameProperties
print(28, pygame.time.get_ticks())

pygame.init()


class AllSprites(pygame.sprite.RenderClear):
    def __init__(self, *sprites):
        super().__init__(*sprites)

    def moveSprites(self, current_window: pygame.rect.Rect, prev_window: pygame.rect.Rect):
        scale_x = current_window.width / prev_window.width
        scale_y = current_window.height / prev_window.height

        GameProperties.win_scale = current_window.width / GameProperties.default_win_size[0]

        for sprite in self.sprites():

            if hasattr(sprite, 'image_path'):
                sprite.image = pygame.transform.scale_by(pygame.image.load(sprite.image_path), scale_x)
            else:
                sprite.image = pygame.transform.scale_by(sprite.image, scale_x)

            new_x = int((sprite.rect.x - prev_window.x) * scale_x + current_window.x)
            new_y = int((sprite.rect.y - prev_window.y) * scale_y + current_window.y)

            sprite.rect = sprite.image.get_rect(topleft=(new_x, new_y))


class UIGroup(AllSprites):
    def __init__(self, *sprites):
        super().__init__(*sprites)


AllSpritesGroup: AllSprites = AllSprites()
InvaderGroup: pygame.sprite.RenderClear = pygame.sprite.RenderClear()
PlayerGroup: pygame.sprite.RenderClear = pygame.sprite.RenderClear()
BulletGroup: pygame.sprite.RenderClear = pygame.sprite.RenderClear()
EnemiesBulletGroup: pygame.sprite.RenderClear = pygame.sprite.RenderClear()
ButtonGroup: pygame.sprite.RenderClear = pygame.sprite.RenderClear()
UIGroup: UIGroup = UIGroup()