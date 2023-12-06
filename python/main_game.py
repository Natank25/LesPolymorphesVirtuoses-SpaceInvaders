import sys
from math import gcd

import pygame

from classes import *

wanted_ratio = [8, 5]
win_size = [random.randint(150, 1440), random.randint(150, 1440)]
win_size = [800, 800]

pygame.init()

screen = pygame.display.set_mode((win_size[0], win_size[1]), pygame.RESIZABLE)

running = True


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
        game_win_size[1] = game_win_size[0] * wanted_ratio[0] / wanted_ratio[1]

        part_filled_1 = [0, (win_size[1] / 2) - (game_win_size[1] / 2), game_win_size[0], game_win_size[1]]

    elif ratio[0] * wanted_ratio[0] > ratio[1] * wanted_ratio[1]:
        game_win_size[1] = win_size[1]
        game_win_size[0] = game_win_size[1] * wanted_ratio[1] / wanted_ratio[0]

        part_filled_1 = [(win_size[0] / 2) - (game_win_size[0] / 2), 0, game_win_size[0], game_win_size[1]]

    GameProperties.win_size = pygame.Rect(part_filled_1)
    return part_filled_1


fullscreen = False


prev_window_size = pygame.display.get_window_size()

screen.fill("orange", rect=update_game_win())

pygame.display.set_caption("Space Invaders")

running = True

EnemiesManager.list_enemies.append(CommonInvader1())
# EnemiesManager.list_enemies.append(SpeedInvader1())

player = Player([random.randint(0, GameProperties.win_size[0]), GameProperties.win_size[1] - 100], "vaisseau")

EnemiesManager.send_waves_levels(1)

# screen.blit(bg, (0, 0))
while running:

    EnemiesManager.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()

        if event.type == GameConstants.GameEvents.CommonInvader1SpawnEvent.value:
            EnemiesManager.spawnEnemy(GameConstants.EnemyType.COMMONINVADER1)
        if event.type == GameConstants.GameEvents.CommonInvader2SpawnEvent.value:
            EnemiesManager.spawnEnemy(GameConstants.EnemyType.COMMONINVADER2)
        if event.type == GameConstants.GameEvents.SpeedInvader1SpawnEvent.value:
            EnemiesManager.spawnEnemy(GameConstants.EnemyType.SPEEDINVADER1)
        if event.type == GameConstants.GameEvents.SpeedInvader2SpawnEvent.value:
            EnemiesManager.spawnEnemy(GameConstants.EnemyType.SPEEDINVADER2)
        if event.type == GameConstants.GameEvents.TankInvader1SpawnEvent.value:
            EnemiesManager.spawnEnemy(GameConstants.EnemyType.TANKINVADER1.value)

        elif event.type == pygame.WINDOWSIZECHANGED:
            screen.fill("orange", rect=update_game_win())

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    prev_window_size = pygame.display.get_window_size()
                    pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN)
                else:
                    pygame.display.set_mode(prev_window_size, pygame.RESIZABLE)

            if event.key == pygame.K_SPACE:
                player.tirer()


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_q or event.key == pygame.K_d:
                player.setSpeed(GameConstants.PlayerSpeed.STOP)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        player.setSpeed(GameConstants.PlayerSpeed.LEFT)
    if keys[pygame.K_d]:
        player.setSpeed(GameConstants.PlayerSpeed.RIGHT)

    player.bouger()

    screen.blit(player.image, player.pos)

    pygame.display.update()

pygame.quit()
