import logging
import datetime
from . import san

NEW_GAME_TOKEN = 42
GAME_OVER_TOKEN = 19860718

def parser(tokens):
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
                continue # let the while condition check if we're done
            
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
                continue # let the while condition check if we're done

            logging.debug("move_idx: %d", move_idx)

            if token == f"{move_idx}.":
                logging.debug("move_idx += 1")
                move_idx += 1
            elif token == f"{move_idx-1}...":
                logging.debug("consuming [%s]", token)
                pass
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

class Metadata:
    def __init__(self, m_dict):
        self.event      = m_dict['Event']
        self.site       = m_dict['Site']
        try:
            self.date     = datetime.date(*map(int, m_dict['Date'].split('.')))
        except:
            try:
                self.date = datetime.date(*map(int, m_dict['UTCDate'].split('.')))
            except:
                self.date = None 
        self.white      = m_dict['White']
        self.black      = m_dict['Black']
        self.result     = m_dict['Result']
        self.opening    = m_dict.get('Opening', None)
        self.annotator  = m_dict.get('Annotator', None)

class Move:
    def __init__(self, idx, sanstr):
        self.idx, self.sanstr = idx, sanstr

class Game:
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
        else:
            self.idx += 1
            return Move(self.idx, token)

class Gamefile:
    def __init__(self, path):
        self.game_count = 0

        with open(path) as f:
            tokens = [ t for t in f.read().split() ]

        self.parser = parser(tokens)

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            token = next(self.parser)
            if token == NEW_GAME_TOKEN:
                self.game_count += 1
                metadata = next(self.parser)
                return Game(self.parser, Metadata(metadata))                    
            elif token is None:
                break
