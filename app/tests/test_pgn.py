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

        for idx, sanstr in enumerate(pgn.moves('tests/games/evergreen.pgn')):
            turn = g.turn
            print(f"{int( idx/2+1)}. {turn}: {sanstr}")
            g.move_san(sanstr)
            print(g.board)
            print("")
            print(repr(g.board))

