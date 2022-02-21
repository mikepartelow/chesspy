"""Julian thinks ahead."""
# pylint:disable=wrong-import-order
import random
from ..san import make_san
from ..color import color_of
from .player import ChessPlayer
from multiprocessing import Pool, set_start_method
from chesspy.analyzers import is_in_check, is_in_mate


SEARCH_DEPTH = 3
MOVES_TO_CONSIDER = 6
PIECE_VALUES = dict(P=1, N=3, B=3, R=5, Q=9, K=1)


class Julian(ChessPlayer):
    """Julian thinks deeply about his moves."""
    def __init__(self, game, color=Color.BLACK, pool=None):
        super().__init__(game, color=color)

        self.pool = pool or Pool()
        # FIXME: do we need this here?
        set_start_method('fork') # necessary for MacOS

    def __str__(self):
        return "Julian"

    def score_board(self, board):
        score = 0

        for y in range(8):
            for x in range(8):
                if (p := board.square_at(y, x)):
                    if color_of(p) == self.color:
                        score += PIECE_VALUES[p.upper()]
                    else:
                        score -= PIECE_VALUES[p.upper()]

        if is_in_check(board, self.color.opponent()):
            score += 1000
        if is_in_check(board, self.color):
            score -= 1000
        if is_in_mate(board, self.color.opponent()):
            score += 10000000
        if is_in_mate(board, self.color):
            score -= 10000000

        return score

    def consider_move(self, sanstr, depth):
        """Returns a score for the sanstr, or None if the move is not legal."""
        score = None
        if test_game := self.check_move(sanstr):
            if depth > 0:
                assert test_game.turn != self.game.turn
                opponent_player = self.__class__(test_game, color=test_game.turn, pool=self.pool)
                # FIXME: decrementing depth here is incorrect but currently necessary to not explode the stack
                opponent_move_san = opponent_player.suggest_move_san(depth=depth-1)

                if opponent_move_san:
                    test_game.move_san(opponent_move_san)

                    assert test_game.turn == self.game.turn
                    future_self_player = self.__class__(test_game, color=test_game.turn, pool=self.pool)
                    future_self_move_san = future_self_player.suggest_move_san(depth=depth-1)

                    if future_self_move_san:
                        test_game.move_san(future_self_move_san)

            score = self.score_board(test_game.board)

        return score

    def suggest_move_san(self, depth=SEARCH_DEPTH):
        """Returns Julian's "best idea" for a move, or None if there are no legal moves."""
        assert depth >= 0

        best_move_score = float("-inf")
        best_move_sanstr = None

        moves = self.imagine_moves()
        random.shuffle(moves)

        # FIXME: if depth == SEARCH_DEPTH and we are in check, we should ignore MOVES_TO_CONSIDER
        #        -> consider all options to escape check
        # FIXME: parallelize: use one Pool per top level game (not per player). pool size scales with MOVES_TO_CONSIDER
        # FIXME: stop making so many temp_games
        # FIXME: combine analyzers (e.g. analyze for mate and check at once, don't scan board twice)
        # FIXME: repr(board) -> score DB to bypass computation
        #        more likely: (repr(board), sanstr) -> score
        # FIXME: openings DB (Bubbles?)
        # FIXME: smarter pruning than random MOVES_TO_CONSIDER. maybe always consider moving Q
        #        -> but maybe smarter behavior belongs in Bubbles
        # FIXME: rename self.check_move, "check" is overloaded.
        # FIXME: consider map/reduce style
        # FIXME: unit/sanity checks. is this actually doing what we expect?

        for move in moves[:MOVES_TO_CONSIDER]:
            # FIXME: this isn't how it works!
            sanstr = make_san(move, verbose=True)
            if (score := pool.async_apply(self.consider_move_san, sanstr, depth)) is not None:
                if score > best_move_score or (score == best_move_score and random.randrange(3) == 1):
                    best_move_score = score
                    best_move_sanstr = sanstr

        return best_move_sanstr
