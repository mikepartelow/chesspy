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
        self.assertEqual(list(moves), [(5, 4), (4, 4)])

        self.game.move_san('e3')

        moves = move_generators.moves_for(5, 4, self.board)
        self.assertEqual(list(moves), [(4, 4)])

    def test_0b(self):
        moves = move_generators.moves_for(1, 2, self.board)
        self.assertEqual(list(moves), [(2, 2), (3, 2)])

        self.game.turn = Color.BLACK
        self.game.move_san('c5')

        moves = move_generators.moves_for(3, 2, self.board)
        self.assertEqual(list(moves), [(4, 2)])

    def test_capture_0w(self):
        self.board.place_piece_at('n', 4, 4)
        moves = move_generators.moves_for(6, 4, self.board)
        self.assertEqual(list(moves), [(5, 4)])

        self.board.place_piece_at('n', 5, 4)
        moves = move_generators.moves_for(6, 4, self.board)
        self.assertEqual(list(moves), [])

        self.board.place_piece_at('n', 5, 3)
        moves = move_generators.moves_for(6, 4, self.board)
        self.assertEqual(list(moves), [(5, 3)])

    def test_capture_0b(self):
        self.board.place_piece_at('N', 3, 2)
        moves = move_generators.moves_for(1, 2, self.board)
        self.assertEqual(list(moves), [(2, 2)])

        self.board.place_piece_at('N', 2, 2)
        moves = move_generators.moves_for(1, 2, self.board)
        self.assertEqual(list(moves), [])

        self.board.place_piece_at('N', 2, 1)
        moves = move_generators.moves_for(1, 2, self.board)
        self.assertEqual(list(moves), [(2, 1)])

    @unittest.skip
    def test_en_passant_0w(self):
        self.assertEqual("generates a move to en_passant", False)

    @unittest.skip
    def test_en_passant_0b(self):
        self.assertEqual("generates a move to en_passant", False)

    def test_blocked_0w(self):
        self.board.place_piece_at('N', 4, 4)
        moves = move_generators.moves_for(6, 4, self.board)
        self.assertEqual(list(moves), [(5, 4)])

        self.board.place_piece_at('N', 5, 4)
        moves = move_generators.moves_for(6, 4, self.board)
        self.assertEqual(list(moves), [])

        self.board.place_piece_at(None, 4, 4)
        moves = move_generators.moves_for(6, 4, self.board)
        self.assertEqual(list(moves), [])

    def test_blocked_0b(self):
        self.board.place_piece_at('N', 3, 2)
        moves = move_generators.moves_for(1, 2, self.board)
        self.assertEqual(list(moves), [(2, 2)])

        self.board.place_piece_at('N', 2, 2)
        moves = move_generators.moves_for(1, 2, self.board)
        self.assertEqual(list(moves), [])

        self.board.place_piece_at(None, 3, 2)
        moves = move_generators.moves_for(1, 2, self.board)
        self.assertEqual(list(moves), [])

    @unittest.skip
    def test_in_bounds_0w(self):
        self.assertEqual("only generates in-bounds moves", False)

    @unittest.skip
    def test_in_bounds_0b(self):
        self.assertEqual("only generates in-bounds moves", False)


