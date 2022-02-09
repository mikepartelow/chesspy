import unittest
from chesspy.game import Game
from chesspy.board import Board
from chesspy.color import Color
from chesspy import move_generators


class TestPawnMoveGenerator(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board

    def test_0w(self):
        moves = move_generators.moves_for(6, 4, self.board)
        self.assertEqual(moves, [(5, 4), (4, 4)])

        self.game.move_san('e3')

        moves = move_generators.moves_for(5, 4, self.board)
        self.assertEqual(moves, [(4, 4)])

    def test_0b(self):
        moves = move_generators.moves_for(1, 2, self.board)
        self.assertEqual(moves, [(2, 2), (3, 2)])

        self.game.turn = Color.BLACK
        self.game.move_san('c5')

        moves = move_generators.moves_for(3, 2, self.board)
        self.assertEqual(moves, [(4, 2)])

    @unittest.skip
    def test_capture_0w(self):
        self.assertEqual("generates a move to capture", False)

    @unittest.skip
    def test_capture_0b(self):
        self.assertEqual("generates a move to capture", False)

    @unittest.skip
    def test_en_passant_0w(self):
        self.assertEqual("generates a move to en_passant", False)

    @unittest.skip
    def test_en_passant_0b(self):
        self.assertEqual("generates a move to en_passant", False)

    @unittest.skip
    def test_blocked_0w(self):
        self.assertEqual("otherwise legal move is blocked by interposing piece", False)
        self.assertEqual("try to move 1 square", False)
        self.assertEqual("try to move 2 squares", False)

    @unittest.skip
    def test_blocked_0b(self):
        self.assertEqual("otherwise legal move is blocked by interposing piece", False)
        self.assertEqual("try to move 1 square", False)
        self.assertEqual("try to move 2 squares", False)

class TestKnightMoveGenerator(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board

    def test_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('N', 3, 3)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(moves, [(2, 1), (2, 5), (4, 1), (4, 5), (1, 2), (1, 4), (5, 2), (5, 4)])

    def test_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('n', 3, 3)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(moves, [(2, 1), (2, 5), (4, 1), (4, 5), (1, 2), (1, 4), (5, 2), (5, 4)])

    @unittest.skip
    def test_capture_0w(self):
        self.assertEqual("generates a move to capture", False)

    @unittest.skip
    def test_capture_0b(self):
        self.assertEqual("generates a move to capture", False)

    @unittest.skip
    def test_blocked_0w(self):
        self.assertEqual("otherwise legal move is blocked by own-side piece", False)

    @unittest.skip
    def test_blocked_0b(self):
        self.assertEqual("otherwise legal move is blocked by own-side piece", False)
