import os
import unittest
import itertools
from chesspy import pgn

def board_reprs(path):
    with open(path, 'r') as f:
        for line in f.readlines():
            yield line.replace("\n", '') # can't strip because space at EOL is OK!

class TestPgnBasic(unittest.TestCase):
    def exec_test_pgn(self, basename, do_print=False):
        gamefile = pgn.Gamefile(f"tests/games/{basename}.pgn")     
        reprspath = f"tests/games/{basename}.boardreprs.txt"
        for game, moves in gamefile.games():
            for move, boardrepr in itertools.zip_longest(moves, board_reprs(reprspath)):
                print(f"{int(move.idx/2 + 1)}. {game.turn}: {move.sanstr}")  
                game.move_san(move.sanstr)  
                print(game.board)
                print("")
                self.assertEqual(repr(game.board), boardrepr, idx)

    def test_immortal(self): 
        self.exec_test_pgn('immortal', do_print=True)

    def test_evergreen(self):
        self.exec_test_pgn('evergreen', do_print=True)

class TestMagnusLichess(unittest.TestCase):
    # indirect correctness check. with enough sample games, bugs compound and reveal themselves.
    #
    # downlaod the file at: https://lichess.org/@/DrNykterstein/download
    # could use any lichess pgn file

    def exec_test_pgn(self, basename, do_print=False):
        g = game.Game()

        pgnfile = f"tests/games/{basename}.pgn"

        if os.path.exists(pgnfile):
            for sanstr in pgn.moves(pgnfile):
                if do_print:
                    print(g.board)
                    print('"{}"'.format(repr(g.board)))
                    print(f"{g.turn}: {sanstr}")

                g.move_san(sanstr)          
                if g.over:
                    g = game.Game()
                    continue
          
    def test_DrNykterstein(self):
        self.exec_test_pgn('lichess_DrNykterstein_2022-01-04', do_print=True)

    def test_n7ZjoKNR(self):
        self.exec_test_pgn('n7ZjoKNR')

    def test_ZVWsf95x(self):
        self.exec_test_pgn('ZVWsf95x')

    def test_YXOWlp4b(self):
        self.exec_test_pgn('YXOWlp4b')

    def test_1Ot7nMcK(self):
        self.exec_test_pgn('1Ot7nMcK')

        
