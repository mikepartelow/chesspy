import unittest
from chesspy import analyzers
from chesspy.board import Board
from chesspy.color import Color


class TestIsCheck(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_not(self):
        self.assertFalse(analyzers.is_in_check(self.board, Color.BLACK))
        self.assertFalse(analyzers.is_in_check(self.board, Color.WHITE))

    def test_knight_0w(self):
        self.board.place_piece_at(None, 7, 4)
        self.board.place_piece_at('K', 3, 4)

        self.board.place_piece_at('n', 5, 3)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

        self.board.place_piece_at(None, 5, 3)
        self.board.place_piece_at('n', 5, 5)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

        self.board.place_piece_at(None, 5, 5)
        self.board.place_piece_at('n', 1, 5)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

        self.board.place_piece_at(None, 1, 5)
        self.board.place_piece_at('n', 1, 3)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

    def test_knight_0b(self):
        self.board.place_piece_at(None, 0, 4)
        self.board.place_piece_at('k', 3, 4)

        self.board.place_piece_at('N', 5, 3)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at(None, 5, 3)
        self.board.place_piece_at('N', 5, 5)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at(None, 5, 5)
        self.board.place_piece_at('N', 1, 5)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at(None, 1, 5)
        self.board.place_piece_at('N', 1, 3)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at('B', 1, 3)
        self.assertFalse(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at('n', 1, 3)
        self.assertFalse(analyzers.is_in_check(self.board, Color.BLACK))

    def test_rook_0w(self):
        self.board.place_piece_at(None, 7, 4)
        self.board.place_piece_at('K', 3, 4)

        self.board.place_piece_at(None, 6, 1)
        self.board.place_piece_at('r', 3, 0)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

        self.board.place_piece_at(None, 3, 0)
        self.board.place_piece_at('r', 3, 7)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

        self.board.place_piece_at(None, 3, 7)
        self.board.place_piece_at('r', 1, 4)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

        self.board.place_piece_at(None, 1, 4)
        self.board.place_piece_at('r', 4, 4)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

    def test_rook_0b(self):
        self.board.place_piece_at(None, 0, 4)
        self.board.place_piece_at('k', 3, 4)

        self.board.place_piece_at('R', 3, 0)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at(None, 3, 0)
        self.board.place_piece_at('R', 3, 7)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at(None, 3, 7)
        self.board.place_piece_at('R', 1, 4)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at(None, 1, 4)
        self.board.place_piece_at('R', 4, 4)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at('B', 4, 4)
        self.assertFalse(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at('r', 4, 4)
        self.assertFalse(analyzers.is_in_check(self.board, Color.BLACK))

    def test_bishop_0w(self):
        self.board.place_piece_at(None, 7, 4)
        self.board.place_piece_at('K', 3, 4)

        self.board.place_piece_at('b', 5, 2)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

        self.board.place_piece_at(None, 5, 2)
        self.board.place_piece_at('b', 6, 7)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

        self.board.place_piece_at(None, 6, 7)
        self.board.place_piece_at('b', 1, 2)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

        self.board.place_piece_at(None, 1, 2)
        self.board.place_piece_at('b', 2, 5)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

    def test_bishop_0b(self):
        self.board.place_piece_at(None, 0, 4)
        self.board.place_piece_at('k', 3, 4)

        self.board.place_piece_at('B', 5, 2)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at(None, 5, 2)
        self.board.place_piece_at('B', 6, 7)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at(None, 6, 7)
        self.board.place_piece_at('B', 1, 2)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at(None, 1, 2)
        self.board.place_piece_at('B', 2, 5)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at('R', 2, 5)
        self.assertFalse(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at('b', 2, 5)
        self.assertFalse(analyzers.is_in_check(self.board, Color.BLACK))

    def test_queen_diag_0w(self):
        self.board.place_piece_at(None, 7, 4)
        self.board.place_piece_at('K', 3, 4)

        self.board.place_piece_at(None, 6, 1)
        self.board.place_piece_at('q', 7, 0)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

        self.board.place_piece_at(None, 7, 0)
        self.board.place_piece_at('q', 6, 7)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

        self.board.place_piece_at(None, 6, 7)
        self.board.place_piece_at('q', 1, 2)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

        self.board.place_piece_at(None, 1, 2)
        self.board.place_piece_at('q', 2, 5)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

    def test_queen_diag_0b(self):
        self.board.place_piece_at(None, 0, 4)
        self.board.place_piece_at('k', 3, 4)

        self.board.place_piece_at('Q', 5, 2)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at(None, 5, 2)
        self.board.place_piece_at('Q', 6, 7)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at(None, 6, 7)
        self.board.place_piece_at('Q', 1, 2)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at(None, 1, 2)
        self.board.place_piece_at('Q', 2, 5)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at('R', 2, 5)
        self.assertFalse(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at('q', 2, 5)
        self.assertFalse(analyzers.is_in_check(self.board, Color.BLACK))

    def test_queen_horiz_0w(self):
        self.board.place_piece_at(None, 7, 4)
        self.board.place_piece_at('K', 3, 4)

        self.board.place_piece_at(None, 6, 1)
        self.board.place_piece_at('q', 3, 0)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

        self.board.place_piece_at(None, 3, 0)
        self.board.place_piece_at('q', 3, 7)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

        self.board.place_piece_at(None, 3, 7)
        self.board.place_piece_at('q', 1, 4)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

        self.board.place_piece_at(None, 1, 4)
        self.board.place_piece_at('q', 4, 4)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

    def test_queen_horiz_0b(self):
        self.board.place_piece_at(None, 0, 4)
        self.board.place_piece_at('k', 3, 4)

        self.board.place_piece_at('Q', 3, 0)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at(None, 3, 0)
        self.board.place_piece_at('Q', 3, 7)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at(None, 3, 7)
        self.board.place_piece_at('Q', 1, 4)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at(None, 1, 4)
        self.board.place_piece_at('Q', 4, 4)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at('B', 4, 4)
        self.assertFalse(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at('q', 4, 4)
        self.assertFalse(analyzers.is_in_check(self.board, Color.BLACK))

    def test_pawn_0w(self):
        self.board.place_piece_at(None, 7, 4)
        self.board.place_piece_at('K', 3, 4)

        self.board.place_piece_at('p', 2, 3)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

        self.board.place_piece_at(None, 2, 3)
        self.board.place_piece_at('p', 2, 5)
        self.assertTrue(analyzers.is_in_check(self.board, Color.WHITE))

    def test_pawn_0b(self):
        self.board.place_piece_at(None, 0, 4)
        self.board.place_piece_at('k', 3, 4)

        self.board.place_piece_at('P', 4, 3)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at(None, 4, 3)
        self.board.place_piece_at('P', 4, 5)
        self.assertTrue(analyzers.is_in_check(self.board, Color.BLACK))

        self.board.place_piece_at('N', 4, 5)
        self.assertFalse(analyzers.is_in_check(self.board, Color.WHITE))

        self.board.place_piece_at('p', 4, 5)
        self.assertFalse(analyzers.is_in_check(self.board, Color.WHITE))

    @unittest.skip
    def test_combo_0(self):
        self.assertFalse("test both black and white")

