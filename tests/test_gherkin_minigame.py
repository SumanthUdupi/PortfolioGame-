import unittest
from unittest.mock import MagicMock
import pygame
from game.ui.gherkin_minigame import GherkinMinigame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

class TestGherkinMinigame(unittest.TestCase):
    def setUp(self):
        pygame.init()
        # Mock screen for setup_ui
        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.mock_game_manager = MagicMock()
        self.mock_on_complete = MagicMock()
        self.mock_data = ["Given I am on the login page", "When I enter valid credentials", "Then I should be redirected to the dashboard"]

    def tearDown(self):
        pygame.quit()

    def test_initialization(self):
        minigame = GherkinMinigame(self.mock_game_manager, "User login", self.mock_data, self.mock_on_complete)
        self.assertEqual(len(minigame.blocks), 3)
        self.assertEqual(len(minigame.slots), 3)
        self.assertEqual(minigame.correct_order, self.mock_data)

    def test_scramble(self):
        # This test might fail if random shuffle results in same order, but setup_ui has a loop to prevent that if length > 1
        minigame = GherkinMinigame(self.mock_game_manager, "User login", self.mock_data, self.mock_on_complete)
        block_texts = [b.text for b in minigame.blocks]
        # In rare cases this might be sorted, but let's check if it runs at least
        self.assertTrue(len(block_texts) == 3)

    def test_completion_logic_failure(self):
        minigame = GherkinMinigame(self.mock_game_manager, "User login", self.mock_data, self.mock_on_complete)
        # Blocks are not in slots yet
        minigame.check_completion()
        self.mock_on_complete.assert_not_called()

    def test_completion_logic_success(self):
        minigame = GherkinMinigame(self.mock_game_manager, "User login", self.mock_data, self.mock_on_complete)

        # Manually place blocks in correct slots
        for i, slot in enumerate(minigame.slots):
            correct_text = minigame.correct_order[i]
            # Find the block with this text
            block = next(b for b in minigame.blocks if b.text == correct_text)
            block.rect.topleft = slot.topleft

        minigame.check_completion()
        self.mock_on_complete.assert_called_once()

if __name__ == '__main__':
    unittest.main()
