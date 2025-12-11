import pygame
from config import *
from game.managers.scene_manager import SceneManager
from game.managers.asset_manager import AssetManager
from game.managers.input_manager import InputManager
from game.managers.save_manager import SaveManager
from game.managers.audio_manager import AudioManager
from game.scenes.menu_scene import MenuScene
from game.scenes.game_scene import GameScene

class GameManager:
    def __init__(self):
        self.asset_manager = AssetManager()
        self.input_manager = InputManager()
        self.save_manager = SaveManager()
        self.audio_manager = AudioManager()
        self.scene_manager = SceneManager()
        self.save_timer = 0.0
        self.save_interval = 30.0  # Save every 30 seconds

        # Initialize scenes
        self.scene_manager.add_scene("menu", MenuScene(self))
        self.scene_manager.add_scene("game", GameScene(self))
        self.scene_manager.set_scene("menu")

    def handle_event(self, event):
        self.input_manager.handle_event(event)
        self.scene_manager.handle_event(event)

    def update(self, dt):
        self.input_manager.update(dt)
        self.scene_manager.update(dt)

        # Periodic saving
        self.save_timer += dt
        if self.save_timer >= self.save_interval:
            self.save_manager.save_game()
            self.save_timer = 0.0

    def render(self, screen):
        screen.fill(BLACK)
        self.scene_manager.render(screen)

    def quit_game(self):
        self.save_manager.save_game()
        pygame.event.post(pygame.event.Event(pygame.QUIT))