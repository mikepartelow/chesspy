"""Implements Analyzers that give insights into Board positions."""
import logging
from .color import Color, colorize


def is_in_check(board, color, king_pos=None):
    """Returns True if the given color's player is in check on the given board."""
    logging.debug("CheckAnalyzer::is_in_check(%s)", color)

    king_pos = king_pos or board.king_position(color)
    logging.debug("CheckAnalyzer::is_in_check() : king_pos = %r", king_pos)

    if is_in_knight_check(board, color, king_pos):
        return True

    if is_in_diagonal_check(board, color, king_pos):
        return True

    if is_in_horizontal_check(board, color, king_pos):
        return True

    if is_in_pawn_check(board, color, king_pos):
        return True

    logging.debug("CheckAnalyzer::is_in_check(%s) -> False", color)
    return False


def is_in_knight_check(board, color, king_pos=None):
    """Returns True if the given color's player is in check on the given board from opponent's Knight."""
    logging.debug("CheckAnalyzer::is_in_knight_check(%s)", color)

    king_pos = king_pos or board.king_position(color)
    logging.debug("CheckAnalyzer::is_in_knight_check() : king_pos = %r", king_pos)

    opponent_knight = colorize('N', color.opponent())

    offsets_y = (-1, -1,  1, 1, -2, -2,  2, 2)
    offsets_x = (-2,  2, -2, 2, -1,  1, -1, 1)
    for (y_offset, x_offset) in zip(offsets_y, offsets_x):
        y, x = king_pos.y + y_offset, king_pos.x + x_offset
        if 0 <= y < 8 and 0 <= x < 8:
            if board.square_at(y, x) == opponent_knight:
                logging.debug("CheckAnalyzer::is_in_knight_check() -> True : Knight at (%s, %s)", y, x)
                return True

    return False


def is_in_diagonal_check(board, color, king_pos=None):
    """Returns True if the given color's player is in check on the given board from opponent's Bishop or Queen."""
    logging.debug("CheckAnalyzer::is_in_diagonal_check(%s)", color)

    king_pos = king_pos or board.king_position(color)
    logging.debug("CheckAnalyzer::is_in_diagonal_check() : king_pos = %r", king_pos)

    opponent_bishop = colorize('B', color.opponent())
    opponent_queen = colorize('Q', color.opponent())

    incrementors = ((-1, -1), (1, 1), (1, -1), (-1, 1),)
    for increments in incrementors:
        if (p := board.find_first_on_diagonal(king_pos, *increments)) and p.piece in (opponent_bishop, opponent_queen):
            logging.debug("CheckAnalyzer::is_in_diagonal_check() -> True : Bishop at (%s, %s)", *p[1:])
            return True

    return False


def is_in_horizontal_check(board, color, king_pos=None):
    """Returns True if the given color's player is in check on the given board from opponent's Rook or Queen."""
    logging.debug("CheckAnalyzer::is_in_horizontal_check(%s)", color)

    king_pos = king_pos or board.king_position(color)
    logging.debug("CheckAnalyzer::is_in_horizontal_check() : king_pos = %r", king_pos)

    opponent_rook = colorize('R', color.opponent())
    opponent_queen = colorize('Q', color.opponent())

    incrementors = ((0, -1), (0, 1), (1, 0), (-1, 0),)
    for increments in incrementors:
        if (p := board.find_first_on_h_or_v(king_pos, *increments)) and p.piece in (opponent_rook, opponent_queen):
            logging.debug("CheckAnalyzer::is_in_horizontal_check() -> True : Rook at (%s, %s)", *p[1:])
            return True

    return False


def is_in_pawn_check(board, color, king_pos=None):
    """Returns True if the given color's player is in check on the given board from opponent's Pawn."""
    logging.debug("CheckAnalyzer::is_in_pawn_check(%s)", color)

    king_pos = king_pos or board.king_position(color)
    logging.debug("CheckAnalyzer::is_in_pawn_check() : king_pos = %r", king_pos)

    opponent_pawn = colorize('P', color.opponent())

    if color == Color.WHITE:
        pawn_maybes = (king_pos.y - 1, king_pos.x - 1), (king_pos.y - 1, king_pos.x + 1)
    else:
        pawn_maybes = (king_pos.y + 1, king_pos.x - 1), (king_pos.y + 1, king_pos.x + 1)

    for pawn_maybe in pawn_maybes:
        if pawn_maybe[0] >= 0 and pawn_maybe[0] < 8 and pawn_maybe[1] >= 0 and pawn_maybe[1] < 8:
            if board.square_at(*pawn_maybe) == opponent_pawn:
                logging.debug("CheckAnalyzer::is_in_pawn_check() -> True : Pawn at (%s, %s)", *pawn_maybe)
                return True

    return False