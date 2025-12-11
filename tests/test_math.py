import unittest
from game.utils.math_utils import MathUtils

class TestMathUtils(unittest.TestCase):
    def test_clamp(self):
        self.assertEqual(MathUtils.clamp(5, 0, 10), 5)
        self.assertEqual(MathUtils.clamp(-5, 0, 10), 0)
        self.assertEqual(MathUtils.clamp(15, 0, 10), 10)

if __name__ == '__main__':
    unittest.main()
