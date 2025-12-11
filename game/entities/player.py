import pygame
from config import *
from game.entities.entity import Entity

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_SIZE, PLAYER_SIZE)
        self.speed = PLAYER_SPEED
        self.zone = 1
        self.level = 1
        self.experience = 0

    def update(self, dt, input_manager, entities=None):
        # Handle movement
        dx = 0
        dy = 0

        if input_manager.is_key_held(KEYS["LEFT"]):
            dx -= self.speed
        if input_manager.is_key_held(KEYS["RIGHT"]):
            dx += self.speed
        if input_manager.is_key_held(KEYS["UP"]):
            dy -= self.speed
        if input_manager.is_key_held(KEYS["DOWN"]):
            dy += self.speed

        # Normalize diagonal movement
        if dx != 0 and dy != 0:
            dx *= 0.707  # 1/sqrt(2)
            dy *= 0.707

        # Calculate new position
        new_x = self.x + dx * dt * 60
        new_y = self.y + dy * dt * 60

        # Check collisions
        can_move = True
        if entities:
            from game.systems.collision_system import CollisionSystem
            temp_rect = pygame.Rect(new_x, new_y, self.width, self.height)
            for entity in entities:
                if entity != self and temp_rect.colliderect(entity.rect):
                    can_move = False
                    break

        if can_move:
            self.x = new_x
            self.y = new_y

        # Keep player in world bounds (assuming world is larger than screen)
        # For now, no bounds, but camera will clamp

        super().update(dt)

    def render(self, screen, camera_x=0, camera_y=0):
        # Draw player as a colored rectangle
        pygame.draw.rect(screen, GREEN, (self.x - camera_x, self.y - camera_y, self.width, self.height))

        super().render(screen, camera_x, camera_y)