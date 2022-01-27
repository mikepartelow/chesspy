"""Implements a Game class encapsulating a Board object and a move engine for the rules of standard chess."""
import copy
import logging
from . import san
from .color import Color
from .board import Board
from .castle import Castle


def color_of(ch):
    """Returns Color.WHITE if given piece character is White, otherwise Color.BLACK.

    Performs no validation."""
    if ch.isupper():
        return Color.WHITE
    return Color.BLACK


def colorize(ch, color):
    """Returns the given piece, ch, altered to represent the given color.

    Performs no validation."""
    if color == Color.WHITE:
        return ch.upper()
    return ch.lower()


class Game:
    """Represents a game of standard chess. Tracks turns, validates moves, analyzes positions.

    game = Game()
    game.move_san("e4")  # move White's pawn
    game.move_san("e5")  # move Black's pawn
    game.move_san("Ke4") # illegal move, raises IndexError
    """
    def __init__(self, board=None, turn=None):
        self.board = board or Board()
        self.turn = turn or Color.WHITE
        self.over = False

    def is_in_check(self):  # pylint: disable=too-many-return-statements,too-many-branches
        """Returns True if the current turn's player is in check, False otherwise."""
        logging.debug("Game::is_in_check(%s)", self.turn)

        king_pos = self.board.king_position(self.turn)
        logging.debug("Game::is_in_check() : king_pos = %r", king_pos)

        offsets_y = (-1, -1,  1, 1, -2, -2,  2, 2)
        offsets_x = (-2,  2, -2, 2, -1,  1, -1, 1)

        opponent_knight = colorize('N', self.turn.opponent())

        for (y_offset, x_offset) in zip(offsets_y, offsets_x):
            y, x = king_pos[0] + y_offset, king_pos[1] + x_offset
            if 0 <= y < 8 and 0 <= x < 8:
                if self.board.square_at(y, x) == opponent_knight:
                    logging.debug("Game::is_in_check() -> True : Knight at (%s, %s)", y, x)
                    return True

        opponent_queen = colorize('Q', self.turn.opponent())

        opponent_bishop = colorize('B', self.turn.opponent())

        if (p := self.board.find_first_on_diagonal(king_pos, -1, -1)) and p.piece in (opponent_bishop, opponent_queen):
            logging.debug("Game::is_in_check() -> True : Bishop at (%s, %s)", *p[1:])
            return True
        if (p := self.board.find_first_on_diagonal(king_pos, 1, 1)) and p.piece in (opponent_bishop, opponent_queen):
            logging.debug("Game::is_in_check() -> True : Bishop at (%s, %s)", *p[1:])
            return True
        if (p := self.board.find_first_on_diagonal(king_pos, 1, -1)) and p.piece in (opponent_bishop, opponent_queen):
            logging.debug("Game::is_in_check() -> True : Bishop at (%s, %s)", *p[1:])
            return True
        if (p := self.board.find_first_on_diagonal(king_pos, -1, 1)) and p.piece in (opponent_bishop, opponent_queen):
            logging.debug("Game::is_in_check() -> True : Bishop at (%s, %s)", *p[1:])
            return True

        opponent_rook = colorize('R', self.turn.opponent())

        if (p := self.board.find_first_on_h_or_v(king_pos, 0, -1)) and p.piece in (opponent_rook, opponent_queen):
            logging.debug("Game::is_in_check() -> True : Rook at (%s, %s)", *p[1:])
            return True
        if (p := self.board.find_first_on_h_or_v(king_pos, 0, 1)) and p.piece in (opponent_rook, opponent_queen):
            logging.debug("Game::is_in_check() -> True : Rook at (%s, %s)", *p[1:])
            return True
        if (p := self.board.find_first_on_h_or_v(king_pos, 1, 0)) and p.piece in (opponent_rook, opponent_queen):
            logging.debug("Game::is_in_check() -> True : Rook at (%s, %s)", *p[1:])
            return True
        if (p := self.board.find_first_on_h_or_v(king_pos, -1, 0)) and p.piece in (opponent_rook, opponent_queen):
            logging.debug("Game::is_in_check() -> True : Rook at (%s, %s)", *p[1:])
            return True

        opponent_pawn = colorize('P', self.turn.opponent())

        if self.turn == Color.WHITE:
            pawn_maybes = (king_pos[0] - 1, king_pos[1] - 1), (king_pos[0] - 1, king_pos[1] + 1)
        else:
            pawn_maybes = (king_pos[0] + 1, king_pos[1] - 1), (king_pos[0] + 1, king_pos[1] + 1)

        for pawn_maybe in pawn_maybes:
            if pawn_maybe[0] >= 0 and pawn_maybe[0] < 8 and pawn_maybe[1] >= 0 and pawn_maybe[1] < 8:
                if self.board.square_at(*pawn_maybe) == opponent_pawn:
                    logging.debug("Game::is_in_check() -> True : Pawn at (%s, %s)", *pawn_maybe)
                    return True

        logging.debug("Game::is_in_check(%s) -> False", self.turn)
        return False

    def move_castle(self, mv):
        """Given a mv for Castling, execute the move on self.board."""
        assert mv.castle
        if mv.castle == Castle.KINGSIDE:
            if self.turn == Color.WHITE:
                self.board.place_piece_at('K', 7, 6)
                self.board.place_piece_at('R', 7, 5)
                self.board.place_piece_at(None, 7, 4)
                self.board.place_piece_at(None, 7, 7)
            else:
                self.board.place_piece_at('k', 0, 6)
                self.board.place_piece_at('r', 0, 5)
                self.board.place_piece_at(None, 0, 4)
                self.board.place_piece_at(None, 0, 7)
        elif mv.castle == Castle.QUEENSIDE:
            if self.turn == Color.WHITE:
                self.board.place_piece_at('K', 7, 2)
                self.board.place_piece_at('R', 7, 3)
                self.board.place_piece_at(None, 7, 4)
                self.board.place_piece_at(None, 7, 0)
            else:
                self.board.place_piece_at('k', 0, 2)
                self.board.place_piece_at('r', 0, 3)
                self.board.place_piece_at(None, 0, 4)
                self.board.place_piece_at(None, 0, 0)

    def move_san(self, sanstr):
        """Executes the given SAN move on self.board if move is legal in standard chess.

        captured_piece = game.move_san("Bxe4")

        Toggles self.turn. Sets self.over in case of checkmate.

        Returns the opponent's captured piece, or None if no piece was captured.
        Raises IndexError if the move is illegal."""
        logging.debug("Game::move_san(%s)", sanstr)

        if sanstr in san.RESULT_SAN:
            self.over = True
            return None

        capture = None

        mv = san.parse(sanstr, self)

        if mv.castle:
            self.move_castle(mv)
        else:
            capture = self.move_move(mv)

        self.turn = Color.toggle(self.turn)

        if mv.mate:
            self.over = True

        # this is a lovely sanity check but it slows us down by about 2.25x
        # it's also slower on average when mv.check is False, which is most of the time.
        #
        logging.debug("assert(mv.check == self.is_in_check())")
        assert mv.check == self.is_in_check()

        return capture

    def move_move(self, mv):
        """Execute the given move. Return captured piece, or None.

        No rules checking applied, move is assumed to be legal."""
        piece = self.board.square_at(mv.src_y, mv.src_x)
        assert piece is not None

        if mv.en_passant:
            y = mv.dst_y + 1 if self.turn == Color.WHITE else mv.dst_y - 1
            capture = self.board.square_at(y, mv.dst_x)
            self.board.place_piece_at(None, y, mv.dst_x)
        else:
            capture = self.board.square_at(mv.dst_y, mv.dst_x)

        assert (capture is None) == (mv.capture is False)

        if mv.promotion:
            piece = colorize(mv.promotion, self.turn)

        self.board.place_piece_at(piece, mv.dst_y, mv.dst_x)
        self.board.place_piece_at(None, mv.src_y, mv.src_x)

        return capture

    def test_move_from_src(self, y, x, mv):
        """Validates move of piece at (y, x) to (mv.dst_y, mv.dst_x) against rules of standard chess.

        If move is legal, intializes (mv.src_y, mv.src_x) and returns True
        If move is illegal, returns False.

        self.board is unaltered upon return but may be altered during test_move_from_src() execution."""
        # this logically necessary but unoptimized check slows us down by about 2x
        #
        logging.debug("test_move_from_src(%s, %s, %r)", y, x, mv)
        test_mv = copy.copy(mv)
        test_mv.src_y, test_mv.src_x = y, x

        test_game = Game(board=Board(repr(self.board)), turn=self.turn)
        test_game.move_move(test_mv)

        logging.debug("if not test_game.is_in_check():")
        if not test_game.is_in_check():
            mv.src_y, mv.src_x = y, x
            logging.debug("test_move_from_src() -> True")
            return True

        logging.debug("test_move_from_src() -> False")
        return False

    def deduce_src_knight(self, mv):
        """Yields "potentially legal" (src_y, src_x) of knight moves to (mv.dst_y, mv.dst_x), if any are found.

        Caller must determine if yielded move exposes player to check (and is therefore illegal)."""
        p_src = colorize('N', self.turn)
        offsets_y = (-1, -1,  1, 1, -2, -2,  2, 2)
        offsets_x = (-2,  2, -2, 2, -1,  1, -1, 1)

        for (offset_y, offset_x) in zip(offsets_y, offsets_x):
            src_y, src_x = mv.dst_y + offset_y, mv.dst_x + offset_x

            if (mv.src_y is not None and src_y != mv.src_y) or (mv.src_x is not None and src_x != mv.src_x):
                continue

            if 0 <= src_y < 8 and 0 <= src_x < 8:
                if self.board.square_at(src_y, src_x) == p_src:
                    logging.debug("deduce_src_knight(%r): yield (%s, %s)", mv, src_y, src_x)
                    yield src_y, src_x

    def deduce_src_moves_like_rook(self, mv, p_target):
        """Yields "potentially legal" (src_y, src_x) of rook/queen moves to (mv.dst_y, mv.dst_x), if any are found.

        Caller must determine if yielded move exposes player to check (and is therefore illegal)."""
        if (p := self.board.find_first_on_h_or_v(mv.dst, 0, -1, mv.src)) and p.piece == p_target:
            yield p[1:]

        if (p := self.board.find_first_on_h_or_v(mv.dst, 0, 1, mv.src)) and p.piece == p_target:
            yield p[1:]

        if (p := self.board.find_first_on_h_or_v(mv.dst, 1, 0, mv.src)) and p.piece == p_target:
            yield p[1:]

        if (p := self.board.find_first_on_h_or_v(mv.dst, -1, 0, mv.src)) and p.piece == p_target:
            yield p[1:]

    def deduce_src_moves_like_bishop(self, mv, p_target):
        """Yields "potentially legal" (src_y, src_x) of bishop/queen moves to (mv.dst_y, mv.dst_x), if any are found.

        Caller must determine if yielded move exposes player to check (and is therefore illegal)."""
        if (p := self.board.find_first_on_diagonal(mv.dst, -1, -1, mv.src)) and p.piece == p_target:
            yield p[1:]

        if (p := self.board.find_first_on_diagonal(mv.dst, 1, 1, mv.src)) and p.piece == p_target:
            yield p[1:]

        if (p := self.board.find_first_on_diagonal(mv.dst, 1, -1, mv.src)) and p.piece == p_target:
            yield p[1:]

        if (p := self.board.find_first_on_diagonal(mv.dst, -1, 1, mv.src)) and p.piece == p_target:
            yield p[1:]

    def deduce_src_pawn(self, mv):  # pylint: disable=too-many-return-statements,too-many-branches
        """Initializes (mv.src_y, mv.src_x) with coordinates of pawn that can legally move to (mv.dst_y, mv.dst_x)"""
        if self.turn == Color.WHITE:
            def ahead_of(y): return y + 1  # pylint: disable=multiple-statements
            def behind(y): return y - 1  # pylint: disable=multiple-statements
        else:
            def ahead_of(y): return y - 1  # pylint: disable=multiple-statements
            def behind(y): return y + 1  # pylint: disable=multiple-statements

        if mv.capture:
            p_src = colorize('P', self.turn)
            p_dst = self.board.square_at(mv.dst_y, mv.dst_x)

            if p_dst and color_of(p_dst) != color_of(p_src):  # regular capture?
                if mv.src_x and self.board.square_at(ahead_of(mv.dst_y), mv.src_x) == p_src:
                    mv.src_y = ahead_of(mv.dst_y)
                elif mv.dst_x > 0 and self.board.square_at(ahead_of(mv.dst_y), mv.dst_x - 1) == p_src:
                    mv.src_y, mv.src_x = ahead_of(mv.dst_y), mv.dst_x - 1
                elif mv.dst_x < 7 and self.board.square_at(ahead_of(mv.dst_y), mv.dst_x + 1) == p_src:
                    mv.src_y, mv.src_x = ahead_of(mv.dst_y), mv.dst_x + 1
            elif p_dst is None:  # en passant?

                logging.debug("%s : %s : %s : %s : %s",
                              behind(mv.dst_y),
                              self.board.square_at(behind(mv.dst_y), mv.dst_x),
                              colorize('P', self.turn.opponent),
                              self.board.square_at(ahead_of(mv.dst_y), mv.dst_x),
                              self.turn.opponent())

                if (p := self.board.square_at(ahead_of(mv.dst_y), mv.dst_x)) and \
                        p == colorize('P', self.turn.opponent()) and \
                        self.board.square_at(behind(mv.dst_y), mv.dst_x) is None:
                    logging.debug("ep-0")
                    if mv.src_x and self.board.square_at(ahead_of(mv.dst_y), mv.src_x) == p_src:
                        mv.src_y = ahead_of(mv.dst_y)
                        mv.en_passant = True
                    elif mv.dst_x > 0 and self.board.square_at(ahead_of(mv.dst_y), mv.dst_x - 1) == p_src:
                        mv.src_y, mv.src_x = ahead_of(mv.dst_y), mv.dst_x - 1
                        mv.en_passant = True
                    elif mv.dst_x < 7 and self.board.square_at(ahead_of(mv.dst_y), mv.dst_x + 1) == p_src:
                        mv.src_y, mv.src_x = ahead_of(mv.dst_y), mv.dst_x + 1
                        mv.en_passant = True

        elif self.board.square_at(mv.dst_y, mv.dst_x) is None:
            if self.turn == Color.WHITE:
                idx, pawn, origin = 1, 'P', 6
            else:
                idx, pawn, origin = -1, 'p', 1

            if (p := self.board.find_first_on_h_or_v(mv.dst, idx, 0)) and p.piece == pawn:
                if (abs(mv.dst_y - p[1]) == 2 and p[1] == origin) or abs(mv.dst_y - p[1]) == 1:
                    mv.src_y, mv.src_x = p[1:]

    def deduce_src(self, mv):  # pylint: disable=too-many-return-statements,too-many-branches
        """Given a partially constructed Move, deduce src coordinates.

        Given initialized and valid .dst_y, .dst_x, .piece, and .capture fields, initialize
        .src_y and src_x with the coordinates of a given piece that can legally move to the given
        coordinates. Performs (expensive) sanity checks.
        """
        if (p := self.board.square_at(mv.dst_y, mv.dst_x)) and color_of(p) == self.turn:
            # can't land on our own piece
            raise IndexError

        match mv.piece:
            case 'P':
                self.deduce_src_pawn(mv)
            case 'N':
                for (y, x) in self.deduce_src_knight(mv):
                    if self.test_move_from_src(y, x, mv):
                        break
            case 'B':
                for (y, x) in self.deduce_src_moves_like_bishop(mv, colorize('B', self.turn)):
                    if self.test_move_from_src(y, x, mv):
                        break
            case 'Q':
                done = False
                for (y, x) in self.deduce_src_moves_like_rook(mv, colorize('Q', self.turn)):
                    if self.test_move_from_src(y, x, mv):
                        done = True
                        break

                if not done:
                    for (y, x) in self.deduce_src_moves_like_bishop(mv, colorize('Q', self.turn)):
                        if self.test_move_from_src(y, x, mv):
                            break
            case 'R':
                for (y, x) in self.deduce_src_moves_like_rook(mv, colorize('R', self.turn)):
                    if self.test_move_from_src(y, x, mv):
                        break
            case 'K':
                p_src = colorize('K', self.turn)
                for y in range(mv.dst_y-1, mv.dst_y+2):
                    for x in range(mv.dst_x-1, mv.dst_x+2):
                        if (y, x) != (mv.dst_y, mv.dst_x) and 0 <= y < 8 and 0 <= x < 8:
                            if self.board.square_at(y, x) == p_src:
                                mv.src_y, mv.src_x = y, x
                                break
                    if mv.src_y and mv.src_x:
                        break

            case _:
                raise IndexError

        return mv
