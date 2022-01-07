import logging

def moves(path):
    tokens = []

    with open(path) as f:
        tokens = [ t for t in f.read().split() ]

    idx, end = 0, len(tokens)

    while idx < end:
        move_idx = 1

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
                logging.debug("yielding [%s]", token)
                yield token                
                if token.endswith('#') or token in ('1-0', '0-1',):                    
                    logging.debug("breaking due to endgame")
                    break