class TestKnightMoveGenerator(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board

    def test_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('N', 3, 3)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(list(moves), [(2, 1), (2, 5), (4, 1), (4, 5), (1, 2), (1, 4), (5, 2), (5, 4)])

    def test_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('n', 3, 3)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(list(moves), [(2, 1), (2, 5), (4, 1), (4, 5), (1, 2), (1, 4), (5, 2), (5, 4)])

    def test_capture_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('N', 3, 3)
        for y, x in [(2, 1), (2, 5), (4, 1), (4, 5), (1, 2), (1, 4), (5, 2), (5, 4)]:
            self.board.place_piece_at('r', y, x)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(list(moves), [(2, 1), (2, 5), (4, 1), (4, 5), (1, 2), (1, 4), (5, 2), (5, 4)])

    def test_capture_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('n', 3, 3)
        for y, x in [(2, 1), (2, 5), (4, 1), (4, 5), (1, 2), (1, 4), (5, 2), (5, 4)]:
            self.board.place_piece_at('R', y, x)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(list(moves), [(2, 1), (2, 5), (4, 1), (4, 5), (1, 2), (1, 4), (5, 2), (5, 4)])

    def test_blocked_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('N', 3, 3)
        for y, x in [(2, 1), (2, 5), (4, 1), (4, 5), (1, 2), (1, 4), (5, 2), (5, 4)]:
            self.board.place_piece_at('R', y, x)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(list(moves), [])

    def test_blocked_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('n', 3, 3)
        for y, x in [(2, 1), (2, 5), (4, 1), (4, 5), (1, 2), (1, 4), (5, 2), (5, 4)]:
            self.board.place_piece_at('r', y, x)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(list(moves), [])

    def test_in_bounds_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('N', 0, 0)
        moves = move_generators.moves_for(0, 0, self.board)
        self.assertEqual(list(moves), [(1, 2), (2, 1)])

    def test_in_bounds_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('n', 7, 7)
        moves = move_generators.moves_for(7, 7, self.board)
        self.assertEqual(list(moves), [(6, 5), (5, 6)])

class TestKingMoveGenerator(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board

    def test_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('K', 3, 3)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([(2, 2), (2, 3), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (3, 2)]))

    def test_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('k', 3, 3)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([(2, 2), (2, 3), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (3, 2)]))

    def test_capture_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('K', 3, 3)
        self.board.place_piece_at('b', 2, 3)
        self.board.place_piece_at('b', 3, 4)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([(2, 2), (2, 3), (2, 4), (4, 3), (4, 2), (3, 2), (3, 4), (4, 4)]))

    def test_capture_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('k', 3, 3)
        self.board.place_piece_at('B', 2, 3)
        self.board.place_piece_at('B', 3, 4)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([(2, 2), (2, 3), (2, 4), (4, 3), (4, 2), (3, 2), (3, 4), (4, 4)]))

    def test_blocked_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('K', 3, 3)
        self.board.place_piece_at('B', 2, 3)
        self.board.place_piece_at('B', 3, 4)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([(2, 2), (2, 4), (4, 4), (4, 3), (4, 2), (3, 2)]))

    def test_blocked_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('k', 3, 3)
        self.board.place_piece_at('b', 3, 2)
        self.board.place_piece_at('b', 4, 4)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([(2, 2), (2, 3), (2, 4), (3, 4), (4, 3), (4, 2)]))

    def test_in_bounds_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('k', 0, 0)
        moves = move_generators.moves_for(0, 0, self.board)
        self.assertEqual(sorted(moves), sorted([(0, 1), (1, 0), (1, 1)]))

    def test_in_bounds_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('k', 7, 7)
        moves = move_generators.moves_for(7, 7, self.board)
        self.assertEqual(sorted(moves), sorted([(6, 6), (6, 7), (7, 6)]))


class TestRookMoveGenerator(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board

    def test_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('R', 3, 3)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([
            (0, 3), (1, 3), (2, 3), (4, 3), (5, 3), (6, 3), (7, 3),
            (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 7)
        ]))

    def test_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('r', 3, 3)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([
            (0, 3), (1, 3), (2, 3), (4, 3), (5, 3), (6, 3), (7, 3),
            (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 7)
        ]))

    def test_capture_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('R', 3, 0)
        self.board.place_piece_at('p', 1, 0)
        self.board.place_piece_at('p', 5, 0)
        self.board.place_piece_at('p', 3, 6)
        moves = move_generators.moves_for(3, 0, self.board)
        self.assertEqual(sorted(moves), sorted([
            (1, 0), (2, 0), (4, 0), (5, 0),
            (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
        ]))

    def test_capture_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('r', 3, 0)
        self.board.place_piece_at('P', 1, 0)
        self.board.place_piece_at('P', 5, 0)
        self.board.place_piece_at('P', 3, 6)
        moves = move_generators.moves_for(3, 0, self.board)
        self.assertEqual(sorted(moves), sorted([
            (1, 0), (2, 0), (4, 0), (5, 0),
            (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
        ]))

    def test_blocked_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('R', 3, 3)
        self.board.place_piece_at('B', 4, 3)
        self.board.place_piece_at('B', 3, 6)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([
            (0, 3), (1, 3), (2, 3),
            (3, 0), (3, 1), (3, 2), (3, 4), (3, 5),
        ]))

    def test_blocked_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('r', 3, 3)
        self.board.place_piece_at('b', 4, 3)
        self.board.place_piece_at('b', 3, 6)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([
            (0, 3), (1, 3), (2, 3),
            (3, 0), (3, 1), (3, 2), (3, 4), (3, 5),
        ]))

    @unittest.skip
    def test_in_bounds_0w(self):
        self.assertEqual("only generates in-bounds moves", False)

    @unittest.skip
    def test_in_bounds_0b(self):
        self.assertEqual("only generates in-bounds moves", False)


