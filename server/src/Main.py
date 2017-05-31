from Game import Game
import sys

if __name__ == '__main__':
    # while True:
        game = Game("eeeeeeeeeeeeeeeeeeeeeeee")
        if len(sys.argv) >= 2:
            game.filename = sys.argv[1]
        if (game.start_server()):
            game.start()