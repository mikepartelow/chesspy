import unittest
from chesspy import san, game, board
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
    def test_friendly_fire(self):
        # don't allow capture of own piece
        # don't allow it with 'x' in the san
        # don't allow it without 'x' in the san
        # don't allow it, san i am
        self.assertEqual(False, True)

    @unittest.expectedFailure
    def test_invalid_syntax(self):
        baddies = ('e33', 'e3++', 'e3#+', 'e3+#', 'xe3', 'x3e', 'xe3+#', 'xRe3', 'R3dxe3', 'O', 'O-', 'bxa8=',
                   'b=xa8Q', 'bxa4=Q+', 'bxa1=K+', 'O-O-)#', 'O-O-O-O', 'O-OxO-O-O')
        for baddy in baddies:
            with self.assertRaises(IndexError, msg=baddy):
                san.parse(baddy)

class TestSanFancy(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    def test_0(self):
        # disambiguated rook move from Game Of The Century. Code is tempted to move wrong rook.
        self.game.board = board.Board("r    rk pp   pbp qp   p   B       BP  b Q n  N  P    PPP   RK  R")
        self.game.turn = Color.BLACK
        mv = san.parse('Rfe8+', game=self.game)
        self.assertEqual(mv.src, (0, 5))
        self.assertEqual(mv.dst, (0, 4))
        self.assertEqual(mv.piece, 'R')
        self.assertTrue(mv.check)

class TestSanAnnotations(unittest.TestCase):
    annotations = ( '!', '!!', '?', '??', '!?', '?!', )
    moves       = ( 'e4', 'O-O-O#', 'bxa1=Q+', 'Rxe3', )

    def test_0(self):
        for move in self.moves:
            for annotation in self.annotations:
                san.parse(f"{move}{annotation}")

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
        self.game.turn = Color.BLACK
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

    def test_6a(self):
        # regular forward move move
        self.game.turn = Color.BLACK
        self.game.board.place_piece_at('p', 3, 4)
        self.game.board.place_piece_at(None, 6, 4)
        mv = san.parse('e4', game=self.game)
        self.assertEqual(mv.src, (3, 4))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'P')
        self.assertFalse(mv.capture)

        self.game.board.place_piece_at('p', 3, 4)
        self.game.board.place_piece_at('R', 4, 4)
        with self.assertRaises(IndexError):
            san.parse('e4', game=self.game)

    def test_en_passant_honor_system_0(self):
        # FIXME: starting this way we aren't testing game memory - no way to know for sure that
        #        black moved their pawn 2 spaces previous move. hence "honor system"
        #
        self.game.board = board.Board("        p p   p  pP k p  P   pP P  PK  P                        ")
        self.game.turn = Color.WHITE
        self.assertEqual('p', self.game.board.square_at(3, 5))
        mv = san.parse('gxf6', game=self.game)
        self.assertEqual(mv.src, (3, 6))
        self.assertEqual(mv.dst, (2, 5))
        self.assertEqual(mv.piece, 'P')
        self.assertTrue(mv.capture)
        self.assertTrue(mv.en_passant)

    def test_en_passant_honor_system_1(self):
        # FIXME: starting this way we aren't testing game memory - no way to know for sure that
        #        black moved their pawn 2 spaces previous move. hence "honor system"
        #
        self.game.board = board.Board("    b            p      p   k  p   NpP   P  K   P      P        ")
        self.game.turn = Color.BLACK
        self.assertEqual('P', self.game.board.square_at(4, 5))
        mv = san.parse('exf3', game=self.game)
        self.assertEqual(mv.src, (4, 4))
        self.assertEqual(mv.dst, (5, 5))
        self.assertEqual(mv.piece, 'P')
        self.assertTrue(mv.capture)
        self.assertTrue(mv.en_passant)

    @unittest.expectedFailure
    def test_en_passant_trust_no_one_0(self):
        self.assertEqual("do like test_en_passant_honor_system_0 but check all the en passant rules", "especially: did white's captured pawn just move 2 spaces?")

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

        self.game.turn = Color.BLACK
        mv = san.parse('Nc6', game=self.game)
        self.assertEqual(mv.src, (0, 1))
        self.assertEqual(mv.dst, (2, 2))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

        self.game.turn = Color.BLACK
        mv = san.parse('Na6', game=self.game)
        self.assertEqual(mv.src, (0, 1))
        self.assertEqual(mv.dst, (2, 0))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

    def test_1(self):
        # knight moves that can only be disambiguated by src knight color
        # move 22 of The Immortal Game is such a move!
        self.game.board = board.Board("r bk  nrp  p pNpn  B Q   p NP  P      P    P    P P K   q     b ")
        self.game.turn = Color.BLACK
        mv = san.parse('Nxf6', game=self.game)
        self.assertEqual(mv.src, (0, 6))
        self.assertEqual(mv.dst, (2, 5))
        self.assertEqual(mv.piece, 'N')
        self.assertTrue(mv.capture)

    def test_2(self):
        # knight move disambiguated by SAN.
        # move 14 of The Evergreen Game is such a move.
        self.game.board = board.Board(" rb k  rp ppnppp bn   q     P   Q B     B Pp N  P    PPPRN  R K ")
        mv = san.parse('Nbd2', game=self.game)
        self.assertEqual(mv.src, (7, 1))
        self.assertEqual(mv.dst, (6, 3))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

    def test_3(self):
        # knight move disambiguated by SAN where a src coordinate is 0
        self.game.board = board.Board("  k rb  pp q  p n p bp     n       P  P    N B  PPPBQ   RN K    ")
        self.game.turn = Color.BLACK
        mv = san.parse("Nab4", game=self.game)
        self.assertEqual(mv.src, (2, 0))
        self.assertEqual(mv.dst, (4, 1))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)        
    
    def test_4(self):
        # knight move disambiguated by "would expose check"
        board_repr = "rnbq rk ppp  ppp    pn           b P      N  B  PPP  PPPR BQK NR"
        self.game.board = board.Board(board_repr)
        mv = san.parse("Ne2", game=self.game)        

        self.assertEqual(mv.src, (7, 6))
        self.assertEqual(mv.dst, (6, 4))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)  

        self.assertEqual(repr(self.game.board), board_repr)

