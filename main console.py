#!/usr/bin/env python
# -*- coding: <utf-8> -*
"""
a ne pas executer dans spyder ou faire la manip expliquer dans le fichier
spyder_user.pdf

"""


from lib_plateau import * #local lib
from time import sleep
import sys
import os
import colorama

P = Plateau()
ia = True
exit = False
print('\n'*3)
choix = input("voulez vous jouer contre une IA ? y/n : ")
if choix == 'n':#c'est fais expres que si on mets rien on joue contre l'ia
    ia = False
else:
    verif = False
    while not verif:
        try:
            lvl = int(input("choisis le niveau de ton IA \n(ultra facile=0 ,facile=1, normal=2, hard=3, ultra hard=4) :  "))
            assert 0 <= lvl <= 4
            verif = True
        except:
            print('entre 0 et 4 !!')


while not P.win:
    try:
        P.clean_console()  # ça clean la console
    except:
        pass
    
    P.txt_color()
    print("\t" * 7, P.tour)

    verif = False
    while not verif:
        try:
            coup = input(f"    Vous etes les {P.tour}s choissiser une colonone: ")
            if coup == "exit" or coup == "stop":
                print("chef on remballe le client est pas content")
                exit = True
                break
            coup = int(coup)
            assert 1<=coup<=7
            verif = True
        except:
            print("un nombre entre 1 et 7!")
    if exit == True:
        sys.exit()# le sys.exit ne fonctionne pas dans le try
    P.play(P.tour, coup-1)
    if P.win:
        break
    if ia:
        P.txt_color()
        sleep(0.5)
        if lvl == 0:
            P.ia0()
        elif lvl == 1:
            P.ia1()



input("Appuyez sur une touche pour continuer... ")#le os.system("pause ne fonctionne pas sur IpadOS 14.5
#os.system("pause")