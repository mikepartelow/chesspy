import logging

def moves(path):
    tokens = []
    move_idx = 1

    with open(path) as f:
        for line in f.readlines():
            tokens.extend(t for t in line.split())

    idx, end = 0, len(tokens)

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
                else:
                    logging.debug("  nom: |%s|", tokens[idx])
                    pass
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
            if token.endswith('#'):
                return

