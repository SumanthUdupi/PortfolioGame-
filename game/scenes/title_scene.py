import pygame
from game.managers.scene_manager import Scene
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, NEON_BLUE

class TitleScene(Scene):
    def __init__(self, manager):
        super().__init__(manager)
        self.font_large = pygame.font.Font(None, 74)
        self.font_small = pygame.font.Font(None, 36)

        self.title_text = self.font_large.render("NEON SPACE", True, NEON_BLUE)
        self.start_text = self.font_small.render("Press SPACE to Start", True, WHITE)
        self.quit_text = self.font_small.render("Press ESC to Quit", True, WHITE)

        self.title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/3))
        self.start_rect = self.start_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2))
        self.quit_rect = self.quit_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 50))

    def update(self, dt):
        input_mgr = self.game.input_manager
        if input_mgr.is_action_pressed('confirm'):
            from game.scenes.game_scene import GameScene
            self.manager.change_scene(GameScene(self.manager))
        elif input_mgr.is_action_pressed('quit'):
            self.game.running = False

    def draw(self, screen):
        screen.fill((0, 0, 0))
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.start_text, self.start_rect)
        screen.blit(self.quit_text, self.quit_rect)
