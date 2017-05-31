from Pos import Pos
from Checker import Checker
from random import shuffle, choice

# TODO choose the best move among doozes that you move for next round
# TODO if you want to move randomely, prevent one of opp

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

        # if num_ok == 2:
        #     print(dooz, "found with", desired)

        if num_ok == 2 and edited_board[desired] == None:
            for adj in game.nei[desired]:
                # print("checking", adj)
                if adj in checkers and adj not in dooz:
                    # print("ok", doozes)
                    doozes.append((adj, desired))
                    # print(doozes)
                    break
    return doozes


def select_inner(availables):
    inner = [x for x in availables if x[1][1] == 1 and x[0][1] != 1]
    if inner:
        return choice(inner)
    return choice(availables)


def find_dooz_mvoe_checker(game, my_cells, mp):
    avai = []
    for dooz in game.lines:
        num_ok = 0
        in_dooz = [x for x in my_cells if x in dooz]
        if len(in_dooz) != 3:
            continue
        for cell in dooz:
            for adj in game.nei[cell]:
                if mp[adj] == None:
                    # return (cell, adj)
                    avai.append((cell, adj))
    return avai


def find_way(game, my_cells, mp):
    one_move, two_move, three_move = [], [], []
    for first in my_cells:
        new_my_cells = [x for x in my_cells if x != first]
        mp[first] = None
        for first_nei in [x for x in game.nei[first] if mp[x] is None]:
            new_my_cells.append(first_nei)
            mp[first_nei] = True
            pos_dooz = pos_dooz_move(game, new_my_cells, mp)
            if pos_dooz:
                one_move.append((first, first_nei))
                new_my_cells.pop()
                mp[first_nei] = None
                continue

            for second in new_my_cells:
                new_my_cells2 = [x for x in new_my_cells if x != second]
                mp[second] = None
                for second_nei in [x for x in game.nei[second] if mp[x] is None]:
                    new_my_cells2.append(second_nei)
                    mp[second_nei] = True
                    pos_dooz = pos_dooz_move(game, new_my_cells2, mp)
                    if pos_dooz:
                        two_move.append((first, first_nei))
                        new_my_cells2.pop()
                        mp[second_nei] = None
                        continue
                    new_my_cells2.pop()
                    mp[second_nei] = None
                mp[second] = True
            new_my_cells.pop()
            mp[first_nei] = None
        mp[first] = True

    if one_move:
        return (one_move, "one")
    return (two_move, "two")


def make_enemy_restricted(game, my_cells):
    des, mx = None, 100
    mp = dict()
    for coor, cell in game.get_board().get_cells().items():
        mp[coor] = cell.get_checker()
    enemy_cells = [(x.get_pos().getx(), x.get_pos().gety()) for x in game.get_board().get_oppcells()]

    for cell in my_cells:
        mp[cell[0]] = None
        mp[cell[1]] = True
        pos = pos_dooz_move(game, enemy_cells, mp)
        if len(pos) < mx:
            mx = len(pos)
            des = cell
        mp[cell[1]] = None
        mp[cell[0]] = True
    return des


def select_best_for_dooz(game, avai, my_cells):
    mp = dict()
    for coor, cell in game.get_board().get_cells().items():
        mp[coor] = cell.get_checker()
    lst = []
    for cell in avai:
        mp[cell[0]] = None
        mp[cell[1]] = True
        new_my_cells = [x for x in my_cells if x != cell[0]]
        new_my_cells.append(cell[1])
        pos = pos_dooz_move(game, new_my_cells, mp)
        if pos:
            lst.append(cell)
        mp[cell[1]] = None
        mp[cell[0]] = True
    if lst:
        return make_enemy_restricted(game, lst)
    return make_enemy_restricted(game, avai)


def move_strategy(game):
    print("\n\n")
    print("round ", game.get_cycle())

    # if doozing is possible, do it
    my_cells = [(x.get_pos().getx(), x.get_pos().gety())
                for x in game.get_board().get_mycells()]
    shuffle(my_cells)

    mp = dict()
    for coor, cell in game.get_board().get_cells().items():
        mp[coor] = cell.get_checker()

    pos = pos_dooz_move(game, my_cells, mp)
    if len(pos):
        cell = select_best_for_dooz(game, pos, my_cells)
        des, ps = cell[0], cell[1]
        print("moving", des, "to", ps, "for dooz")
        return game.move(game.get_board().get_cell(des[0], des[1]).get_checker(), Pos(ps[0], ps[1]))


        # if you can prevent enemy from doozing, do it
        enemy_cells = [(x.get_pos().getx(), x.get_pos().gety()) for x in game.get_board().get_oppcells()]

        enemy_pos = pos_dooz_move(game, enemy_cells, mp)
        if len(enemy_pos):
            avai = []
            for cell in my_cells:
                tmp_cell = mp[cell]
                mp[cell] = None
                for nei_cell in game.nei[cell]:
                    if mp[nei_cell] == None:
                        mp[nei_cell] = tmp_cell
                        enemy_pos = pos_dooz_move(game, enemy_cells, mp)
                        if not len(enemy_pos):
                            avai.append((cell, nei_cell))
                        mp[nei_cell] = None

                mp[cell] = tmp_cell
            if avai:
                cell = select_inner(avai)
                print("moving", cell[0], "to", cell[1], "preventing")
                return game.move(game.get_board().get_cell(cell[0][0], cell[0][1]).get_checker(), Pos(cell[1][0], cell[1][1]))

    avai = find_dooz_mvoe_checker(game, my_cells, mp)
    if avai:
        cell = make_enemy_restricted(game, avai)
        print("foudn dooz", cell)
        return game.move(game.get_board().get_cell(cell[0][0], cell[0][1]).get_checker(), Pos(cell[1][0], cell[1][1]))


    moves = find_way(game, my_cells, mp)
    if moves[0]:
        print("found way with", moves[1], "moves", moves[0])
        cell = make_enemy_restricted(game, moves[0])
        print("moving to", cell)
        return game.move(game.get_board().get_cell(cell[0][0], cell[0][1]).get_checker(), Pos(cell[1][0], cell[1][1]))



    mp = dict()
    for coor, cell in game.get_board().get_cells().items():
        mp[coor] = cell.get_checker()

    possible_moves = []
    my_cells = [(x.get_pos().getx(), x.get_pos().gety()) for x in game.get_board().get_mycells()]

    for cell in my_cells:
        for adj in game.nei[cell]:
            if mp[adj] == None:
                possible_moves.append((cell, adj))
    cell = make_enemy_restricted(game, possible_moves)
    print("just restricting", cell)
    if not cell:
        cell = choice(possible_moves)
    return game.move(game.get_board().get_cell(cell[0][0], cell[0][1]).get_checker(), Pos(cell[1][0], cell[1][1]))
