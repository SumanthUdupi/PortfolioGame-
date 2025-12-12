import pygame
from game.entities.entity import Entity
from game.managers.input_manager import InputManager
from config import BLACK, WHITE

class Player(Entity):
    def __init__(self, x, y, width, height, image=None):
        super().__init__(x, y, width, height, image)
        self.speed = 200 # pixels per second
        self.input_manager = InputManager() # Singleton instance

        # Placeholder image if none provided
        if not image:
            self.image = pygame.Surface([width, height])
            self.image.fill(WHITE) # Player is white by default

    def update(self, dt):
        self.velocity.x = 0
        self.velocity.y = 0

        if self.input_manager.is_key_held(pygame.K_LEFT) or self.input_manager.is_key_held(pygame.K_a):
            self.velocity.x = -1
        if self.input_manager.is_key_held(pygame.K_RIGHT) or self.input_manager.is_key_held(pygame.K_d):
            self.velocity.x = 1
        if self.input_manager.is_key_held(pygame.K_UP) or self.input_manager.is_key_held(pygame.K_w):
            self.velocity.y = -1
        if self.input_manager.is_key_held(pygame.K_DOWN) or self.input_manager.is_key_held(pygame.K_s):
            self.velocity.y = 1

        # Normalize diagonal movement
        if self.velocity.length() > 0:
            self.velocity.normalize_ip()

        super().update(dt) # Call parent's update for position change

    def draw(self, screen):
        super().draw(screen)
