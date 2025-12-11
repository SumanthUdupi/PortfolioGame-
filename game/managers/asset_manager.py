import pygame
from config import *
import os

class AssetManager:
    def __init__(self):
        self.images = {}
        self.sounds = {}
        self.fonts = {}
        self.cache = {}

    def load_image(self, path, use_cache=True):
        if use_cache and path in self.cache:
            return self.cache[path]

        full_path = os.path.join(SPRITES_DIR, path)
        if os.path.exists(full_path):
            image = pygame.image.load(full_path).convert_alpha()
        else:
            # Placeholder: create a colored rectangle
            image = pygame.Surface((TILE_SIZE, TILE_SIZE))
            image.fill(BLUE)  # Default blue placeholder

        if use_cache:
            self.cache[path] = image
        return image

    def load_sound(self, path, use_cache=True):
        if use_cache and path in self.cache:
            return self.cache[path]

        full_path = os.path.join(SOUNDS_DIR, path)
        if os.path.exists(full_path):
            sound = pygame.mixer.Sound(full_path)
        else:
            # Placeholder: return None, audio system will handle text feedback
            sound = None

        if use_cache:
            self.cache[path] = sound
        return sound

    def load_font(self, name, size):
        key = f"{name}_{size}"
        if key in self.fonts:
            return self.fonts[key]

        full_path = os.path.join(FONTS_DIR, name)
        if os.path.exists(full_path):
            font = pygame.font.Font(full_path, size)
        else:
            font = pygame.font.SysFont("Arial", size)

        self.fonts[key] = font
        return font

    def get_placeholder_sprite(self, color, size=(TILE_SIZE, TILE_SIZE)):
        key = f"placeholder_{color}_{size}"
        if key in self.cache:
            return self.cache[key]

        surface = pygame.Surface(size)
        surface.fill(color)
        self.cache[key] = surface
        return surface