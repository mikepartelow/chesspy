import unittest
from chesspy import board

class TestBoard(unittest.TestCase):
    def test_init(self):
        b = board.Board()
        self.assertEqual(repr(b), "rnbqkbnrpppppppp                                PPPPPPPPRNBQKBNR")

        b = board.Board("rnbqkbnrpppppppp                   p            PPPPPPPPRNBQKBNR")
        self.assertEqual(repr(b), "rnbqkbnrpppppppp                   p            PPPPPPPPRNBQKBNR")

    def test_repr(self):
        b = board.Board()
        self.assertEqual(repr(b), "rnbqkbnrpppppppp                                PPPPPPPPRNBQKBNR")

        b.place_piece_at('p', 4, 3)
        self.assertEqual(repr(b), "rnbqkbnrpppppppp                   p            PPPPPPPPRNBQKBNR")

    def test_0(self):
        b = board.Board()

        for y in range(2, 6):
            for x in range(0, 8):
                self.assertEqual(None, b.square_at(y, x))

        for x in range(0, 8):
            self.assertEqual('p', b.square_at(1, x))
            self.assertEqual('P', b.square_at(6, x))

        self.assertEqual('k', b.square_at(0, 4))
        self.assertEqual('K', b.square_at(7, 4))

    def test_1(self):
        b = board.Board()

        self.assertEqual(None, b.square_at(3, 4))
        b.place_piece_at('K', 3, 4)
        self.assertEqual('K', b.square_at(3, 4))

    def test_out_of_bounds(self):
        b = board.Board()

        with self.assertRaises(IndexError):
            b.square_at(-1, 1)

        with self.assertRaises(IndexError):
            b.square_at(1, -1)

        with self.assertRaises(IndexError):
            b.square_at(1, 8)

        with self.assertRaises(IndexError):
            b.square_at(8, 1)

class TestBoardFindFrom(unittest.TestCase):
    def setUp(self):
        self.board = board.Board()

    def test_0a(self): # ^
        self.assertEqual(self.board.find_first_on_h_or_v((5, 4), -1, 0), ('p', 1, 4))
        self.board.place_piece_at(None, 1, 4)
        self.assertEqual(self.board.find_first_on_h_or_v((5, 4), -1, 0), ('k', 0, 4))
        self.assertEqual(self.board.find_first_on_h_or_v((0, 4), -1, 0), None)

    def test_0b(self): # v
        self.assertEqual(self.board.find_first_on_h_or_v((2, 4), 1, 0), ('P', 6, 4))
        self.board.place_piece_at(None, 6, 4)
        self.assertEqual(self.board.find_first_on_h_or_v((2, 4), 1, 0), ('K', 7, 4))
        self.assertEqual(self.board.find_first_on_h_or_v((7, 4), 1, 0), None)

    def test_0c(self): # <-
        self.board.place_piece_at('Q', 5, 0)
        self.board.place_piece_at('R', 5, 1)

        self.assertEqual(self.board.find_first_on_h_or_v((5, 6), 0, -1), ('R', 5, 1))
        self.board.place_piece_at(None, 5, 1)
        self.assertEqual(self.board.find_first_on_h_or_v((5, 6), 0, -1), ('Q', 5, 0))
        self.assertEqual(self.board.find_first_on_h_or_v((5, 0), 0, -1), None)

    def test_0d(self): # ->
        self.board.place_piece_at('Q', 2, 7)
        self.board.place_piece_at('R', 2, 6)

        self.assertEqual(self.board.find_first_on_h_or_v((2, 3), 0, 1), ('R', 2, 6))
        self.board.place_piece_at(None, 2, 6)
        self.assertEqual(self.board.find_first_on_h_or_v((2, 3), 0, 1), ('Q', 2, 7))
        self.assertEqual(self.board.find_first_on_h_or_v((2, 7), 0, 1), None)  

    @unittest.skip
    def test_1a(self): # ^ ->
        self.assertTrue(False)

    @unittest.skip
    def test_1b(self): # v ->
        self.assertTrue(False)

    @unittest.skip
    def test_1c(self): # ^ <-
        self.assertTrue(False)

    @unittest.skip
    def test_1d(self): # v <-
        self.assertTrue(False)

    @unittest.skip
    def test_2a(self): # specifies src_y/src_x to disambiguate
        self.assertTrue(False)
