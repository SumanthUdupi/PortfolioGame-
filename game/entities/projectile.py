import pygame
from game.entities.entity import Entity
from config import SCREEN_HEIGHT, BULLET_SPEED

class Projectile(Entity):
    def __init__(self, x, y, image_name, game, direction_y):
        super().__init__(x, y, image_name, game)
        self.velocity = pygame.math.Vector2(0, direction_y * BULLET_SPEED)

    def update(self, dt):
        super().update(dt)
        # Kill if off screen
        if self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT:
            self.kill()
