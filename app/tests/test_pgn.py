import os
import unittest
import itertools
from chesspy import pgn
import chesspy.game

def board_reprs(path):
    with open(path, 'r') as f:
        for line in f.readlines():
            yield line.replace("\n", '') # can't strip because space at EOL is OK!

class TestPgnVsReprs(unittest.TestCase):
    def exec_test_pgn(self, basename, do_print=False):
        
        reprspath = f"tests/games/{basename}.boardreprs.txt"

        for pgn_game in pgn.Gamefile(f"tests/games/{basename}.pgn"):
            game = chesspy.game.Game()
            for move, boardrepr in itertools.zip_longest(pgn_game, board_reprs(reprspath)):
                if do_print:
                    print(f"{int(move.idx/2 + 1)}. {game.turn}: {move.sanstr}")  

                game.move_san(move.sanstr)  

                if do_print:
                    print(game.board)
                    print("")

                self.assertEqual(repr(game.board), boardrepr, move.idx)

    def test_immortal(self): 
        self.exec_test_pgn('immortal', do_print=False)

    def test_evergreen(self):
        self.exec_test_pgn('evergreen', do_print=False)

class TestPgnBasic(unittest.TestCase):
    def exec_test_pgn(self, basename, game_count=1, do_print=False):
        pgnfile = f"tests/games/{basename}.pgn"

        game_count_actual = 0

        for pgn_game in pgn.Gamefile(pgnfile):
            game = chesspy.game.Game()
            game_count_actual += 1
            for move in pgn_game:
                if do_print:
                    print(f"{int(move.idx/2 + 1)}. {game.turn}: {move.sanstr}")  

                game.move_san(move.sanstr)  

                if do_print:
                    print(game.board)
                    print("")

        self.assertEqual(game_count, game_count_actual)

    def test_multi(self):
        self.exec_test_pgn('multi', game_count=3)

class TestMagnusLichess(unittest.TestCase):
    # indirect correctness check. with enough sample games, bugs compound and reveal themselves.
    #
    # downlaod the file at: https://lichess.org/@/DrNykterstein/download
    # could use any lichess pgn file

    def exec_test_pgn(self, basename, game_count=1, do_print=False):
        pgnfile = f"tests/games/{basename}.pgn"

        if os.path.exists(pgnfile):
            game_count_actual = 0

            for pgn_game in pgn.Gamefile(pgnfile):
                game = chesspy.game.Game()
                game_count_actual += 1
                for move in pgn_game:
                    if do_print:
                        print(f"{int(move.idx/2 + 1)}. {game.turn}: {move.sanstr}")  

                    game.move_san(move.sanstr)  

                    if do_print:
                        print(game.board)
                        print("")

            self.assertEqual(game_count, game_count_actual)
                                  
    def test_DrNykterstein(self):
        # AssertionError: 9667 != 9662
        # FIXME: cat lichess_DrNykterstein_2022-01-04 | grep UTCDate | wc -l == 9667, but pgn.Gamefile counts 9662
        #        discover discrepancy by parsing metadata like UTCDate, recording to file, diffing vs .pgn file
        #
        self.exec_test_pgn('lichess_DrNykterstein_2022-01-04', game_count=9667, do_print=True)

    def test_n7ZjoKNR(self):
        self.exec_test_pgn('n7ZjoKNR')

    def test_ZVWsf95x(self):
        self.exec_test_pgn('ZVWsf95x')

    def test_YXOWlp4b(self):
        self.exec_test_pgn('YXOWlp4b')

    def test_1Ot7nMcK(self):
        self.exec_test_pgn('1Ot7nMcK')

        
