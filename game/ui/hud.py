import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, WHITE, BLACK, PRIMARY_BLUE

class HUD:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 32)

    def draw(self, screen):
        # Experience/Level Bar at the top
        self.draw_experience_bar(screen)

        # Current Job Title (Zone name)
        self.draw_zone_info(screen)

    def draw_experience_bar(self, screen):
        # Placeholder for experience.
        # Assuming player has .experience and .level attributes or we use placeholders.
        # Since I don't see Player class implementation details yet, I'll assume some values or check Player class.

        player = self.game.scene_manager.scenes.get('game_scene').player if 'game_scene' in self.game.scene_manager.scenes else None

        # Let's check if player exists and has attributes, otherwise defaults.
        level = getattr(player, 'level', 1)
        experience = getattr(player, 'experience', 0)
        max_experience = getattr(player, 'max_experience', 100)

        bar_width = SCREEN_WIDTH * 0.8
        bar_height = 20
        x = (SCREEN_WIDTH - bar_width) / 2
        y = 10

        # Background
        pygame.draw.rect(screen, (50, 50, 50), (x, y, bar_width, bar_height))

        # Progress
        fill_width = int(bar_width * (experience / max_experience))
        pygame.draw.rect(screen, PRIMARY_BLUE, (x, y, fill_width, bar_height))

        # Border
        pygame.draw.rect(screen, WHITE, (x, y, bar_width, bar_height), 2)

        # Text
        text = self.font.render(f"Level {level}", True, WHITE)
        text_rect = text.get_rect(midleft=(x + 10, y + bar_height / 2))
        screen.blit(text, text_rect)

        xp_text = self.font.render(f"{experience}/{max_experience}", True, WHITE)
        xp_rect = xp_text.get_rect(midright=(x + bar_width - 10, y + bar_height / 2))
        screen.blit(xp_text, xp_rect)

    def draw_zone_info(self, screen):
        # Current Zone Name
        # Assuming GameScene has current_zone or active_zone
        game_scene = self.game.scene_manager.scenes.get('game_scene')
        zone_name = "Unknown Zone"
        if game_scene:
            # Check how zone is stored. Based on memory, there are Zones.
            # I'll check GameScene code in a moment, but for now placeholder.
            if hasattr(game_scene, 'current_zone') and game_scene.current_zone:
                 zone_name = getattr(game_scene.current_zone, 'name', "Zone 1")
            elif hasattr(game_scene, 'active_zone'):
                 zone_name = getattr(game_scene.active_zone, 'name', "Zone 1")

        # Draw styled box for Zone Name
        text = self.title_font.render(zone_name, True, WHITE)
        padding = 10
        box_width = text.get_width() + 2 * padding
        box_height = text.get_height() + 2 * padding

        x = 20
        y = SCREEN_HEIGHT - box_height - 20

        # Box background
        s = pygame.Surface((box_width, box_height))
        s.set_alpha(200)
        s.fill((0, 0, 0))
        screen.blit(s, (x, y))

        # Border
        pygame.draw.rect(screen, PRIMARY_BLUE, (x, y, box_width, box_height), 2)

        # Text
        screen.blit(text, (x + padding, y + padding))
