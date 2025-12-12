import pygame
import random
from config import SUCCESS_GREEN

class Particle(pygame.sprite.Sprite):
    def __init__(self, x, y, color=SUCCESS_GREEN, lifetime=1.0):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pygame.math.Vector2(random.uniform(-50, 50), random.uniform(-50, 50))
        self.lifetime = lifetime
        self.timer = 0

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.lifetime:
            self.kill()

        self.rect.x += self.velocity.x * dt
        self.rect.y += self.velocity.y * dt

class ParticleSystem:
    def __init__(self):
        self.particles = pygame.sprite.Group()

    def emit(self, x, y, count=15, color=SUCCESS_GREEN):
        for _ in range(count):
            self.particles.add(Particle(x, y, color))

    def update(self, dt):
        self.particles.update(dt)

    def draw(self, screen):
        self.particles.draw(screen)
