import pygame
import random
from game.managers.scene_manager import Scene
from game.entities.player import Player
from game.entities.enemy import Enemy
from game.entities.particle import Particle
from config import SCREEN_WIDTH, SCREEN_HEIGHT, SPAWN_RATE, WHITE

class GameScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()

        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100, self.game)
        self.all_sprites.add(self.player)

        self.spawn_timer = 0
        self.game.score = 0

        self.font = pygame.font.Font(None, 36)

    def add_projectile(self, projectile):
        self.projectiles.add(projectile)
        self.all_sprites.add(projectile)

    def spawn_enemy(self):
        x = random.randint(50, SCREEN_WIDTH - 50)
        enemy = Enemy(x, -50, self.game)
        self.enemies.add(enemy)
        self.all_sprites.add(enemy)

    def spawn_explosion(self, x, y, color):
        for _ in range(10):
            p = Particle(x, y, color)
            self.particles.add(p)
            self.all_sprites.add(p)
        self.game.audio_manager.play_sound('explosion')

    def update(self, dt):
        # Spawning
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_enemy()
            self.spawn_timer = SPAWN_RATE

        self.all_sprites.update(dt)

        # Collisions: Bullets hit Enemies
        hits = pygame.sprite.groupcollide(self.enemies, self.projectiles, True, True)
        for enemy, bullets in hits.items():
            self.spawn_explosion(enemy.rect.centerx, enemy.rect.centery, (255, 50, 50))
            self.game.score += 100

        # Collisions: Player hits Enemy
        hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
        if hits:
            self.spawn_explosion(self.player.rect.centerx, self.player.rect.centery, (0, 255, 255))
            from game.scenes.game_over_scene import GameOverScene
            self.manager.change_scene(GameOverScene(self.manager))

    def draw(self, screen):
        screen.fill((10, 10, 20)) # Dark Blue background
        self.all_sprites.draw(screen)

        # Draw HUD
        score_surf = self.font.render(f"Score: {self.game.score}", True, WHITE)
        screen.blit(score_surf, (10, 10))
