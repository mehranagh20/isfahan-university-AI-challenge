from Pos import Pos
from Checker import Checker
def move_strategy(game):
    #write your move strategy here and at the end call game.move() function
    # try:
        p = None
        for cell in game.get_board().get_mycells():
            c = cell.get_checker()
            for n in game.get_board().get_neighbors(cell):
                if n.get_checker() is None:
                    p = n.get_pos()
                    return game.move(c, p)

    # except:
    #     p = Pos(0, 0)
    #     c = Checker(game.get_board().get_cell(0,0), 'm')
    #     game.move(c, p)