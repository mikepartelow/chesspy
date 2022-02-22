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
    def __init__(self, game, color=Color.BLACK, pool=None, search_depth=2, moves_to_consider=6):
        self.game, self.color = game, color
        self.pool = pool

        self.search_depth = search_depth
        self.moves_to_consider = moves_to_consider

    def __str__(self):
        return "Julian"

    def __getstate__(self):
        """Remove self.pool before Pickling so we can use Pool.map."""
        self_dict = self.__dict__.copy()
        del self_dict['pool']
        return self_dict

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

    def consider_move_san(self, packet):
        sanstr, depth = packet
        score = None
        if test_game := self.check_move(sanstr):
            if depth > 0:
                assert test_game.turn != self.game.turn
                opponent_player = self.__class__(test_game, color=test_game.turn)
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

    def suggest_move_san(self, depth=None):
        """Returns Julian's "best idea" for a move, or None if there are no legal moves."""
        if depth is None:
            depth = self.search_depth
        assert depth >= 0

        # FIXME: stop making so many temp_games
        # FIXME: combine analyzers (e.g. analyze for mate and check at once, don't scan board twice)
        # FIXME: don't do anything twice, like generators and analyzers
        # FIXME: repr(board) -> score DB to bypass computation
        #        more likely: (repr(board), sanstr) -> (score, is_check, is_mate). might want to use shared memory for that
        # FIXME: rename self.check_move, "check" is overloaded.

        best_move_score, best_move_sanstr = float("-inf"), None

        moves = self.imagine_moves()
        if not is_in_check(self.game.board, self.color) and len(moves) > self.moves_to_consider:
            moves = random.sample(moves, self.moves_to_consider)

        sanstrs = [make_san(move, verbose=True) for move in moves]
        packets = [(sanstr, depth) for sanstr in sanstrs]

        if self.pool:
            scores = self.pool.map(self.consider_move_san, packets)
        else:
            scores = map(self.consider_move_san, packets)

        for score, sanstr in zip(scores, sanstrs):
            if score is None:
                continue

            if score > best_move_score or (score == best_move_score and random.randrange(3) == 1):
                best_move_score = score
                best_move_sanstr = sanstr

        return best_move_sanstr
