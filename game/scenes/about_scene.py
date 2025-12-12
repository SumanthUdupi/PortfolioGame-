import pygame
from game.scenes.base_scene import BaseScene
from game.managers.asset_manager import AssetManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, WARM_BEIGE, PRIMARY_BLUE

class AboutScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.asset_manager = AssetManager()
        self.resume_data = self.asset_manager.get_json('resume.json')
        self.font_title = pygame.font.Font(None, 60)
        self.font_header = pygame.font.Font(None, 40)
        self.font_text = pygame.font.Font(None, 28)
        self.padding = 50

    def wrap_text(self, text, font, max_width):
        words = text.split(' ')
        lines = []
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            w, h = font.size(test_line)
            if w <= max_width:
                current_line.append(word)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
        if current_line:
            lines.append(' '.join(current_line))
        return lines

    def render_content(self, screen):
        screen.fill(WARM_BEIGE)

        # Title
        title_surf = self.font_title.render("About Developer", True, PRIMARY_BLUE)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, self.padding))
        screen.blit(title_surf, title_rect)

        if not self.resume_data:
            error_surf = self.font_text.render("Resume data not found.", True, BLACK)
            screen.blit(error_surf, (self.padding, self.padding * 2))
            return

        # Contact Info
        info = self.resume_data.get('contact_info', {})
        y_offset = self.padding * 2.5

        name_surf = self.font_header.render(info.get('name', ''), True, BLACK)
        name_rect = name_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(name_surf, name_rect)
        y_offset += 40

        # Title
        title_text = info.get('title', '')
        title_lines = self.wrap_text(title_text, self.font_text, SCREEN_WIDTH - 2 * self.padding)
        for line in title_lines:
            line_surf = self.font_text.render(line, True, (50, 50, 50))
            line_rect = line_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            screen.blit(line_surf, line_rect)
            y_offset += 30

        y_offset += 20

        # Summary
        summary_surf = self.font_header.render("Professional Summary", True, PRIMARY_BLUE)
        screen.blit(summary_surf, (self.padding, y_offset))
        y_offset += 40

        summary_text = self.resume_data.get('professional_summary', '')
        summary_lines = self.wrap_text(summary_text, self.font_text, SCREEN_WIDTH - 2 * self.padding)

        for line in summary_lines:
            line_surf = self.font_text.render(line, True, BLACK)
            screen.blit(line_surf, (self.padding, y_offset))
            y_offset += 30

        # Instructions
        y_offset = SCREEN_HEIGHT - self.padding
        instr_surf = self.font_text.render("Press ESC to Return", True, (100, 100, 100))
        instr_rect = instr_surf.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
        screen.blit(instr_surf, instr_rect)

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                    self.game.scene_manager.set_scene("menu_scene")

    def update(self, dt):
        pass

    def draw(self, screen):
        self.render_content(screen)
