import json

from python import GameProperties, Utils


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Utils.MutableObject):
            return {'_mutable_object': obj._value}
        return super().default(obj)


class DataManager:
    """
    A class for managing game data and providing utility functions

    Methods:
        - save_game(username): save the game data for a specific user to a Json file
        - get_coins_players(username): retrieves the number of coins for a specific user
        - get_gems_players(username): retrieves the number of gems for a specific player
        - get_current_waves(username): retrieves the current wave for a specific user
        - get_difficulty(username): retrieves the current difficulty for a specific user
        - get_coin_shop(username): retrieves the coin shop data for a specific user
        - get_gems_shop(username): retrieves the gem shop data for a specific user
        - get_all_users(username): retrieves a list of all username with saved data game
        - add_user(username): adds a new user with default game data
        - load_game(username="default_user"): loads the game data for a specific user # A CHANGER
    """

    @staticmethod
    def get_coins_player(username):
        with open("data.json", 'r') as f:
            data = json.load(f)
            return data["players"][username]["coins"]

    @staticmethod
    def get_gems_player(username):
        with open("data.json", 'r') as f:
            data = json.load(f)
            return data["players"][username]["gems"]

    @staticmethod
    def save_game(username):
        with open("data.json", 'rt') as f:
            current_save = json.load(f)

        if username in current_save["players"]:
            return "Account with username '" + username + "' already exists.'"

        new_data = {
            username: {
                "password": GameProperties.password,
                "gems": GameProperties.gems, "coins": GameProperties.coins,

                "game_properties": {
                    "waves_game": {
                        "current_wave": GameProperties.current_wave
                    },

                    "difficulty": {
                        "current_difficulty": GameProperties.difficulty
                    }
                },

                "shops": {
                    "coins": GameProperties.coin_shop, "gems": GameProperties.gem_shop
                },
                "settings": {
                    "coins_type": "big_numbers"
                }
            }
        }

        current_save["players"].update(new_data)

        with open("data.json", "w") as f:
            f.write(json.dumps(current_save, indent=2, sort_keys=False, cls=CustomEncoder))

    @staticmethod
    def get_current_waves(username):
        with open("data.json", 'r') as f:
            data = json.load(f)
            return data["players"][username]["game_properties"]["waves_game"]["current_wave"]

    @staticmethod
    def get_difficulty(username):
        with open("data.json", 'r') as f:
            data = json.load(f)
            return data["players"][username]["game_properties"]["difficulty"]["current_difficulty"]

    @staticmethod
    def get_coin_shop(username):
        with open("data.json", "r") as f:
            data = json.load(f)
            return data["players"][username]["shops"]["coins"]

    @staticmethod
    def get_gems_shop(username):
        with open("data.json", "r") as f:
            data = json.load(f)
            return data["players"][username]["shops"]["gems"]

    @staticmethod
    def get_all_usernames():
        with open("data.json", 'r') as f:
            data = json.load(f)
            return list(data["players"].keys())

    @staticmethod
    def get_settings(username):
        with open("data.json", 'r') as f:
            data = json.load(f)
            return data["players"][username]["settings"]

    @staticmethod
    def get_password(username):
        with open("data.json", 'r') as f:
            data = json.load(f)
            return data["players"][username]["password"]

    @staticmethod
    def add_user(username, password):
        with open("data.json", 'rt') as f:
            current_save = json.load(f)

        GameProperties.password = password

        new_player = {
            username: {
                "password": GameProperties.password,
                "gems": GameProperties.gems, "coins": GameProperties.coins,

                "game_properties": {
                    "waves_game": {
                        "current_wave": GameProperties.current_wave
                    },

                    "difficulty": {
                        "current_difficulty": GameProperties.difficulty
                    },
                },

                "shops": {
                    "coins": GameProperties.coin_shop, "gems": GameProperties.gem_shop
                },
                "settings": {
                    "coins_type": "big_number"
                }
            }

        }

        current_save["players"].update(new_player)

        with open("data.json", "w") as f:
            f.write(json.dumps(current_save, indent=2, sort_keys=False, cls=CustomEncoder))

    @staticmethod
    def load_game(username="guest"):
        if username == "guest":
            GameProperties.difficulty = 1
            GameProperties.current_wave = 0
            GameProperties.coins = Utils.MutableNumber(0)
            GameProperties.gems = Utils.MutableNumber(0)
            GameProperties.coin_shop = {"atk_speed_upgrade": 0, "damage_upgrade": 0, "health_upgrade": 0}
            GameProperties.gems_shop = {"gems_10": 0, "gems_25": 0, "gems_50": 0, "gems_100": 0, "red1_skin": 0}

        else:
            GameProperties.difficulty = DataManager.get_difficulty(username)
            GameProperties.current_wave = DataManager.get_current_waves(username)
            GameProperties.coins = Utils.MutableNumber(DataManager.get_coins_player(username))
            GameProperties.gems = Utils.MutableNumber(DataManager.get_gems_player(username))
            GameProperties.coin_shop = DataManager.get_coin_shop(username)
            GameProperties.gems_shop = DataManager.get_gems_shop(username)
            GameProperties.username = username
            GameProperties.password = DataManager.get_password(username)

    @staticmethod
    def verify_successful_login(username, password):
        with open("data.json", 'r') as f:
            data = json.load(f)
            if username in data["players"] and "password" in data["players"][username]:
                if data["players"][username]["password"] == password:
                    return "logged in with the name", username
                return "wrong password for the password", username
            return "not account registered"
