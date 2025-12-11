import pygame

class AudioManager:
    def __init__(self, asset_manager):
        self.asset_manager = asset_manager
        # Pygame mixer is initialized in main

    def play_sound(self, name):
        sound = self.asset_manager.get_sound(name)
        if sound:
            sound.play()

    def play_music(self, filename):
        # Placeholder for music
        pass
