import unittest
from chesspy import san, game
from chesspy.color import Color

class TestMove(unittest.TestCase):
    def test_0(self):
        mv = san.Move()
        self.assertFalse(mv.capture)
        mv.capture = True
        self.assertTrue(mv.capture)
        with self.assertRaises(IndexError):
            mv.capture = False

    def test_1(self):
        mv = san.Move()
        self.assertEqual(mv.src_y, None)
        mv.src_y = 1
        self.assertEqual(mv.src_y, 1)
        with self.assertRaises(IndexError):
            mv.src_y = 2

class TestSanBasic(unittest.TestCase):
    def test_0(self):
        mv = san.parse('e3')
        self.assertEqual(mv.src, (None, None))
        self.assertEqual(mv.dst, (5, 4))
        self.assertEqual(mv.piece, 'P')
        self.assertFalse(mv.capture)

    def test_1(self):
        mv = san.parse('Re3')
        self.assertEqual(mv.src, (None, None))
        self.assertEqual(mv.dst, (5, 4))
        self.assertEqual(mv.piece, 'R')
        self.assertFalse(mv.capture)

    def test_2(self):
        mv = san.parse('Rxe3')
        self.assertEqual(mv.src, (None, None))
        self.assertEqual(mv.dst, (5, 4))
        self.assertEqual(mv.piece, 'R')
        self.assertTrue(mv.capture)

    def test_3(self):
        mv = san.parse('Rexe3')
        self.assertEqual(mv.src, (None, 4))
        self.assertEqual(mv.dst, (5, 4))
        self.assertEqual(mv.piece, 'R')
        self.assertTrue(mv.capture)

    def test_4(self):
        mv = san.parse('R3xe3')
        self.assertEqual(mv.src, (5, None))
        self.assertEqual(mv.dst, (5, 4))
        self.assertEqual(mv.piece, 'R')
        self.assertTrue(mv.capture)

    def test_5(self):
        mv = san.parse('Rd3xe3')
        self.assertEqual(mv.src, (5, 3))
        self.assertEqual(mv.dst, (5, 4))
        self.assertEqual(mv.piece, 'R')
        self.assertTrue(mv.capture)

    def test_6(self):
        mv = san.parse('Rd3xe3+')
        self.assertEqual(mv.src, (5, 3))
        self.assertEqual(mv.dst, (5, 4))
        self.assertEqual(mv.piece, 'R')
        self.assertTrue(mv.capture)
        self.assertTrue(mv.check)

    def test_7(self):
        mv = san.parse('Rd3xe3#')
        self.assertEqual(mv.src, (5, 3))
        self.assertEqual(mv.dst, (5, 4))
        self.assertEqual(mv.piece, 'R')
        self.assertTrue(mv.capture)
        self.assertTrue(mv.check)
        self.assertTrue(mv.mate)

    def test_8(self):
        mv = san.parse('O-O')
        self.assertEqual(mv.castle, 'kingside')

        mv = san.parse('O-O-O')
        self.assertEqual(mv.castle, 'queenside')

        mv = san.parse('O-O+')
        self.assertEqual(mv.castle, 'kingside')
        self.assertTrue(mv.check)

        mv = san.parse('O-O#')
        self.assertEqual(mv.castle, 'kingside')
        self.assertTrue(mv.check)
        self.assertTrue(mv.mate)

        mv = san.parse('O-O-O+')
        self.assertEqual(mv.castle, 'queenside')
        self.assertTrue(mv.check)

        mv = san.parse('O-O-O#')
        self.assertEqual(mv.castle, 'queenside')
        self.assertTrue(mv.check)
        self.assertTrue(mv.mate)

    def test_9(self):
        mv = san.parse('bxa1=Q')
        self.assertEqual(mv.src, (None, 1))
        self.assertEqual(mv.dst, (7, 0))
        self.assertEqual(mv.piece, 'P')
        self.assertTrue(mv.capture)
        self.assertEqual(mv.promotion, 'Q')
        self.assertFalse(mv.check)
        self.assertFalse(mv.mate)

    def test_a(self):
        mv = san.parse('bxa1=Q+')
        self.assertEqual(mv.src, (None, 1))
        self.assertEqual(mv.dst, (7, 0))
        self.assertEqual(mv.piece, 'P')
        self.assertTrue(mv.capture)
        self.assertEqual(mv.promotion, 'Q')
        self.assertTrue(mv.check)
        self.assertFalse(mv.mate)

    @unittest.expectedFailure
    def test_invalid_syntax(self):
        baddies = ('e33', 'e3++', 'e3#+', 'e3+#', 'xe3', 'x3e', 'xe3+#', 'xRe3', 'R3dxe3', 'O', 'O-', 'bxa8=',
                   'b=xa8Q', 'bxa4=Q+', 'bxa1=K+', 'O-O-)#', 'O-O-O-O', 'O-OxO-O-O')
        for baddy in baddies:
            with self.assertRaises(IndexError, msg=baddy):
                san.parse(baddy)

