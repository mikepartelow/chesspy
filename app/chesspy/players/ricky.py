"""Ricky plays smart chess. He's self-smarted basically by himself."""
# pylint:disable=wrong-import-order
import random
from ..san import make_san
from ..color import color_of
from .player import ChessPlayer
from chesspy.analyzers import is_in_check, is_in_mate

PIECE_VALUES = dict(P=1, N=3, B=3, R=5, Q=9, K=1)


class Ricky(ChessPlayer):
    """Ricky thinks a little about his moves."""
    moves_suggested = set()

    def __str__(self):
        return "Ricky"

    def score_move_san(self, sanstr):
        """Evaluates a move. Returns None if the move is not legal, or a score for relative move value."""
        score = None

        if (test_game := self.test_move_san(sanstr)):
            score = 0

            # easy/dumb way to discourage repeating the same move.
            #
            if sanstr in self.moves_suggested:
                score -= 20

            for y in range(8):
                for x in range(8):
                    if (p := test_game.board.square_at(y, x)):
                        if color_of(p) == self.color:
                            score += PIECE_VALUES[p.upper()]
                        else:
                            score -= PIECE_VALUES[p.upper()]

            if is_in_check(test_game.board, self.color.opponent()):
                score += 1000
            if is_in_mate(test_game.board, self.color.opponent()):
                score += 1000000

        return score

    def suggest_move_san(self):
        """Returns Ricky's "best idea" (low expectations) for a move, or None if there are no legal moves."""
        best_move_score = float("-inf")
        best_move_sanstr = None

        for move in self.imagine_moves():
            sanstr = make_san(move, verbose=True)
            if (score := self.score_move_san(sanstr)) is not None:
                score += 2*PIECE_VALUES[move.piece or 'P']  # bias toward moving high value pieces
                if score > best_move_score or (score == best_move_score and random.randrange(3) == 1):
                    best_move_score = score
                    best_move_sanstr = sanstr

        if best_move_sanstr:
            self.moves_suggested.add(best_move_sanstr)

        return best_move_sanstr
