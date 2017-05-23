from Pos import Pos

# TODO pos-dooz
# TODO enemy-pos-dooz
# TODO my-doozes
# TODO enemy-doozes
# TODO make one way and two way moves ... a function

def pos_dooz(game, checkers):
    doozes = []
    for dooz in game.lines:
        num_ok = 0
        for checker in checkers:
            num_ok += 1 if checker in dooz else 0
        if num_ok == 2:
            for cell in dooz:
                if game.get_board().get_cell(cell[0], cell[1]).get_checker() == None and cell not in checkers:
                    doozes.append(cell)
    return doozes

def put_strategy(game):
    print("round ", game.get_cycle())

    my_cells = game.get_board().get_mycells()
    pos_doozes = pos_dooz(game, [(i.get_pos().getx(), i.get_pos().gety()) for i in my_cells])

    print("your possible doozes:")
    print(pos_doozes)

    # dooz if you can
    if pos_doozes:
        return game.put(Pos(pos_doozes[0][0], pos_doozes[0][1]))

    enemy_cells = game.get_board().get_oppcells()
    enemy_pos_doozes = pos_dooz(game, [(i.get_pos().getx(), i.get_pos().gety()) for i in enemy_cells])

    # prevent enemy's dooz if you can
    if len(enemy_pos_doozes) == 1:
        return game.put(Pos(enemy_pos_doozes[0][0], enemy_pos_doozes[0][1]))

    # make yourself a two way possible gooz
    empty_cells = game.get_board().get_emptycells()

    # first try with just one move
    c, mx = None, 0
    for cell in empty_cells:
        my_new_cells = [(x.get_pos().getx(), x.get_pos().gety()) for x in my_cells]
        my_new_cells.append((cell.get_pos().getx(), cell.get_pos().gety()))
        possible = pos_dooz(game, my_new_cells)
        if(len(possible) > mx):
            mx = len(possible)
            c = (cell.get_pos().getx(), cell.get_pos().gety())

    if mx >= 2:
        print("two way found with one move:")
        print(c)
        return game.put(Pos(c[0], c[1]))

    # try with two move_strategy
    for first_cell in [(x.get_pos().getx(), x.get_pos().gety()) for x in empty_cells]:
        my_new_cells = [(x.get_pos().getx(), x.get_pos().gety()) for x in my_cells]
        my_new_cells.append((first_cell))
        possible = pos_dooz(game, my_new_cells)
        if len(possible) == 1:
            continue
        for second_cell in [(x.get_pos().getx(), x.get_pos().gety()) for x in empty_cells]:
            if first_cell == second_cell:
                continue
            my_new_cells.append((second_cell))
            possible = pos_dooz(game, my_new_cells)
            if(len(possible) > mx):
                mx = len(possible)
                c = first_cell
            del(my_new_cells[-1])

    if mx >= 2:
        print("two way found with two moves")
        print(c)
        return game.put(Pos(c[0], c[1]))

    print("\n\n")
