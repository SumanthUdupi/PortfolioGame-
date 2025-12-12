import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, image=None):
        super().__init__()
        self.image = image if image else pygame.Surface([width, height])
        if not image:
            self.image.fill((255, 255, 255)) # Default white rectangle
        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 0

    def update(self, dt):
        self.rect.x += self.velocity.x * self.speed * dt
        self.rect.y += self.velocity.y * self.speed * dt

    def draw(self, screen):
        screen.blit(self.image, self.rect)
