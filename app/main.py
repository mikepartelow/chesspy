#!/usr/bin/env python3.10

"""Print a chess board if run with argument 'board', otherwise, print all moves of The Immortal Game."""
import sys
import logging
import chesspy.game
import chesspy.players


def play(player_class):
    """Play an interactive game of chess against the supplied player_class."""
    game = chesspy.game.Game()
    game.assert_check = False
    game.assert_mate = False

    player = player_class(game)

    move_num = 1

    with open(f"{str(player)}.pgn", "w", encoding="utf-8") as game_file:
        while not game.over:
            print(game.board)

            while True:
                sanstr = input(f"{move_num}. ")
                try:
                    game.move_san(sanstr)
                    break
                except (IndexError, AssertionError) as exc:
                    logging.exception(str(exc))
                    print("---")
                    print(game.board)
                    print(game.turn)
                    print("---")

            game_file.write(f"{move_num}. {sanstr}")

            if not game.over:
                # pylint:disable=fixme
                # FIXME: deduce_src_pawn and deduce_src_king do not check for check!
                # FIXME: unit tests for deduce_src moves that expose check
                sanstr = player.suggest_move_san()
                if sanstr is None:
                    game.over = True  # FIXME: this should be auto-detected
                else:
                    game.move_san(sanstr)
                    print(f"{move_num}... {sanstr}")
                    game_file.write(f" {sanstr}\n")

            move_num += 1


def play_immortal():
    """Play The Immortal Game, exhibition style."""

    # The Immortal Game:  Adolf Anderssen vs Lionel Kieseritzky, 21 June 1851.
    #
    with open('games/simple/immortal.txt', encoding="utf-8") as game_file:
        game = chesspy.game.Game()

        for move_num, line in enumerate(game_file.readlines()):
            sanstr_white, *sanstr_black = line.split()

            game.move_san(sanstr_white)
            print(game.board)
            print(f"{move_num+1}. {sanstr_white}")
            print("")

            if sanstr_black:
                sanstr_black = sanstr_black[0]
                game.move_san(sanstr_black)
                print(game.board)
                print(f"{move_num+1}... {sanstr_black}")
                print("")


if __name__ == "__main__":
    logging.basicConfig(filename='logs/chesspy.log',
                        encoding='utf-8',
                        format='[%(asctime)s]::[%(levelname).1s]::[%(filename)s:%(lineno)d]::[%(message)s]',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        level=logging.DEBUG)

    if len(sys.argv) > 1:
        if sys.argv[1] == "board":
            print(chesspy.game.Game().board)
            sys.exit(0)
        elif sys.argv[1] == "randy":
            play(chesspy.players.Randy)
            sys.exit(0)
        elif sys.argv[1] == "ricky":
            play(chesspy.players.Ricky)
            sys.exit(0)
        elif sys.argv[1] == "julian":
            play(chesspy.players.Julian)
            sys.exit(0)

    play_immortal()
    sys.exit(0)
