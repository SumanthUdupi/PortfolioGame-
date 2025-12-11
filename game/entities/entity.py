import pygame

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image_name, game):
        super().__init__()
        self.game = game
        self.image = self.game.asset_manager.get_image(image_name)
        if self.image is None:
            # Fallback if image not loaded
            self.image = pygame.Surface((32, 32))
            self.image.fill((255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.position = pygame.math.Vector2(x, y)
        self.velocity = pygame.math.Vector2(0, 0)

    def update(self, dt):
        self.position += self.velocity * dt
        self.rect.x = int(self.position.x)
        self.rect.y = int(self.position.y)
