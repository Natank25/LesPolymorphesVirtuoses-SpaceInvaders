import sys
from math import gcd

import pygame.transform

from classes import *

wanted_ratio = [8, 5]
win_size = GameConstants.default_win_size.copy()


pygame.init()

screen = pygame.display.set_mode((win_size[0], win_size[1]), pygame.RESIZABLE)

background = pygame.image.load(os.path.join("..", "img", "background.png")).convert()

background_rect = background.get_rect()


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

screen.blit(background, GameProperties.win_size.topleft)
pygame.display.set_caption("Space Invaders")

pygame.image.save(screen.copy(), "bg.png")
group_background = pygame.image.load("bg.png")

running = True

# EnemiesManager.list_enemies.append(CommonInvader1())
# EnemiesManager.list_enemies.append(SpeedInvader1())

player = Player([random.randint(GameProperties.win_size.x, GameProperties.win_size.width), GameProperties.win_size.height - 100], "vaisseau")

# EnemiesManager.send_waves_levels(1)

EnemiesManager.spawnEnemy(GameConstants.EnemyType.COMMONINVADER1)

"""
leave_game_button = Button("Quitter", GameProperties.win_size.x+200, GameProperties.win_size.y+200, 2, 1, "white", 'black',
                      50, screen, True)

play_level_button = Button("Mode Normal", GameProperties.win_size.x +100, GameProperties.win_size.y+100, 2, 1, "white", 'black',
                      50, screen, True)
"""

clock = pygame.time.Clock()
# screen.blit(bg, (0, 0))
while running:
    GameProperties.deltatime = clock.tick(200)

    EnemiesManager.update()

    GameConstants.AllSprites.clear(screen, group_background)
    GameConstants.AllSprites.draw(screen)
    GameConstants.AllSprites.update()

    title(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()


        elif event.type == pygame.WINDOWSIZECHANGED:
            prev_game_window = GameProperties.win_size.copy()
            update_game_win()
            screen.fill("black")
            screen.blit(pygame.transform.scale(background, GameProperties.win_size.size), GameProperties.win_size.topleft)

            pygame.image.save(screen.copy(), "bg.png")
            group_background = pygame.image.load("bg.png")

            GameConstants.AllSprites.moveSprites(GameProperties.win_size, prev_game_window)

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen

                prev_game_window = GameProperties.win_size.copy()

                if fullscreen:
                    pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
                else:
                    pygame.display.set_mode(prev_window_size, pygame.RESIZABLE)

                screen.fill("black")

            if event.key == pygame.K_SPACE:
                player.tirer()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pass
            #leave_game_button.check_click_quit()
            #play_level_button.check_click_level()

    pygame.display.flip()

pygame.quit()
