"""Move Generators generate lists of legal moves for pieces on a Board."""
import itertools
from .board import in_bounds
from .color import Color, color_of


def moves_for(y, x, board):
    """Yields legal moves for the piece at (y, x) on the given board.

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
            return itertools.chain(rook_moves_for(y, x, board, piece='Q'), bishop_moves_for(y, x, board, piece='Q'))

    raise IndexError


def collision(y, x, piece, board):
    """Returns True if (y, x) on board contains a piece of the same color as piece."""

    if (p := board.square_at(y, x)):
        return 'blocked' if color_of(p) == color_of(piece) else 'capture'
    return False


def pawn_moves_for(y, x, board):
    """Yields legal moves for the Pawn at (y, x) on the given board."""
    pawn = board.square_at(y, x)
    assert pawn.upper() == 'P'

    if color_of(pawn) == Color.BLACK:
        def ahead_of(y, inc=1): return y + inc  # pylint: disable=multiple-statements
        starting_row = 1
    else:
        def ahead_of(y, inc=1): return y - inc  # pylint: disable=multiple-statements
        starting_row = 6

    # collision() returning 'capture' for ahead_of() pawn is never really a capture, since pawn
    # only captures diagonally, so we treat 'capture' and 'blocked' the same here
    #
    if not collision(ahead_of(y), x, pawn, board):
        yield (ahead_of(y), x)

        if y == starting_row:
            if not collision(ahead_of(y, 2), x, pawn, board):
                yield (ahead_of(y, 2), x)

    for offset_x in (-1, 1):
        dst_y, dst_x = ahead_of(y), x+offset_x
        if in_bounds(dst_y, dst_x) and collision(dst_y, dst_x, pawn, board) == 'capture':
            yield (dst_y, dst_x)


def knight_moves_for(y, x, board):
    """Yields legal moves for the Knight at (y, x) on the given board."""
    knight = board.square_at(y, x)
    assert knight.upper() == 'N'

    offsets_y = (-1, -1,  1, 1, -2, -2,  2, 2)
    offsets_x = (-2,  2, -2, 2, -1,  1, -1, 1)

    for (offset_y, offset_x) in zip(offsets_y, offsets_x):
        dst_y, dst_x = y+offset_y, x+offset_x
        if in_bounds(dst_y, dst_x):
            match collision(dst_y, dst_x, knight, board):
                case 'blocked':
                    pass
                case _:
                    yield (dst_y, dst_x)


def king_moves_for(y, x, board):
    """Yields legal moves for the King at (y, x) on the given board."""
    king = board.square_at(y, x)
    assert king.upper() == 'K'

    for dst_y in range(y-1, y+2):
        for dst_x in range(x-1, x+2):
            if in_bounds(dst_y, dst_x) and (dst_y, dst_x) != (y, x):
                match collision(dst_y, dst_x, king, board):
                    case 'blocked':
                        pass
                    case _:
                        yield (dst_y, dst_x)


def rook_moves_for(y, x, board, piece='R'):
    """Yields legal moves for the Rook-like piece at (y, x) on the given board."""
    rook = board.square_at(y, x)
    assert rook.upper() == piece

    for the_range in (range(y+1, 8), range(y-1, -1, -1)):
        for dst_y in the_range:
            match collision(dst_y, x, rook, board):
                case 'capture':
                    yield (dst_y, x)
                    break
                case 'blocked':
                    break
            yield (dst_y, x)

    for the_range in (range(x+1, 8), range(x-1, -1, -1)):
        for dst_x in the_range:
            match collision(y, dst_x, rook, board):
                case 'capture':
                    yield (y, dst_x)
                    break
                case 'blocked':
                    break
            yield (y, dst_x)


def bishop_moves_for(y, x, board, piece='B'):
    """Yields legal moves for the Bishop-like piece at (y, x) on the given board."""
    bishop = board.square_at(y, x)
    assert bishop.upper() == piece

    incrementors = ((-1, -1), (1, 1), (1, -1), (-1, 1),)

    for incs in incrementors:
        dst_y, dst_x = y, x
        while in_bounds(dst_y, dst_x):
            if (dst_y, dst_x) != (y, x):
                match collision(dst_y, dst_x, bishop, board):
                    case 'capture':
                        yield (dst_y, dst_x)
                        break
                    case 'blocked':
                        break
                yield (dst_y, dst_x)
            dst_y, dst_x = dst_y - incs[0], dst_x - incs[1]

