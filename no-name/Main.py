from Game import Game
import sys

if __name__ == '__main__':
    game = Game("127.0.0.1", 9999, "mehran")
    if game.start_client():
        game.start()
