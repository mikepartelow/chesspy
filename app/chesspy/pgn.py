"""Simple parser for PGN files."""
import logging
import datetime
from . import san
import collections  # pylint: disable=wrong-import-order

NEW_GAME_TOKEN = 42
GAME_OVER_TOKEN = 19860718


def pgn_parser(tokens):  # pylint: disable=too-many-branches,too-many-statements
    """Generator that yields SAN strings and special markers given a list of PGN file tokens.

    Yields NEW_GAME_TOKEN at the beginning of a game, GAME_OVER_TOKEN at the end, otherwise SAN strings."""
    idx, end = 0, len(tokens)

    while idx < end:
        move_idx = 1
        new_game = True
        metadata_line = None
        metadata = {}

        logging.debug("consuming until first move.")

        while idx < end and tokens[idx] != '1.' and tokens[idx] not in san.RESULT_SAN:
            logging.debug(" consuming: |%s| (%s)", tokens[idx], metadata_line)
            if tokens[idx].startswith('['):
                metadata_line = tokens[idx]
            elif metadata_line and tokens[idx].endswith(']'):
                metadata_line += tokens[idx]
                key, value = metadata_line.split('"', 1)
                key, value = key[1:], value[:-2]

                metadata[key] = value

                metadata_line = None
            elif metadata_line:
                metadata_line += tokens[idx] + ' '

            idx += 1

        while idx < end:
            token = tokens[idx]
            idx += 1

            if token.startswith("{"):
                # PGN comments do not nest
                logging.debug("consuming comment")
                while idx < end and not tokens[idx].endswith('}'):
                    # logging.debug("  nom: |%s|", tokens[idx])
                    idx += 1
                idx += 1
                continue  # let the while condition check if we're done

            if token.startswith("("):
                # nobody says PGN annotations can't nest, so they apparently can and do
                count = 1
                logging.debug("consuming annotation from |%s| |%s|", token, tokens[idx])
                while idx < end and count > 0:
                    if tokens[idx].startswith('('):
                        count += 1
                    elif tokens[idx].endswith(')'):
                        count -= 1
                    idx += 1
                continue  # let the while condition check if we're done

            logging.debug("move_idx: %d", move_idx)

            if token == f"{move_idx}.":
                logging.debug("move_idx += 1")
                move_idx += 1
            elif token == f"{move_idx-1}...":
                logging.debug("consuming [%s]", token)
            else:
                if new_game:
                    new_game = False
                    logging.debug("yielding NEW_GAME_TOKEN")
                    logging.debug("metadata: %r", metadata)
                    yield NEW_GAME_TOKEN
                    yield metadata

                logging.debug("yielding [%s] for %d", token, move_idx)
                yield token
                if token in san.RESULT_SAN:
                    yield GAME_OVER_TOKEN

                    logging.debug("break due to endgame")
                    break


def normalize_metadata(meta_dict):
    """Returns a namedtuple of metadata initializes from raw PGN metadata fields. Parses dates into datetime.date()."""
    try:
        date = datetime.date(*map(int, meta_dict['Date'].split('.')))
    except (TypeError, ValueError):
        try:
            date = datetime.date(*map(int, meta_dict['UTCDate'].split('.')))
        except (TypeError, ValueError):
            date = None

    Metadata = collections.namedtuple("Metadata", "event site date white black result opening annotator")

    return Metadata(event=meta_dict['Event'],
                    site=meta_dict['Site'],
                    date=date,
                    white=meta_dict['White'],
                    black=meta_dict['Black'],
                    result=meta_dict['Result'],
                    opening=meta_dict.get('Opening', None),
                    annotator=meta_dict.get('Annotator', None))


class Game:
    """Iterator for a game of chess encoded in PGN. Don't use this directly, use Gamefile().

    for move in Game(parser, metadata)
       print(move.sanstr)
    """

    # Named Tuple representing a move's index in the game, and the move's SAN string
    Move = collections.namedtuple('Move', 'idx sanstr')

    def __init__(self, parser, metadata):
        self.parser = parser
        self.idx = -1
        self.metadata = metadata

    def __iter__(self):
        return self

    def __next__(self):
        token = next(self.parser)
        if token == GAME_OVER_TOKEN:
            raise StopIteration
        self.idx += 1
        return self.Move(self.idx, token)


class Gamefile:
    """Iterator over a PGN file. Yields a Game() object for each game in the PGN file.

    for game in Gamefile("/path/to/my.pgn"):
        for move in game:
            print(move.idx, move.sanstr)
    """
    def __init__(self, path):
        self.game_count = 0

        with open(path, encoding='utf-8') as pgn_f:
            tokens = list(pgn_f.read().split())

        self.parser = pgn_parser(tokens)

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            token = next(self.parser)
            if token == NEW_GAME_TOKEN:
                self.game_count += 1
                metadata = normalize_metadata(next(self.parser))
                return Game(self.parser, metadata)

            if token is None:
                break
