import pygame
import os

class AssetManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance.images = {}
            cls._instance.fonts = {}
            cls._instance.sounds = {}
            cls._instance.base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
        return cls._instance

    def load_image(self, path, colorkey=None):
        full_path = os.path.join(self.base_path, 'sprites', path)
        if full_path not in self.images:
            try:
                image = pygame.image.load(full_path).convert_alpha()
                if colorkey is not None:
                    if colorkey == -1:
                        colorkey = image.get_at((0,0))
                    image.set_colorkey(colorkey)
                self.images[full_path] = image
            except pygame.error as e:
                print(f"Error loading image {full_path}: {e}")
                return None
        return self.images[full_path]

    def load_font(self, path, size):
        full_path = os.path.join(self.base_path, 'fonts', path)
        font_key = (full_path, size)
        if font_key not in self.fonts:
            try:
                font = pygame.font.Font(full_path, size)
                self.fonts[font_key] = font
            except FileNotFoundError:
                print(f"Error loading font {full_path}: File not found. Using default font.")
                font = pygame.font.Font(None, size)
                self.fonts[font_key] = font
            except Exception as e:
                print(f"Error loading font {full_path}: {e}")
                font = pygame.font.Font(None, size)
                self.fonts[font_key] = font
        return self.fonts[font_key]

    def load_sound(self, path):
        full_path = os.path.join(self.base_path, 'sounds', path)
        if full_path not in self.sounds:
            try:
                sound = pygame.mixer.Sound(full_path)
                self.sounds[full_path] = sound
            except pygame.error as e:
                print(f"Error loading sound {full_path}: {e}")
                return None
        return self.sounds[full_path]

    def get_image(self, path):
        return self.images.get(os.path.join(self.base_path, 'sprites', path))

    def get_font(self, path, size):
        return self.fonts.get((os.path.join(self.base_path, 'fonts', path), size))

    def get_sound(self, path):
        return self.sounds.get(os.path.join(self.base_path, 'sounds', path))

    def clear_cache(self):
        self.images = {}
        self.fonts = {}
        self.sounds = {}