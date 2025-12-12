import pygame
from game.scenes.base_scene import BaseScene
from config import WHITE, BLACK, CAPTION, PRIMARY_BLUE, WARM_BEIGE, SCREEN_WIDTH, SCREEN_HEIGHT

class MenuScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 74)
        self.option_font = pygame.font.Font(None, 50)

        self.options = ["Start Career", "View Resume", "Exit"]
        self.selected_index = 0

        self.title_text = self.font.render(CAPTION, True, PRIMARY_BLUE)

        # Simple animation state
        self.animation_timer = 0
        self.cursor_visible = True

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.selected_index = (self.selected_index - 1) % len(self.options)
                    if hasattr(self.game, 'audio_manager'):
                        self.game.audio_manager.play_ui_sound('hover')
                elif event.key == pygame.K_DOWN:
                    self.selected_index = (self.selected_index + 1) % len(self.options)
                    if hasattr(self.game, 'audio_manager'):
                        self.game.audio_manager.play_ui_sound('hover')
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    if hasattr(self.game, 'audio_manager'):
                        self.game.audio_manager.play_ui_sound('click')
                    self.select_option()

    def select_option(self):
        option = self.options[self.selected_index]
        if option == "Start Career":
            print("Starting game...")
            self.game.scene_manager.set_scene("game_scene")
        elif option == "View Resume":
            self.game.scene_manager.set_scene("resume_scene")
        elif option == "Exit":
            self.game.running = False

    def update(self, dt):
        self.animation_timer += dt
        if self.animation_timer > 0.5:
            self.cursor_visible = not self.cursor_visible
            self.animation_timer = 0

    def draw_desk_scene(self, screen):
        # Background
        screen.fill(WARM_BEIGE)

        # Floor
        pygame.draw.rect(screen, (200, 180, 150), (0, SCREEN_HEIGHT * 0.7, SCREEN_WIDTH, SCREEN_HEIGHT * 0.3))

        # Desk
        desk_rect = pygame.Rect(SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.6, SCREEN_WIDTH * 0.6, SCREEN_HEIGHT * 0.4)
        pygame.draw.rect(screen, (139, 69, 19), desk_rect) # SaddleBrown

        # Computer Monitor
        monitor_rect = pygame.Rect(SCREEN_WIDTH * 0.35, SCREEN_HEIGHT * 0.45, SCREEN_WIDTH * 0.3, SCREEN_HEIGHT * 0.25)
        pygame.draw.rect(screen, (50, 50, 50), monitor_rect)
        pygame.draw.rect(screen, (30, 30, 30), monitor_rect.inflate(-10, -10)) # Screen bezel

        # Screen content (Blue screen)
        screen_content = monitor_rect.inflate(-20, -20)
        pygame.draw.rect(screen, (0, 0, 150), screen_content)

        # Monitor stand
        pygame.draw.rect(screen, (50, 50, 50), (SCREEN_WIDTH * 0.48, SCREEN_HEIGHT * 0.7, SCREEN_WIDTH * 0.04, SCREEN_HEIGHT * 0.05))
        pygame.draw.rect(screen, (50, 50, 50), (SCREEN_WIDTH * 0.4, SCREEN_HEIGHT * 0.75, SCREEN_WIDTH * 0.2, SCREEN_HEIGHT * 0.02))

        # Player (Back of head/shoulders) - Simplistic
        pygame.draw.circle(screen, (0, 0, 0), (int(SCREEN_WIDTH * 0.5), int(SCREEN_HEIGHT * 0.7)), 40) # Head
        pygame.draw.rect(screen, (20, 20, 100), (SCREEN_WIDTH * 0.42, SCREEN_HEIGHT * 0.7, SCREEN_WIDTH * 0.16, SCREEN_HEIGHT * 0.1)) # Shoulders

    def draw(self, screen):
        self.draw_desk_scene(screen)

        # Draw Title
        title_rect = self.title_text.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4))
        screen.blit(self.title_text, title_rect)

        # Draw Options
        start_y = SCREEN_HEIGHT / 2 + 50
        for i, option in enumerate(self.options):
            color = PRIMARY_BLUE if i == self.selected_index else BLACK
            text_surf = self.option_font.render(option, True, color)
            rect = text_surf.get_rect(center=(SCREEN_WIDTH / 2, start_y + i * 60))
            screen.blit(text_surf, rect)

            if i == self.selected_index and self.cursor_visible:
                # Draw cursor/arrow
                cursor_rect = pygame.Rect(rect.left - 30, rect.centery - 10, 20, 20)
                pygame.draw.polygon(screen, PRIMARY_BLUE, [
                    (cursor_rect.left, cursor_rect.top),
                    (cursor_rect.left, cursor_rect.bottom),
                    (cursor_rect.right, cursor_rect.centery)
                ])