import logging

def moves(path):
    move_idx, ignore_until = 2, '1.'

    # ignoring might need to be a stack - we might have nested { () }

    with open(path) as f:
        for line in f.readlines():            

            for token in line.split(' '):                
                logging.debug("|%s| : ignore_until=%r, move_idx=%d", token, ignore_until, move_idx)

                if ignore_until:
                    if token.endswith(ignore_until) or token.endswith(ignore_until):
                        ignore_until = None
                elif token.startswith("{"):
                    ignore_until = '}'
                elif token.startswith("("):
                    ignore_until = ')'
                elif token == f"{move_idx}.":
                    move_idx += 1
                elif token == f"{move_idx-1}...":
                    pass
                else:
                    logging.debug("yielding [%s]", token)
                    yield token
                    if token.endswith('#'):
                        return