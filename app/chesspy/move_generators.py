"""Move Generators generate lists of legal moves for pieces on a Board."""
from .board import in_bounds
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
        case 'K' | 'k':
            return king_moves_for(y, x, board)
        case 'R' | 'r':
            return rook_moves_for(y, x, board)
        case 'B' | 'b':
            return bishop_moves_for(y, x, board)
        case 'Q' | 'q':
            return list(set(rook_moves_for(y, x, board, piece='Q') + bishop_moves_for(y, x, board, piece='Q')))

    raise IndexError


def collision(y, x, piece, board):
    """Returns True if (y, x) on board contains a piece of the same color as piece."""

    return (p := board.square_at(y, x)) and color_of(p) == color_of(piece)


def pawn_moves_for(y, x, board):
    """Return a list of legal moves for the Pawn at (y, x) on the given board."""
    pawn = board.square_at(y, x)
    assert pawn.upper() == 'P'

    if color_of(pawn) == Color.BLACK:
        def ahead_of(y, inc=1): return y + inc  # pylint: disable=multiple-statements
        starting_row = 1
    else:
        def ahead_of(y, inc=1): return y - inc  # pylint: disable=multiple-statements
        starting_row = 6

    moves = [(ahead_of(y), x)]

    if y == starting_row:
        moves.append((ahead_of(y, 2), x))

    return moves


def knight_moves_for(y, x, board):
    """Return a list of legal moves for the Knight at (y, x) on the given board."""
    knight = board.square_at(y, x)
    assert knight.upper() == 'N'

    offsets_y = (-1, -1,  1, 1, -2, -2,  2, 2)
    offsets_x = (-2,  2, -2, 2, -1,  1, -1, 1)

    moves = []

    for (offset_y, offset_x) in zip(offsets_y, offsets_x):
        dst_y, dst_x = y+offset_y, x+offset_x
        if in_bounds(dst_y, dst_x) and not collision(dst_y, dst_x, knight, board):
            moves.append((dst_y, dst_x))

    return moves


def king_moves_for(y, x, board):
    """Return a list of legal moves for the King at (y, x) on the given board."""
    king = board.square_at(y, x)
    assert king.upper() == 'K'

    moves = []

    for dst_y in range(y-1, y+2):
        for dst_x in range(x-1, x+2):
            if in_bounds(dst_y, dst_x) and \
                    (dst_y, dst_x) != (y, x) and \
                    not collision(dst_y, dst_x, king, board):
                moves.append((dst_y, dst_x))

    return moves


def rook_moves_for(y, x, board, piece='R'):
    """Return a list of legal moves for the Rook-like piece at (y, x) on the given board."""
    rook = board.square_at(y, x)
    assert rook.upper() == piece

    moves = []

    for dst_y in range(0, 8):
        if dst_y != y:
            if collision(dst_y, x, rook, board):
                break
            moves.append((dst_y, x))

    for dst_x in range(0, 8):
        if dst_x != x:
            if collision(y, dst_x, rook, board):
                break
            moves.append((y, dst_x))

    return moves


def bishop_moves_for(y, x, board, piece='B'):
    """Return a list of legal moves for the Bishop-like piece at (y, x) on the given board."""
    bishop = board.square_at(y, x)
    assert bishop.upper() == piece

    moves = []
    incrementors = ((-1, -1), (1, 1), (1, -1), (-1, 1),)

    for incs in incrementors:
        dst_y, dst_x = y, x
        while in_bounds(dst_y, dst_x):
            if (dst_y, dst_x) != (y, x):
                if collision(dst_y, dst_x, bishop, board):
                    break
                moves.append((dst_y, dst_x))
            dst_y, dst_x = dst_y - incs[0], dst_x - incs[1]

    return moves
