import unittest
import itertools
from chesspy import players
from chesspy.game import Game
from chesspy.color import Color


class TestRandy(unittest.TestCase):
    def test_0(self):
        game = Game()
        player_w = players.Randy(game)
        player_b = players.Randy(game)
        moves = 100

        with open("tests/games/randy_v_randy.txt", "w") as game_file:
            for player in itertools.cycle((player_w, player_b)):
                if game.over or moves < 0:
                    break
                moves -= 1

                sanstr = player.suggest_move_san()
                game_file.write(f"{repr(game.board)}\n")
                game_file.write(sanstr + "\n")

                game.move_san(sanstr)
