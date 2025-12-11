import unittest
import os
import json
from game.managers.save_manager import SaveManager

class TestSaveManager(unittest.TestCase):
    def setUp(self):
        self.filename = 'test_save.json'
        self.manager = SaveManager(self.filename)

    def tearDown(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_save_load(self):
        self.manager.set_high_score(100)
        self.manager.save()

        new_manager = SaveManager(self.filename)
        new_manager.load()
        self.assertEqual(new_manager.get_high_score(), 100)

if __name__ == '__main__':
    unittest.main()