class TestSanBishop(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    def test_0a(self):
        self.game.turn = Color.BLACK

        with self.assertRaises(IndexError):
            san.parse('Bg7', game=self.game)

        self.game.board.place_piece_at(None, 1, 6)
        mv = san.parse('Bg7', game=self.game) # v ->
        self.assertEqual(mv.src, (0, 5))
        self.assertEqual(mv.dst, (1, 6))
        self.assertEqual(mv.piece, 'B')
        self.assertFalse(mv.capture)

    def test_0b(self):
        self.game.turn = Color.BLACK

        with self.assertRaises(IndexError):
            san.parse('Ba3', game=self.game)

        self.game.board.place_piece_at(None, 1, 4)

        mv = san.parse('Ba3', game=self.game) # v <-
        self.assertEqual(mv.src, (0, 5))
        self.assertEqual(mv.dst, (5, 0))
        self.assertEqual(mv.piece, 'B')
        self.assertFalse(mv.capture)

    def test_0c(self):
        with self.assertRaises(IndexError):
            san.parse('Bf4', game=self.game)

        self.game.board.place_piece_at(None, 6, 3)

        mv = san.parse('Bf4', game=self.game) # ^ ->
        self.assertEqual(mv.src, (7, 2))
        self.assertEqual(mv.dst, (4, 5))
        self.assertEqual(mv.piece, 'B')
        self.assertFalse(mv.capture)

    def test_0d(self):
        with self.assertRaises(IndexError):
            san.parse('Bb5', game=self.game)

        self.game.board.place_piece_at(None, 6, 4)

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

class TestSanKing(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    def test_0a(self):
        self.game.board.place_piece_at('K', 4, 3)
        mv = san.parse('Ke4', game=self.game) # ->
        self.assertEqual(mv.src, (4, 3))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'K')
        self.assertFalse(mv.capture)

    def test_0b(self):
        self.game.board.place_piece_at('K', 4, 5)
        mv = san.parse('Ke4', game=self.game) # <-
        self.assertEqual(mv.src, (4, 5))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'K')
        self.assertFalse(mv.capture)

    def test_0c(self):
        self.game.board.place_piece_at('K', 3, 4)
        mv = san.parse('Ke4', game=self.game) # v
        self.assertEqual(mv.src, (3, 4))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'K')
        self.assertFalse(mv.capture)

    def test_0d(self):
        self.game.board.place_piece_at('K', 5, 4)
        mv = san.parse('Ke4', game=self.game) # ^
        self.assertEqual(mv.src, (5, 4))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'K')
        self.assertFalse(mv.capture)

    def test_1a(self):
        self.game.board.place_piece_at('K', 3, 3)
        mv = san.parse('Ke4', game=self.game) # v ->
        self.assertEqual(mv.src, (3, 3))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'K')
        self.assertFalse(mv.capture)

    def test_1b(self):
        self.game.board.place_piece_at('K', 3, 5)
        mv = san.parse('Ke4', game=self.game) # v <-
        self.assertEqual(mv.src, (3, 5))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'K')
        self.assertFalse(mv.capture)

    def test_1c(self):
        self.game.board.place_piece_at('K', 5, 3)
        mv = san.parse('Ke4', game=self.game) # ^ ->
        self.assertEqual(mv.src, (5, 3))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'K')
        self.assertFalse(mv.capture)

    def test_1d(self):
        self.game.board.place_piece_at('K', 5, 5)
        mv = san.parse('Ke4', game=self.game) # ^ <-
        self.assertEqual(mv.src, (5, 5))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'K')
        self.assertFalse(mv.capture)

    @unittest.expectedFailure
    def test_2a(self):
        # various kinds of illegal moves. > 1 square, into check, etc.
        self.assertFalse(True)

