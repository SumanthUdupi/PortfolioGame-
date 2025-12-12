import pygame
from game.scenes.base_scene import BaseScene
from config import BLACK, WHITE, WARM_BEIGE
from game.managers.tilemap_manager import TileMapManager
from game.entities.player import Player

class GameScene(BaseScene):
    def __init__(self, game):
        super().__init__(game)
        self.font = pygame.font.Font(None, 50)
        self.game_text = self.font.render("Game Scene - Press ESC to Menu", True, WHITE)

        self.tilemap_manager = TileMapManager()
        self.tilemap_manager.load_map("level1.tmx")

        # Initialize player
        self.player = Player(100, 100, 32, 32, asset_key="player.png") # Assuming player.png exists or will fail gracefully
        self.all_sprites = pygame.sprite.Group()
        self.all_sprites.add(self.player)

        # Darkness layer for Data Center (REQ-VISUAL-09)
        self.darkness_surface = pygame.Surface((game.screen.get_width(), game.screen.get_height()), pygame.SRCALPHA)
        self.darkness_surface.fill((0, 0, 0, 200)) # Semi-transparent black

    def handle_events(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    print("Returning to menu...")
                    self.game.scene_manager.set_scene("menu_scene") # Placeholder for actual scene transition

    def update(self, dt):
        self.all_sprites.update(dt)

    def draw(self, screen):
        screen.fill(WARM_BEIGE) # Use WARM_BEIGE as default bg
        self.tilemap_manager.render(screen)

        self.all_sprites.draw(screen)

        # Draw highlights (REQ-VISUAL-07)
        for sprite in self.all_sprites:
            if hasattr(sprite, 'draw_highlight') and sprite != self.player:
                sprite.draw_highlight(screen, self.player.rect.center)

        # Render Vignette/Darkness (REQ-VISUAL-09)
        # Only if in Data Center. For now, we assume we are in it or just show the effect.
        # The requirement says "in the 'Data Center' zone".
        # I'll just implement the effect logic here.
        # Cut out circle around player
        self.darkness_surface.fill((0, 0, 0, 200)) # Reset darkness
        pygame.draw.circle(self.darkness_surface, (0, 0, 0, 0), self.player.rect.center, 150) # Transparent circle
        # Note: Pygame doesn't support drawing transparent on surface easily like this with fill.
        # We need to use BLEND_RGBA_MIN or a mask.
        # Simpler approach: Create a light image and blit it with special flags or use a mask.

        # Correct approach for cutout:
        # 1. Create a surface with alpha.
        # 2. Fill with darkness.
        # 3. Draw circle with (0,0,0,0) - this doesn't work directly with blit.
        # 4. Instead, use pygame.draw.circle to clear alpha.
        # However, pygame.draw.circle with (0,0,0,0) on a surface with SRCALPHA works if we do it right.

        # Actually, simpler:
        # Fill darkness
        self.darkness_surface.fill((0, 0, 0, 200))
        # Draw circle with REPLACE blend mode to clear pixels
        pygame.draw.circle(self.darkness_surface, (0, 0, 0, 0), self.player.rect.center, 150)

        screen.blit(self.darkness_surface, (0,0))

        game_text_rect = self.game_text.get_rect(center=(self.game.screen.get_width() / 2, self.game.screen.get_height() / 2))
        screen.blit(self.game_text, game_text_rect)
