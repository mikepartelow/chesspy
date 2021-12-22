import logging
import collections
from .move import Move

def char_to_y(ch):
    logging.debug("char_to_y(%s)", ch)
    return ord('8') - ord(ch)

def char_to_x(ch):
    logging.debug("char_to_x(%s)", ch)
    return ord(ch) - ord('a')

def parse(sanstr, game=None):
    """Parse a SAN formatted string and return a populated Move object.

    Raises IndexError in case of syntax error.
    """
    logging.debug("parse(%s)", sanstr)
    mv = Move()

    if sanstr.startswith('O-O'):
        mv.castle = 'queenside' if 'O-O-O' in sanstr else 'kingside'
        if sanstr.endswith('+'):
            mv.check = True
        elif sanstr.endswith('#'):
            mv.check, mv.mate = True, True
        return mv

    dq = collections.deque(sanstr)

    while mv.dst_y is None:
        match dq.pop():
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

    mv.dst_x = char_to_x(dq.pop())

    while len(dq):
        match dq.pop():
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
            raise IndexError

    if mv.dst_y is None or mv.dst_x is None or mv.dst_y < 0 or mv.dst_y > 7 or mv.dst_x < 0 or mv.dst_x > 7:
        # invalid SAN like "33"
        raise IndexError

    return mv