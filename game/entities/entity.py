import pygame

from game.managers.asset_manager import AssetManager
from config import MAGENTA, BLACK

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, asset_key=None, image=None):
        super().__init__()
        self.asset_manager = AssetManager()
        self.width = width
        self.height = height

        if asset_key:
            loaded_image = self.asset_manager.get_image(asset_key)
            if loaded_image:
                self.image = pygame.transform.scale(loaded_image, (width, height))
            else:
                loaded_image = self.asset_manager.load_image(asset_key)
                if loaded_image:
                     self.image = pygame.transform.scale(loaded_image, (width, height))
                else:
                    self.image = self._create_missing_texture_surface(width, height)
        elif image:
            self.image = image
        else:
            self.image = self._create_missing_texture_surface(width, height)

        self.rect = self.image.get_rect(topleft=(x, y))
        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 0
        self.interaction_range = 50 # Default interaction range

    def draw_highlight(self, screen, player_pos):
        # Calculate distance to player
        # Assuming player_pos is a Vector2 or tuple (x, y)
        entity_center = pygame.math.Vector2(self.rect.center)
        if isinstance(player_pos, pygame.math.Vector2):
             dist = entity_center.distance_to(player_pos)
        else:
             dist = entity_center.distance_to(pygame.math.Vector2(player_pos))

        if dist < self.interaction_range:
            # Draw white outline
            pygame.draw.rect(screen, (255, 255, 255), self.rect, 2)
            # Draw "!" bubble
            font = pygame.font.Font(None, 30)
            text = font.render("!", True, (255, 255, 255))
            text_rect = text.get_rect(center=(self.rect.centerx, self.rect.top - 20))
            # Draw bubble bg
            bubble_rect = text_rect.inflate(10, 10)
            pygame.draw.ellipse(screen, (0, 0, 0), bubble_rect)
            pygame.draw.ellipse(screen, (255, 255, 255), bubble_rect, 2)
            screen.blit(text, text_rect)

    def _create_missing_texture_surface(self, width, height):
        surface = pygame.Surface((width, height))
        # Create magenta/black checkerboard
        check_size = 8
        for x in range(0, width, check_size):
            for y in range(0, height, check_size):
                color = MAGENTA if (x // check_size + y // check_size) % 2 == 0 else BLACK
                rect = pygame.Rect(x, y, check_size, check_size)
                # Clip rect to surface bounds
                rect = rect.clip(surface.get_rect())
                pygame.draw.rect(surface, color, rect)
        return surface

    def update(self, dt):
        self.rect.x += self.velocity.x * self.speed * dt
        self.rect.y += self.velocity.y * self.speed * dt

    def draw(self, screen):
        screen.blit(self.image, self.rect)
