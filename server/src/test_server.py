
import socket
from time import sleep

HOST = 'localhost'    # The remote host
PORT = 9999              # The same port as used by the server
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect((HOST, PORT))
s1.sendall('REGISTER team1\n')

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect((HOST, PORT))
s2.sendall('REGISTER team2\n')
i = 0
def send(s,m):
    global i
    # sleep(1)
    data = s.recv(1024)
    print(i, str(data))
    i += 1
    i %= 2
    # sleep(5)
    s.sendall(m)
while True:
    send (s1,'put  1,1\n')
    send (s2,'put  1,1\n')
















s1.close()

