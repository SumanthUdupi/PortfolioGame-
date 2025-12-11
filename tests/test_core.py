import unittest
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from game.managers.save_manager import SaveManager
from game.entities.player import Player
from game.systems.collision_system import CollisionSystem

class TestCore(unittest.TestCase):
    def test_save_manager(self):
        save_manager = SaveManager()
        self.assertIsInstance(save_manager.save_data, dict)
        self.assertIn("player", save_manager.save_data)
        self.assertIn("game", save_manager.save_data)

    def test_player_creation(self):
        player = Player(100, 100)
        self.assertEqual(player.x, 100)
        self.assertEqual(player.y, 100)
        self.assertEqual(player.level, 1)
        self.assertEqual(player.experience, 0)

    def test_collision_system(self):
        # Create mock entities
        entity1 = type('Entity', (), {'x': 0, 'y': 0, 'width': 10, 'height': 10, 'rect': None})()
        entity1.rect = type('Rect', (), {'colliderect': lambda self, other: True})()

        entity2 = type('Entity', (), {'x': 5, 'y': 5, 'width': 10, 'height': 10, 'rect': None})()
        entity2.rect = type('Rect', (), {'colliderect': lambda self, other: True})()

        self.assertTrue(CollisionSystem.check_collision(entity1, entity2))

    def test_point_collision(self):
        entity = type('Entity', (), {'rect': type('Rect', (), {'collidepoint': lambda self, point: point == (5, 5)})()})()
        self.assertTrue(CollisionSystem.check_point_collision((5, 5), entity))
        self.assertFalse(CollisionSystem.check_point_collision((10, 10), entity))

if __name__ == '__main__':
    unittest.main()