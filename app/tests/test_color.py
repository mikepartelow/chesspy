import unittest
from chesspy.color import Color

class TestColor(unittest.TestCase):
    def test_0(self):
        self.assertEqual(Color.WHITE, Color.toggle(Color.BLACK))
        self.assertEqual(Color.BLACK, Color.toggle(Color.WHITE))
