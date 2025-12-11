import pygame
from config import SPRITES_DIR, SOUNDS_DIR
import os

class AssetManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance.images = {}
            cls._instance.sounds = {}
            cls._instance.fonts = {}
        return cls._instance

    def load_image(self, name, filename):
        path = os.path.join(SPRITES_DIR, filename)
        try:
            image = pygame.image.load(path).convert_alpha()
            self.images[name] = image
            return image
        except Exception as e:
            print(f"Failed to load image {filename}: {e}")
            # Return a fallback surface
            s = pygame.Surface((32, 32))
            s.fill((255, 0, 255))
            return s

    def load_sound(self, name, filename):
        path = os.path.join(SOUNDS_DIR, filename)
        try:
            sound = pygame.mixer.Sound(path)
            self.sounds[name] = sound
            return sound
        except Exception as e:
            print(f"Failed to load sound {filename}: {e}")
            return None

    def get_image(self, name):
        return self.images.get(name)

    def get_sound(self, name):
        return self.sounds.get(name)
