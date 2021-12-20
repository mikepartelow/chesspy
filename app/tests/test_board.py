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