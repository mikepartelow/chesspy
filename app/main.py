import os
import sys
import logging
import chesspy.game

logging.basicConfig(filename='logs/chesspy.log', encoding='utf-8', level=logging.DEBUG)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "board":
        g = chesspy.game.Game()
        print(g.board)
        sys.exit(0)

    print("Run Unit Tests")

    # d = 'games/simple'
    # for e in os.listdir(d):
    #     print(e)
    #     print("---")
    #     g = chesspy.game.Game()
    #     with open(os.path.join(d, e), 'r') as f:
    #         for line in f.readlines():
    #             sanstr_white, *sanstr_black = line.split()
    #             print(sanstr_white)
    #             g.move_san(sanstr_white)
    #             print(g.board)

    #             if sanstr_black:
    #                 print(sanstr_black)
    #                 g.move_san(sanstr_black[0])
    #                 print(g.board)
