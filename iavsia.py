from lib_plateau import *
from time import sleep

P = Plateau()


while not P.win:
    P.txt_color()
    P.ia1()
    sleep(0.1)


