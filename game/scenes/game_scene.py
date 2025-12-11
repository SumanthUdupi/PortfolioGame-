import pygame
from config import *
from game.scenes.base_scene import BaseScene
from game.scenes.zones.zone1 import Zone1
from game.scenes.zones.zone2 import Zone2
from game.scenes.zones.zone3 import Zone3
from game.scenes.zones.zone4 import Zone4

class GameScene(BaseScene):
    def __init__(self, game_manager):
        super().__init__(game_manager)
        self.current_zone_id = 1
        self.zones = {}
        self.current_zone = None
        self.initialize_zones()

    def initialize_zones(self):
        self.zones = {
            1: Zone1(self.game_manager),
            2: Zone2(self.game_manager),
            3: Zone3(self.game_manager),
            4: Zone4(self.game_manager)
        }
        self.set_zone(self.current_zone_id)

    def set_zone(self, zone_id):
        if zone_id in self.zones:
            if self.current_zone:
                self.current_zone.on_exit()
            self.current_zone = self.zones[zone_id]
            self.current_zone_id = zone_id
            self.current_zone.on_enter()

            # Update save data
            if self.current_zone.player:
                player_pos = [self.current_zone.player.x, self.current_zone.player.y]
                self.game_manager.save_manager.set_player_data({
                    "position": player_pos,
                    "zone": zone_id
                })
                self.game_manager.save_manager.set_game_data({
                    "current_zone": zone_id
                })
                self.game_manager.save_manager.save_game()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                self.set_zone(1)
            elif event.key == pygame.K_2:
                self.set_zone(2)
            elif event.key == pygame.K_3:
                self.set_zone(3)
            elif event.key == pygame.K_4:
                self.set_zone(4)
            elif event.key == KEYS["PAUSE"]:
                self.game_manager.scene_manager.set_scene("menu")
            else:
                if self.current_zone:
                    self.current_zone.handle_event(event)

    def update(self, dt):
        if self.current_zone:
            self.current_zone.update(dt)

    def render(self, screen):
        if self.current_zone:
            self.current_zone.render(screen)

        # Render zone selection UI
        self.render_zone_selector(screen)

    def render_zone_selector(self, screen):
        font = self.game_manager.asset_manager.load_font("default.ttf", 18)

        # Zone selector in top right
        selector_x = SCREEN_WIDTH - 200
        selector_y = 10

        pygame.draw.rect(screen, (50, 50, 50), (selector_x - 10, selector_y - 5, 190, 120))

        for i in range(1, 5):
            color = YELLOW if i == self.current_zone_id else WHITE
            zone_name = ZONES[i][:12]  # Truncate long names
            text = font.render(f"{i}: {zone_name}", True, color)
            screen.blit(text, (selector_x, selector_y + (i-1) * 25))

        # Instructions
        instr_font = self.game_manager.asset_manager.load_font("default.ttf", 14)
        instr_text = instr_font.render("Press 1-4 to switch zones", True, WHITE)
        screen.blit(instr_text, (selector_x, selector_y + 105))