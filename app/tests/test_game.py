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

class TestMoveSan(unittest.TestCase):
    def test_0(self):
        self.assertTrue(False)

    def test_1(self):
        self.assertTrue(False)

    def test_2(self):
        self.assertTrue(False)

    def test_king_side_castle(self):
        # use Board.__init__(repr) to set up a board where castling can happen
        self.assertTrue(False)

    def test_queen_side_castle(self):
        # use Board.__init__(repr) to set up a board where castling can happen
        self.assertTrue(False)

# Putting the "FG" in "FGDD"
#
class TestFamousGames(unittest.TestCase):
    def test_gotc(self):
        g = game.Game()

        for sanstr, boardrepr in itertools.zip_longest(simple_moves('tests/games/gotc.txt'), board_reprs('tests/games/gotc.boardreprs.txt')):
            g.move_san(sanstr)
            # FIXME: remove the print()s once the test passes
            print(g.board)
            print(sanstr)
            self.assertEqual(repr(g.board), boardrepr)

    @unittest.expectedFailure
    def test_immortal(self):
        self.assertTrue(False)