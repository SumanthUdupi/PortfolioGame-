import unittest
import pygame
from game.scenes.menu_scene import MenuScene

class MockGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 600))
        self.running = True
        self.scene_manager = MockSceneManager()

class MockSceneManager:
    def __init__(self):
        self.current_scene = None

    def set_scene(self, scene_name):
        self.current_scene = scene_name

class TestMenuScene(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = MockGame()
        self.menu_scene = MenuScene(self.game)

    def tearDown(self):
        pygame.quit()

    def test_menu_options(self):
        self.assertEqual(self.menu_scene.options, ["Start Career", "View Resume", "Exit"])

    def test_menu_navigation(self):
        # Initial selection
        self.assertEqual(self.menu_scene.selected_index, 0)

        # Press Down
        self.menu_scene.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)])
        self.assertEqual(self.menu_scene.selected_index, 1)

        # Press Down again
        self.menu_scene.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)])
        self.assertEqual(self.menu_scene.selected_index, 2)

        # Wrap around
        self.menu_scene.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)])
        self.assertEqual(self.menu_scene.selected_index, 0)

        # Press Up
        self.menu_scene.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)])
        self.assertEqual(self.menu_scene.selected_index, 2)

    def test_select_start_career(self):
        self.menu_scene.selected_index = 0
        self.menu_scene.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)])
        self.assertEqual(self.game.scene_manager.current_scene, "game_scene")

    def test_select_view_resume(self):
        self.menu_scene.selected_index = 1
        self.menu_scene.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)])
        self.assertEqual(self.game.scene_manager.current_scene, "resume_scene")

    def test_select_exit(self):
        self.menu_scene.selected_index = 2
        self.menu_scene.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)])
        self.assertFalse(self.game.running)
