import unittest
import itertools
from chesspy import game, board
from chesspy.color import Color

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
            yield line.replace("\n", '') # can't strip because space at EOL is OK!

class TestTurns(unittest.TestCase):
    def test_0(self):
        g = game.Game()
        self.assertEqual(g.turn, Color.WHITE)

        g.move_san('e4')

        self.assertEqual(g.turn, Color.BLACK)

class TestMoveSan(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    def test_pinned_0(self):
        # SAN is disambiguated because one rook is pinned
        #
        self.game.board = board.Board("       kp         p   R    b         q        RP     PPK        ")
        self.assertEqual('R', self.game.board.square_at(2, 6)) # this one should move
        self.assertEqual('R', self.game.board.square_at(5, 6)) # this one is pinned
        self.game.move_san("Rg5")
        self.assertEqual('R', self.game.board.square_at(3, 6))
        self.assertEqual(None, self.game.board.square_at(2, 6))
        self.assertEqual('R', self.game.board.square_at(5, 6))

class TestGameOverMan(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    def test_0(self):
        self.game.board = board.Board("           bk         p   KPp       q                           ")
        self.game.turn = Color.BLACK
        self.assertFalse(self.game.over)
        self.game.move_san('Qd4#')
        self.assertTrue(self.game.over)

    def test_1(self):
        self.game.board = board.Board("           bk         p   KPp       q                           ")
        self.game.turn = Color.BLACK
        self.assertFalse(self.game.over)
        self.game.move_san('1-0')
        self.assertTrue(self.game.over)

    def test_2(self):
        self.assertFalse(self.game.over)
        self.game.move_san('0-1')
        self.assertTrue(self.game.over)

    def test_3(self):
        self.assertFalse(self.game.over)
        self.game.move_san('1/2-1/2')
        self.assertTrue(self.game.over)

class TestIsMate(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    def test_immortal(self):
        self.game.board = board.Board("r bk   rp  pBpNpn    n   p NP  P      P    P    P P K   q     b ")
        self.assertTrue(self.game.is_in_mate())
        self.assertTrue(self.game.over)

        self.game.board = board.Board("r bk   rp  p pNpn  B n   p NP  P      P    P    P P K   q     b ")
        self.game.move_san("Be7#")
        self.assertTrue(self.game.is_in_mate())
        self.assertTrue(self.game.over)

    def test_gotc(self):
        self.game.board = board.Board(" Q           pk   p   p  p  N  p b     P bn       r   P   K     ")
        self.game.turn = Color.BLACK
        self.assertTrue(self.game.is_in_mate())
        self.assertTrue(self.game.over)

        self.game.board = board.Board("Q           pk   p   p  p  N  p b     P bn     r     P   K     ")
        self.game.turn = Color.BLACK
        self.game.move_san("Rc2#")
        self.assertTrue(self.game.is_in_mate())
        self.assertTrue(self.game.over)

class TestPromotion(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    def test_white(self):
        self.game.board.place_piece_at(None, 0, 6)
        self.game.board.place_piece_at('P', 1, 6)
        self.game.move_san("g8=N")
        self.assertEqual(None, self.game.board.square_at(1, 6))
        self.assertEqual('N', self.game.board.square_at(0, 6))

    def test_black(self):
        self.game.board.place_piece_at(None, 7, 6)
        self.game.board.place_piece_at('p', 6, 6)
        self.game.turn = Color.BLACK
        self.game.move_san("g1=Q")
        self.assertEqual(None, self.game.board.square_at(6, 6))
        self.assertEqual('q', self.game.board.square_at(7, 6))

class TestEnPassant(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    def test_opponent_removed_from_board_w(self):
        # FIXME: starting this way we aren't testing game memory - no way to know for sure that
        #        black moved their pawn 2 spaces previous move. hence "honor system"
        #
        self.game.board = board.Board("        p p   p  pP k p  P   pP P  PK  P                        ")
        self.game.turn = Color.WHITE
        self.assertEqual('p', self.game.board.square_at(3, 5))
        capture = self.game.move_san('gxf6')
        self.assertEqual(None, self.game.board.square_at(3, 5))
        self.assertEqual(capture, 'p')

    def test_opponent_removed_from_board_b(self):
        # FIXME: starting this way we aren't testing game memory - no way to know for sure that
        #        black moved their pawn 2 spaces previous move. hence "honor system"
        #
        self.game.board = board.Board("    b            p      p   k  p   NpP   P  K   P      P        ")
        self.game.turn = Color.BLACK
        self.assertEqual('P', self.game.board.square_at(4, 5))
        capture = self.game.move_san('exf3')
        self.assertEqual(None, self.game.board.square_at(4, 5))
        self.assertEqual(capture, 'P')


class TestCastle(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    @unittest.skip
    def test_illegal_0(self):
        self.assertEqual("rook has", "already moved")
        self.assertEqual("Now", "Do It For Black")
        self.assertEqual("works ok for white", "after first moving non-castling rook")
        self.assertEqual("works ok for black", "after first moving non-castling rook")

    @unittest.skip
    def test_illegal_1(self):
        self.assertEqual("king has", "already moved")
        self.assertEqual("Now", "Do It For Black")

    @unittest.skip
    def test_illegal_2(self):
        self.assertEqual("king moves", "through check")
        self.assertEqual("Now", "Do It For Black")

    @unittest.skip
    def test_illegal_3(self):
        self.assertEqual("king moves", "into check")
        self.assertEqual("Now", "Do It For Black")

    def test_king_side_castle(self):
        self.game.board = board.Board("rnbqk  rpppppppp                                PPPPPPPPRNBQK  R")

        self.game.move_san('O-O')
        self.assertEqual(repr(self.game.board), "rnbqk  rpppppppp                                PPPPPPPPRNBQ RK ")

        self.game.move_san('O-O')
        self.assertEqual(repr(self.game.board), "rnbq rk pppppppp                                PPPPPPPPRNBQ RK ")

    def test_queen_side_castle(self):
        g = game.Game()
        g.board = board.Board("r   kbnrpppppppp                                PPPPPPPPR   KBNR")

        g.move_san('O-O-O')
        self.assertEqual(repr(g.board), "r   kbnrpppppppp                                PPPPPPPP  KR BNR")

        g.move_san('O-O-O')
        self.assertEqual(repr(g.board), "  kr bnrpppppppp                                PPPPPPPP  KR BNR")

# Putting the "FG" in "FGDD"
#
class TestFamousGames(unittest.TestCase):

    def test_gotc(self):
        g = game.Game()

        for idx, (sanstr, boardrepr) in enumerate(itertools.zip_longest(simple_moves('tests/games/gotc.txt'), board_reprs('tests/games/gotc.boardreprs.txt'))):
            # print(f"{int(idx/2+1)}. {g.turn}: {sanstr}")
            g.move_san(sanstr)
            # print(g.board)
            # print("")
            self.assertEqual(repr(g.board), boardrepr)

    def test_immortal(self):
        g = game.Game()

        for idx, (sanstr, boardrepr) in enumerate(itertools.zip_longest(simple_moves('tests/games/immortal.txt'), board_reprs('tests/games/immortal.boardreprs.txt'))):
            # print(f"{int( idx/2+1)}. {g.turn}: {sanstr}")
            g.move_san(sanstr)
            # print(g.board)
            # print("")
            self.assertEqual(repr(g.board), boardrepr, idx)
