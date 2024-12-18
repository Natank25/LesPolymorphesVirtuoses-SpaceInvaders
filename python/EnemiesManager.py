import random
from random import randint

import pygame.time

from Enemies import EnemyType
from python import GameProperties
from python import Groups
from python import UIManager

next_spawns = []

on_going_wave = False


def send_waves_endless(difficulty: int):
    for i in range(difficulty * 3):
        pass


def send_waves_levels(num_wave):
    UIManager.Game.waves_text()
    match num_wave:
        case 1:
            for i in range(3 + GameProperties.difficulty):
                spawnEnemy(EnemyType.COMMONINVADER1, 1500 * i)

        case 2:
            for i in range(2 + GameProperties.difficulty):
                spawnEnemy(EnemyType.COMMONINVADER1, 1500 * i)
                spawnEnemy(EnemyType.SPEEDINVADER1, 3000 * i)

        case 3:
            for i in range(4 + GameProperties.difficulty):
                spawnEnemy(EnemyType.COMMONINVADER1, 1500 * i)
            for i in range(2 + GameProperties.difficulty):
                spawnEnemy(EnemyType.SPEEDINVADER1, 3000 * i)

        case 4:
            for i in range(2 + GameProperties.difficulty):
                spawnEnemy(EnemyType.COMMONINVADER1, 1500 * i)
                spawnEnemy(EnemyType.SPEEDINVADER1, 3000 * i)
            spawnEnemy(EnemyType.SHOOTERINVADER1, 6500)

        case 5:
            spawnEnemy(EnemyType.BOSS1)

        case 6:
            pygame.mixer.music.stop()
            for i in range(2 + GameProperties.difficulty):
                spawnEnemy(EnemyType.COMMONINVADER1, 1500 * i)
                spawnEnemy(EnemyType.SPEEDINVADER1, 3000 * i)
                spawnEnemy(EnemyType.SHOOTERINVADER1, 3500 * i)
            spawnEnemy(EnemyType.COMMONINVADER2, 4500)

        case 7:
            for i in range(2 + GameProperties.difficulty):
                spawnEnemy(EnemyType.COMMONINVADER1, 1500 * i)
                spawnEnemy(EnemyType.SPEEDINVADER1, 3000 * i)
                spawnEnemy(EnemyType.COMMONINVADER2, 4500 * i)
                spawnEnemy(EnemyType.SHOOTERINVADER1, 3500 * i)
            spawnEnemy(EnemyType.SPEEDINVADER2, 10000)

        case 8:
            for i in range(2 + GameProperties.difficulty):
                for j in range(2 + GameProperties.difficulty):
                    spawnEnemy(EnemyType.COMMONINVADER2, 1500 * (i + 1) * j)
                    spawnEnemy(EnemyType.SPEEDINVADER2, 2500 * (i + 1) * j)
                    spawnEnemy(EnemyType.SHOOTERINVADER1, 3500 * (i + 1) * j)
                spawnEnemy(EnemyType.TANKINVADER1, 5500 * i)

        case 9:
            for i in range(4 + GameProperties.difficulty):
                for j in range(3 + GameProperties.difficulty):
                    spawnEnemy(EnemyType.COMMONINVADER2, 2500 * (i + 1) * j)
                    spawnEnemy(EnemyType.SPEEDINVADER2, 4000 * (i + 1) * j)
                    spawnEnemy(EnemyType.SHOOTERINVADER1, 3500 * (i + 1) * j)
                spawnEnemy(EnemyType.TANKINVADER1, 6000 * i)

        case 10:
            pass

        case 11:
            pygame.mixer.music.stop()
            for i in range(2 + GameProperties.difficulty):
                spawnEnemy(EnemyType.SPEEDINVADER2, 2500 * i)
                spawnEnemy(EnemyType.TANKINVADER1, 5000 * i)
                spawnEnemy(EnemyType.SHOOTERINVADER2, 5500 * i)
                for j in range(3 + GameProperties.difficulty):
                    spawnEnemy(EnemyType.COMMONINVADER2, 1500 * (i + 1) * j)

        case 12:
            for i in range(3 + GameProperties.difficulty):
                for j in range(3 + GameProperties.difficulty):
                    spawnEnemy(EnemyType.COMMONINVADER2, 1500 * (i + 1) * j)
                    spawnEnemy(EnemyType.TANKINVADER1, 3000 * (i + 1) * j)
                spawnEnemy(EnemyType.SPEEDINVADER2, 5000 * i)
                spawnEnemy(EnemyType.SHOOTERINVADER2, 3500 * i)

        case 13:
            for i in range(2 + GameProperties.difficulty):
                spawnEnemy(EnemyType.COMMONINVADER3, 10000 * i)
                for j in range(3 + GameProperties.difficulty):
                    spawnEnemy(EnemyType.TANKINVADER1, 4000 * (i + 1) * j)
                    spawnEnemy(EnemyType.SPEEDINVADER2, 6000 * (i + 1) * j)
                    spawnEnemy(EnemyType.SHOOTERINVADER2, 5000 * (i + 1) * j)
                    for k in range(2 + GameProperties.difficulty):
                        spawnEnemy(EnemyType.COMMONINVADER2, 3000 * (i + 1) * (j + 1) * k)

        case 14:
            for i in range(2 + GameProperties.difficulty):
                spawnEnemy(EnemyType.COMMONINVADER3, 7500 * i)
                for j in range(3 + GameProperties.difficulty):
                    spawnEnemy(EnemyType.TANKINVADER1, 4500 * (i + 1) * j)
                    spawnEnemy(EnemyType.SPEEDINVADER2, 4000 * (i + 1) * j)
                    spawnEnemy(EnemyType.SHOOTERINVADER2, 5000 * (i + 1) * j)
                    for k in range(3 + GameProperties.difficulty):
                        spawnEnemy(EnemyType.COMMONINVADER2, 1500 * (i + 1) * (j + 1) * k)

        case 15:
            spawnEnemy(EnemyType.BOSS3)

        case 16:
            for i in range(3 + GameProperties.difficulty):
                spawnEnemy(EnemyType.COMMONINVADER3, 7500 * i)
                for j in range(2 + GameProperties.difficulty):
                    spawnEnemy(EnemyType.SHOOTERINVADER2, 5000 * (i + 1) * j)
                    spawnEnemy(EnemyType.TANKINVADER1, 4500 * (i + 1) * j)
                    for k in range(2 + GameProperties.difficulty):
                        spawnEnemy(EnemyType.SPEEDINVADER2, 3500 * (i + 1) * (j + 1) * k)

        case 17:
            for i in range(2 + GameProperties.difficulty):
                spawnEnemy(EnemyType.SPEEDINVADER3, 8000 * i)
                for j in range(2 + GameProperties.difficulty):
                    spawnEnemy(EnemyType.COMMONINVADER3, 5000 * (i + 1) * j)
                    spawnEnemy(EnemyType.TANKINVADER1, 4500 * (i + 1) * j)
                    for k in range(2 + GameProperties.difficulty):
                        spawnEnemy(EnemyType.SHOOTERINVADER2, 3500 * (i + 1) * (j + 1) * k)
            spawnEnemy(EnemyType.TANKINVADER2, 10000)

        case 18:
            pass

        case 19:
            pass

        case 20:
            spawnEnemy(EnemyType.BOSS4)

        case 21:
            pass

        case 22:
            pass

        case 23:
            pass

        case 24:
            pass

        case 25:
            spawnEnemy(EnemyType.BOSS5)

        case 26:
            pass

        case 27:
            pass

        case 28:
            pass

        case 29:
            pass

        case 30:
            spawnEnemy(EnemyType.BOSS6)

        case 31:
            pass

        case 32:
            pass

        case 33:
            pass

        case 34:
            pass

        case 35:
            spawnEnemy(EnemyType.BOSS7)

        case 36:
            pass

        case 37:
            pass

        case 39:
            pass

        case 40:
            spawnEnemy(EnemyType.BOSS8)

        case 41:
            pass

        case 42:
            pass

        case 43:
            pass

        case 44:
            pass

        case 45:
            spawnEnemy(EnemyType.BOSS9)

        case 46:
            pass

        case 47:
            pass

        case 48:
            pass

        case 49:
            pass

        case 50:
            spawnEnemy(EnemyType.BOSS10)

        case 51:
            pass

        case 52:
            pass

        case 53:
            pass

        case 54:
            pass

        case 55:
            spawnEnemy(EnemyType.BOSS11)

        case 56:
            pass

        case 57:
            pass

        case 58:
            pass

        case 59:
            pass

        case 60:
            spawnEnemy(EnemyType.BOSS12)

        case 61:
            pass

        case 62:
            pass

        case 63:
            pass

        case 64:
            pass

        case 65:
            spawnEnemy(EnemyType.BOSS13)

        case 66:
            pass

        case 67:
            pass

        case 68:
            pass

        case 69:
            pass

        case 70:
            spawnEnemy(EnemyType.BOSS14)

        case 71:
            pass

        case 72:
            pass

        case 73:
            pass

        case 74:
            pass

        case 75:
            spawnEnemy(EnemyType.BOSS15)

        case 76:
            pass

        case 77:
            pass

        case 78:
            pass

        case 79:
            pass

        case 80:
            spawnEnemy(EnemyType.BOSS16)

        case 81:
            pass

        case 82:
            pass

        case 83:
            pass

        case 84:
            pass

        case 85:
            spawnEnemy(EnemyType.BOSS17)

        case 86:
            pass

        case 87:
            pass

        case 88:
            pass

        case 89:
            pass

        case 90:
            spawnEnemy(EnemyType.BOSS18)

        case 91:
            pass

        case 92:
            pass

        case 93:
            pass

        case 94:
            pass

        case 95:
            spawnEnemy(EnemyType.BOSS19)

        case 96:
            pass

        case 97:
            pass

        case 98:
            pass

        case 99:
            pass

        case 100:
            spawnEnemy(EnemyType.BOSS20)


def spawnEnemy(enemy_type: EnemyType, delay: float = None):
    if delay is None or delay <= 0:
        enemy_type.enemy_class()
    else:
        new_delay = randint(-2500, 2500)

        if 500 > new_delay > -500:
            new_delay = random.choice([-500, 500])
            new_delay += randint(-100, 100)

        next_spawns.append({enemy_type: delay + pygame.time.get_ticks() + new_delay})


def update():
    global on_going_wave
    on_going_wave = len(next_spawns) != 0

    for i_dict in range(len(next_spawns) - 1, -1, -1):
        for enemy_type, delay in next_spawns[i_dict].items():
            if GameProperties.paused:
                next_spawns[i_dict][enemy_type] += int(GameProperties.deltatime)

            if delay <= pygame.time.get_ticks():
                next_spawns.pop(i_dict)
                spawnEnemy(enemy_type)


def spawn_current_wave():
    for next_spawn in next_spawns:
        for enemy_type, delay in next_spawn.items():
            spawnEnemy(enemy_type)
    next_spawns.clear()


def kill_all():
    for invader in Groups.InvaderGroup.sprites():
        if hasattr(invader, "coin_drop"):
            GameProperties.coins += invader.coin_drop
        invader.kill()
