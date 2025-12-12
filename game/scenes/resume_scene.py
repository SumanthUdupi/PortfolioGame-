import pygame
from game.scenes.base_scene import BaseScene
from game.managers.asset_manager import AssetManager
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, WARM_BEIGE, PRIMARY_BLUE

class ResumeScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.asset_manager = AssetManager()
        self.resume_data = self.asset_manager.get_json('resume.json')
        self.font_title = pygame.font.Font(None, 40)
        self.font_header = pygame.font.Font(None, 32)
        self.font_text = pygame.font.Font(None, 24)

        self.scroll_y = 0
        self.content_height = 0
        self.surface = None
        self.padding = 40

        # Tooltip state
        self.skill_rects = []
        self.tooltip_text = None
        self.tooltip_pos = (0, 0)

        if self.resume_data:
            self.render_resume_surface()

    def render_resume_surface(self):
        # Calculate height first (rough estimation or dynamic)
        # For now, let's render to a large surface and then crop/blit

        lines = []
        self.skill_rects = []

        def add_line(text, font, color=BLACK, spacing=5, is_skill=False):
            lines.append({"text": text, "font": font, "color": color, "spacing": spacing, "is_skill": is_skill})

        # Process data
        info = self.resume_data.get('contact_info', {})
        add_line(info.get('name', 'Name'), self.font_title, PRIMARY_BLUE, 10)
        add_line(info.get('title', 'Title'), self.font_header, BLACK, 5)
        add_line(f"{info.get('location', '')} | {info.get('phone', '')} | {info.get('email', '')}", self.font_text, BLACK, 20)

        add_line("Professional Summary", self.font_header, PRIMARY_BLUE, 5)
        summary = self.resume_data.get('professional_summary', '')
        # Simple word wrap would be good here, but for now just add it
        self.wrap_text(summary, self.font_text, lines, SCREEN_WIDTH - 2 * self.padding)
        add_line("", self.font_text, BLACK, 10)

        add_line("Skills", self.font_header, PRIMARY_BLUE, 5)
        skills = self.resume_data.get('skills', {})
        for category, items in skills.items():
            cat_text = category.replace('_', ' ').title() + ": " + ", ".join(items)
            self.wrap_text(cat_text, self.font_text, lines, SCREEN_WIDTH - 2 * self.padding, is_skill=True)
        add_line("", self.font_text, BLACK, 10)

        add_line("Professional Experience", self.font_header, PRIMARY_BLUE, 5)
        for job in self.resume_data.get('professional_experience', []):
            role_line = f"{job.get('role')} at {job.get('company')}"
            add_line(role_line, self.font_header, BLACK, 2)
            add_line(job.get('dates', ''), self.font_text, BLACK, 5)
            for ach in job.get('key_achievements', []):
                self.wrap_text(f"- {ach}", self.font_text, lines, SCREEN_WIDTH - 2 * self.padding)
            add_line("", self.font_text, BLACK, 10)

        add_line("Education", self.font_header, PRIMARY_BLUE, 5)
        for edu in self.resume_data.get('education', []):
            add_line(f"{edu.get('degree')}, {edu.get('institution')} ({edu.get('year')})", self.font_text, BLACK, 5)
        add_line("", self.font_text, BLACK, 10)

        add_line("Certifications", self.font_header, PRIMARY_BLUE, 5)
        for cert in self.resume_data.get('certifications', []):
             add_line(f"- {cert}", self.font_text, BLACK, 5)

        # Calculate total height
        total_height = self.padding * 2
        for line in lines:
            total_height += line['font'].get_height() + line['spacing']

        self.content_height = total_height
        self.surface = pygame.Surface((SCREEN_WIDTH, total_height))
        self.surface.fill(WARM_BEIGE)

        y = self.padding
        for line in lines:
            rendered = line['font'].render(line['text'], True, line['color'])
            rect = rendered.get_rect(topleft=(self.padding, y))
            self.surface.blit(rendered, rect)

            if line.get('is_skill'):
                self.skill_rects.append(rect)

            y += line['font'].get_height() + line['spacing']

    def wrap_text(self, text, font, lines_list, max_width, is_skill=False):
        words = text.split(' ')
        current_line = []

        for word in words:
            test_line = ' '.join(current_line + [word])
            w, h = font.size(test_line)
            if w <= max_width:
                current_line.append(word)
            else:
                lines_list.append({"text": ' '.join(current_line), "font": font, "color": BLACK, "spacing": 2, "is_skill": is_skill})
                current_line = [word]
        if current_line:
            lines_list.append({"text": ' '.join(current_line), "font": font, "color": BLACK, "spacing": 2, "is_skill": is_skill})

    def handle_events(self, events):
        # Mouse hover detection for tooltip
        mouse_pos = pygame.mouse.get_pos()
        # Adjust mouse_pos by scroll_y to match surface coordinates
        surface_mouse_y = mouse_pos[1] + self.scroll_y

        self.tooltip_text = None
        for rect in self.skill_rects:
            if rect.collidepoint(mouse_pos[0], surface_mouse_y):
                self.tooltip_text = "Verified by: Project PortfolioGame"
                self.tooltip_pos = (mouse_pos[0] + 10, mouse_pos[1] + 10)
                break

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_i:
                    self.game.scene_manager.set_scene("menu_scene")
            elif event.type == pygame.MOUSEWHEEL:
                self.scroll_y -= event.y * 20

        # Clamp scroll
        max_scroll = max(0, self.content_height - SCREEN_HEIGHT)
        self.scroll_y = max(0, min(self.scroll_y, max_scroll))

    def update(self, dt):
        pass

    def draw(self, screen):
        screen.fill(BLACK)
        if self.surface:
            # Draw the visible part of the surface
            visible_rect = pygame.Rect(0, self.scroll_y, SCREEN_WIDTH, SCREEN_HEIGHT)
            screen.blit(self.surface, (0, 0), visible_rect)

            # Draw scroll bar if needed
            if self.content_height > SCREEN_HEIGHT:
                scroll_ratio = self.scroll_y / (self.content_height - SCREEN_HEIGHT)
                bar_height = max(20, (SCREEN_HEIGHT / self.content_height) * SCREEN_HEIGHT)
                bar_y = scroll_ratio * (SCREEN_HEIGHT - bar_height)
                pygame.draw.rect(screen, PRIMARY_BLUE, (SCREEN_WIDTH - 10, bar_y, 8, bar_height))

        # Draw tooltip
        if self.tooltip_text:
            tooltip_surf = self.font_text.render(self.tooltip_text, True, WHITE, (50, 50, 50))
            # Ensure tooltip stays on screen
            tooltip_rect = tooltip_surf.get_rect(topleft=self.tooltip_pos)
            if tooltip_rect.right > SCREEN_WIDTH:
                tooltip_rect.right = SCREEN_WIDTH - 5
            if tooltip_rect.bottom > SCREEN_HEIGHT:
                tooltip_rect.bottom = SCREEN_HEIGHT - 5

            screen.blit(tooltip_surf, tooltip_rect)
