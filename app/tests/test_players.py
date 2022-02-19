import unittest
import itertools
import traceback
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

                game_file.write(f"{str(game.board)}\n")
                game_file.write(f"{repr(game.board)}\n")

                sanstr = player.suggest_move_san()

                game_file.write(f"{move}: {color}: {sanstr}\n")
                game_file.write("\n")

                try:
                    game.move_san(sanstr)
                except (IndexError, AssertionError) as exc:
                    traceback.print_exception(exc, file=game_file)
                    raise