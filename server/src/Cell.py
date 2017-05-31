from Pos import Pos

class Cell:
    def __init__(self, x, y):
        self.__pos = Pos(x, y)
        self.__checker = None
        # if c != 'e':
        #     self.__checker = Checker(x, y, c)
    def to_str(self):
        return self.get_checker()
    def get_checker(self):
        return self.__checker

    def get_pos(self):
        return self.__pos

    def set_pos(self, newPos):
        self.__pos = newPos

    def set_checker(self, newChecker):
        self.__checker = newChecker
