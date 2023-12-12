import threading

from GameProperties import GameProperties
from Enemies import EnemyType

class EnemiesManager:

    @staticmethod
    def update():
        pass

    @staticmethod
    def send_waves_endless(difficulty: int):
        for i in range(difficulty * 3):
            pass

    @staticmethod
    def send_waves_levels(num_lvl: int):
        match num_lvl:
            case 1:
                for i in range(3 + GameProperties.difficulty):
                    EnemiesManager.spawnEnemy(EnemyType.COMMONINVADER1, 1500 * i)

            case 2:
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.spawnEnemy(EnemyType.COMMONINVADER1, 1500 * i)
                    EnemiesManager.spawnEnemy(EnemyType.SPEEDINVADER1, 3000 * i)

            case 3:
                for i in range(4 + GameProperties.difficulty):
                    EnemiesManager.spawnEnemy(EnemyType.COMMONINVADER1, 1500 * i)
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.spawnEnemy(EnemyType.SPEEDINVADER1, 3000 * i)

            case 4:
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.spawnEnemy(EnemyType.COMMONINVADER1, 1500 * i)
                    EnemiesManager.spawnEnemy(EnemyType.SPEEDINVADER1, 3000 * i)
            case 5:
                EnemiesManager.spawnEnemy(EnemyType.BOSS1)
            case 6:
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.spawnEnemy(EnemyType.COMMONINVADER1, 1500 * i)
                    EnemiesManager.spawnEnemy(EnemyType.SPEEDINVADER1, 3000 * i)
                    EnemiesManager.spawnEnemy(EnemyType.SPEEDINVADER2, 4500 * i)
            case 7:
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.spawnEnemy(EnemyType.COMMONINVADER1, 1500 * i)
                    EnemiesManager.spawnEnemy(EnemyType.SPEEDINVADER1, 3000 * i)
                    EnemiesManager.spawnEnemy(EnemyType.SPEEDINVADER2, 4500 * i)
            case 8:
                for i in range(4 + GameProperties.difficulty):
                    for j in range(2 + GameProperties.difficulty):
                        EnemiesManager.spawnEnemy(EnemyType.COMMONINVADER2, 1500 * i * j)
                        EnemiesManager.spawnEnemy(EnemyType.SPEEDINVADER2, 3000 * i * j)
                    EnemiesManager.spawnEnemy(EnemyType.TANKINVADER1, 4500 * i)
            case 9:
                for i in range(2 + GameProperties.difficulty):
                    for j in range(3 + GameProperties.difficulty):
                        EnemiesManager.spawnEnemy(EnemyType.COMMONINVADER2, 1500 * i * j)
                    EnemiesManager.spawnEnemy(EnemyType.SPEEDINVADER2, 3000 * i)
                    EnemiesManager.spawnEnemy(EnemyType.TANKINVADER1, 4500 * i)
            case 10:
                EnemiesManager.spawnEnemy(EnemyType.BOSS2)
            case 11:
                for i in range(2 + GameProperties.difficulty):
                    EnemiesManager.spawnEnemy(EnemyType.SPEEDINVADER2, 1500 * i)
                    EnemiesManager.spawnEnemy(EnemyType.TANKINVADER1, 3000 * i)
                    for j in range(3 + GameProperties.difficulty):
                        EnemiesManager.spawnEnemy(EnemyType.COMMONINVADER2, 1500 * i * j)
            case 12:
                for i in range(3 + GameProperties.difficulty):
                    for j in range(3 + GameProperties.difficulty):
                        EnemiesManager.spawnEnemy(EnemyType.SPEEDINVADER2, 1500 * i * j)
                        EnemiesManager.spawnEnemy(EnemyType.TANKINVADER1, 3000 * i * j)
                    EnemiesManager.spawnEnemy(EnemyType.SPEEDINVADER2, 1500 * i)
            case 13:
                pass
            case 14:
                pass
            case 15:
                EnemiesManager.spawnEnemy(EnemyType.BOSS3)
            case 16:
                pass
            case 17:
                pass
            case 18:
                pass
            case 19:
                pass
            case 20:
                EnemiesManager.spawnEnemy(EnemyType.BOSS4)
            case 21:
                pass
            case 22:
                pass
            case 23:
                pass
            case 24:
                pass
            case 25:
                EnemiesManager.spawnEnemy(EnemyType.BOSS5)
            case 26:
                pass
            case 27:
                pass
            case 28:
                pass
            case 29:
                pass
            case 30:
                EnemiesManager.spawnEnemy(EnemyType.BOSS6)
            case 31:
                pass
            case 32:
                pass
            case 33:
                pass
            case 34:
                pass
            case 35:
                EnemiesManager.spawnEnemy(EnemyType.BOSS7)
            case 36:
                pass
            case 37:
                pass
            case 39:
                pass
            case 40:
                EnemiesManager.spawnEnemy(EnemyType.BOSS8)
            case 41:
                pass
            case 42:
                pass
            case 43:
                pass
            case 44:
                pass
            case 45:
                EnemiesManager.spawnEnemy(EnemyType.BOSS9)
            case 46:
                pass
            case 47:
                pass
            case 48:
                pass
            case 49:
                pass
            case 50:
                EnemiesManager.spawnEnemy(EnemyType.BOSS10)
            case 51:
                pass
            case 52:
                pass
            case 53:
                pass
            case 54:
                pass
            case 55:
                EnemiesManager.spawnEnemy(EnemyType.BOSS11)
            case 56:
                pass
            case 57:
                pass
            case 58:
                pass
            case 59:
                pass
            case 60:
                EnemiesManager.spawnEnemy(EnemyType.BOSS12)
            case 61:
                pass
            case 62:
                pass
            case 63:
                pass
            case 64:
                pass
            case 65:
                EnemiesManager.spawnEnemy(EnemyType.BOSS13)
            case 66:
                pass
            case 67:
                pass
            case 68:
                pass
            case 69:
                pass
            case 70:
                EnemiesManager.spawnEnemy(EnemyType.BOSS14)
            case 71:
                pass
            case 72:
                pass
            case 73:
                pass
            case 74:
                pass
            case 75:
                EnemiesManager.spawnEnemy(EnemyType.BOSS15)
            case 76:
                pass
            case 77:
                pass
            case 78:
                pass
            case 79:
                pass
            case 80:
                EnemiesManager.spawnEnemy(EnemyType.BOSS16)
            case 81:
                pass
            case 82:
                pass
            case 83:
                pass
            case 84:
                pass
            case 85:
                EnemiesManager.spawnEnemy(EnemyType.BOSS17)
            case 86:
                pass
            case 87:
                pass
            case 88:
                pass
            case 89:
                pass
            case 90:
                EnemiesManager.spawnEnemy(EnemyType.BOSS18)
            case 91:
                pass
            case 92:
                pass
            case 93:
                pass
            case 94:
                pass
            case 95:
                EnemiesManager.spawnEnemy(EnemyType.BOSS19)
            case 96:
                pass
            case 97:
                pass
            case 98:
                pass
            case 99:
                pass
            case 100:
                EnemiesManager.spawnEnemy(EnemyType.BOSS20)

    @staticmethod
    def spawnEnemy(enemy_type: EnemyType, delay: float = None):
        if delay is None:
            enemy_type.enemy_class()
        else:
            thread = threading.Timer(delay / 1000, lambda: EnemiesManager.spawnEnemy(enemy_type))
            GameProperties.on_going_threads.append(thread)
            thread.start()
