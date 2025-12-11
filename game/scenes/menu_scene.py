import pygame
from config import *
from game.scenes.base_scene import BaseScene

class MenuScene(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.font = self.game_manager.asset_manager.load_font("default.ttf", 36)
        self.title_font = self.game_manager.asset_manager.load_font("default.ttf", 48)
        self.selected_option = 0
        self.options = ["Start Game", "Settings", "Quit"]

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                self.select_option()

    def select_option(self):
        if self.selected_option == 0:  # Start Game
            self.game_manager.scene_manager.set_scene("game")
        elif self.selected_option == 1:  # Settings
            pass  # Placeholder
        elif self.selected_option == 2:  # Quit
            self.game_manager.quit_game()

    def render(self, screen):
        # Title
        title_text = self.title_font.render(TITLE, True, WHITE)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 150))
        screen.blit(title_text, title_rect)

        # Menu options
        for i, option in enumerate(self.options):
            color = YELLOW if i == self.selected_option else WHITE
            text = self.font.render(option, True, color)
            rect = text.get_rect(center=(SCREEN_WIDTH // 2, 300 + i * 60))
            if i == self.selected_option:
                # Highlight background
                bg_rect = pygame.Rect(rect.left - 20, rect.top - 10, rect.width + 40, rect.height + 20)
                pygame.draw.rect(screen, (50, 50, 50), bg_rect)  # Dark gray background
                pygame.draw.rect(screen, YELLOW, bg_rect, 2)  # Yellow border
            screen.blit(text, rect)

        # Instructions
        instr_font = self.game_manager.asset_manager.load_font("default.ttf", 24)
        instr_text = instr_font.render("Use UP/DOWN arrows to navigate, ENTER to select", True, WHITE)
        instr_rect = instr_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 50))
        screen.blit(instr_text, instr_rect)