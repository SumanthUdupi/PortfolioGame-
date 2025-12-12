import pygame
from game.scenes.base_scene import BaseScene
from config import BLACK, WHITE

class GameScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 50)
        self.game_text = self.font.render("Game Scene - Press ESC to Menu", True, WHITE)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Returning to menu...")
                    self.game.scene_manager.set_scene("menu_scene") # Placeholder for actual scene transition

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(BLACK)
        game_text_rect = self.game_text.get_rect(center=(self.game.screen.get_width() / 2, self.game.screen.get_height() / 2))
        screen.blit(self.game_text, game_text_rect)
