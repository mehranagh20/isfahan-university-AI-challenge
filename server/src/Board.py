from Cell import Cell
from random import shuffle


def command_validate(command, param1, param2):
    return True


class Board:
    def __init__(self, s):
        self.cells = {}
        self.player1_cells = []
        self.player2_cells = []
        # self.emptyCells = {}
        for i in range(0, 8):
            for j in range(0, 3):
                tmp = Cell(i, j)
                self.cells[(i,j)] = tmp
                # self.emptyCells[(i,j)]= tmp


    def __str__(self):
        l = []
        for i in range(0,8):
            for j in range(0,3):
                l.append(self.cells[(i,j)])
        return str(l)

    def to_list(self):
        l = []
        for i in range(0,8):
            for j in range(0,3):
                l.append(self.cells[(i,j)].to_str())
        return l


    def get_neigbors(self, cell):
        if hasattr(cell, "neigbors"):
            return cell.neigbors
        cell.neigbors = []
        x = cell.get_pos().getx()
        y = cell.get_pos().gety()
        if y < 2:
            cell.neigbors.append(self.cells[(x,y + 1)])
        if y > 0:
            cell.neigbors.append(self.cells[(x,y - 1)])
        cell.neigbors.append(self.cells[((x + 1) % 8,y)])
        cell.neigbors.append(self.cells[((x - 1) % 8,y)])
        return cell.neigbors

    def is_line(self, cell):
        y = cell.get_pos().gety()
        x = cell.get_pos().getx()
        if self.cells[(x,0)].get_checker() == self.cells[(x,1)].get_checker() and self.cells[(x,0)].get_checker() == self.cells[(x,2)].get_checker():
            return True

        if x%2 == 0:
            if  self.cells[((x-1) % 8, y)].get_checker() == self.cells[(x, y)].get_checker() and \
                self.cells[((x-2) % 8, y)].get_checker() == self.cells[(x, y)].get_checker():
                return True

            if  self.cells[((x+1) % 8, y)].get_checker() == self.cells[(x, y)].get_checker() and \
                self.cells[((x+2) % 8, y)].get_checker() == self.cells[(x, y)].get_checker():
                return True
        else:
            if  self.cells[((x-1) % 8, y)].get_checker() == self.cells[(x, y)].get_checker() and \
                self.cells[((x+1) % 8, y)].get_checker() == self.cells[(x, y)].get_checker():
                return True


        return False

    def get_lines(self, x, y):
        self.__ans = []
        self.__tmp = []
        for i in range(0, 3):
            self.__tmp.append(self.__cells[x][i])
            self.__ans.append(self.__tmp)
        self.__tmp.clear()
        if x % 2 == 1 :
            self.__tmp.append(self.__cells[x-1][y])
            self.__tmp.append(self.__cells[(x + 1) % 8][y])
            self.__tmp.append(self.__cells[x][y])
        else:
            for i in range(0, 3):
                self.__tmp.append(self.__cells[(x + i) % 8][y])
            self.__ans.append(self.__tmp)
            self.__tmp.clear()

            for i in range(0, 3):
                self.__tmp.append(self.__cells[(x - i + 8) % 8][y])
            self.__ans.append(self.__tmp)
            self.__tmp.clear()

        return self.__ans

    def random_work(self,player):
        if player["inhand"] == 0:
            l = list(range(0, 24))
            shuffle(l)
            for i in l:
                cell = self.cells[(int(i / 3), i % 3)]
                if cell.get_checker() == player:
                    for neighbour in self.get_neigbors(cell):
                        if neighbour.get_checker() is None:
                            dest = self.update("mov", player, (cell.get_pos().getx(),cell.get_pos().gety(),neighbour.get_pos().getx(),neighbour.get_pos().gety()))
                            return dest[0]
        else:
            l = list(range(0, 24))
            shuffle(l)
            for i in l:
                cell = self.cells[(int(i / 3), i % 3)]
                if cell.get_checker() is None:
                    dest = self.update("put", player, (cell.get_pos().getx(), cell.get_pos().gety()))
                    # player["inhand"] -= 1
                    return dest[0]

        pass
        # if player.inhandcheckernumber > 0:
        #     index = randint(0, self.emptyCells.count())
        #     self.emptyCells[index].set_checker()
    def random_pop(self,player, all_is_line):
        l = list(range(0,24))
        shuffle(l)
        for i in l:
            cell = self.cells[(int(i / 3), i % 3)]
            if cell.get_checker() == player:
                if not(self.is_line(cell)) or all_is_line:
                    cell.set_checker(None)
                    return True

    def update(self,command, player, param1, param2=None):
        dest = None
        isRandom = False
        try:
            if not command_validate(command, param1, param2):
                raise Exception("wrong command")
            if command == "put": #__________________push___________________
                x = param1[0]
                y = param1[1]

                if player["inhand"] == 0 or self.cells[(x,y)].get_checker() is not None:
                    raise Exception("wrong command")
                else:
                    self.cells[(x,y)].set_checker(player)
                    dest = self.cells[(x,y)]
                # del self.emptyCells[x,y]
                player["inhand"] -= 1



            elif command == "mov": #move
                x1 = param1[0]
                y1 = param1[1]
                x2 = param1[2]
                y2 = param1[3]
                cs = self.cells[(x1, y1)]
                cd = self.cells[(x2, y2)]
                if cd in self.get_neigbors(cs) and \
                        cs.get_checker() == player and \
                        cd.get_checker() is None:
                    cs.set_checker(None)
                    cd.set_checker(player)
                    dest = cd
                else:
                    raise Exception("wrong command")
        except Exception as e:
            print("%s: %s %s %s" % (e.message,str(command), str(param1), str(param2)))
            dest = self.random_work(player)
            isRandom = True

        return dest, isRandom




