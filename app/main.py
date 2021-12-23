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

    # The Immortal Game:  Adolf Anderssen vs Lionel Kieseritzky, 21 June 1851.
    #
    with open('games/simple/immortal.txt') as f:
        g = chesspy.game.Game()

        for move_num, line in enumerate(f.readlines()):
            sanstr_white, *sanstr_black = line.split()

            print(f"{move_num+1}. {sanstr_white}")
            g.move_san(sanstr_white)
            print(g.board)
            print("")
            
            if sanstr_black:
                sanstr_black = sanstr_black[0]
                print(f"{move_num+1}... {sanstr_black}")
                g.move_san(sanstr_black)
                print(g.board)                
                print("")
