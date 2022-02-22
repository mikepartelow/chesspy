"""Bubbles is smart but conventional."""
from .player import ChessPlayer

class Bubbles(ChessPlayer):
    # iterative, not recursive
    # search harder as number of pieces decreases!
    # openings DB (scores not based on sum of piece values, based on strength of opening sequence)
    # smarter pruning than random MOVES_TO_CONSIDER. e.g. always consider moving Q, or... ??
    pass
