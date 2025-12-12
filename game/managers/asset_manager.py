import pygame
import os
import json
import logging
from typing import Dict, Any, Optional, Tuple

class AssetManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance.images = {}
            cls._instance.fonts = {}
            cls._instance.sounds = {}
            cls._instance.json_data = {}
            cls._instance.base_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets')
            cls._instance.logger = logging.getLogger("AssetManager")
        return cls._instance

    def load_json(self, path: str) -> Optional[Any]:
        full_path = os.path.join(self.base_path, 'data', path)
        if full_path not in self.json_data:
            try:
                with open(full_path, 'r') as f:
                    data = json.load(f)
                self.json_data[full_path] = data
            except (FileNotFoundError, json.JSONDecodeError) as e:
                self.logger.error(f"Error loading JSON {full_path}: {e}")
                return None
        return self.json_data[full_path]

    def get_json(self, path: str) -> Optional[Any]:
        full_path = os.path.join(self.base_path, 'data', path)
        return self.json_data.get(full_path) or self.load_json(path)

    def load_image(self, path: str, colorkey: Optional[Any] = None) -> Optional[pygame.Surface]:
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
                self.logger.error(f"Error loading image {full_path}: {e}")
                return None
        return self.images[full_path]

    def load_font(self, path: str, size: int) -> pygame.font.Font:
        full_path = os.path.join(self.base_path, 'fonts', path)
        font_key = (full_path, size)
        if font_key not in self.fonts:
            try:
                font = pygame.font.Font(full_path, size)
                self.fonts[font_key] = font
            except FileNotFoundError:
                self.logger.warning(f"Error loading font {full_path}: File not found. Using default font.")
                font = pygame.font.Font(None, size)
                self.fonts[font_key] = font
            except Exception as e:
                self.logger.error(f"Error loading font {full_path}: {e}")
                font = pygame.font.Font(None, size)
                self.fonts[font_key] = font
        return self.fonts[font_key]

    def load_sound(self, path: str) -> Optional[pygame.mixer.Sound]:
        full_path = os.path.join(self.base_path, 'sounds', path)
        if full_path not in self.sounds:
            try:
                sound = pygame.mixer.Sound(full_path)
                self.sounds[full_path] = sound
            except pygame.error as e:
                self.logger.error(f"Error loading sound {full_path}: {e}")
                return None
        return self.sounds[full_path]

    def get_image(self, path: str) -> Optional[pygame.Surface]:
        return self.images.get(os.path.join(self.base_path, 'sprites', path))

    def get_font(self, path: str, size: int) -> Optional[pygame.font.Font]:
        return self.fonts.get((os.path.join(self.base_path, 'fonts', path), size))

    def get_sound(self, path: str) -> Optional[pygame.mixer.Sound]:
        return self.sounds.get(os.path.join(self.base_path, 'sounds', path))

    def clear_cache(self) -> None:
        self.images = {}
        self.fonts = {}
        self.sounds = {}
        self.json_data = {}

    def preload_zone_assets(self, zone_id: str) -> None:
        # REQ-TECH-06: Asset Pre-loading
        self.logger.info(f"Preloading assets for zone: {zone_id}")

        # Example: Preload player and common UI
        self.load_image("player.png")
        # Add more assets as needed based on zone_id
