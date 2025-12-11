import pygame
from game.managers.scene_manager import Scene
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, NEON_RED
import json
import os

class GameOverScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)

        self.game_over_text = self.font_large.render("GAME OVER", True, NEON_RED)
        self.score_text = self.font_small.render(f"Score: {self.game.score}", True, WHITE)
        self.high_score_text = self.font_small.render(f"High Score: {self.game.high_score}", True, WHITE)
        self.retry_text = self.font_small.render("Press SPACE to Retry", True, WHITE)

        self.go_rect = self.game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
        self.score_rect = self.score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.hs_rect = self.high_score_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 40))
        self.retry_rect = self.retry_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 100))

        self.save_high_score()

    def save_high_score(self):
        if self.game.score > self.game.high_score:
            self.game.high_score = self.game.score
            self.game.save_manager.set_high_score(self.game.high_score)

    def update(self, dt):
        input_mgr = self.game.input_manager
        if input_mgr.is_action_pressed('confirm'):
            from game.scenes.game_scene import GameScene
            self.manager.change_scene(GameScene(self.manager))
        elif input_mgr.is_action_pressed('quit'):
             from game.scenes.title_scene import TitleScene
             self.manager.change_scene(TitleScene(self.manager))

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.game_over_text, self.go_rect)
        screen.blit(self.score_text, self.score_rect)
        screen.blit(self.high_score_text, self.hs_rect)
        screen.blit(self.retry_text, self.retry_rect)
