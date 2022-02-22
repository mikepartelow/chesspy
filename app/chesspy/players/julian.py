"""Julian thinks ahead."""
# pylint:disable=wrong-import-order
import random
from ..san import make_san
from .player import ChessPlayer
from ..color import Color, color_of
from chesspy.analyzers import is_in_check, is_in_mate


PIECE_VALUES = dict(P=1, N=3, B=3, R=5, Q=9, K=1)


class Julian(ChessPlayer):
    """Julian thinks deeply about his moves."""
    def __init__(self, game, color=Color.BLACK, search_depth=2, moves_to_consider=8):
        self.game, self.color = game, color
        self.search_depth = search_depth
        self.moves_to_consider = moves_to_consider

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

    def consider_move_san(self, sanstr, depth):
        """Returns a score for the sanstr, or None if the move is not legal."""
        score = None
        if test_game := self.check_move(sanstr):
            if depth > 0:
                assert test_game.turn != self.game.turn
                opponent_player = self.__class__(test_game, color=test_game.turn)
                # FIXME: decrementing depth here is incorrect but currently necessary to not explode the stack
                opponent_move_san = opponent_player.suggest_move_san(depth=depth-1)

                if opponent_move_san:
                    test_game.move_san(opponent_move_san)

                    assert test_game.turn == self.game.turn
                    future_self_player = self.__class__(test_game, color=test_game.turn)
                    future_self_move_san = future_self_player.suggest_move_san(depth=depth-1)

                    if future_self_move_san:
                        test_game.move_san(future_self_move_san)

            score = self.score_board(test_game.board)

        return score

    def suggest_move_san(self, pool=None, depth=None):
        """Returns Julian's "best idea" for a move, or None if there are no legal moves."""
        if depth is None:
            depth = self.search_depth

        assert depth >= 0

        best_move_score = float("-inf")
        best_move_sanstr = None

        moves = self.imagine_moves()
        random.shuffle(moves)

        # FIXME: stop making so many temp_games
        # FIXME: combine analyzers (e.g. analyze for mate and check at once, don't scan board twice)
        # FIXME: don't do anything twice, like generators and analyzers
        # FIXME: repr(board) -> score DB to bypass computation
        #        more likely: (repr(board), sanstr) -> (score, is_check, is_mate)
        # FIXME: openings DB (scores are not based on simple sum of piece values) -> Bubbles
        # FIXME: smarter pruning than random MOVES_TO_CONSIDER. maybe always consider moving Q
        #        -> but maybe smarter behavior belongs in Bubbles
        # FIXME: rename self.check_move, "check" is overloaded.
        # FIXME: unit/sanity checks. is this actually doing what we expect?
        # FIXME: search harder as number of pieces decreases!
        # FIXME: iterative, not recurseive (Bubbles?)

        results = []

        # if we are in check, we must consider all possible moves
        moves_to_consider = None if is_in_check(self.game.board, self.color) else self.moves_to_consider

        # FIXME: okay, it works, now make it pretty
        #
        for move in moves[:moves_to_consider]:
            sanstr = make_san(move, verbose=True)
            if pool:
                result = pool.apply_async(self.consider_move_san, (sanstr, depth))
                results.append((result, sanstr))
            else:
                score = self.consider_move_san(sanstr, depth)
                results.append((score, sanstr))

        if pool:
            [r[0].wait() for r in results]

        for result, sanstr in results:
            if (score := (result.get() if hasattr(result, 'get') else result)) is not None:
                if score > best_move_score or (score == best_move_score and random.randrange(3) == 1):
                    best_move_score = score
                    best_move_sanstr = sanstr

        return best_move_sanstr
