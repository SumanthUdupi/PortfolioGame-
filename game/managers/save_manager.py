import json
import os
from config import SAVE_FILE

class SaveManager:
    def __init__(self):
        self.save_data = {
            "player": {
                "position": [100, 100],
                "zone": 1,
                "level": 1,
                "experience": 0,
                "inventory": []
            },
            "game": {
                "current_zone": 1,
                "completed_zones": [],
                "settings": {
                    "master_volume": 0.7,
                    "sfx_volume": 0.8,
                    "music_volume": 0.6
                }
            }
        }
        self.load_game()

    def save_game(self):
        try:
            with open(SAVE_FILE, 'w') as f:
                json.dump(self.save_data, f, indent=2)
        except Exception as e:
            print(f"Error saving game: {e}")

    def load_game(self):
        if os.path.exists(SAVE_FILE):
            try:
                with open(SAVE_FILE, 'r') as f:
                    self.save_data = json.load(f)
            except Exception as e:
                print(f"Error loading game: {e}")
                # Keep default save data

    def get_player_data(self):
        return self.save_data["player"]

    def set_player_data(self, data):
        self.save_data["player"].update(data)

    def get_game_data(self):
        return self.save_data["game"]

    def set_game_data(self, data):
        self.save_data["game"].update(data)

    def get_setting(self, key):
        return self.save_data["game"]["settings"].get(key)

    def set_setting(self, key, value):
        self.save_data["game"]["settings"][key] = value