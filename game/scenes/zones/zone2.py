import pygame
from config import *
from game.scenes.zones.base_zone import BaseZone
from game.entities.player import Player
from game.entities.entity import Entity

class Zone2(BaseZone):
    def __init__(self, game_manager):
        super().__init__(game_manager, 2)
        self.sql_terminals = []
        self.analytics_dashboards = []
        self.completed_sql = 0
        self.completed_analytics = 0

    def load_zone_data(self):
        player_data = self.game_manager.save_manager.get_player_data()
        self.player = Player(player_data["position"][0], player_data["position"][1])
        self.add_entity(self.player)

        self.create_sql_terminals()
        self.create_analytics_dashboards()

    def create_sql_terminals(self):
        terminals = [
            {"x": 200, "y": 200, "query": "SELECT users FROM database"},
            {"x": 400, "y": 300, "query": "JOIN tables ON condition"},
            {"x": 600, "y": 250, "query": "GROUP BY aggregate"}
        ]

        for terminal in terminals:
            entity = Entity(terminal["x"], terminal["y"], 64, 64)
            entity.query = terminal["query"]
            entity.completed = False
            entity.render = lambda screen, cx=0, cy=0: pygame.draw.rect(screen, PURPLE, (entity.x - cx, entity.y - cy, entity.width, entity.height))
            entity.update = lambda dt: None
            self.sql_terminals.append(entity)
            self.add_entity(entity)

    def create_analytics_dashboards(self):
        dashboards = [
            {"x": 150, "y": 400, "type": "Sales Analytics"},
            {"x": 350, "y": 450, "type": "User Metrics"},
            {"x": 550, "y": 350, "type": "Performance Data"}
        ]

        for dashboard in dashboards:
            entity = Entity(dashboard["x"], dashboard["y"], 48, 48)
            entity.type = dashboard["type"]
            entity.completed = False
            entity.render = lambda screen, cx=0, cy=0: pygame.draw.rect(screen, ORANGE, (entity.x - cx, entity.y - cy, entity.width, entity.height))
            entity.update = lambda dt: None
            self.analytics_dashboards.append(entity)
            self.add_entity(entity)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == KEYS["INTERACT"]:
            self.check_interactions()

    def check_interactions(self):
        player_center_x = self.player.x + self.player.width // 2
        player_center_y = self.player.y + self.player.height // 2

        for terminal in self.sql_terminals:
            if not terminal.completed and abs(player_center_x - (terminal.x + 32)) < 50 and abs(player_center_y - (terminal.y + 32)) < 50:
                self.solve_sql_query(terminal)
                break

        for dashboard in self.analytics_dashboards:
            if not dashboard.completed and abs(player_center_x - (dashboard.x + 24)) < 40 and abs(player_center_y - (dashboard.y + 24)) < 40:
                self.create_analytics_dashboard(dashboard)
                break

    def solve_sql_query(self, terminal):
        self.show_message(f"SQL query solved: {terminal.query}")
        terminal.completed = True
        self.completed_sql += 1
        self.player.experience += 60
        self.game_manager.audio_manager.play_sound("sql_success.wav")
        self.check_completion()

    def create_analytics_dashboard(self, dashboard):
        self.show_message(f"Analytics dashboard created: {dashboard.type}")
        dashboard.completed = True
        self.completed_analytics += 1
        self.player.experience += 80
        self.game_manager.audio_manager.play_sound("dashboard_created.wav")
        self.check_completion()

    def get_zone_color(self):
        return (10, 10, 20)  # Dark purple for data zone

    def update(self, dt):
        super().update(dt)
        # REQ-AUDIO-03: Spatial Audio (Simple)
        # Update spatial audio for terminals (simulating server fans)
        if hasattr(self.game_manager, 'audio_manager') and self.player:
            player_pos = (self.player.x, self.player.y)
            # Use the first terminal as the main server fan noise source
            if self.sql_terminals:
                server = self.sql_terminals[0]
                # Calculate volume based on distance
                max_dist = 400
                dx = server.x - player_pos[0]
                dy = server.y - player_pos[1]
                dist = (dx*dx + dy*dy)**0.5

                if dist <= max_dist:
                    volume = 1.0 - (dist / max_dist)
                    volume = max(0.1, min(1.0, volume))
                else:
                    volume = 0.1 # Minimum volume when far away

                # Update ambient volume (assuming ambient track in this zone is the server hum)
                self.game_manager.audio_manager.set_ambient_volume(volume)

    def render_ui(self, screen):
        super().render_ui(screen)
        font = self.game_manager.asset_manager.load_font("default.ttf", 20)
        progress_text = font.render(f"SQL: {self.completed_sql}/{len(self.sql_terminals)}  Analytics: {self.completed_analytics}/{len(self.analytics_dashboards)}", True, WHITE)
        screen.blit(progress_text, (10, SCREEN_HEIGHT - 40))

    def check_completion(self):
        if self.completed_sql == len(self.sql_terminals) and self.completed_analytics == len(self.analytics_dashboards):
            completed = self.game_manager.save_manager.get_game_data()["completed_zones"]
            if self.zone_id not in completed:
                completed.append(self.zone_id)
                self.game_manager.save_manager.set_game_data({"completed_zones": completed})
                self.show_message(f"Zone {self.zone_id} completed!")