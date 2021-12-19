import unittest
import itertools
from chesspy import game

def simple_moves(path):
    with open(path, 'r') as f:
        for line in f.readlines():
            sanstr_white, *sanstr_black = line.split()
            yield sanstr_white

            if sanstr_black:
                yield sanstr_black[0]

def board_reprs(path):
    with open(path, 'r') as f:
        for line in f.readlines():
            yield line.strip()

class TestGame(unittest.TestCase):
    def test_gotc(self):
        g = game.Game()

        for sanstr, boardrepr in itertools.zip_longest(simple_moves('tests/games/gotc.txt'), board_reprs('tests/games/gotc.boardreprs.txt')):
            g.move_san(sanstr)
            print(g.board)
            print(sanstr)
            self.assertEqual(repr(g.board), boardrepr)

    @unittest.expectedFailure
    def test_immortal(self):
        self.assertTrue(False)