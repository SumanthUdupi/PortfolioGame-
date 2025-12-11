import pygame
from config import *
from game.scenes.zones.base_zone import BaseZone
from game.entities.player import Player
from game.entities.entity import Entity

class Zone3(BaseZone):
    def __init__(self, game_manager):
        super().__init__(game_manager, 3)
        self.model_workbenches = []
        self.research_terminals = []
        self.completed_models = 0
        self.completed_research = 0

    def load_zone_data(self):
        player_data = self.game_manager.save_manager.get_player_data()
        self.player = Player(player_data["position"][0], player_data["position"][1])
        self.add_entity(self.player)
        self.create_model_workbenches()
        self.create_research_terminals()

    def create_model_workbenches(self):
        workbenches = [
            {"x": 200, "y": 200, "model": "Linear Regression"},
            {"x": 400, "y": 300, "model": "Decision Tree"},
            {"x": 600, "y": 250, "model": "Neural Network"}
        ]
        for wb in workbenches:
            entity = Entity(wb["x"], wb["y"], 64, 64)
            entity.model = wb["model"]
            entity.completed = False
            entity.render = lambda screen, cx=0, cy=0: pygame.draw.rect(screen, TEAL, (entity.x - cx, entity.y - cy, entity.width, entity.height))
            entity.update = lambda dt: None
            self.model_workbenches.append(entity)
            self.add_entity(entity)

    def create_research_terminals(self):
        terminals = [
            {"x": 150, "y": 400, "topic": "Statistical Analysis"},
            {"x": 350, "y": 450, "topic": "Machine Learning"},
            {"x": 550, "y": 350, "topic": "Data Visualization"}
        ]
        for term in terminals:
            entity = Entity(term["x"], term["y"], 48, 48)
            entity.topic = term["topic"]
            entity.completed = False
            entity.render = lambda screen, cx=0, cy=0: pygame.draw.rect(screen, YELLOW, (entity.x - cx, entity.y - cy, entity.width, entity.height))
            entity.update = lambda dt: None
            self.research_terminals.append(entity)
            self.add_entity(entity)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == KEYS["INTERACT"]:
            self.check_interactions()

    def check_interactions(self):
        player_center_x = self.player.x + self.player.width // 2
        player_center_y = self.player.y + self.player.height // 2

        for wb in self.model_workbenches:
            if not wb.completed and abs(player_center_x - (wb.x + 32)) < 50 and abs(player_center_y - (wb.y + 32)) < 50:
                self.build_model(wb)
                break

        for term in self.research_terminals:
            if not term.completed and abs(player_center_x - (term.x + 24)) < 40 and abs(player_center_y - (term.y + 24)) < 40:
                self.conduct_research(term)
                break

    def build_model(self, wb):
        self.show_message(f"Model built: {wb.model}")
        wb.completed = True
        self.completed_models += 1
        self.player.experience += 70
        self.game_manager.audio_manager.play_sound("model_built.wav")
        self.check_completion()

    def conduct_research(self, term):
        self.show_message(f"Research completed: {term.topic}")
        term.completed = True
        self.completed_research += 1
        self.player.experience += 90
        self.game_manager.audio_manager.play_sound("research_complete.wav")
        self.check_completion()

    def get_zone_color(self):
        return (20, 30, 20)  # Dark green for academy

    def render_ui(self, screen):
        super().render_ui(screen)
        font = self.game_manager.asset_manager.load_font("default.ttf", 20)
        progress_text = font.render(f"Models: {self.completed_models}/{len(self.model_workbenches)}  Research: {self.completed_research}/{len(self.research_terminals)}", True, WHITE)
        screen.blit(progress_text, (10, SCREEN_HEIGHT - 40))

    def check_completion(self):
        if self.completed_models == len(self.model_workbenches) and self.completed_research == len(self.research_terminals):
            completed = self.game_manager.save_manager.get_game_data()["completed_zones"]
            if self.zone_id not in completed:
                completed.append(self.zone_id)
                self.game_manager.save_manager.set_game_data({"completed_zones": completed})
                self.show_message(f"Zone {self.zone_id} completed!")