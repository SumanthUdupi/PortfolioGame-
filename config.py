# Window configuration
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
CAPTION = "Neon Space Shooter"

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
NEON_BLUE = (0, 255, 255)
NEON_RED = (255, 0, 100)

# Gameplay settings
PLAYER_SPEED = 300  # Pixels per second
BULLET_SPEED = 500
ENEMY_SPEED = 100
SPAWN_RATE = 1.5    # Seconds between enemies

# Paths
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
SPRITES_DIR = os.path.join(ASSETS_DIR, 'sprites')
SOUNDS_DIR = os.path.join(ASSETS_DIR, 'sounds')

# Input Configuration
import pygame
KEY_BINDINGS = {
    'left': [pygame.K_LEFT, pygame.K_a],
    'right': [pygame.K_RIGHT, pygame.K_d],
    'up': [pygame.K_UP, pygame.K_w],
    'down': [pygame.K_DOWN, pygame.K_s],
    'shoot': [pygame.K_SPACE],
    'confirm': [pygame.K_SPACE, pygame.K_RETURN],
    'quit': [pygame.K_ESCAPE]
}
