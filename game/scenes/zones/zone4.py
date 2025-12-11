import pygame
from config import *
from game.scenes.zones.base_zone import BaseZone
from game.entities.player import Player
from game.entities.entity import Entity

class Zone4(BaseZone):
    def __init__(self, game_manager):
        super().__init__(game_manager, 4)
        self.blueprint_tables = []
        self.qa_stations = []
        self.completed_blueprints = 0
        self.completed_qa = 0

    def load_zone_data(self):
        player_data = self.game_manager.save_manager.get_player_data()
        self.player = Player(player_data["position"][0], player_data["position"][1])
        self.add_entity(self.player)
        self.create_blueprint_tables()
        self.create_qa_stations()

    def create_blueprint_tables(self):
        tables = [
            {"x": 200, "y": 200, "system": "Process Control"},
            {"x": 400, "y": 300, "system": "Quality Management"},
            {"x": 600, "y": 250, "system": "Safety Systems"}
        ]
        for table in tables:
            entity = Entity(table["x"], table["y"], 64, 64)
            entity.system = table["system"]
            entity.completed = False
            entity.render = lambda screen, cx=0, cy=0: pygame.draw.rect(screen, ORANGE, (entity.x - cx, entity.y - cy, entity.width, entity.height))
            entity.update = lambda dt: None
            self.blueprint_tables.append(entity)
            self.add_entity(entity)

    def create_qa_stations(self):
        stations = [
            {"x": 150, "y": 400, "test": "System Validation"},
            {"x": 350, "y": 450, "test": "Performance Testing"},
            {"x": 550, "y": 350, "test": "Safety Compliance"}
        ]
        for station in stations:
            entity = Entity(station["x"], station["y"], 48, 48)
            entity.test = station["test"]
            entity.completed = False
            entity.render = lambda screen, cx=0, cy=0: pygame.draw.rect(screen, RED, (entity.x - cx, entity.y - cy, entity.width, entity.height))
            entity.update = lambda dt: None
            self.qa_stations.append(entity)
            self.add_entity(entity)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == KEYS["INTERACT"]:
            self.check_interactions()

    def check_interactions(self):
        player_center_x = self.player.x + self.player.width // 2
        player_center_y = self.player.y + self.player.height // 2

        for table in self.blueprint_tables:
            if not table.completed and abs(player_center_x - (table.x + 32)) < 50 and abs(player_center_y - (table.y + 32)) < 50:
                self.design_blueprint(table)
                break

        for station in self.qa_stations:
            if not station.completed and abs(player_center_x - (station.x + 24)) < 40 and abs(player_center_y - (station.y + 24)) < 40:
                self.perform_qa_test(station)
                break

    def design_blueprint(self, table):
        self.show_message(f"Blueprint designed: {table.system}")
        table.completed = True
        self.completed_blueprints += 1
        self.player.experience += 85
        self.game_manager.audio_manager.play_sound("blueprint_done.wav")
        self.check_completion()

    def perform_qa_test(self, station):
        self.show_message(f"QA test completed: {station.test}")
        station.completed = True
        self.completed_qa += 1
        self.player.experience += 65
        self.game_manager.audio_manager.play_sound("qa_complete.wav")
        self.check_completion()

    def get_zone_color(self):
        return (30, 20, 10)  # Brown for workshop

    def render_ui(self, screen):
        super().render_ui(screen)
        font = self.game_manager.asset_manager.load_font("default.ttf", 20)
        progress_text = font.render(f"Blueprints: {self.completed_blueprints}/{len(self.blueprint_tables)}  QA: {self.completed_qa}/{len(self.qa_stations)}", True, WHITE)
        screen.blit(progress_text, (10, SCREEN_HEIGHT - 40))

    def check_completion(self):
        if self.completed_blueprints == len(self.blueprint_tables) and self.completed_qa == len(self.qa_stations):
            completed = self.game_manager.save_manager.get_game_data()["completed_zones"]
            if self.zone_id not in completed:
                completed.append(self.zone_id)
                self.game_manager.save_manager.set_game_data({"completed_zones": completed})
                self.show_message(f"Zone {self.zone_id} completed!")