import logging

def moves(path):
    move_idx, ignoring = 1, True

    # ignoring might need to be a stack - we might have nested { () }

    with open(path) as f:
        for line in f.readlines():

            if line.startswith('1. '):
                ignoring = False

            for token in line.split(' '):                
                logging.debug("|%s| : ignoring=%r", token, ignoring)

                if ignoring:
                    if token.endswith("}") or token.endswith(")"):
                        ignoring = False
                elif token.startswith("{") or token.startswith("("):
                    ignoring = True
                elif token == f"{move_idx}.":
                    move_idx += 1
                elif token == f"{move_idx-1}...":
                    pass
                else:
                    logging.debug("yielding [%s]", token)
                    yield token
                    if token.endswith('#'):
                        return