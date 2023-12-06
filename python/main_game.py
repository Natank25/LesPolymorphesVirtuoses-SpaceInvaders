import sys

from classes import *

aspect_ratio = (3, 4)

pygame.init()

'''
screen_height = pygame.display.Info().current_h
screen_width = int(screen_height / aspect_ratio[0] * aspect_ratio[1])
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

height, width = 400, 300
screen = pygame.display.set_mode((height, width), pygame.RESIZABLE)
bg = pygame.image.load('../img/pixel art bg.png').convert_alpha()
scale_bg = pygame.transform.scale(bg, (height, width))'''

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ASPECT_RATIO = 4 / 3
GAME_WIDTH = SCREEN_WIDTH
GAME_HEIGHT = int(GAME_WIDTH / ASPECT_RATIO)
BLACK = (0, 0, 0)
GameConstants.win_size = [SCREEN_WIDTH, SCREEN_HEIGHT]

# Create the Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)


fullscreen = False

pygame.display.set_caption("Space Invaders")

running = True

EnemiesManager.list_enemies.append(CommonInvader1())
EnemiesManager.list_enemies.append(SpeedInvader1())

player = Player([random.randint(0, GameConstants.win_size[0]), GameConstants.win_size[1] - 100], "vaisseau")

EnemiesManager.send_waves_levels(9)

# screen.blit(bg, (0, 0))
while running:

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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

            if event.key == pygame.K_SPACE:
                player.tirer()


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_q or event.key == pygame.K_d:
                player.setSpeed(GameConstants.PlayerSpeed.STOP)

    window_width, window_height = pygame.display.get_surface().get_size()

    # Calculate the position to center the game on the window
    game_x = (window_width - GAME_WIDTH) // 2
    game_y = (window_height - GAME_HEIGHT) // 2
    screen.fill(BLACK)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_q]:
        player.setSpeed(GameConstants.PlayerSpeed.LEFT)
    if keys[pygame.K_d]:
        player.setSpeed(GameConstants.PlayerSpeed.RIGHT)

    player.bouger()

    for enemy in EnemiesManager.list_enemies:
        enemy.avancer()
        screen.blit(enemy.image, (enemy.depart, enemy.hauteur))

    screen.blit(player.image, player.pos)

    pygame.display.update()

pygame.quit()
