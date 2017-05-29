from Pos import Pos
from Checker import Checker


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


def move_strategy(game):
    print("\n\n")
    print("round ", game.get_cycle())

    # if doozing is possible, do it
    my_cells = [(x.get_pos().getx(), x.get_pos().gety())
                for x in game.get_board().get_mycells()]

    mp = dict()
    for coor, cell in game.get_board().get_cells().items():
        mp[coor] = cell.get_checker()

    pos = pos_dooz_move(game, my_cells, mp)
    if len(pos):
        des, ps = pos[0][0], pos[0][1]
        print("moving", des, "to", ps, "for dooz")
        return game.move(game.get_board().get_cell(des[0], des[1]).get_checker(), Pos(ps[0], ps[1]))

    # if you can prevent enemy from doozing, do it
    enemy_cells = [(x.get_pos().getx(), x.get_pos().gety()) for x in game.get_board().get_oppcells()]
    enemy_pos = pos_dooz_move(game, enemy_cells, mp)
    if len(enemy_pos):
        for cell in my_cells:
            tmp_cell = mp[cell]
            mp[cell] = None
            new_my_cells = [x for x in my_cells if x != cell]
            for nei_cell in game.nei[cell]:
                if mp[nei_cell] == None:
                    mp[nei_cell] = tmp_cell
                    new_my_cells.append(nei_cell)
                    enemy_pos = pos_dooz_move(game, new_my_cells, mp)
                    if not len(enemy_pos):
                        print("moving", cell, "to", nei_cell, "preventing")
                        return game.move(game.get_board().get_cell(cell[0], cell[1]).get_checker(), Pos(nei_cell[0], nei_cell[1]))
                    new_my_cells.pop()
                    mp[nei_cell] = None

            mp[cell] = tmp_cell










    print("moving randomely")
