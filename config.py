import pygame

# Game Configuration
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60
TITLE = "Pixel Art RPG Portfolio - The System Chronicles"

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
TEAL = (0, 128, 128)
PINK = (255, 192, 203)

# Grid and Pixel Art
TILE_SIZE = 32
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE

# World Settings
WORLD_WIDTH = 2048
WORLD_HEIGHT = 2048

# Player Settings
PLAYER_SPEED = 5
PLAYER_SIZE = TILE_SIZE

# Zones
ZONES = {
    1: "Enterprise Integration",
    2: "Data Processing",
    3: "Analytics Academy",
    4: "Engineering Workshop"
}

# Audio Settings
MASTER_VOLUME = 0.7
SFX_VOLUME = 0.8
MUSIC_VOLUME = 0.6

# Save/Load
SAVE_FILE = "savegame.json"

# Asset Paths
ASSETS_DIR = "assets"
SPRITES_DIR = f"{ASSETS_DIR}/sprites"
SOUNDS_DIR = f"{ASSETS_DIR}/sounds"
FONTS_DIR = f"{ASSETS_DIR}/fonts"

# Game States
GAME_STATES = {
    "MENU": 0,
    "PLAYING": 1,
    "PAUSED": 2,
    "GAME_OVER": 3,
    "SETTINGS": 4
}

# Input Keys
KEYS = {
    "UP": pygame.K_w,
    "DOWN": pygame.K_s,
    "LEFT": pygame.K_a,
    "RIGHT": pygame.K_d,
    "INTERACT": pygame.K_e,
    "PAUSE": pygame.K_ESCAPE,
    "INVENTORY": pygame.K_i
}