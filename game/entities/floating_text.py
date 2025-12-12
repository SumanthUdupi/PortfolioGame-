import pygame

class FloatingText(pygame.sprite.Sprite):
    def __init__(self, x, y, text, color=(255, 255, 255), duration=1.0, speed=50):
        super().__init__()
        self.font = pygame.font.Font(None, 24)
        self.image = self.font.render(text, True, color)
        self.rect = self.image.get_rect(center=(x, y))
        self.velocity = pygame.math.Vector2(0, -speed) # Float up
        self.duration = duration
        self.timer = 0
        self.original_y = y
        self.alpha = 255

    def update(self, dt):
        self.timer += dt
        if self.timer >= self.duration:
            self.kill()
            return

        self.rect.y += self.velocity.y * dt

        # Fade out
        progress = self.timer / self.duration
        self.alpha = max(0, 255 - int(255 * progress))
        self.image.set_alpha(self.alpha)
