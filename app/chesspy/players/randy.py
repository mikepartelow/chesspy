"""Randy is a chess player who moves randomly."""
import random
from ..san import make_san
from .player import ChessPlayer


class Randy(ChessPlayer):
    """Randy moves randomly."""
    def __str__(self):
        return "Randy"

    def suggest_move_san(self):
        """Returns Randy's best idea for a move, or None if there are no legal moves."""
        moves = self.imagine_moves()

        random.shuffle(moves)  # that's so Randy

        for move in moves:
            sanstr = make_san(move, verbose=True)
            if self.check_move(sanstr):
                return sanstr

        return None
