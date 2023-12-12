from math import gcd

import pygame.transform

from classes import *

wanted_ratio = [8, 5]
win_size = GameConstants.default_win_size.copy()

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

UI.show_menu()


clock = pygame.time.Clock()
# screen.blit(bg, (0, 0))
while running:

    GameProperties.deltatime = clock.tick(60)

    GameProperties.AllSprites.clear(GameProperties.screen, GameProperties.group_background)
    GameProperties.AllSprites.draw(GameProperties.screen)
    GameProperties.AllSprites.update()
    GameProperties.UIGroup.draw(GameProperties.screen)

    # GameProperties.screen.fill("black", GameProperties.screen_mask.)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.WINDOWSIZECHANGED:
            prev_game_window = GameProperties.win_size.copy()
            update_game_win()
            GameProperties.screen.fill("black")
            GameProperties.screen.blit(pygame.transform.scale(GameProperties.background, GameProperties.win_size.size), GameProperties.win_size.topleft)

            pygame.image.save(GameProperties.screen.copy(), "bg.png")
            GameProperties.group_background = pygame.image.load("bg.png")

            GameProperties.AllSprites.moveSprites(GameProperties.win_size, prev_game_window)
            GameProperties.UIGroup.moveSprites(GameProperties.win_size, prev_game_window)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen

                prev_game_window = GameProperties.win_size.copy()

                if fullscreen:
                    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    pygame.display.set_mode(prev_window_size, pygame.RESIZABLE)

                GameProperties.screen.fill("black")
            if event.key == pygame.K_ESCAPE:
                UI.show_menu()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            GameProperties.ButtonGroup.update()

    pygame.display.flip()

for on_going_thread in GameProperties.on_going_threads:
    on_going_thread.cancel()
pygame.quit()
sys.exit()
