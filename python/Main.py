import os
import sys
from math import gcd

import pygame.transform

from python import EnemiesSpawner
from python.Groups import *
from python.UIManager import UIManager

wanted_ratio = [8, 5]
win_size = GameProperties.default_win_size.copy()

os.chdir(os.path.dirname(os.path.abspath(__file__)))

pygame.init()

GameProperties.screen = pygame.display.set_mode((win_size[0], win_size[1]), pygame.RESIZABLE)

background_rect = GameProperties.background.get_rect()



def update_game_win() -> list:
    win_size = [pygame.display.get_window_size()[0], pygame.display.get_window_size()[1]]

    ratio = [win_size[0], win_size[1]]
    g = gcd(win_size[0], win_size[1])
    if ratio[1] < 0:
        g = -g
    ratio[0] //= g
    ratio[1] //= g

    game_win_size = [0, 0]

    part_filled_1 = []

    if ratio[0] * wanted_ratio[0] == ratio[1] * wanted_ratio[1]:
        game_win_size = [win_size[0], win_size[1]]
        part_filled_1 = [0, 0, game_win_size[0], game_win_size[1]]

    elif ratio[0] * wanted_ratio[0] < ratio[1] * wanted_ratio[1]:
        game_win_size[0] = win_size[0]
        game_win_size[1] = int(game_win_size[0] * wanted_ratio[0] / wanted_ratio[1])

        part_filled_1 = [0, (win_size[1] / 2) - (game_win_size[1] / 2), game_win_size[0], game_win_size[1]]

    elif ratio[0] * wanted_ratio[0] > ratio[1] * wanted_ratio[1]:
        game_win_size[1] = win_size[1]
        game_win_size[0] = int(game_win_size[1] * wanted_ratio[1] / wanted_ratio[0])

        part_filled_1 = [(win_size[0] / 2) - (game_win_size[0] / 2), 0, game_win_size[0], game_win_size[1]]

    GameProperties.win_size = pygame.Rect(part_filled_1)

    return part_filled_1


fullscreen = False

prev_window_size = pygame.display.get_window_size()

update_game_win()

GameProperties.screen.blit(GameProperties.background, GameProperties.win_size.topleft)
pygame.display.set_caption("Space Invaders")

running = True

UIManager.show_starting_screen()

clock = pygame.time.Clock()
# screen.blit(bg, (0, 0))
while running:

    UIManager.update()

    GameProperties.deltatime = clock.tick(60)

    Groups.AllSprites.clear(GameProperties.screen, GameProperties.group_background)
    Groups.AllSprites.draw(GameProperties.screen)
    Groups.AllSprites.update()
    Groups.UIGroup.draw(GameProperties.screen)

    # GameProperties.screen.fill("black", GameProperties.screen_mask.)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.WINDOWSIZECHANGED:
            prev_game_window = GameProperties.win_size.copy()
            update_game_win()
            GameProperties.screen.fill("black")
            GameProperties.screen.blit(pygame.transform.scale(GameProperties.background, GameProperties.win_size.size),
                                       GameProperties.win_size.topleft)

            pygame.image.save(GameProperties.screen.copy(), "bg.png")
            GameProperties.group_background = pygame.image.load("bg.png")

            Groups.AllSprites.moveSprites(GameProperties.win_size, prev_game_window)
            Groups.UIGroup.moveSprites(GameProperties.win_size, prev_game_window)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen

                prev_game_window = GameProperties.win_size.copy()

                if fullscreen:
                    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    pygame.display.set_mode(prev_window_size, pygame.RESIZABLE)

                GameProperties.screen.fill("black")
        elif event.type == pygame.MOUSEBUTTONDOWN:
            Groups.ButtonGroup.update()

    if GameProperties.game_started and len(Groups.InvaderGroup.sprites()) == 0:
        GameProperties.current_wave += 1
        EnemiesSpawner.EnemiesManager.send_waves_levels(GameProperties.current_wave)

    for sprite in Groups.AllSprites.sprites():
        if sprite.rect.x < GameProperties.win_size.height + GameProperties.win_size.y:
            Groups.AllSprites.remove(sprite)
            sprite.kill()

    pygame.display.flip()

for on_going_thread in GameProperties.on_going_threads:
    on_going_thread.cancel()

pygame.quit()
sys.exit()
