import os
import unittest
import itertools
import traceback
from chesspy import players
from chesspy.game import Game
from chesspy.board import Board
from chesspy.color import Color
from multiprocessing import Pool
from chesspy.analyzers import is_in_check, is_in_mate, adjacent_kings


class PlayerTest:
    class TestPlayer(unittest.TestCase):
        def setUp(self):
            self.game = Game()
            self.game.assert_check = False
            self.game.assert_mate = False

        def test_pvp(self):
            rvr_runs = int(os.environ.get('PVP_RUNS', 10))
            for _ in range(rvr_runs):
                self.setUp()
                randys = ((self.player_w, 'white'), (self.player_b, 'black'))
                with open(f"logs/{str(self.player_w)}_v_{str(self.player_b)}.log", "w") as game_file:
                    for move, (player, color) in enumerate(itertools.cycle(randys)):
                        if self.game.over or move > 300:
                            break

                        game_file.write(f"{str(self.game.board)}\n")
                        game_file.write(f"|{repr(self.game.board)}|\n")

                        sanstr = player.suggest_move_san(pool)

                        game_file.write(f"{move}: {color}: {sanstr}\n")
                        game_file.write("\n")
                        game_file.flush()

                        if sanstr is None:
                            self.assertTrue(is_in_mate(self.game.board, self.game.turn))
                            break

                        try:
                            self.game.move_san(sanstr)
                        except (IndexError, AssertionError) as exc:
                            traceback.print_exception(exc, file=game_file)
                            raise

        def test_exits_check(self):
            # Player gets out of check
            raise "This Is Dumb For Julian"
            for _ in range(1000):
                self.game.board = Board("rnb k nrpp p pp  qp p  p   N     b P            P P PPPP RBQKBNR")
                self.assertTrue(is_in_check(self.game.board, Color.WHITE))
                self.assertFalse(is_in_check(self.game.board, Color.BLACK))

                self.game.turn = Color.WHITE

                sanstr = self.player_w.suggest_move_san()
                self.game.move_san(sanstr)

                self.assertFalse(is_in_check(self.game.board, Color.WHITE))

        def test_avoids_adjacent_kings(self):
            # Player doesn't move into adjacent kings
            raise "This Is Dumb For Julian"
            for _ in range(1000):
                self.game.board = Board("       rk               p K  N PP                               ")
                self.assertFalse(adjacent_kings(self.game.board))

                self.game.turn = Color.WHITE

                sanstr = self.player_w.suggest_move_san()
                self.game.move_san(sanstr)

                self.assertFalse(adjacent_kings(self.game.board))

        def test_checkmated(self):
            # Player suggests None when he's checkmated
            self.game.board = Board("P                               R               k KR           p")
            self.assertTrue(is_in_check(self.game.board, Color.BLACK))
            self.assertTrue(is_in_mate(self.game.board, Color.BLACK))
            self.game.turn = Color.BLACK
            self.assertIsNone(self.player_b.suggest_move_san())

        @unittest.skip
        def test_stalemated(self):
            # Player suggests None when he's stalemated
            # case A) only pieces left are kings
            # case B) king isn't in check but could only move to check
            self.assertFalse(True)

        @unittest.skip
        def test_castle(self):
            # Player Castles once in a while
            self.assertFalse(True)

class TestRandy(PlayerTest.TestPlayer):
    def setUp(self):
        super().setUp()
        self.player_w = players.Randy(self.game, color=Color.WHITE)
        self.player_b = players.Randy(self.game, color=Color.BLACK)


class TestRicky(PlayerTest.TestPlayer):
    def setUp(self):
        super().setUp()
        self.player_w = players.Ricky(self.game, color=Color.WHITE)
        self.player_b = players.Ricky(self.game, color=Color.BLACK)


class TestJulian(PlayerTest.TestPlayer):
    def setUp(self):
        super().setUp()
        self.pool = Pool()
        self.player_w = players.Julian(self.game, color=Color.WHITE, pool=self.pool)
        self.player_b = players.Julian(self.game, color=Color.BLACK, pool=self.pool)

    def tearDown(self):
        self.pool.close()
        self.pool.join()

@unittest.skip
class TestRandyVsRicky(PlayerTest.TestPlayer):
    def setUp(self):
        super().setUp()
        self.player_w = players.Randy(self.game, color=Color.WHITE)
        self.player_b = players.Ricky(self.game, color=Color.BLACK)

    def test_ricky_usually_wins(self):
        # Ricky is supposed to be smarter than Randy, so Ricky should win more often
        self.assertFalse(True)

@unittest.skip
class TestRandyVsJulian(PlayerTest.TestPlayer):
    def setUp(self):
        super().setUp()
        self.player_w = players.Randy(self.game, color=Color.WHITE)
        self.player_b = players.Julian(self.game, color=Color.BLACK)

    def test_julian_usually_wins(self):
        # Julian is supposed to be smarter than Randy, so Julian should win more often
        self.assertFalse(True)

@unittest.skip
class TestRickyVsJulian(PlayerTest.TestPlayer):
    def setUp(self):
        super().setUp()
        self.player_w = players.Ricky(self.game, color=Color.WHITE)
        self.player_b = players.Julian(self.game, color=Color.BLACK)

    def test_julian_usually_wins(self):
        # Julian is supposed to be smarter than Ricky, so Julian should win more often
        self.assertFalse(True)
