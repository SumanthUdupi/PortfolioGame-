from config import *
from game.scenes.base_scene import BaseScene
from game.systems.collision_system import CollisionSystem

class BaseZone(BaseScene):
    def __init__(self, game_manager, zone_id):
        super().__init__(game_manager)
        self.zone_id = zone_id
        self.entities = []
        self.player = None
        self.camera_x = 0
        self.camera_y = 0
        self.current_message = None
        self.message_timer = 0.0

    def on_enter(self):
        # Load zone-specific data
        self.load_zone_data()

        # Audio & Atmosphere: Start zone music and ambient
        # REQ-AUDIO-01: Zone-Specific Soundtracks
        # REQ-AUDIO-05: Ambient Layers
        if hasattr(self.game_manager, 'audio_manager'):
            self.game_manager.audio_manager.play_music(self.zone_id)
            self.game_manager.audio_manager.start_ambient(self.zone_id)

    def on_exit(self):
        # Clear entities to prevent memory leaks
        self.entities.clear()

    def show_message(self, message, duration=3.0):
        self.current_message = message
        self.message_timer = duration
        # Typewriter effect state
        self.displayed_text = ""
        self.typewriter_timer = 0
        self.typewriter_speed = 0.05
        self.text_index = 0

    def check_completion(self):
        # Override in subclasses
        pass

    def load_zone_data(self):
        # Override in subclasses
        pass

    def add_entity(self, entity):
        self.entities.append(entity)

    def remove_entity(self, entity):
        if entity in self.entities:
            self.entities.remove(entity)

    def update(self, dt):
        # Update player
        if self.player:
            self.player.update(dt, self.game_manager.input_manager, self.entities)

        # Update other entities
        for entity in self.entities:
            if entity != self.player:
                entity.update(dt)

        # Update camera to follow player
        if self.player:
            self.camera_x = self.player.x - SCREEN_WIDTH // 2
            self.camera_y = self.player.y - SCREEN_HEIGHT // 2

            # Clamp camera to world bounds
            self.camera_x = max(0, min(self.camera_x, WORLD_WIDTH - SCREEN_WIDTH))
            self.camera_y = max(0, min(self.camera_y, WORLD_HEIGHT - SCREEN_HEIGHT))

        # Update message timer and typewriter effect
        if self.message_timer > 0:
            self.message_timer -= dt
            if self.message_timer <= 0:
                self.current_message = None
                self.displayed_text = ""

            # Typewriter update
            if self.current_message and self.text_index < len(self.current_message):
                self.typewriter_timer += dt
                if self.typewriter_timer >= self.typewriter_speed:
                    self.typewriter_timer = 0
                    self.text_index += 1
                    self.displayed_text = self.current_message[:self.text_index]
                    # Play typing sound
                    if hasattr(self.game_manager, 'audio_manager'):
                        self.game_manager.audio_manager.play_typing_sound()
            elif self.current_message:
                self.displayed_text = self.current_message

    def render(self, screen):
        # Clear screen with zone-specific color
        screen.fill(self.get_zone_color())

        # Render entities
        for entity in self.entities:
            entity.render(screen, self.camera_x, self.camera_y)

        # Render UI
        self.render_ui(screen)

    def get_zone_color(self):
        # Override in subclasses
        return BLACK

    def render_ui(self, screen):
        # Render HUD elements
        font = self.game_manager.asset_manager.load_font("default.ttf", 24)

        # Zone name
        zone_text = font.render(f"Zone {self.zone_id}: {ZONES[self.zone_id]}", True, WHITE)
        screen.blit(zone_text, (10, 10))

        # Player stats
        if self.player:
            level_text = font.render(f"Level: {self.player.level}", True, WHITE)
            exp_text = font.render(f"XP: {self.player.experience}", True, WHITE)
            screen.blit(level_text, (10, 40))
            screen.blit(exp_text, (10, 70))

        # Interaction message
        if self.current_message:
            msg_font = self.game_manager.asset_manager.load_font("default.ttf", 20)
            # Use displayed_text instead of current_message for typewriter effect
            text_to_render = getattr(self, 'displayed_text', self.current_message)
            msg_text = msg_font.render(text_to_render, True, YELLOW)
            msg_x = SCREEN_WIDTH // 2 - msg_text.get_width() // 2
            msg_y = SCREEN_HEIGHT - 50
            screen.blit(msg_text, (msg_x, msg_y))