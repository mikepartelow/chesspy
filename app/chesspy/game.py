from .board import Board
from . import san
import itertools
import logging

class Game:
    def __init__(self):
        self.board = Board()
        # FIXME: enum
        self.turn = 'white'

    def move_san(self, sanstr):
        logging.debug("Game::move_san(%s)", sanstr)

        capture = None

        mv = san.parse(sanstr, self)

        if mv.castle:
            # FIXME: refactor to do_castle()
            # FIXME: enum
            if mv.castle == 'kingside':
                # FIXME: enum
                if self.turn == 'white':
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
                # FIXME: enum
                if self.turn == 'white':
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

        self.turn = 'black' if self.turn == 'white' else 'white'

        return capture

    def deduce_src(self, mv):
        """Given a partially constructed Move, deduce the src coordinates for the move.
        """
        # FIXME: this is well tested through test_san but deserves its own unit test.
        match mv.piece:
            case 'P':
                if mv.dst_y in (4, 5):
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
                ranges = itertools.chain(zip(range(mv.dst_y+1, 8), range(mv.dst_x+1, 8)),
                                         zip(range(mv.dst_y-1, -1, -1), range(mv.dst_x-1, -1, -1)),
                                         zip(range(mv.dst_y-1, -1, -1), range(mv.dst_x+1, 8)),
                                         zip(range(mv.dst_y+1, 8), range(mv.dst_x-1, -1, -1)))

                for y, x in ranges:
                    if self.board.square_at(y, x) in ('Q', 'q'):
                        mv.src_y, mv.src_x = y, x
                        break

            case _:
                raise IndexError

        return mv
