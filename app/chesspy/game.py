from .board import Board
from . import san
import itertools
import logging

class Game:
    def __init__(self):
        self.board = Board()

    def move_san(self, sanstr):
        logging.debug("Game::move_san(%s)", sanstr)

        mv = san.parse(sanstr, self)
        piece = self.board.square_at(mv.src_y, mv.src_x)
        assert(piece is not None)

        capture = self.board.square_at(mv.dst_y, mv.dst_x)
        assert((capture is None) == (mv.capture is False))

        self.board.place_piece_at(piece, mv.dst_y, mv.dst_x)
        self.board.place_piece_at(None, mv.src_y, mv.src_x)

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
                ranges = itertools.chain(zip(range(mv.dst_y+1, 8), range(mv.dst_x+1, 8)),
                                         zip(range(mv.dst_y-1, -1, -1), range(mv.dst_x-1, -1, -1)),
                                         zip(range(mv.dst_y-1, -1, -1), range(mv.dst_x+1, 8)),
                                         zip(range(mv.dst_y+1, 8), range(mv.dst_x-1, -1, -1)))

                for y, x in ranges:
                    if self.board.square_at(y, x) in ('B', 'b'):
                        mv.src_y, mv.src_x = y, x
                        break

            case _:
                raise IndexError

        return mv
