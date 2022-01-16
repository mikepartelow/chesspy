import logging

NEW_GAME_TOKEN = 42
GAME_OVER_TOKEN = 19860718

def tokenizer(tokens):
    idx, end = 0, len(tokens)

    while idx < end:
        move_idx = 1
        new_game = True

        logging.debug("consuming until first move.")
        while idx < end and tokens[idx] != '1.':
            logging.debug(" consuming: |%s|", tokens[idx])
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
                    yield NEW_GAME_TOKEN
                logging.debug("yielding [%s] for %d", token, move_idx)
                yield token                
                if token.endswith('#') or token in ('1-0', '0-1', '1/2-1/2',):                    
                    yield GAME_OVER_TOKEN
                    logging.debug("break due to endgame")
                    break

class Move:
    def __init__(self, idx, sanstr):
        self.idx, self.sanstr = idx, sanstr

class Game:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer
        self.idx = -1

    def __iter__(self):
        return self

    def __next__(self):
        token = next(self.tokenizer)
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

        self.tokenizer = tokenizer(tokens)

    def __iter__(self):
        return self

    def __next__(self):
        while True:
            token = next(self.tokenizer)
            if token == NEW_GAME_TOKEN:
                self.game_count += 1
                return Game(self.tokenizer)                    
            elif token is None:
                break
