from .board import Board
from .color import Color
from . import san
import itertools
import logging

def color_of(ch):
    if ch.isupper():
        return Color.WHITE
    else:
        return Color.BLACK

def colorize(ch, color):
    if color == Color.WHITE:
        return ch.upper()
    else:
        return ch.lower()

def deduce_src_moves_like_rook(mv, board, p_target):
    if (p := board.find_first_on_h_or_v(mv.dst, 0, -1, mv.src_y, mv.src_x)) and p[0] == p_target:
        mv.src_y, mv.src_x = p[1:]
    elif (p := board.find_first_on_h_or_v(mv.dst, 0, 1, mv.src_y, mv.src_x)) and p[0] == p_target:
        mv.src_y, mv.src_x = p[1:]
    elif (p := board.find_first_on_h_or_v(mv.dst, 1, 0, mv.src_y, mv.src_x)) and p[0] == p_target:
        mv.src_y, mv.src_x = p[1:]
    elif (p := board.find_first_on_h_or_v(mv.dst, -1, 0, mv.src_y, mv.src_x)) and p[0] == p_target:
        mv.src_y, mv.src_x = p[1:]

    return mv.src != (None, None)

def deduce_src_moves_like_bishop(mv, board, p_target):
    if (p := board.find_first_on_diagonal(mv.dst, -1, -1, mv.src_y, mv.src_x)) and p[0] == p_target:
        mv.src_y, mv.src_x = p[1:]
    elif (p := board.find_first_on_diagonal(mv.dst, 1, 1, mv.src_y, mv.src_x)) and p[0] == p_target:
        mv.src_y, mv.src_x = p[1:]
    elif (p := board.find_first_on_diagonal(mv.dst, 1, -1, mv.src_y, mv.src_x)) and p[0] == p_target:
        mv.src_y, mv.src_x = p[1:]
    elif (p := board.find_first_on_diagonal(mv.dst, -1, 1, mv.src_y, mv.src_x)) and p[0] == p_target:
        mv.src_y, mv.src_x = p[1:]

    return mv.src != (None, None)

class Game:
    def __init__(self):
        self.board = Board()
        self.turn = Color.WHITE

    def move_san(self, sanstr):
        logging.debug("Game::move_san(%s)", sanstr)

        capture = None

        mv = san.parse(sanstr, self)

        if mv.castle:
            # FIXME: refactor to do_castle()
            # FIXME: enum
            if mv.castle == 'kingside':
                if self.turn == Color.WHITE:
                    self.board.place_piece_at('K', 7 , 6)
                    self.board.place_piece_at('R', 7, 5)
                    self.board.place_piece_at(None, 7, 4)
                    self.board.place_piece_at(None, 7, 7)
                else:
                    self.board.place_piece_at('k', 0, 6)
                    self.board.place_piece_at('r', 0, 5)
                    self.board.place_piece_at(None, 0, 4)
                    self.board.place_piece_at(None, 0, 7)
            elif mv.castle == 'queenside':
                if self.turn == Color.WHITE:
                    self.board.place_piece_at('K', 7, 2)
                    self.board.place_piece_at('R', 7, 3)
                    self.board.place_piece_at(None, 7, 4)
                    self.board.place_piece_at(None, 7, 0)
                else:
                    self.board.place_piece_at('k', 0 , 2)
                    self.board.place_piece_at('r', 0, 3)
                    self.board.place_piece_at(None, 0, 4)
                    self.board.place_piece_at(None, 0, 0)
        else:
            piece = self.board.square_at(mv.src_y, mv.src_x)
            assert(piece is not None)

            capture = self.board.square_at(mv.dst_y, mv.dst_x)
            assert((capture is None) == (mv.capture is False))

            self.board.place_piece_at(piece, mv.dst_y, mv.dst_x)
            self.board.place_piece_at(None, mv.src_y, mv.src_x)

        self.turn = Color.toggle(self.turn)

        return capture

    def deduce_src(self, mv):
        """Given a partially constructed Move, deduce the src coordinates for the move.
        """
        # FIXME: this is well tested through test_san but deserves its own unit test.

        if (p := self.board.square_at(mv.dst_y, mv.dst_x)) and color_of(p) == self.turn:
            # can't land on our own piece
            raise IndexError

        match mv.piece:
            case 'P':
                if self.turn == Color.WHITE:
                    def ahead_of(y): return y + 1
                    def behind(y):   return y - 1
                else:
                    def ahead_of(y): return y - 1
                    def behind(y):   return y + 1

                if mv.capture:
                    p_src = colorize('P', self.turn)
                    if (p_dst := self.board.square_at(mv.dst_y, mv.dst_x)) and color_of(p_dst) != color_of(p_src):
                        if mv.src_x and self.board.square_at(ahead_of(mv.dst_y), mv.src_x) == p_src:
                            mv.src_y = ahead_of(mv.dst_y)
                        elif mv.dst_x > 0 and self.board.square_at(ahead_of(mv.dst_y), mv.dst_x - 1) == p_src:
                            mv.src_y, mv.src_x = ahead_of(mv.dst_y), mv.dst_x - 1
                        elif mv.dst_x < 7 and self.board.square_at(ahead_of(mv.dst_y), mv.dst_x + 1) == p_src:
                            mv.src_y, mv.src_x = ahead_of(mv.dst_y), mv.dst_x + 1

                elif self.board.square_at(mv.dst_y, mv.dst_x) is None:
                    if self.turn == Color.WHITE:
                        idx, pawn, origin = 1, 'P', 6
                    else:
                        idx, pawn, origin = -1, 'p', 1

                    if (p := self.board.find_first_on_h_or_v(mv.dst, idx, 0)) and p[0] == pawn:
                        if (abs(mv.dst_y - p[1]) == 2 and p[1] == origin) or abs(mv.dst_y - p[1]) == 1:
                            mv.src_y, mv.src_x = p[1:]

            case 'N':
                p_src = colorize('N', self.turn)
                offsets_y = (-1, -1,  1, 1, -2, -2,  2, 2)
                offsets_x = (-2,  2, -2, 2, -1,  1, -1, 1)

                for (offset_y, offset_x) in zip(offsets_y, offsets_x):
                    src_y, src_x = mv.dst_y + offset_y, mv.dst_x + offset_x

                    if (mv.src_y and src_y != mv.src_y) or (mv.src_x and src_x != mv.src_x):
                        continue

                    if src_y >= 0 and src_y < 8 and src_x >= 0 and src_x < 8:
                        if (p := self.board.square_at(src_y, src_x)) == p_src:
                            mv.src_y, mv.src_x = src_y, src_x                            
                            break
            case 'B':
                deduce_src_moves_like_bishop(mv, self.board, colorize('B', self.turn))
            case 'Q':
                p_target = colorize('Q', self.turn)
                deduce_src_moves_like_rook(mv, self.board, p_target) or deduce_src_moves_like_bishop(mv, self.board, p_target)
            case 'R':
                deduce_src_moves_like_rook(mv, self.board, colorize('R', self.turn))
            case 'K':
                p_src = colorize('K', self.turn)
                for y in range(mv.dst_y-1, mv.dst_y+2):
                    for x in range(mv.dst_x-1, mv.dst_x+2):
                        if (y, x) != (mv.dst_y, mv.dst_x) and y >= 0 and y < 8 and x >= 0 and x < 8:
                            if self.board.square_at(y, x) == p_src:
                                mv.src_y, mv.src_x = y, x
                                break
                    if mv.src_y and mv.src_x:
                        break

            case _:
                raise IndexError

        return mv
