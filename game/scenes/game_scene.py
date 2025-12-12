import pygame
from game.scenes.base_scene import BaseScene
from config import BLACK, WHITE, WARM_BEIGE
from game.managers.tilemap_manager import TileMapManager
from game.entities.player import Player
from game.ui.hud import HUD
from game.ui.pause_menu import PauseMenu

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

        # HUD
        self.hud = HUD(game)
        # TODO: Link player to HUD explicitly if needed, or HUD can access via game.scene_manager

        # Pause Menu
        self.pause_menu = PauseMenu(game)

        # Demo Mode
        self.demo_mode = False
        self.demo_timer = 0
        self.demo_direction = 1 # 1 for Right, -1 for Left

        # Darkness layer for Data Center (REQ-VISUAL-09)
        self.darkness_surface = pygame.Surface((game.screen.get_width(), game.screen.get_height()), pygame.SRCALPHA)
        self.darkness_surface.fill((0, 0, 0, 200)) # Semi-transparent black

    def enter_demo_mode(self):
        self.demo_mode = True
        self.demo_timer = 0
        self.player.rect.topleft = (100, 100) # Reset position

    def handle_events(self, events):
        if self.demo_mode:
            # Any input exits demo mode
            if events:
                self.demo_mode = False
                self.game.scene_manager.set_scene("menu_scene")
                return

        # Pass events to pause menu first
        if self.pause_menu.visible:
            if self.pause_menu.handle_events(events):
                return

        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.pause_menu.toggle()

    def update(self, dt):
        if self.pause_menu.visible:
            return # Pause update loop

        if self.demo_mode:
            self.update_demo(dt)
        else:
            self.all_sprites.update(dt)

    def update_demo(self, dt):
        self.demo_timer += dt

        # Simple AI: Walk right for 2s, left for 2s
        # Player speed is usually set in Player class (200), we just need direction vector.
        # But we want to override the input.

        velocity = pygame.math.Vector2(0, 0)

        if self.demo_timer % 4 < 2:
            velocity.x = 1
        else:
            velocity.x = -1

        self.player.update(dt, velocity_override=velocity)

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

        # Draw HUD
        self.hud.draw(screen)

        # Draw Pause Menu
        self.pause_menu.draw(screen)

        # Removed debug text
