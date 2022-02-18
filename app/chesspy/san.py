"""Parser for Standard Algebraic Notation"""

import logging
from .move import Move
from .castle import Castle

RESULT_SAN = ('1-0', '0-1', '1/2-1/2')


def char_to_y(ch):
    """Given a chess file a-h return a y coordinate 0-7"""
    logging.debug("char_to_y(%s)", ch)
    return ord('8') - ord(ch)


def char_to_x(ch):
    """Given a chess rank 1-8 return a y coordinate 7-0"""
    logging.debug("char_to_x(%s)", ch)
    return ord(ch) - ord('a')


def y_to_char(y):
    """Given a y coordinate 7-0 return a chess file a-h"""
    logging.debug("y_to_char(%s)", y)
    return chr(ord('8') - y)


def x_to_char(x):
    """Given a x coordinate 0-7 return a chess rank 1-8"""
    logging.debug("x_to_char(%s)", x)
    return chr(ord('a') + x)


def out_of_bounds(coords):
    """Given coordinates (y, x) return True if the coordinates are valid for 0-indexed 8x8 grid."""
    return coords[0] < 0 or coords[0] > 7 or coords[1] < 0 or coords[1] > 7


def make_san(move, verbose=False):
    """Create a SAN formatted string from the given Move object."""
    piece = move.piece or ''
    rank_src, file_src = y_to_char(move.src_y), x_to_char(move.src_x)
    rank_dst, file_dst = y_to_char(move.dst_y), x_to_char(move.dst_x)
    capture = 'x' if move.capture else ''

    if move.mate:
        check = '#'
    elif move.check:
        check = '+'
    else:
        check = ''

    return f"{piece}{file_src}{rank_src}{capture}{file_dst}{rank_dst}{check}"


def parse(sanstr, game=None):
    """Parse a SAN formatted string and return a populated Move object.

    Raises IndexError in case of syntax error.
    """
    logging.debug("parse(%s)", sanstr)
    mv = Move()

    if sanstr.startswith('O-O'):
        mv.castle = Castle.QUEENSIDE if 'O-O-O' in sanstr else Castle.KINGSIDE
        if sanstr.endswith('+'):
            mv.check = True
        elif sanstr.endswith('#'):
            mv.check, mv.mate = True, True
        return mv

    sanchars = list(sanstr)

    while mv.dst_y is None:
        match sanchars.pop():
            case '!' | '?':
                # annotations: ignore them
                pass
            case '+':
                mv.check = True
            case '#':
                mv.check, mv.mate = (True, True)
            case ('R' | 'N' | 'B' | 'Q') as promotion:
                mv.promotion = promotion
            case '=':
                if mv.promotion is None:
                    raise IndexError
            case _ as ch:
                mv.dst_y = char_to_y(ch)

    mv.dst_x = char_to_x(sanchars.pop())

    while sanchars:
        match sanchars.pop():
            case 'x':
                mv.capture = True
            case ('a' | 'b' | 'c' | 'd' | 'e' | 'f' | 'g' | 'h') as src_file:
                mv.src_x = char_to_x(src_file)
            case ('1' | '2' | '3' | '4' | '5' | '6' | '7' | '8') as src_rank:
                mv.src_y = char_to_y(src_rank)
            case ('R' | 'N' | 'B' | 'Q' | 'K') as piece:
                mv.piece = piece
            case _:
                raise IndexError

    if mv.piece is None:
        mv.piece = 'P'

    if game is not None:
        mv = game.deduce_src(mv)
        if mv.src_y is None or mv.src_x is None:
            # failed to fully deduce src
            raise IndexError("Failed to deduce_src()")

    if mv.dst_y is None or mv.dst_x is None or out_of_bounds(mv.dst):
        # invalid SAN like "33"
        raise IndexError

    return mv
