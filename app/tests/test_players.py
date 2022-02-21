import unittest
import itertools
import traceback
from chesspy import players
from chesspy.game import Game
from chesspy.board import Board
from chesspy.color import Color
from chesspy.analyzers import is_in_check


class TestRandy(unittest.TestCase):
    def setUp(self):
        self.game = Game()
        self.game.assert_check = False
        self.game.assert_mate = False

        self.player_w = players.Randy(self.game, color=Color.WHITE)
        self.player_b = players.Randy(self.game, color=Color.BLACK)

    def test_rvr(self):
        randys = ((self.player_w, 'white'), (self.player_b, 'black'))
        with open("logs/randy_v_randy.log", "w") as game_file:
            for move, (player, color) in enumerate(itertools.cycle(randys)):
                if self.game.over or move > 300:
                    break

                game_file.write(f"{str(self.game.board)}\n")
                game_file.write(f"{repr(self.game.board)}\n")

                sanstr = player.suggest_move_san()

                game_file.write(f"{move}: {color}: {sanstr}\n")
                game_file.write("\n")

                try:
                    self.game.move_san(sanstr)
                except (IndexError, AssertionError) as exc:
                    traceback.print_exception(exc, file=game_file)
                    raise

    def test_exits_check(self):
        # Randy gets out of check
        for _ in range(1000):
            self.game.board = Board("rnb k nrpp p pp  qp p  p   N     b P            P P PPPP RBQKBNR")
            self.assertTrue(is_in_check(self.game.board, Color.WHITE))
            self.assertFalse(is_in_check(self.game.board, Color.BLACK))

            self.game.turn = Color.WHITE

            sanstr = self.player_w.suggest_move_san()
            self.game.move_san(sanstr)

            self.assertFalse(is_in_check(self.game.board, Color.WHITE))

    def test_avoids_adjacent_kings(self):
        # Randy doesn't move into adjacent kings
        self.assertFalse(True)

    def test_checkmated(self):
        # Randy suggests None when he's checkmated
        self.assertFalse(True)

    def test_stalemated(self):
        # Randy suggests None when he's stalemated
        self.assertFalse(True)