class TestSanPawn(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    def test_0(self):
        mv = san.parse('e3', game=self.game)
        self.assertEqual(mv.src, (6, 4))
        self.assertEqual(mv.dst, (5, 4))
        self.assertEqual(mv.piece, 'P')
        self.assertFalse(mv.capture)

        mv = san.parse('e4', game=self.game)
        self.assertEqual(mv.src, (6, 4))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'P')
        self.assertFalse(mv.capture)

    def test_1(self):
        mv = san.parse('e5', game=self.game)
        self.assertEqual(mv.src, (1, 4))
        self.assertEqual(mv.dst, (3, 4))
        self.assertEqual(mv.piece, 'P')
        self.assertFalse(mv.capture)

        mv = san.parse('e6', game=self.game)
        self.assertEqual(mv.src, (1, 4))
        self.assertEqual(mv.dst, (2, 4))
        self.assertEqual(mv.piece, 'P')
        self.assertFalse(mv.capture)

    def test_2a(self):
        # test 'e5' with interposition
        self.game.board.place_piece_at('p', 2, 4)
        with self.assertRaises(IndexError):
            san.parse('e5', game=self.game)

    def test_2b(self):
        # test 'e4' with interposition
        self.game.board.place_piece_at('p', 5, 4)
        with self.assertRaises(IndexError):
            san.parse('e4', game=self.game)

    def test_3a(self):
        # test 'e6' with occupied dst
        self.game.board.place_piece_at('p', 2, 4)
        with self.assertRaises(IndexError):
            san.parse('e6', game=self.game)

    def test_3b(self):
        # test 'e5' with occupied dst
        self.game.board.place_piece_at('p', 3, 4)
        with self.assertRaises(IndexError):
            san.parse('e5', game=self.game)

    def test_3c(self):
        # test 'e4' with occupied dst
        self.game.board.place_piece_at('p', 4, 4)
        with self.assertRaises(IndexError):
            san.parse('e4', game=self.game)

    def test_3d(self):
        # test 'e3' with occupied dst
        self.game.board.place_piece_at('p', 5, 4)
        with self.assertRaises(IndexError):
            san.parse('e3', game=self.game)

    @unittest.expectedFailure
    def test_4(self):
        # test 'e6' with black pawn on e7 and white pawn on e5
        #   game.turn == black returns src==e7
        #   game.turn == white returns src==e5
        self.assertTrue(False)

    def test_5a(self):
        # capture opponent
        self.game.board.place_piece_at('p', 5, 2)
        mv = san.parse('bxc3', game=self.game) # ^ ->
        self.assertEqual(mv.src, (6, 1))
        self.assertEqual(mv.dst, (5, 2))
        self.assertEqual(mv.piece, 'P')
        self.assertTrue(mv.capture)

        # don't capture self
        self.game.board.place_piece_at('P', 5, 2)
        with self.assertRaises(IndexError):
            mv = san.parse('bxc3', game=self.game)        

    def test_5b(self):
        # capture opponent
        self.game.board.place_piece_at('p', 5, 2)
        mv = san.parse('dxc3', game=self.game) # ^ <-
        self.assertEqual(mv.src, (6, 3))
        self.assertEqual(mv.dst, (5, 2))
        self.assertEqual(mv.piece, 'P')
        self.assertTrue(mv.capture)

        # don't capture self
        self.game.board.place_piece_at('P', 5, 2)
        with self.assertRaises(IndexError):
            mv = san.parse('dxc3', game=self.game)        

    def test_5c(self):
        # capture opponent
        self.game.board.place_piece_at('P', 2, 5)
        self.game.turn = Color.BLACK
        mv = san.parse('exf6', game=self.game) # v ->
        self.assertEqual(mv.src, (1, 4))
        self.assertEqual(mv.dst, (2, 5))
        self.assertEqual(mv.piece, 'P')
        self.assertTrue(mv.capture)

        # don't capture self
        self.game.board.place_piece_at('p', 2, 5)
        with self.assertRaises(IndexError):
            mv = san.parse('exf6', game=self.game)        


    def test_5d(self):
        # capture opponent
        self.game.turn = Color.BLACK
        self.game.board.place_piece_at('P', 2, 5)
        mv = san.parse('gxf6', game=self.game) # v <-
        self.assertEqual(mv.src, (1, 6))
        self.assertEqual(mv.dst, (2, 5))
        self.assertEqual(mv.piece, 'P')
        self.assertTrue(mv.capture)

        # don't capture self
        self.game.board.place_piece_at('p', 2, 5)
        with self.assertRaises(IndexError):
            mv = san.parse('gxf6', game=self.game)        


