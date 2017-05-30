from Checker import Checker
from Pos import Pos
from random import shuffle, randrange, choice


def pos_dooz_put(game, checkers, edited_board):
    doozes = []
    for dooz in game.lines:
        num_ok = 0
        for checker in checkers:
            num_ok += 1 if checker in dooz else 0
        if num_ok == 2:
            for cell in dooz:
                if edited_board[(cell[0], cell[1])] is None and cell not in checkers:
                    doozes.append(cell)
    return doozes


def pos_dooz_move(game, checkers, edited_board):
    doozes, desired = [], None
    for dooz in game.lines:
        num_ok = 0
        for checker in checkers:
            if checker in dooz:
                num_ok += 1

        for tmp in dooz:
            if tmp not in checkers:
                desired = tmp

        if num_ok == 2 and edited_board[desired] is None:
            for adj in game.nei[desired]:
                if adj in checkers and adj not in dooz:
                    doozes.append((adj, desired))
                    break
    return doozes


def best_pop_dooz_based(game, checkers):
    # returns best checker to pop for getting more and better doozes
    # it must return something!

    cycle = game.get_cycle()

    my_cells = [(x.get_pos().getx(), x.get_pos().gety())
                for x in game.get_board().get_mycells()]

    mp = dict()
    for coor, cell in game.get_board().get_cells().items():
        mp[coor] = cell.get_checker()

    inner_base = [x for x in checkers if x[1] == 1]
    outer = [x for x in checkers if x[1] != 1]
    checkers = inner_base + outer

    num_pos, cell = 0, None
    for checker in checkers:
        tmp_cell = mp[checker]
        mp[checker] = None

        # if we are in second stage of game, use the other function for pos
        pos = []
        if cycle <= 24:
            pos = pos_dooz_put(game, my_cells, mp)
        else:
            pos = pos_dooz_move(game, my_cells, mp)
        if len(pos) > num_pos:
            num_pos = len(pos)
            cell = checker

        mp[checker] = tmp_cell

    if cell == None:
        if inner_base:
            cell = choice(inner_base)
        else:
            cell = choice(checkers)

    return cell

def pop_strategy(game):
    # return game.pop(checker)
    print("\n\n")
    cycle = game.get_cycle()

    mp = dict()
    for coor, cell in game.get_board().get_cells().items():
        mp[coor] = cell.get_checker()

    enemy_cells = [(x.get_pos().getx(), x.get_pos().gety()) for x in game.get_board().get_oppcells()]
    shuffle(enemy_cells)

    # holds checkers which poping them makes enemy to have no other option for dooz!
    all_good_pops = []

    # if enemy can dooz, then ...
    if cycle <= 24:
        still_pos_doozes = pos_dooz_put(game, enemy_cells, mp)
    else:
        still_pos_doozes = pos_dooz_move(game, enemy_cells, mp)

    if len(still_pos_doozes):
        # check to see if you can prevent his/her dooz :|
        for cell in enemy_cells:
            new_enemy_cells = [x for x in enemy_cells if x != cell]
            tmp_cell = mp[cell]
            mp[cell] = None
            if cycle <= 24:
                still_pos_doozes = pos_dooz_put(game, new_enemy_cells, mp)
            else:
                still_pos_doozes = pos_dooz_move(game, new_enemy_cells, mp)
            mp[cell] = tmp_cell

            if not still_pos_doozes:
                all_good_pops.append(cell)

        shuffle(all_good_pops)
        if len(all_good_pops):
            cell = best_pop_dooz_based(game, all_good_pops)
            print("poping for prevent", cell)
            return game.pop(game.get_board().get_cell(cell[0], cell[1]).get_checker())

    cell = best_pop_dooz_based(game, enemy_cells)
    print("poping", cell)
    return game.pop(game.get_board().get_cell(cell[0], cell[1]).get_checker())
