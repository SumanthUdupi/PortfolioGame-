import pygame
from game.entities.entity import Entity
from game.entities.projectile import Projectile
from config import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_SPEED

class Player(Entity):
    def __init__(self, x, y, game):
        super().__init__(x, y, 'player', game)
        self.speed = PLAYER_SPEED
        self.shoot_timer = 0
        self.shoot_cooldown = 0.2

    def update(self, dt):
        input_mgr = self.game.input_manager

        # Movement
        direction = pygame.math.Vector2(0, 0)
        if input_mgr.is_action_pressed('left'):
            direction.x = -1
        if input_mgr.is_action_pressed('right'):
            direction.x = 1
        if input_mgr.is_action_pressed('up'):
            direction.y = -1
        if input_mgr.is_action_pressed('down'):
            direction.y = 1

        if direction.length_squared() > 0:
            direction = direction.normalize()

        self.velocity = direction * self.speed

        super().update(dt)

        # Bounds check
        if self.rect.left < 0:
            self.rect.left = 0
            self.position.x = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
            self.position.x = SCREEN_WIDTH - self.rect.width
        if self.rect.top < 0:
            self.rect.top = 0
            self.position.y = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.position.y = SCREEN_HEIGHT - self.rect.height

        # Shooting
        self.shoot_timer -= dt
        if input_mgr.is_action_pressed('shoot') and self.shoot_timer <= 0:
            self.shoot()

    def shoot(self):
        self.shoot_timer = self.shoot_cooldown
        # Spawn bullet centered
        bx = self.rect.centerx - 8 # 8 is half bullet width approx
        by = self.rect.top
        bullet = Projectile(bx, by, 'bullet', self.game, -1)
        self.game.current_scene.add_projectile(bullet)
        self.game.audio_manager.play_sound('shoot')
