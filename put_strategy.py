from Pos import Pos
def put_strategy(game):
    try:
        l = [x.get_pos() for x in game.get_board().get_emptycells()]
        l = sorted(l, key=lambda x: (x.getx(), x.gety()))
        p = l[0]
    except:
        p = Pos(0, 0)

    print(p.getx(), p.gety())
    return game.put(p)
