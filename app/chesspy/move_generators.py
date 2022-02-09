"""Move Generators generate lists of legal moves for pieces on a Board."""
import logging
from .color import Color, color_of


def moves_for(y, x, board):
    """Return a list of legal moves for the piece at (y, x) on the given board.

    Raises IndexError if no piece exists at (y, x).
    """
    match board.square_at(y, x):
        case 'P' | 'p':
            return pawn_moves_for(y, x, board)
        case 'N' | 'n':
            return knight_moves_for(y, x, board)

    raise IndexError


def pawn_moves_for(y, x, board):
    """Return a list of legal moves for the Pawn at (y, x) on the given board."""
    pawn = board.square_at(y, x)
    assert pawn in ('p', 'P')

    if color_of(pawn) == Color.BLACK:
        # FIXME: DRY, copied from game.py
        def ahead_of(y, inc=1): return y + inc
        starting_row = 1
    else:
        # FIXME: DRY, copied from game.py
        def ahead_of(y, inc=1): return y - inc
        starting_row = 6

    moves = [(ahead_of(y), x)]

    if y == starting_row:
        moves.append((ahead_of(y, 2), x))

    return moves


def knight_moves_for(y, x, board):
    """Return a list of legal moves for the Knight at (y, x) on the given board."""
    knight = board.square_at(y, x)
    assert knight in ('n', 'N')

    offsets_y = (-1, -1,  1, 1, -2, -2,  2, 2)
    offsets_x = (-2,  2, -2, 2, -1,  1, -1, 1)

    moves = []

    for (offset_y, offset_x) in zip(offsets_y, offsets_x):
        moves.append((y+offset_y, x+offset_x))

    return moves



