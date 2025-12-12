import pygame

class BaseScene:
    def __init__(self, game):
        self.game = game

    def enter(self):
        # Called when the scene becomes active
        pass

    def exit(self):
        # Called when the scene becomes inactive
        pass

    def handle_events(self, events):
        # Handle input events specific to this scene
        pass

    def update(self, dt):
        # Update game logic specific to this scene
        pass

    def draw(self, screen):
        # Draw elements specific to this scene
        pass