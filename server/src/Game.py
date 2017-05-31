from Board import Board
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR



def simplelinesplit(sock):
    data = ""
    try:
        while True:
            sock.settimeout(2)
            data += (sock.recv(1).decode())
            if len(data) > 0 and data[-1] == '\n':
                break
    except Exception as e:
        pass
    finally:
        return data


class Game:
    cycle_count = 100
    BUFF = 1024
    HOST = '0.0.0.0'  # must be input parameter @TODO
    PORT = 9999  # must be input parameter @TODO


    def __init__(self,s, port=9999):
        self.board = Board(s)
        self.round = 0
        self.current_player = 0
        self.players = [None, None]
        self.filename = None
        self.logfile = None
        self.messagefile = None

    def __str__(self):
        ret = "%d %d %s %d,%d" % (
            self.round,
            self.current_player,
            ','.join(['e' if item == None else '0' if item == self.players[0] else '1' for item in self.board.to_list()]),
            self.players[0]["inhand"],
            self.players[1]["inhand"]
        )
        return ret

    def parse_command(self, command_str):
        try:
            command = list(filter(bool, command_str.strip('\n').split(' ')))
            c = command[0]
            param2 = None
            if len(command) >= 3:
                i,j = command[2].split(',')
                param2 = (int(i),int(j))

            if c == 'put':
                i1,j1 = command[1].split(',')

                return c,(int(i1),int(j1)), param2
            elif c == 'mov':
                i1,j1,i2,j2 = command[1].split(',')
                return c,(int(i1),int(j1),int(i2),int(j2)), param2
        except:
            raise Exception("Invalid Command")


    def send_board(self):
        board_str = ','.join(['e' if item == None else 'm' if item == self.players[self.current_player] else 'o' for item in self.board.to_list()])
        ret = board_str + "," + "%d,%d,%d" % (self.players[self.current_player]["inhand"], self.players[1 - self.current_player]["inhand"], self.round)
        self.players[self.current_player]["sock"].send((str(ret) + "\n").encode())
        self.messagefile.write("S %d: %s" % (self.round, (str(ret) + "\n")))

    def start_server(self):
        ADDR = (self.HOST, self.PORT)
        self.serversock = socket(AF_INET, SOCK_STREAM)
        self.serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.serversock.bind(ADDR)
        self.serversock.listen(5)
        while 1:
            print('waiting for Player...')
            clientsock, addr = self.serversock.accept()
            print('...connected from:', addr)
            # try:
            data = simplelinesplit(clientsock)
            data = data.replace('\n', '').replace('\r', '')
            cmd, name = data.split(' ')
            if cmd != "REGISTER":
                raise Exception("INVALID COMMAND")

            self.players[self.current_player] = {"name": name, "inhand": 12, "total": 12, 'sock': clientsock, 'index': self.current_player}
            self.current_player +=1

            if self.current_player >= 2:
                print("%s and %s joned. ready to start" % (self.players[0]["name"],self.players[1]["name"]))
                return True
            # except:
            #     raise Exception(" Cannot Register")
        from time import sleep
        r=sleep(1)





    def start(self):
        from datetime import datetime
        gamename = "%s__%s" % (self.players[0]["name"],self.players[1]["name"])
        if not self.filename:
            self.filename = "%s_%s" % (datetime.now().strftime("%Y%m%d%H%M%S"),gamename)
        self.filename = "log"
        self.logfile = open(self.filename,'w')
        self.messagefile = open("%s.messagelog" % self.filename,'w')
        self.logfile.write("START %s %s %s\n" % (self.players[0]["name"],self.players[1]["name"], gamename))

        self.current_player = 0
        noWinner = True

        for self.round in range(1,self.cycle_count):
            try:
                self.send_board()
                command_str = simplelinesplit(self.players[self.current_player]["sock"])
                self.messagefile.write("R %d: %s" % (self.round, command_str))
                command, param1, param2 = self.parse_command(command_str)
                dest, isRandom = self.board.update(command=command, param1=param1, player=self.players[self.current_player])
            except Exception as e:
                isRandom = True
                dest = self.board.random_work(self.players[self.current_player])

            if dest is not None and self.board.is_line(dest):
                self.logfile.write("%s %sD\n" % (str(self), "R" if isRandom else ""))
                isRandom = False
                all_is_line = True
                try:
                    l = list(range(0, 24))
                    for i in l:
                        cell = self.board.cells[(int(i / 3), i % 3)]
                        if cell.get_checker() == self.players[1 - self.current_player]:
                            if not (self.board.is_line(cell)):
                                all_is_line = False
                                break

                    # if self.players[(self.current_player + 1) % 2]["inhand"] > 0:
                    #     self.players[(self.current_player + 1) % 2]["inhand"] -= 1
                    # else:
                    x = int(param2[0])
                    y = int(param2[1])
                    c = self.board.cells[(x,y)]
                    if c.get_checker() == self.players[1 - self.current_player] and\
                        (all_is_line or not self.board.is_line(c)):
                        c.set_checker(None)
                        self.players[1 - self.current_player]["total"] -= 1
                    else:
                        raise Exception("Choosen checker for POP is not an enemy checker.")
                except:

                    if self.board.random_pop(self.players[1 - self.current_player], all_is_line):
                        self.players[1 - self.current_player]["total"] -= 1
                        isRandom = True

            self.logfile.write("%s %s\n" % (str(self), "R" if isRandom else ""))

            if self.players[1 - self.current_player]["total"] < 3:
                noWinner=False
                self.logfile.write("winner %d\n" % self.current_player)
                print("winner %d\n" % self.current_player)
                break

            if dest is None:
                break
            self.current_player = 1 - self.current_player

        if noWinner:
            score_0 = 0
            score_1 = 0
            for i in range(0, 24):
                cell = self.board.cells[(int(i / 3), i % 3)]
                if cell.get_checker() == self.players[0]:
                    score_0 += 1
                elif cell.get_checker() == self.players[1]:
                    score_1 += 1
            if score_0 == score_1:
                self.logfile.write("draw\n")
                print("draw\n")
            else:
                self.logfile.write("winner %d\n" % (0 if score_0 > score_1 else 1))
                print("winner %d" % (0 if score_0 > score_1 else 1))

        self.players[0]["sock"].send("FINISH".encode())
        self.players[1]["sock"].send("FINISH".encode())

        self.players[0]["sock"].close()
        self.players[1]["sock"].close()
        self.serversock.close()
        self.logfile.close()
        self.messagefile.close()
        print("GAME FINISHED after %d rounds!" % self.round)
