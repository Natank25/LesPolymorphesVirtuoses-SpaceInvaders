import sys
from math import gcd
import pygame
from python import Resources

print(1,pygame.time.get_ticks())

from python import Groups
print(2,pygame.time.get_ticks())
from python import EnemiesManager
print(3,pygame.time.get_ticks())
from python import GameProperties
print(4,pygame.time.get_ticks())
from python.Player import Player
print(5,pygame.time.get_ticks())
from python import UIManager
print(6,pygame.time.get_ticks())

wanted_ratio = [8, 5]
win_size = GameProperties.default_win_size.copy()


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

# UIManager.show_game()
UIManager.show_starting_screen()
clock = pygame.time.Clock()
while running:

    UIManager.update()
    EnemiesManager.update()

    GameProperties.deltatime = clock.tick(60)

    Groups.AllSpritesGroup.clear(GameProperties.screen, GameProperties.group_background)
    Groups.UIGroup.clear(GameProperties.screen, GameProperties.group_background)

    if not GameProperties.paused:
        Groups.AllSpritesGroup.draw(GameProperties.screen)
        Groups.AllSpritesGroup.update()

    Groups.UIGroup.draw(GameProperties.screen)
    Groups.UIGroup.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.WINDOWSIZECHANGED:
            prev_game_window = GameProperties.win_size.copy()
            update_game_win()
            GameProperties.screen.fill("black")
            GameProperties.screen.blit(pygame.transform.scale(GameProperties.background, GameProperties.win_size.size), GameProperties.win_size.topleft)

            """pygame.image.save(GameProperties.screen.copy(), "bg.png")
            GameProperties.group_background = pygame.image.load("bg.png")"""
            GameProperties.group_background = GameProperties.screen.copy()

            Groups.AllSpritesGroup.moveSprites(GameProperties.win_size, prev_game_window)
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

            if event.key == pygame.K_ESCAPE:
                GameProperties.paused = not GameProperties.paused
                if GameProperties.paused:
                    UIManager.show_pause()
                else:
                    UIManager.resume_game()

            elif event.key == pygame.K_m:
                EnemiesManager.spawn_current_wave()
            elif event.key == pygame.K_p:
                EnemiesManager.kill_all()
            elif event.key == pygame.K_EXCLAIM:
                GameProperties.coins += 99999**9
            elif event.key == pygame.K_COLON:
                GameProperties.gems += 100
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                Groups.ButtonGroup.update(button_group_update=True)

    if GameProperties.game_overed:
        Resources.Ennemies.Sons.PlayerDeathSound.play()
        UIManager.show_game_over()
        GameProperties.game_overed = False

    pygame.display.flip()


pygame.quit()
sys.exit()
