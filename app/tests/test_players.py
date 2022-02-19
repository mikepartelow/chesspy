import unittest
import itertools
from chesspy import players
from chesspy.game import Game
from chesspy.color import Color


class TestRandy(unittest.TestCase):
    def test_0(self):
        game = Game()
        game.assert_check = False
        game.assert_mate = False

        player_w = players.Randy(game, color=Color.WHITE)
        player_b = players.Randy(game, color=Color.BLACK)

        with open("logs/randy_v_randy.log", "w") as game_file:
            for move, (player, color) in enumerate(itertools.cycle(((player_w, 'white'), (player_b, 'black')))):
                if game.over or move > 200:
                    break

                sanstr = player.suggest_move_san()

                game.move_san(sanstr)

                game_file.write(f"{str(game.board)}\n")
                game_file.write(f"{repr(game.board)}\n")
                game_file.write(f"{move}: {color}: {sanstr}\n")
                game_file.write("\n")

                # FIXME: game should assert the 2 kings are on the board after each move