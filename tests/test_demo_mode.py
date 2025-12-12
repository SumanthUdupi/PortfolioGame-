import unittest
import pygame
from game.scenes.menu_scene import MenuScene
from game.scenes.game_scene import GameScene

class MockGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.running = True
        self.scene_manager = MockSceneManager(self)
        self.audio_manager = MockAudioManager()

class MockAudioManager:
    def play_ui_sound(self, sound):
        pass

class MockSceneManager:
    def __init__(self, game):
        self.scenes = {}
        self.current_scene = None
        self.game = game

    def add_scene(self, name, scene):
        self.scenes[name] = scene

    def set_scene(self, scene_name):
        self.current_scene = scene_name
        if scene_name == "game_scene" and self.scenes.get("game_scene").demo_mode:
            # Simulate entering demo
            pass

class TestDemoMode(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = MockGame()
        self.menu_scene = MenuScene(self.game)
        self.game_scene = GameScene(self.game)
        self.game.scene_manager.add_scene("menu_scene", self.menu_scene)
        self.game.scene_manager.add_scene("game_scene", self.game_scene)

    def tearDown(self):
        pygame.quit()

    def test_idle_timer_increment(self):
        self.menu_scene.idle_timer = 0
        self.menu_scene.update(1.0)
        self.assertEqual(self.menu_scene.idle_timer, 1.0)

    def test_idle_timer_reset(self):
        self.menu_scene.idle_timer = 5.0
        # Send an event
        self.menu_scene.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)])
        self.assertEqual(self.menu_scene.idle_timer, 0)

    def test_start_demo_mode(self):
        self.menu_scene.idle_timer = 61.0
        self.menu_scene.update(0.1) # Trigger check
        # Since update calls start_demo_mode which sets scene
        self.assertEqual(self.game.scene_manager.current_scene, "game_scene")
        self.assertTrue(self.game_scene.demo_mode)

    def test_exit_demo_mode(self):
        self.game_scene.enter_demo_mode()
        self.assertTrue(self.game_scene.demo_mode)

        # Simulate input
        self.game_scene.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)])

        self.assertFalse(self.game_scene.demo_mode)
        self.assertEqual(self.game.scene_manager.current_scene, "menu_scene")

    def test_demo_movement(self):
        self.game_scene.enter_demo_mode()
        initial_x = self.game_scene.player.velocity.x

        self.game_scene.update(0.1)
        # Should be moving right initially
        self.assertTrue(self.game_scene.player.velocity.x > 0)
