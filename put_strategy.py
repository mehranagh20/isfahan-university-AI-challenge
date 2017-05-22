from Pos import Pos

#TODO pos-dooz
#TODO enemy-pos-dooz
#TODO my-doozes
#TODO enemy-doozes

def pos_dooz(game, checkers):
    doozes = []
    for dooz in game.lines:
        num_ok = 0
        for checker in checkers:
            num_ok += 1 if checker in dooz else 0
        if num_ok == 2:
            for cell in dooz:
                if game.get_board().get_cell(cell[0], cell[1]).get_checker() == None:
                    doozes.append(cell)
    return doozes

def put_strategy(game):
    print("round ", game.get_cycle())

    my_cells = game.get_board().get_mycells()
    pos_doozes = pos_dooz(game, [(i.get_pos().getx(), i.get_pos().gety()) for i in my_cells])

    print("your possible doozes:")
    print(pos_doozes)

    if pos_doozes:
        return game.put(Pos(pos_doozes[0][0], pos_doozes[0][1]))

    # enemy_cells = game.get_board().get_oppcells()
    # pos_doozes = pos_dooz(game, [(i.get_pos().getx(), i.get_pos().gety()) for i in enemy_cells])


    print("\n\n")
