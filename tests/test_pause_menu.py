import unittest
import pygame
from game.ui.pause_menu import PauseMenu
from game.scenes.game_scene import GameScene

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

class TestPauseMenu(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = MockGame()
        self.pause_menu = PauseMenu(self.game)

    def tearDown(self):
        pygame.quit()

    def test_toggle(self):
        self.assertFalse(self.pause_menu.visible)
        self.pause_menu.toggle()
        self.assertTrue(self.pause_menu.visible)
        self.pause_menu.toggle()
        self.assertFalse(self.pause_menu.visible)

    def test_navigation(self):
        self.pause_menu.visible = True
        self.assertEqual(self.pause_menu.selected_index, 0)

        # Down
        self.pause_menu.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)])
        self.assertEqual(self.pause_menu.selected_index, 1)

        # Down
        self.pause_menu.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_DOWN)])
        self.assertEqual(self.pause_menu.selected_index, 2)

        # Up
        self.pause_menu.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_UP)])
        self.assertEqual(self.pause_menu.selected_index, 1)

    def test_resume(self):
        self.pause_menu.visible = True
        self.pause_menu.selected_index = 0
        self.pause_menu.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)])
        self.assertFalse(self.pause_menu.visible)

    def test_main_menu(self):
        self.pause_menu.visible = True
        self.pause_menu.selected_index = 2
        self.pause_menu.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_RETURN)])
        self.assertFalse(self.pause_menu.visible)
        self.assertEqual(self.game.scene_manager.current_scene, "menu_scene")

    # Ignoring export_resume test as it involves file I/O and webbrowser which are hard to test in this env without excessive mocking.
