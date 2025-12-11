import pygame
from config import *
from game.scenes.zones.base_zone import BaseZone
from game.entities.player import Player
from game.entities.entity import Entity

class Zone1(BaseZone):
    def __init__(self, game_manager):
        super().__init__(game_manager, 1)
        self.gherkin_puzzles = []
        self.api_terminals = []
        self.completed_gherkin = 0
        self.completed_apis = 0

    def load_zone_data(self):
        # Create player
        player_data = self.game_manager.save_manager.get_player_data()
        self.player = Player(player_data["position"][0], player_data["position"][1])
        self.add_entity(self.player)

        # Create Gherkin puzzle stations
        self.create_gherkin_stations()

        # Create API validation terminals
        self.create_api_terminals()

    def create_gherkin_stations(self):
        stations = [
            {"x": 200, "y": 200, "scenario": "User login"},
            {"x": 400, "y": 300, "scenario": "Data export"},
            {"x": 600, "y": 250, "scenario": "Report generation"}
        ]

        for station in stations:
            # Create visual representation (placeholder rectangle)
            entity = Entity(station["x"], station["y"], 64, 64)
            entity.scenario = station["scenario"]
            entity.completed = False
            entity.render = lambda screen, cx=0, cy=0: pygame.draw.rect(screen, BLUE, (entity.x - cx, entity.y - cy, entity.width, entity.height))
            entity.update = lambda dt: None
            self.gherkin_puzzles.append(entity)
            self.add_entity(entity)

    def create_api_terminals(self):
        terminals = [
            {"x": 150, "y": 400, "endpoint": "/api/users"},
            {"x": 350, "y": 450, "endpoint": "/api/reports"},
            {"x": 550, "y": 350, "endpoint": "/api/data"}
        ]

        for terminal in terminals:
            entity = Entity(terminal["x"], terminal["y"], 48, 48)
            entity.endpoint = terminal["endpoint"]
            entity.validated = False
            entity.render = lambda screen, cx=0, cy=0: pygame.draw.rect(screen, GREEN, (entity.x - cx, entity.y - cy, entity.width, entity.height))
            entity.update = lambda dt: None
            self.api_terminals.append(entity)
            self.add_entity(entity)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == KEYS["INTERACT"]:
            self.check_interactions()

    def check_interactions(self):
        player_center_x = self.player.x + self.player.width // 2
        player_center_y = self.player.y + self.player.height // 2

        # Check Gherkin stations
        for station in self.gherkin_puzzles:
            if not station.completed and abs(player_center_x - (station.x + 32)) < 50 and abs(player_center_y - (station.y + 32)) < 50:
                self.start_gherkin_puzzle(station)
                break

        # Check API terminals
        for terminal in self.api_terminals:
            if not terminal.validated and abs(player_center_x - (terminal.x + 24)) < 40 and abs(player_center_y - (terminal.y + 24)) < 40:
                self.start_api_validation(terminal)
                break

    def start_gherkin_puzzle(self, station):
        # Simple text-based puzzle (placeholder)
        self.show_message(f"Gherkin puzzle completed: {station.scenario}")
        station.completed = True
        self.completed_gherkin += 1
        self.player.experience += 50
        self.game_manager.audio_manager.play_sound("gherkin_complete.wav")
        self.check_completion()

    def start_api_validation(self, terminal):
        # Simple API validation (placeholder)
        self.show_message(f"API validated: {terminal.endpoint}")
        terminal.validated = True
        self.completed_apis += 1
        self.player.experience += 75
        self.game_manager.audio_manager.play_sound("api_validated.wav")
        self.check_completion()

    def get_zone_color(self):
        return (20, 20, 40)  # Dark blue for enterprise zone

    def render_ui(self, screen):
        super().render_ui(screen)

        font = self.game_manager.asset_manager.load_font("default.ttf", 20)

        # Zone progress
        progress_text = font.render(f"Gherkin: {self.completed_gherkin}/{len(self.gherkin_puzzles)}  APIs: {self.completed_apis}/{len(self.api_terminals)}", True, WHITE)
        screen.blit(progress_text, (10, SCREEN_HEIGHT - 40))

    def check_completion(self):
        if self.completed_gherkin == len(self.gherkin_puzzles) and self.completed_apis == len(self.api_terminals):
            completed = self.game_manager.save_manager.get_game_data()["completed_zones"]
            if self.zone_id not in completed:
                completed.append(self.zone_id)
                self.game_manager.save_manager.set_game_data({"completed_zones": completed})
                self.show_message(f"Zone {self.zone_id} completed!")