class TestSanQueen(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    def test_0a(self):
        self.game.board.place_piece_at('Q', 4, 0)
        mv = san.parse('Qe4', game=self.game) # ->
        self.assertEqual(mv.src, (4, 0))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'Q')
        self.assertFalse(mv.capture)

    def test_0b(self):
        self.game.board.place_piece_at('Q', 4, 7)
        mv = san.parse('Qe4', game=self.game) # <-
        self.assertEqual(mv.src, (4, 7))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'Q')
        self.assertFalse(mv.capture)

    def test_0c(self):
        self.game.board.place_piece_at('Q', 2, 4)
        mv = san.parse('Qe4', game=self.game) # v
        self.assertEqual(mv.src, (2, 4))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'Q')
        self.assertFalse(mv.capture)

    def test_0d(self):
        self.game.board.place_piece_at('Q', 5, 4)
        mv = san.parse('Qe4', game=self.game) # ^
        self.assertEqual(mv.src, (5, 4))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'Q')
        self.assertFalse(mv.capture)

    def test_1a(self):
        self.game.turn = Color.BLACK
        with self.assertRaises(IndexError):
            san.parse('Qa5', game=self.game)

        self.game.board.place_piece_at(None, 1, 4)

        mv = san.parse('Qg5', game=self.game) # v ->
        self.assertEqual(mv.src, (0, 3))
        self.assertEqual(mv.dst, (3, 6))
        self.assertEqual(mv.piece, 'Q')
        self.assertFalse(mv.capture)

    def test_1b(self):
        self.game.turn = Color.BLACK
        with self.assertRaises(IndexError):
            san.parse('Qa5', game=self.game)

        self.game.board.place_piece_at(None, 1, 2)

        mv = san.parse('Qa5', game=self.game) # v <-
        self.assertEqual(mv.src, (0, 3))
        self.assertEqual(mv.dst, (3, 0))
        self.assertEqual(mv.piece, 'Q')
        self.assertFalse(mv.capture)

    def test_1c(self):
        with self.assertRaises(IndexError):
            san.parse('Qe2', game=self.game)

        self.game.board.place_piece_at(None, 6, 4)

        mv = san.parse('Qe2', game=self.game) # ^ ->
        self.assertEqual(mv.src, (7, 3))
        self.assertEqual(mv.dst, (6, 4))
        self.assertEqual(mv.piece, 'Q')
        self.assertFalse(mv.capture)

    def test_1d(self):
        with self.assertRaises(IndexError):
            san.parse('Qb3', game=self.game)

        self.game.board.place_piece_at(None, 6, 2)
        mv = san.parse('Qb3', game=self.game) # ^ <-
        self.assertEqual(mv.src, (7, 3))
        self.assertEqual(mv.dst, (5, 1))
        self.assertEqual(mv.piece, 'Q')
        self.assertFalse(mv.capture)

    def test_2a(self):
        self.game.board = board.Board(" Q   QK        R              p      r       k P                ")
        self.game.turn = Color.WHITE
        mv = san.parse('Qbxf4+', game=self.game)
        self.assertEqual(mv.src, (0, 1))
        self.assertEqual(mv.dst, (4, 5))
        self.assertEqual(mv.piece, 'Q')
        self.assertTrue(mv.capture)

