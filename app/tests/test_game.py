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

class TestIsCheck(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    def test_not(self):
        self.assertFalse(self.game.is_in_check())
        self.game.turn = Color.BLACK
        self.assertFalse(self.game.is_in_check())

    def test_knight_0b(self):
        self.game.board.place_piece_at(None, 7, 4)
        self.game.board.place_piece_at('K', 3, 4)

        self.game.board.place_piece_at('n', 5, 3)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 5, 3)
        self.game.board.place_piece_at('n', 5, 5)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 5, 5)
        self.game.board.place_piece_at('n', 1, 5)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 1, 5)
        self.game.board.place_piece_at('n', 1, 3)
        self.assertTrue(self.game.is_in_check())

    def test_knight_0w(self):
        self.game.turn = Color.BLACK
        
        self.game.board.place_piece_at(None, 0, 4)
        self.game.board.place_piece_at('k', 3, 4)

        self.game.board.place_piece_at('N', 5, 3)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 5, 3)
        self.game.board.place_piece_at('N', 5, 5)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 5, 5)
        self.game.board.place_piece_at('N', 1, 5)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 1, 5)
        self.game.board.place_piece_at('N', 1, 3)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at('B', 1, 3)
        self.assertFalse(self.game.is_in_check())

        self.game.board.place_piece_at('n', 1, 3)
        self.assertFalse(self.game.is_in_check())

    @unittest.expectedFailure
    def test_rook_0(self):
        self.assertFalse("test both black and white")

    @unittest.expectedFailure
    def test_rook_0(self):
        self.assertFalse("test both black and white")

    def test_bishop_0b(self):
        self.game.board.place_piece_at(None, 7, 4)
        self.game.board.place_piece_at('K', 3, 4)

        self.game.board.place_piece_at('b', 5, 2)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 5, 2)
        self.game.board.place_piece_at('b', 6, 7)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 6, 7)
        self.game.board.place_piece_at('b', 1, 2)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 1, 2)
        self.game.board.place_piece_at('b', 2, 5)
        self.assertTrue(self.game.is_in_check())        

    def test_bishop_0w(self):
        self.game.turn = Color.BLACK

        self.game.board.place_piece_at(None, 0, 4)
        self.game.board.place_piece_at('k', 3, 4)

        self.game.board.place_piece_at('B', 5, 2)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 5, 2)
        self.game.board.place_piece_at('B', 6, 7)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 6, 7)
        self.game.board.place_piece_at('B', 1, 2)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 1, 2)
        self.game.board.place_piece_at('B', 2, 5)
        self.assertTrue(self.game.is_in_check())        

        self.game.board.place_piece_at('R', 2, 5)
        self.assertFalse(self.game.is_in_check())

        self.game.board.place_piece_at('b', 2, 5)
        self.assertFalse(self.game.is_in_check())

    def test_queen_diag_0b(self):
        self.game.board.place_piece_at(None, 7, 4)
        self.game.board.place_piece_at('K', 3, 4)

        self.game.board.place_piece_at(None, 6, 1)
        self.game.board.place_piece_at('q', 7, 0)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 7, 0)
        self.game.board.place_piece_at('q', 6, 7)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 6, 7)
        self.game.board.place_piece_at('q', 1, 2)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 1, 2)
        self.game.board.place_piece_at('q', 2, 5)
        self.assertTrue(self.game.is_in_check())        

    def test_queen_diag_0w(self):
        self.game.turn = Color.BLACK

        self.game.board.place_piece_at(None, 0, 4)
        self.game.board.place_piece_at('k', 3, 4)

        self.game.board.place_piece_at('Q', 5, 2)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 5, 2)
        self.game.board.place_piece_at('Q', 6, 7)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 6, 7)
        self.game.board.place_piece_at('Q', 1, 2)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 1, 2)
        self.game.board.place_piece_at('Q', 2, 5)
        self.assertTrue(self.game.is_in_check())        

        self.game.board.place_piece_at('R', 2, 5)
        self.assertFalse(self.game.is_in_check())

        self.game.board.place_piece_at('q', 2, 5)
        self.assertFalse(self.game.is_in_check())

    def test_queen_horiz_0b(self):
        self.game.board.place_piece_at(None, 7, 4)
        self.game.board.place_piece_at('K', 3, 4)

        self.game.board.place_piece_at(None, 6, 1)
        self.game.board.place_piece_at('q', 3, 0)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 3, 0)
        self.game.board.place_piece_at('q', 3, 7)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 3, 7)
        self.game.board.place_piece_at('q', 1, 4)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 1, 4)
        self.game.board.place_piece_at('q', 4, 4)
        self.assertTrue(self.game.is_in_check())        

    def test_queen_horiz_0w(self):
        self.game.turn = Color.BLACK

        self.game.board.place_piece_at(None, 0, 4)
        self.game.board.place_piece_at('k', 3, 4)

        self.game.board.place_piece_at('Q', 3, 0)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 3, 0)
        self.game.board.place_piece_at('Q', 3, 7)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 3, 7)
        self.game.board.place_piece_at('Q', 1, 4)
        self.assertTrue(self.game.is_in_check())

        self.game.board.place_piece_at(None, 1, 4)
        self.game.board.place_piece_at('Q', 4, 4)
        self.assertTrue(self.game.is_in_check())        

        self.game.board.place_piece_at('B', 4, 4)
        self.assertFalse(self.game.is_in_check())

        self.game.board.place_piece_at('q', 4, 4)
        self.assertFalse(self.game.is_in_check())

    @unittest.expectedFailure
    def test_pawn_0(self):
        self.assertFalse("test both black and white")

    @unittest.expectedFailure
    def test_combo_0(self):
        self.assertFalse("test both black and white")

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
                
class TestMoveSan(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    @unittest.expectedFailure
    def test_0(self):
        self.assertTrue(False)

    @unittest.expectedFailure
    def test_1(self):
        self.assertTrue(False)

    @unittest.expectedFailure
    def test_2(self):
        self.assertTrue(False)

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

    @unittest.expectedFailure
    def test_illegal_0(self):
        self.assertEqual("rook has", "already moved")
        self.assertEqual("Now", "Do It For Black")
        self.assertEqual("works ok for white", "after first moving non-castling rook")
        self.assertEqual("works ok for black", "after first moving non-castling rook")

    @unittest.expectedFailure
    def test_illegal_1(self):
        self.assertEqual("king has", "already moved")
        self.assertEqual("Now", "Do It For Black")

    @unittest.expectedFailure
    def test_illegal_2(self):
        self.assertEqual("king moves", "through check")
        self.assertEqual("Now", "Do It For Black")

    @unittest.expectedFailure
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
            turn = g.turn
            # print(f"{int(idx/2+1)}. {turn}: {sanstr}")
            g.move_san(sanstr)
            # print(g.board)
            # print("")
            self.assertEqual(repr(g.board), boardrepr)

    def test_immortal(self):
        g = game.Game()

        for idx, (sanstr, boardrepr) in enumerate(itertools.zip_longest(simple_moves('tests/games/immortal.txt'), board_reprs('tests/games/immortal.boardreprs.txt'))):
            turn = g.turn
            # print(f"{int( idx/2+1)}. {turn}: {sanstr}")
            g.move_san(sanstr)
            # print(g.board)
            # print("")
            self.assertEqual(repr(g.board), boardrepr, idx)
