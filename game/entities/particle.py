import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

        speed = random.uniform(50, 150)
        angle = random.uniform(0, 360)
        vec = pygame.math.Vector2()
        vec.from_polar((speed, angle))
        self.velocity = vec
        self.position = pygame.math.Vector2(x, y)
        self.lifetime = random.uniform(0.3, 0.8)

    def update(self, dt):
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.kill()

        self.position += self.velocity * dt
        self.rect.center = self.position
