from Pos import Pos
from random import shuffle, randrange, choice


def pos_dooz(game, checkers, mp):
    doozes = []
    for dooz in game.lines:
        num_ok = 0
        for checker in checkers:
            num_ok += 1 if checker in dooz else 0
        if num_ok == 2:
            for cell in dooz:
                if mp[cell] == None and cell not in checkers:
                    doozes.append(cell)
    return doozes


def find_two_ways(game):
    empty_cells = [(x.get_pos().getx(), x.get_pos().gety()) for x in game.get_board().get_emptycells()]
    my_cells = [(x.get_pos().getx(), x.get_pos().gety()) for x in game.get_board().get_mycells()]
    shuffle(my_cells)
    one_move, two_move, three_move = [], [], []

    mp = dict()
    for coor, cell in game.get_board().get_cells().items():
        mp[coor] = cell.get_checker()

    for first in empty_cells:
        my_cells.append(first)
        mp[first] = True
        possible = pos_dooz(game, my_cells, mp)

        if len(possible) >= 2:
            one_move.append(first)

        if len(possible):
            my_cells.pop()
            mp[first] = None
            continue

        for second in empty_cells:
            if first == second:
                continue

            my_cells.append(second)
            mp[second] = True
            possible = pos_dooz(game, my_cells, mp)

            if len(possible) >= 2:
                two_move.append(first)

            if len(possible):
                my_cells.pop()
                mp[second] = None
                continue

            for third in empty_cells:
                if third == first or third == second:
                    continue

                my_cells.append(third)
                mp[third] = True
                possible = pos_dooz(game, my_cells, mp)

                if len(possible) >= 2:
                    three_move.append(first)
                mp[third] = None
                my_cells.pop()

            mp[second] = None
            my_cells.pop()
        my_cells.pop()
        mp[first] = None

    if len(one_move):
        return (one_move, "one move")
    if len(two_move):
        return (two_move, "two move")
    if len(three_move):
        return (three_move, "three move")
    return ([], "no")


def select_inner(availables):
    new = [x for x in availables if x[1] == 1]
    if len(new):
        return choice(new)
    return choice(availables)


def restrict_enemy(game, avai, mp, enemy_cells):
    tmp = [x for x in avai if x[1] == 1]
    avai = tmp + [x for x in avai if x[1] != 1]
    des, mx = None, 100
    for cell in avai:
        mp[cell] = True
        pos = pos_dooz(game, enemy_cells, mp)
        if len(pos) < mx:
            mx = len(pos)
            des = cell
        mp[cell] = None
    return des


def put_strategy(game):
    print("\n\n")
    print("round ", game.get_cycle())

    my_cells = game.get_board().get_mycells()
    shuffle(my_cells)
    empty_cells = [(x.get_pos().getx(), x.get_pos().gety()) for x in game.get_board().get_emptycells()]

    mp = dict()
    for coor, cell in game.get_board().get_cells().items():
        mp[coor] = cell.get_checker()

    pos_doozes = pos_dooz(game, [(i.get_pos().getx(), i.get_pos().gety()) for i in my_cells], mp)
    enemy_cells = [(x.get_pos().getx(), x.get_pos().gety()) for x in game.get_board().get_oppcells()]
    shuffle(enemy_cells)

    print("your possible doozes:", pos_doozes)

    # dooz if you can
    if len(pos_doozes):
        cell = restrict_enemy(game, pos_doozes, mp, enemy_cells)
        return game.put(Pos(cell[0], cell[1]))

    enemy_pos_doozes = pos_dooz(game, enemy_cells, mp)

    # prevent enemy's dooz if you can
    if len(enemy_pos_doozes):
        for emp in empty_cells:
            mp[emp] = True
            enemy_pos_doozes = pos_dooz(game, enemy_cells, mp)
            mp[emp] = None
            if not enemy_pos_doozes:
                print("put for preventing enemy", emp)
                return game.put(Pos(emp[0], emp[1]))

    two_way = find_two_ways(game)
    if two_way[0]:
        print("two_way with", two_way[1])
        cell = restrict_enemy(game, two_way[0], mp, enemy_cells)
        return game.put(Pos(cell[0], cell[1]))

    # here we should select one way :( or random if not possible
    avai = []
    for cell in empty_cells:
        my_cells.append(cell)
        mp[cell] = True
        pos = pos_dooz(game, my_cells, mp)
        mp[cell] = None
        if len(pos):
            avai.append(cell)
        my_cells.pop()
    if avai:
        cell = restrict_enemy(game, avai, mp, enemy_cells)
        print("making one way with", cell)
        return game.put(Pos(cell[0], cell[1]))

    # random move
    shuffle(empty_cells)
    cell = restrict_enemy(game, empty_cells, mp, enemy_cells)
    print("putting randomely in", cell)
    return game.put(Pos(cell[0], cell[1]))
