import pygame
import random
from game.entities.entity import Entity
from config import SCREEN_WIDTH, SCREEN_HEIGHT, ENEMY_SPEED

class Enemy(Entity):
    def __init__(self, x, y, game):
        super().__init__(x, y, 'enemy', game)
        self.velocity = pygame.math.Vector2(0, ENEMY_SPEED)
        # Random horizontal sway
        self.sway_speed = random.choice([-50, 50])
        self.sway_timer = 0

    def update(self, dt):
        self.velocity.x = self.sway_speed

        # Bounce off walls
        if self.rect.left <= 0:
            self.sway_speed = abs(self.sway_speed)
        elif self.rect.right >= SCREEN_WIDTH:
            self.sway_speed = -abs(self.sway_speed)

        super().update(dt)

        if self.rect.top > SCREEN_HEIGHT:
            self.kill()
