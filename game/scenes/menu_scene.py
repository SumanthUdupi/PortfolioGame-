import pygame
from game.scenes.base_scene import BaseScene
from config import WHITE, BLACK, CAPTION

class MenuScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 50)
        self.title_text = self.font.render(CAPTION, True, WHITE)
        self.start_text = self.small_font.render("Press SPACE to Start", True, WHITE)
        self.quit_text = self.small_font.render("Press Q to Quit", True, WHITE)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("Starting game...")
                    self.game.scene_manager.set_scene("game_scene") # Placeholder for actual scene transition
                elif event.key == pygame.K_q:
                    self.game.running = False

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(BLACK)
        title_rect = self.title_text.get_rect(center=(self.game.screen.get_width() / 2, self.game.screen.get_height() / 3))
        start_rect = self.start_text.get_rect(center=(self.game.screen.get_width() / 2, self.game.screen.get_height() / 2))
        quit_rect = self.quit_text.get_rect(center=(self.game.screen.get_width() / 2, self.game.screen.get_height() / 2 + 60))

        screen.blit(self.title_text, title_rect)
        screen.blit(self.start_text, start_rect)
        screen.blit(self.quit_text, quit_rect)