class TestSanRook(unittest.TestCase):
    def setUp(self):
        self.game = game.Game()

    def test_0a(self):
        self.game.board.place_piece_at('R', 4, 0)
        mv = san.parse('Re4', game=self.game) # ->
        self.assertEqual(mv.src, (4, 0))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'R')
        self.assertFalse(mv.capture)

    def test_0b(self):
        self.game.board.place_piece_at('R', 4, 7)
        mv = san.parse('Re4', game=self.game) # <-
        self.assertEqual(mv.src, (4, 7))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'R')
        self.assertFalse(mv.capture)

    def test_0c(self):
        self.game.board.place_piece_at('R', 2, 4)
        mv = san.parse('Re4', game=self.game) # v
        self.assertEqual(mv.src, (2, 4))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'R')
        self.assertFalse(mv.capture)

    def test_0d(self):
        self.game.board.place_piece_at('R', 5, 4)
        mv = san.parse('Re4', game=self.game) # ^
        self.assertEqual(mv.src, (5, 4))
        self.assertEqual(mv.dst, (4, 4))
        self.assertEqual(mv.piece, 'R')
        self.assertFalse(mv.capture)

    def test_1a(self):
        # illegal move: interposition
        self.game.board.place_piece_at(None, 7, 7)
        with self.assertRaises(IndexError):
            san.parse('Rh1', game=self.game) # ->

    def test_1b(self):
        # illegal move: interposition
        self.game.board.place_piece_at(None, 7, 0)
        with self.assertRaises(IndexError):
            san.parse('Ra1', game=self.game) # <-

    def test_1c(self):
        # illegal move: interposition
        self.game.board.place_piece_at(None, 0, 7)
        with self.assertRaises(IndexError):
            san.parse('Rh8', game=self.game) # ^

    def test_1d(self):
        # illegal move: interposition
        self.game.board.place_piece_at(None, 7, 7)
        with self.assertRaises(IndexError):
            san.parse('Rh1', game=self.game) # v

    @unittest.expectedFailure
    def test_ef(self):
        # illegal moves: diagonal move
        mv = san.parse('Rf3', game=self.game)
        self.assertEqual(mv.src, (7, 6))
        self.assertEqual(mv.dst, (5, 5))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

        mv = san.parse('Rf3', game=self.game)
        self.assertEqual(mv.src, (7, 6))
        self.assertEqual(mv.dst, (5, 5))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

        mv = san.parse('Rf3', game=self.game)
        self.assertEqual(mv.src, (7, 6))
        self.assertEqual(mv.dst, (5, 5))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

        mv = san.parse('Rf3', game=self.game)
        self.assertEqual(mv.src, (7, 6))
        self.assertEqual(mv.dst, (5, 5))
        self.assertEqual(mv.piece, 'N')
        self.assertFalse(mv.capture)

        self.assertFalse(True)

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

        self.assertFalse(True)

    @unittest.expectedFailure
    def test_3(self):
        # one rook could move vertically, one could move horizontally, both to same square, but first choice would expose check.
        # so move second done
        self.assertFalse(True)

class TestSanDeluxe1(unittest.TestCase):
    @unittest.expectedFailure
    def test_0(self):
        # if 'x' in san then mv.capture is True
        self.assertTrue(False)