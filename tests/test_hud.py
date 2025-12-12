import unittest
import pygame
from game.ui.hud import HUD
from game.scenes.game_scene import GameScene

class MockGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.scene_manager = MockSceneManager()

class MockSceneManager:
    def __init__(self):
        self.scenes = {}

class TestHUD(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = MockGame()
        self.hud = HUD(self.game)

    def tearDown(self):
        pygame.quit()

    def test_hud_draw(self):
        # Just ensure no crashes when drawing
        self.hud.draw(self.game.screen)

    def test_hud_with_game_scene(self):
        game_scene = GameScene(self.game)
        self.game.scene_manager.scenes['game_scene'] = game_scene
        self.hud.draw(self.game.screen)
