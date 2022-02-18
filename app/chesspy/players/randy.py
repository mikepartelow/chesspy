"""Randy is a chess player who moves randomly."""
import random
from ..move import Move
from ..san import make_san
from ..color import Color, color_of
from ..move_generators import moves_for


class Randy:
    """Randy moves randomly."""
    def __init__(self, game, color=Color.BLACK):
        self.game, self.color = game, color

    def __str__(self):
        return "Randy"

    def suggest_move_san(self):
        """Returns Randy's best idea for a move."""
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

        return make_san(random.choice(moves), verbose=True)