class TestSanKnight(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    def test_0(self):
        mv = san.parse('Nf3', game=self.game)
        self.assertEqual(mv.src, (7, 6))
        self.assertEqual(mv.dst, (5, 5))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

        mv = san.parse('Nh3', game=self.game)
        self.assertEqual(mv.src, (7, 6))
        self.assertEqual(mv.dst, (5, 7))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

        mv = san.parse('Nc6', game=self.game)
        self.assertEqual(mv.src, (0, 1))
        self.assertEqual(mv.dst, (2, 2))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

        mv = san.parse('Na6', game=self.game)
        self.assertEqual(mv.src, (0, 1))
        self.assertEqual(mv.dst, (2, 0))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

    @unittest.expectedFailure
    def test_1(self):
        # test knight moves that can only be disambiguated by src knight color
        #   game.turn == black returns black knight
        #   game.turn == white returns white knight
        self.assertTrue(False)

    @unittest.expectedFailure
    def test_2(self):
        # test knight moves that can only be disambiguated by "would expose check"
        self.assertTrue(False)

class TestSanBishop(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    def test_0(self):
        mv = san.parse('Bg7', game=self.game) # v ->
        self.assertEqual(mv.src, (0, 5))
        self.assertEqual(mv.dst, (1, 6))
        self.assertEqual(mv.piece, 'B')
        self.assertFalse(mv.capture)

        mv = san.parse('Bb4', game=self.game) # v <-
        self.assertEqual(mv.src, (0, 5))
        self.assertEqual(mv.dst, (4, 1))
        self.assertEqual(mv.piece, 'B')
        self.assertFalse(mv.capture)

        mv = san.parse('Bf4', game=self.game) # ^ ->
        self.assertEqual(mv.src, (7, 2))
        self.assertEqual(mv.dst, (4, 5))
        self.assertEqual(mv.piece, 'B')
        self.assertFalse(mv.capture)

        mv = san.parse('Bb5', game=self.game) # ^ <-
        self.assertEqual(mv.src, (7, 5))
        self.assertEqual(mv.dst, (3, 1))
        self.assertEqual(mv.piece, 'B')
        self.assertFalse(mv.capture)

    @unittest.expectedFailure
    def test_1(self):
        # illegal moves: interposition
        mv = san.parse('Nf3', game=self.game)
        self.assertEqual(mv.src, (7, 6))
        self.assertEqual(mv.dst, (5, 5))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

        mv = san.parse('Nf3', game=self.game)
        self.assertEqual(mv.src, (7, 6))
        self.assertEqual(mv.dst, (5, 5))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

        mv = san.parse('Nf3', game=self.game)
        self.assertEqual(mv.src, (7, 6))
        self.assertEqual(mv.dst, (5, 5))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

        mv = san.parse('Nf3', game=self.game)
        self.assertEqual(mv.src, (7, 6))
        self.assertEqual(mv.dst, (5, 5))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

    @unittest.expectedFailure
    def test_2(self):
        # capture
        mv = san.parse('Nf3', game=self.game)
        self.assertEqual(mv.src, (7, 6))
        self.assertEqual(mv.dst, (5, 5))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

        mv = san.parse('Nf3', game=self.game)
        self.assertEqual(mv.src, (7, 6))
        self.assertEqual(mv.dst, (5, 5))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

        mv = san.parse('Nf3', game=self.game)
        self.assertEqual(mv.src, (7, 6))
        self.assertEqual(mv.dst, (5, 5))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

        mv = san.parse('Nf3', game=self.game)
        self.assertEqual(mv.src, (7, 6))
        self.assertEqual(mv.dst, (5, 5))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

class TestSanQueen(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    def test_0(self):
        mv = san.parse('Qg5', game=self.game) # v ->
        self.assertEqual(mv.src, (0, 3))
        self.assertEqual(mv.dst, (3, 6))
        self.assertEqual(mv.piece, 'Q')
        self.assertFalse(mv.capture)

    def test_1(self):
        mv = san.parse('Qa5', game=self.game) # v <-
        self.assertEqual(mv.src, (0, 3))
        self.assertEqual(mv.dst, (3, 0))
        self.assertEqual(mv.piece, 'Q')
        self.assertFalse(mv.capture)

    def test_2(self):
        mv = san.parse('Qe2', game=self.game) # ^ ->
        self.assertEqual(mv.src, (7, 3))
        self.assertEqual(mv.dst, (6, 4))
        self.assertEqual(mv.piece, 'Q')
        self.assertFalse(mv.capture)

    def test_3(self):
        mv = san.parse('Qb3', game=self.game) # ^ <-
        self.assertEqual(mv.src, (7, 3))
        self.assertEqual(mv.dst, (5, 1))
        self.assertEqual(mv.piece, 'Q')
        self.assertFalse(mv.capture)

    @unittest.expectedFailure
    def test_4(self):
        mv = san.parse('Qg7', game=self.game) # ->
        self.assertEqual(mv.src, (0, 5))
        self.assertEqual(mv.dst, (1, 6))
        self.assertEqual(mv.piece, 'Q')
        self.assertFalse(mv.capture)

    @unittest.expectedFailure
    def test_5(self):
        mv = san.parse('Qb4', game=self.game) # <-
        self.assertEqual(mv.src, (0, 5))
        self.assertEqual(mv.dst, (4, 1))
        self.assertEqual(mv.piece, 'B')
        self.assertFalse(mv.capture)

    @unittest.expectedFailure
    def test_6(self):
        mv = san.parse('Qf4', game=self.game) # ^
        self.assertEqual(mv.src, (7, 2))
        self.assertEqual(mv.dst, (4, 5))
        self.assertEqual(mv.piece, 'B')
        self.assertFalse(mv.capture)

    @unittest.expectedFailure
    def test_7(self):
        mv = san.parse('Qb5', game=self.game) # v
        self.assertEqual(mv.src, (7, 5))
        self.assertEqual(mv.dst, (3, 1))
        self.assertEqual(mv.piece, 'B')
        self.assertFalse(mv.capture)

class TestSanDeluxe1(unittest.TestCase):
    @unittest.expectedFailure
    def test_0(self):
        # if 'x' in san then mv.capture is True
        self.assertTrue(False)