class TestBishopMoveGenerator(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board

    def test_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('B', 3, 3)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([
            (0, 0), (1, 1), (2, 2), (4, 4), (5, 5), (6, 6), (7, 7),
            (6, 0), (5, 1), (4, 2), (2, 4), (1, 5), (0, 6),
        ]))

    def test_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('b', 3, 3)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([
            (0, 0), (1, 1), (2, 2), (4, 4), (5, 5), (6, 6), (7, 7),
            (6, 0), (5, 1), (4, 2), (2, 4), (1, 5), (0, 6),
        ]))

    def test_capture_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('B', 3, 3)
        self.board.place_piece_at('r', 4, 2)
        self.board.place_piece_at('r', 5, 5)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([
            (4, 2), (4, 4), (5, 5),
            (2, 2), (1, 1), (0, 0), (2, 4), (1, 5), (0, 6)
        ]))

    def test_capture_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('b', 3, 3)
        self.board.place_piece_at('R', 4, 2)
        self.board.place_piece_at('R', 5, 5)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([
            (4, 2), (4, 4), (5, 5),
            (2, 2), (1, 1), (0, 0), (2, 4), (1, 5), (0, 6)
        ]))

    def test_blocked_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('B', 3, 3)
        self.board.place_piece_at('R', 4, 2)
        self.board.place_piece_at('R', 5, 5)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([
            (4, 4), (2, 2), (1, 1),
            (0, 0), (2, 4), (1, 5), (0, 6),
        ]))

    def test_blocked_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('b', 3, 3)
        self.board.place_piece_at('r', 4, 2)
        self.board.place_piece_at('r', 5, 5)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([
            (4, 4), (2, 2), (1, 1),
            (0, 0), (2, 4), (1, 5), (0, 6),
        ]))

    @unittest.skip
    def test_in_bounds_0w(self):
        self.assertEqual("only generates in-bounds moves", False)

    @unittest.skip
    def test_in_bounds_0b(self):
        self.assertEqual("only generates in-bounds moves", False)


class TestQueenMoveGenerator(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.board = self.game.board

    def test_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('Q', 3, 3)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([
            (0, 0), (1, 1), (2, 2), (4, 4), (5, 5), (6, 6), (7, 7),
            (6, 0), (5, 1), (4, 2), (2, 4), (1, 5), (0, 6),
            (0, 3), (1, 3), (2, 3), (4, 3), (5, 3), (6, 3), (7, 3),
            (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 7)
        ]))

    def test_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('q', 3, 3)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([
            (0, 0), (1, 1), (2, 2), (4, 4), (5, 5), (6, 6), (7, 7),
            (6, 0), (5, 1), (4, 2), (2, 4), (1, 5), (0, 6),
            (0, 3), (1, 3), (2, 3), (4, 3), (5, 3), (6, 3), (7, 3),
            (3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 7)
        ]))

    def test_capture_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('Q', 3, 3)
        self.board.place_piece_at('r', 4, 2)
        self.board.place_piece_at('r', 5, 5)
        self.board.place_piece_at('r', 6, 3)
        self.board.place_piece_at('r', 3, 5)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([
            (3, 0), (3, 1), (3, 2),
            (2, 3), (1, 3), (0, 3),
            (3, 4), (3, 5),
            (4, 3), (5, 3), (6, 3),
            (2, 2), (1, 1), (0, 0),
            (2, 4), (1, 5), (0, 6),
            (4, 4), (5, 5),
            (4, 2)
        ]))

    def test_capture_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('q', 3, 3)
        self.board.place_piece_at('R', 4, 2)
        self.board.place_piece_at('R', 5, 5)
        self.board.place_piece_at('R', 6, 3)
        self.board.place_piece_at('R', 3, 5)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([
            (3, 0), (3, 1), (3, 2),
            (2, 3), (1, 3), (0, 3),
            (3, 4), (3, 5),
            (4, 3), (5, 3), (6, 3),
            (2, 2), (1, 1), (0, 0),
            (2, 4), (1, 5), (0, 6),
            (4, 4), (5, 5),
            (4, 2)
        ]))

    def test_blocked_0w(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('Q', 3, 3)
        self.board.place_piece_at('B', 1, 5)
        self.board.place_piece_at('B', 3, 6)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([
            (3, 4), (4, 3), (3, 1), (5, 1), (2, 2), (1, 3), (7, 7),
            (4, 2), (3, 0), (5, 3), (2, 4), (7, 3),
            (3, 2), (3, 5), (4, 4), (5, 5), (0, 0), (1, 1), (0, 3),
            (2, 3), (6, 0), (6, 6), (6, 3)
        ]))

    def test_blocked_0b(self):
        self.board = Board(' ' * 64)
        self.board.place_piece_at('q', 3, 3)
        self.board.place_piece_at('b', 1, 5)
        self.board.place_piece_at('b', 3, 6)
        moves = move_generators.moves_for(3, 3, self.board)
        self.assertEqual(sorted(moves), sorted([
            (3, 4), (4, 3), (3, 1), (5, 1), (2, 2), (1, 3), (7, 7),
            (4, 2), (3, 0), (5, 3), (2, 4), (7, 3),
            (3, 2), (3, 5), (4, 4), (5, 5), (0, 0), (1, 1), (0, 3),
            (2, 3), (6, 0), (6, 6), (6, 3)
        ]))

    @unittest.skip
    def test_in_bounds_0w(self):
        self.assertEqual("only generates in-bounds moves", False)

    @unittest.skip
    def test_in_bounds_0b(self):
        self.assertEqual("only generates in-bounds moves", False)

