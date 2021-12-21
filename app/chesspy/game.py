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
        match mv.piece:
            case 'P':
                if mv.capture:
                    p_src = colorize('P', self.turn)
                    if (p_dst := self.board.square_at(mv.dst_y, mv.dst_x)) and color_of(p_dst) != color_of(p_src):
                        if self.turn == Color.WHITE:
                            def dirop(y):
                                return y + 1
                        else:
                            def dirop(y):
                                return y - 1

                        if mv.src_x and self.board.square_at(dirop(mv.dst_y), mv.src_x) == p_src:
                            mv.src_y = dirop(mv.dst_y)
                        elif mv.dst_x > 0 and self.board.square_at(dirop(mv.dst_y), mv.dst_x - 1) == p_src:
                            mv.src_y, mv_src_x = dirop(mv.dst_y), mv.dst_x - 1
                        elif mv.dst_x < 7 and self.board.square_at(dirop(mv.dst_y), mv.dst_x + 1) == p_src:
                            mv.src_y, mv_src_x = dirop(mv.dst_y), mv.dst_x + 1

                elif mv.dst_y in (4, 5):
                    if self.board.square_at(5, mv.dst_x) is None and \
                      self.board.square_at(mv.dst_y, mv.dst_x) is None and \
                      self.board.square_at(6, mv.dst_x) == 'P':
                        mv.src_y, mv.src_x = 6, mv.dst_x
                elif mv.dst_y in (2, 3):
                    if self.board.square_at(2, mv.dst_x) is None and \
                      self.board.square_at(mv.dst_y, mv.dst_x) is None and \
                      self.board.square_at(1, mv.dst_x) == 'p':
                        mv.src_y, mv.src_x = 1, mv.dst_x
            case 'N':
                offsets_y = (-1, -1,  1, 1, -2, -2,  2, 2)
                offsets_x = (-2,  2, -2, 2, -1,  1, -1, 1)

                for (offset_y, offset_x) in zip(offsets_y, offsets_x):
                    src_y, src_x = mv.dst_y + offset_y, mv.dst_x + offset_x

                    if src_y >= 0 and src_y < 8 and src_x >= 0 and src_x < 8:
                        if self.board.square_at(src_y, src_x) in ('N', 'n'):
                            mv.src_y, mv.src_x = src_y, src_x
                            break
            case 'B':
                # FIXME: refactor with Queen
                ranges = itertools.chain(zip(range(mv.dst_y+1, 8), range(mv.dst_x+1, 8)),
                                         zip(range(mv.dst_y-1, -1, -1), range(mv.dst_x-1, -1, -1)),
                                         zip(range(mv.dst_y-1, -1, -1), range(mv.dst_x+1, 8)),
                                         zip(range(mv.dst_y+1, 8), range(mv.dst_x-1, -1, -1)))

                for y, x in ranges:
                    if self.board.square_at(y, x) in ('B', 'b'):
                        mv.src_y, mv.src_x = y, x
                        break
            case 'Q':
                # FIXME: refactor with Bishop
                # FIXME: refactor with Rook
                ranges = itertools.chain(zip(range(mv.dst_y+1, 8), range(mv.dst_x+1, 8)),
                                         zip(range(mv.dst_y-1, -1, -1), range(mv.dst_x-1, -1, -1)),
                                         zip(range(mv.dst_y-1, -1, -1), range(mv.dst_x+1, 8)),
                                         zip(range(mv.dst_y+1, 8), range(mv.dst_x-1, -1, -1)),
                                         zip([mv.dst_y]*8, [x for x in range(0, 8) if x != mv.dst_x]),
                                         zip([y for y in range(0, 8) if y != mv.dst_y], [mv.dst_x]*8))

                for y, x in ranges:
                    if self.board.square_at(y, x) in ('Q', 'q'):
                        mv.src_y, mv.src_x = y, x
                        break

            case 'R':
                # FIXME: refactor with Queen
                if (p := self.board.find_first_from(mv.dst_y, mv.dst_x, 0, -1)) is not None and p[0] in ['R', 'r']:
                    mv.src_y, mv.src_x = p[1:]
                elif (p := self.board.find_first_from(mv.dst_y, mv.dst_x, 0, 1)) is not None and p[0] in ['R', 'r']:
                    mv.src_y, mv.src_x = p[1:]
                elif (p := self.board.find_first_from(mv.dst_y, mv.dst_x, 1, 0)) is not None and p[0] in ['R', 'r']:
                    mv.src_y, mv.src_x = p[1:]
                elif (p := self.board.find_first_from(mv.dst_y, mv.dst_x, -1, 0)) is not None and p[0] in ['R', 'r']:
                    mv.src_y, mv.src_x = p[1:]

            case 'K':
                for y in range(mv.dst_y-1, mv.dst_y+2):
                    for x in range(mv.dst_x-1, mv.dst_x+2):
                        if (y, x) != (mv.dst_y, mv.dst_x) and y >= 0 and y < 8 and x >= 0 and y < 8:
                            if self.board.square_at(y, x) in ('K', 'k'):
                                mv.src_y, mv.src_x = y, x
                                break
                    if mv.src_y and mv.src_x:
                        break

            case _:
                raise IndexError

        return mv
