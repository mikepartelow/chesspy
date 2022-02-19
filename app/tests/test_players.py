import unittest
from chesspy import players
from chesspy.game import Game
from chesspy.color import Color


class TestRandy(unittest.TestCase):
    def test_0(self):
        game = Game()
        player_w = players.Randy(game)
        player_b = players.Randy(game)

        with open("tests/games/randy_v_randy.txt", "w") as game_file:
            for turn in range(50):
                if game.over:
                    break

                sanstr = player_w.suggest_move_san()
                game_file.write(f"{repr(game.board)}\n")
                game_file.write(sanstr + "\n")

                game.move_san(sanstr)

                if game.over:
                    break

                sanstr = player_b.suggest_move_san()
                game_file.write(f"{repr(game.board)}\n")
                game_file.write(sanstr + "\n")

                game.move_san(sanstr)

