import unittest
import itertools
from chesspy import game, board

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

class TestTurns(unittest.TestCase):
    def test_0(self):
        g = game.Game()
        self.assertEqual(g.turn, Color.WHITE)

        g.move_san('e4')

        self.assertEqual(g.turn, Color.BLACK)

class TestMoveSan(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    def test_0(self):
        self.assertTrue(False)

    def test_1(self):
        self.assertTrue(False)

    def test_2(self):
        self.assertTrue(False)

class TestCastle(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    def test_illegal_0(self):
        self.assertEqual("rook has", "already moved")
        self.assertEqual("Now", "Do It For Black")

    def test_illegal_1(self):
        self.assertEqual("king has", "already moved")
        self.assertEqual("Now", "Do It For Black")

    def test_illegal_2(self):
        self.assertEqual("king moves", "through check")
        self.assertEqual("Now", "Do It For Black")

    def test_illegal_3(self):
        self.assertEqual("king moves", "into check")
        self.assertEqual("Now", "Do It For Black")

    def test_king_side_castle(self):        
        self.game.board = board.Board("rnbqk  rpppppppp                                PPPPPPPPRNBQK  R")
        
        self.game.move_san('O-O')
        self.assertEqual(repr(self.game.board), "rnbqk  rpppppppp                                PPPPPPPPRNBQ RK ")

        self.game.move_san('O-O')
        self.assertEqual(repr(self.game.board), "rnbq rk pppppppp                                PPPPPPPPRNBQ RK ")

        self.assertEqual("works ok for white", "after first moving non-castling rook")
        self.assertEqual("works ok for black", "after first moving non-castling rook")

    def test_queen_side_castle(self):
        g = game.Game()
        g.board = board.Board("r   kbnrpppppppp                                PPPPPPPPR   KBNR")
        
        g.move_san('O-O-O')
        self.assertEqual(repr(g.board), "r   kbnrpppppppp                                PPPPPPPP  KR BNR")

        g.move_san('O-O-O')
        self.assertEqual(repr(g.board), "  kr bnrpppppppp                                PPPPPPPP  KR BNR")

        self.assertEqual("works ok for white", "after first moving non-castling rook")
        self.assertEqual("works ok for black", "after first moving non-castling rook")

# Putting the "FG" in "FGDD"
#
class TestFamousGames(unittest.TestCase):
    def test_gotc(self):
        g = game.Game()

        for sanstr, boardrepr in itertools.zip_longest(simple_moves('tests/games/gotc.txt'), board_reprs('tests/games/gotc.boardreprs.txt')):
            turn = g.turn
            g.move_san(sanstr)
            # FIXME: remove the print()s once the test passes
            print(g.board)
            print(f"{turn}: {sanstr}")
            self.assertEqual(repr(g.board), boardrepr)

    def test_immortal(self):
        g = game.Game()

        for sanstr, boardrepr in itertools.zip_longest(simple_moves('tests/games/immortal.txt'), board_reprs('tests/games/immortal.boardreprs.txt')):
            turn = g.turn
            g.move_san(sanstr)
            # FIXME: remove the print()s once the test passes
            print(g.board)
            print(f"{turn}: {sanstr}")
            self.assertEqual(repr(g.board), boardrepr)
