import unittest
import pygame
from game.scenes.resume_scene import ResumeScene

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

class TestResumeScene(unittest.TestCase):
    def setUp(self):
        pygame.init()
        self.game = MockGame()
        # ResumeScene loads resume.json, so we need to make sure asset manager works or mock it.
        # But since we have the file, we can let it load.
        self.resume_scene = ResumeScene(self.game)

    def tearDown(self):
        pygame.quit()

    def test_resume_scene_initialization(self):
        self.assertIsNotNone(self.resume_scene.resume_data)
        self.assertIsNotNone(self.resume_scene.surface)

    def test_exit_resume_scene(self):
        self.resume_scene.handle_events([pygame.event.Event(pygame.KEYDOWN, key=pygame.K_ESCAPE)])
        self.assertEqual(self.game.scene_manager.current_scene, "menu_scene")

    def test_scroll(self):
        initial_scroll = self.resume_scene.scroll_y
        # Scroll down
        self.resume_scene.handle_events([pygame.event.Event(pygame.MOUSEWHEEL, y=-1)])
        self.assertTrue(self.resume_scene.scroll_y > initial_scroll)
