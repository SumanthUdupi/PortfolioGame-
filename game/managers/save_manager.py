import json
import os

class SaveManager:
    def __init__(self, filename='save_data.json'):
        self.filename = filename
        self.data = {'high_score': 0}

    def load(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    self.data = json.load(f)
            except Exception as e:
                print(f"Error loading save: {e}")
        return self.data

    def save(self):
        try:
            with open(self.filename, 'w') as f:
                json.dump(self.data, f)
        except Exception as e:
            print(f"Error saving data: {e}")

    def get_high_score(self):
        return self.data.get('high_score', 0)

    def set_high_score(self, score):
        self.data['high_score'] = score
        self.save()
