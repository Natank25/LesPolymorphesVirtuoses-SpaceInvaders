import json

from python import GameProperties
from python.Player import PlayerProperties


class DataManager:

    @staticmethod
    def save_game():
        with open("data.json", 'rt') as f:
            current_save = json.load(f)

        new_save = {
            "players": {
                "default_player": {
                    "gems": GameProperties.gems,
                    "coins": GameProperties.coins
                },
            },

            "game_properties": {
                "waves_game": {
                    "current_wave": GameProperties.current_wave
                },

                "difficulty": {
                    "current_difficulty": GameProperties.difficulty
                },
            },

            "shops": {
                "coins": {
                    "damage_upgrade": PlayerProperties.DAMAGE_UPGRADE,
                    "health_upagrade": PlayerProperties.HEALTH_UPGRADE
                },
                "gems": {
                    "unlocked_upgrade": []
                }
            }
        }

        current_save.update(new_save)

        with open("data.json", "wt") as f:
            f.write(json.dumps(current_save, indent=4, sort_keys=True))

    @staticmethod
    def get_players():
        with open("data.json", 'rt') as f:
            return json.load(f)["players"]

    @staticmethod
    def get_coins_player():
        with open("data.json", 'rt') as f:
            return json.load(f)["players"]["default_player"]["coins"]

    @staticmethod
    def get_gems_player():
        with open("data.json", 'rt') as f:
            return json.load(f)["players"]["default_player"]["gems"]

    @staticmethod
    def get_waves():
        with open("data.json", 'rt') as f:
            return json.load(f)["waves_game"]["current_wave"]

    @staticmethod
    def get_diffculty():
        with open("data.json", 'rt') as f:
            return json.load(f)["difficulty"]["current_difficulty"]

    @staticmethod
    def get_shop():
        with open("data.json", "rt") as f:
            return json.load(f)["coins"]["unlocked_upgrade"], json.load(f)["gems"]["unlocked_upgrade"]
