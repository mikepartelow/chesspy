"""Abstract Base Class for Players."""
import copy
from ..move import Move
from ..color import Color, color_of
from ..move_generators import moves_for
from ..analyzers import is_in_check, adjacent_kings


class ChessPlayer:
    """Abstract Chess Player who checks their moves."""
    def __init__(self, game, color=Color.BLACK):
        self.game, self.color = game, color

    def check_move(self, sanstr):
        """Returns False if the move is not legal.

        If move is legal, returns a new Game where the given move was executed."""
        test_game = copy.deepcopy(self.game)
        test_game.move_san(sanstr)

        if adjacent_kings(test_game.board) or is_in_check(test_game.board, self.game.turn):
            return False

        return test_game

    def imagine_moves(self):
        """Returns a list of Moves that could be played. Some may not be legal."""
        moves = []

        for y in range(8):
            for x in range(8):
                if (p := self.game.board.square_at(y, x)) and color_of(p) == self.color:
                    for dst_y, dst_x in moves_for(y, x, self.game.board):  # pylint:disable=not-an-iterable
                        mv = Move()
                        if p not in ('p', 'P'):
                            mv.piece = p.upper()
                        mv.dst_y, mv.dst_x = dst_y, dst_x
                        mv.src_y, mv.src_x = y, x
                        mv.capture = (self.game.board.square_at(mv.dst_y, mv.dst_x) is not None)
                        moves.append(mv)

        return moves
