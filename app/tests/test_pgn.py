import os
import unittest
import itertools
from chesspy import game, pgn

def board_reprs(path):
    with open(path, 'r') as f:
        for line in f.readlines():
            yield line.replace("\n", '') # can't strip because space at EOL is OK!

class TestPgnBasic(unittest.TestCase):
    def test_immortal(self):        
        g = game.Game()

        for idx, (sanstr, boardrepr) in enumerate(itertools.zip_longest(pgn.moves('tests/games/immortal.pgn'), board_reprs('tests/games/immortal.boardreprs.txt'))):
            turn = g.turn
            # print(f"{int( idx/2+1)}. {turn}: {sanstr}")
            g.move_san(sanstr)
            # print(g.board)
            # print("")
            self.assertEqual(repr(g.board), boardrepr, idx)

    def test_evergreen(self):
        g = game.Game()

        for idx, (sanstr, boardrepr) in enumerate(itertools.zip_longest(pgn.moves('tests/games/evergreen.pgn'), board_reprs('tests/games/evergreen.boardreprs.txt'))):
            turn = g.turn
            # print(f"{int( idx/2+1)}. {turn}: {sanstr}")
            g.move_san(sanstr)
            # print(g.board)
            # print("")
            self.assertEqual(repr(g.board), boardrepr, idx)

class TestMagnusLichess(unittest.TestCase):
    # indirect correctness check. with enough sample games, bugs compound and reveal themselves.
    #
    # downlaod the file at: https://lichess.org/@/DrNykterstein/download
    # could use any lichess pgn file

    def test_pgn(self):
        g = game.Game()

        pgnfile = 'tests/games/lichess_DrNykterstein_2022-01-04.pgn'

        if os.path.exists(pgnfile):
            for sanstr in pgn.moves(pgnfile):
                # print('"{}"'.format(repr(g.board)))
                # print(sanstr)

                g.move_san(sanstr)          
                if g.over:
                    g = game.Game()
                    continue
          

    def test_n7ZjoKNR(self):
        g = game.Game()

        pgnfile = 'tests/games/n7ZjoKNR.pgn'

        for idx, sanstr in enumerate(pgn.moves(pgnfile)):
            turn = g.turn
            # print(f"{int( idx/2+1)}. {turn}: {sanstr}")
            g.move_san(sanstr)
            if g.over:
                break
            # print(g.board)
            # print("")

    def test_ZVWsf95x(self):
        g = game.Game()

        pgnfile = 'tests/games/ZVWsf95x.pgn'

        for idx, sanstr in enumerate(pgn.moves(pgnfile)):
            turn = g.turn
            # print(f"{int( idx/2+1)}. {turn}: {sanstr}")
            g.move_san(sanstr)
            if g.over:
                break
            # print(g.board)
            # print("'{}'".format(repr(g.board)))
            # print("")

    def test_YXOWlp4b(self):
        g = game.Game()

        pgnfile = 'tests/games/YXOWlp4b.pgn'

        for idx, sanstr in enumerate(pgn.moves(pgnfile)):
            turn = g.turn
            # print(f"{int( idx/2+1)}. {turn}: {sanstr}")
            g.move_san(sanstr)
            if g.over:
                break
            # print(g.board)
            # print('"{}"'.format(repr(g.board)))
            # print("")

        
