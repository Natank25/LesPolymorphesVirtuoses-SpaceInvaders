import pygame.sprite

from python import Groups
from python import GameProperties


class Sprite(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups, Groups.AllSpritesGroup)

    def update(self, *args, **kwargs):
        if self.rect.top > GameProperties.win_size.height + GameProperties.win_size.y:
            self.kill()

    def kill(self):
        super().kill()
        del self
