import os
import glob
import logging
import datetime
import unittest
import itertools
import chesspy.game
from chesspy import pgn
from multiprocessing import Process, set_start_method

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

    def test_metadata(self):
        gamefile = pgn.Gamefile("tests/games/immortal.pgn")
        game = next(gamefile)

        # Caution: metadata parsing is based on test data (lichess output), not a careful read of PGN spec.
        #
        self.assertEqual(game.metadata.event, "London")
        self.assertEqual(game.metadata.site, "London ENG")
        self.assertEqual(game.metadata.date, datetime.date(1851, 6, 21))
        self.assertEqual(game.metadata.white, "Adolf Anderssen")
        self.assertEqual(game.metadata.black, "Lionel Adalbert Bagration Felix Kieseritzky")
        self.assertEqual(game.metadata.result, "1-0")
        self.assertEqual(game.metadata.opening, "King's Gambit Accepted: Bishop's Gambit, Bryan Countergambit")
        self.assertEqual(game.metadata.annotator, "https://lichess.org/@/Chess_Poems")

class TestMagnusLichess(unittest.TestCase):
    # indirect correctness check. with enough sample games, bugs compound and reveal themselves.
    #
    # downlaod the file at: https://lichess.org/@/DrNykterstein/download
    # could use any lichess pgn file

    def exec_test_pgn(self, basename, do_print=False, continue_on_fail=False):
        pgnfile = f"tests/games/{basename}.pgn"
        failure_file = f"tests/games/failures.metadata.{basename}.pgn"

        if os.path.exists(pgnfile):
            with open(failure_file, "w") as failure_f:
                failure_f.truncate()

            for pgn_game in pgn.Gamefile(pgnfile):
                game = chesspy.game.Game()
                for move in pgn_game:
                    if do_print:
                        print(f"{int(move.idx/2 + 1)}. {game.turn}: {move.sanstr}")

                    try:
                        game.move_san(move.sanstr)
                    except (AssertionError, IndexError) as e:
                        print("")
                        print(game.board)
                        print(f"|{repr(game.board)}|")
                        print(move.sanstr)
                        with open(failure_file, "a") as failure_f:
                            failure_f.write('[Site "{}"]\n'.format(pgn_game.metadata.site))

                        if continue_on_fail:
                            break
                        else:
                            raise

                    if do_print:
                        print(game.board)
                        print(f"|{repr(game.board)}|")
                        print("")

    def test_long(self):
        if (long_basename := os.environ.get('TEST_LONG', None)):
            logging.disable(logging.CRITICAL)

            filenames = glob.glob(f"tests/games/{long_basename}.*.pgn")
            filenames = [ os.path.basename(n).split('.pgn')[0] for n in filenames ]

            procs = []
            set_start_method('fork') # necessary for MacOS
            for filename in filenames:
                p = Process(target=self.exec_test_pgn, args=(filename,),
                                                       kwargs={'do_print': False, 'continue_on_fail': False})
                p.start()
                procs.append(p)

            [ p.join() for p in procs ]

            logging.disable(logging.NOTSET)

            self.assertEqual([0], list(set(p.exitcode for p in procs)))

    def test_n7ZjoKNR(self):
        self.exec_test_pgn('n7ZjoKNR')

    def test_ZVWsf95x(self):
        self.exec_test_pgn('ZVWsf95x')

    def test_YXOWlp4b(self):
        self.exec_test_pgn('YXOWlp4b')

    def test_1Ot7nMcK(self):
        self.exec_test_pgn('1Ot7nMcK')

    def test_CWefAkiK(self):
        self.exec_test_pgn('CWefAkiK')
