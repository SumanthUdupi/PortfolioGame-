import pygame

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Game title
CAPTION = "PortfolioGame"

# Frames per second
FPS = 60

# Colors (RGB)
# Professional Tech Palette
PRIMARY_BLUE = (17, 141, 255)  # #118DFF
WARM_BEIGE = (230, 213, 184)   # #E6D5B8
SUCCESS_GREEN = (0, 255, 0)    # Placeholder, need to verify strict requirement if given.
                               # REQ-VISUAL-06 mentions "success-green color from the style guide" but guide isn't fully visible here.
                               # Assuming standard green or I'll pick a nice one.
                               # Let's keep existing colors but rename/add the new ones.

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)

# Game states
GAME_STATE_MENU = 0
GAME_STATE_PLAYING = 1
GAME_STATE_PAUSED = 2
GAME_STATE_GAME_OVER = 3

# Key bindings
KEYS = {
    "UP": pygame.K_w,
    "DOWN": pygame.K_s,
    "LEFT": pygame.K_a,
    "RIGHT": pygame.K_d,
    "INTERACT": pygame.K_e,
    "MENU": pygame.K_ESCAPE
}
