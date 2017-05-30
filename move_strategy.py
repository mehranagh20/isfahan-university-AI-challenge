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
    if not avai:
        return None
    return select_inner(avai)


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
        cell = select_inner(pos)
        des, ps = cell[0], cell[1]
        print("moving", des, "to", ps, "for dooz")
        return game.move(game.get_board().get_cell(des[0], des[1]).get_checker(), Pos(ps[0], ps[1]))

    # if you can prevent enemy from doozing, do it
    enemy_cells = [(x.get_pos().getx(), x.get_pos().gety()) for x in game.get_board().get_oppcells()]
    shuffle(enemy_cells)

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

    # choose a dooz and move a checker in that dooz
    cell = find_dooz_mvoe_checker(game, my_cells, mp)
    if cell:
        print("found dooz moving a cell", cell)
        return game.move(game.get_board().get_cell(cell[0][0], cell[0][1]).get_checker(), Pos(cell[1][0], cell[1][1]))

    # some bug here
    mp = dict()
    for coor, cell in game.get_board().get_cells().items():
        mp[coor] = cell.get_checker()

    possible_moves = []
    my_cells = [(x.get_pos().getx(), x.get_pos().gety()) for x in game.get_board().get_mycells()]

    for cell in my_cells:
        for adj in game.nei[cell]:
            if mp[adj] == None:
                possible_moves.append((cell, adj))
    if possible_moves:
        mv = select_inner(possible_moves)
        print("moving randomely from", mv[0], "to", mv[1])
        return game.move(game.get_board().get_cell(mv[0][0], mv[0][1]).get_checker(), Pos(mv[1][0], mv[1][1]))
