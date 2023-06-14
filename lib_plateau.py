#!/usr/bin/env python
# -*- coding: <utf-8> -*

import os
import platform # pour trouver le nom de la platforme ( OS)
import socket # pour trouver le nom de la machine ( le nom du pc)
import sys
import random
import colorama
import sqlite3
try:
    from fonction_recurante import *  # dans le pythonpath ou dans le dossier
except:
    sys.path.append("C:\\10 rayan\\NSI\\fonction")
    from fonction_recurante import *
    print('import via sys.path')


class Plateau:

    def __init__(self):
        self.liste = [[" " * 5 for j in range(6)] for i in range(7)]
        self.historique = []
        self.cpt_ia = 0
        self.win = False
        self.egalite = False
        self.tour = "Rouge"

        with open("log/log_coup_last_game.txt", "w",
                  encoding="utf-8") as fichier:  # on fais un with pour etre sur de perdre le moins de donné en cas de pb \
            # ce fichier est reset a chaque game
            fichier.write("Ces log contienent les coups éffecutés lors de la derniere game\n")
        with open("log/log_verif_win.txt",
                  "w", encoding="utf-8") as fichier:
            fichier.write("ce fichier contient les logs éffectué pour la verif")



    def open_bdd(self, color="jaune"):
        self.bdd = sqlite3.connect(f'bdd_{color}')
        self.curseur = self.bdd.cursor()
        
    def close_bdd(self):
        self.bdd.commit()
        self.bdd.close()
        


    def play(self, color, case, ia="player"):

        self.dernier_coup = ["attente", -1]#pour l'interface graphique

        if not ( 0 <= case <=7 ):
            log = f"{ia}: La case est hors du tableau /  le coup a été tenter par les {color} en {case} \n {self.liste}\n"
            self.write_log(log)
            return (False, "La case est hors du tableau")
        j = 0
        coup_effectuer = False
        for i in self.liste[case]:
            if i == " " * 5 :
                self.liste[case][j] = color
                coup_effectuer = True
                break
            j += 1
        if not coup_effectuer:
            self.write_log(f"{ia}: le coup est hors du tableau car la colonne est pleine \n")
            return (False, "le coup est hors du tableau")
        if self.tour == "Rouge":
            self.tour = "Jaune"
        else:
            self.tour = "Rouge"

        self.dernier_coup = [color, (case,j)]
        if 'ia' in ia:
            self.cpt_ia += 1
        log = f"{ia}: le coup a été correctement éffectuer /  le coup a été fais par les {color} en {case} \n {self.liste}\n"
        self.write_log(log)
        verif = self.detect_win()
        if verif[0]:
            self.write_log_verif(f"verif win: Le joueur {verif[1]} a gagner")
            if self.win:#pour etre sur
                self.txt_color()# si  console
                print(f"Le joueur {verif[1]} a gagner")
                self.write_log(f"{ia}: Le joueur {verif[1]} a gagner")
        else:
            verif = False
            for i in self.liste:
                if " "*5 in i:
                    verif = True
            if not verif:
                print("egalité le jeu est complet")
                self.write_log("égalité le jeu est complet")
                self.egalite = True
                return (True, "egalite")
            else:
                self.write_log_verif("verif win: personne n'a gagner ")
        self.write_log_verif("\n")



        return (True, "le coup a correctement été effectué")


    def detect_win(self):
        for y in range(6):
            for x in range(7):
                if self.liste[x][y] == " "*5:
                    continue
                self.write_log_verif(f"verif win: on verif en {(x, y)}; la case x y est {self.liste[x][y]};\n {self.liste}\n")

                #ligne horizontal
                if x <= 3:
                    if self.liste[x][y] == self.liste[x+1][y] == self.liste[x+2][y] == self.liste[x+3][y]:
                        self.win = True
                        return (True, self.liste[x][y], x,y, x+3,y)
                #vertical
                if y <= 2 :
                    if self.liste[x][y] == self.liste[x][y+1] == self.liste[x][y+2] == self.liste[x][y+3]:
                        self.win = True
                        return (True, self.liste[x][y], x, y, x, y+3)
                #diagonale droite
                if y <= 2 and x <= 3:
                    if self.liste[x][y] == self.liste[x+1][y+1] == self.liste[x+2][y+2] == self.liste[x+3][y+3]:
                        self.win = True
                        return (True, self.liste[x][y], x, y, x+3,y+3)
                #diagonale gauche
                if y <= 2 and x >= 3:
                    if self.liste[x][y] == self.liste[x-1][y+1] == self.liste[x-2][y+2] == self.liste[x-3][y+3]:
                        self.win = True
                        return (True, self.liste[x][y], x, y, x-3,y+3)
        return (False, self.liste[x][y])


    def possible_win(self):
        """on regarde tous les coup qui sont possiblement gagnant"""
        self.liste_danger = []
        for y in range(6):
            for x in range(7):
                if self.liste[x][y] == " "*5:
                    continue
                self.write_log_verif(f"possible win: on verif en {(x, y)}; la case x y est {self.liste[x][y]};\n {self.liste}\n")


                #on regarde si y a une ligne de 4 horizontal  possible au sol
                if x <= 3 and y==0:# pour y=0 c'est simple car il faut pas verifier si la case en bas est vide
                    if self.liste[x][y] == self.liste[x+1][y] == self.liste[x+2][y] and self.liste[x+3][y] == ' '*5 :# case en x+3 danger
                        danger = (self.liste[x][y], x+3, y)#couleur, x, y
                        self.liste_danger.append(danger)
                    elif self.liste[x][y] == self.liste[x+1][y] == self.liste[x+3][y] and self.liste[x+2][y] == ' '*5 :#case en x+2 danger
                        danger = (self.liste[x][y], x+2, y)  # couleur, x, y
                        self.liste_danger.append(danger)
                    elif self.liste[x][y] == self.liste[x+2][y] == self.liste[x+3][y] and self.liste[x+1][y] == ' '*5 :#case en x+1 danger
                        danger = (self.liste[x][y], x+1, y)  # couleur, x, y
                        self.liste_danger.append(danger)
                    elif self.liste[x][y] == self.liste[x+1][y] == self.liste[x+2][y] and self.liste[x-1][y] == ' '*5 :# case en x danger
                        danger = (self.liste[x][y], x-1, y)  # couleur, x, y
                        self.liste_danger.append(danger)

                #on regarde si y a une ligne de 4 horizontal
                if x <= 3 and y!=0:
                    if self.liste[x][y] == self.liste[x+1][y] == self.liste[x+2][y] and self.liste[x+3][y] == " "*5 and self.liste[x+3][y-1] != " "*5 :# case en x+3 danger
                        danger = (self.liste[x][y], x+3, y)#couleur, x, y
                        self.liste_danger.append(danger)
                    elif self.liste[x][y] == self.liste[x+1][y] == self.liste[x+3][y] and self.liste[x+2][y] == " "*5 and self.liste[x+2][y-1] != " "*5 :#case en x+2 danger
                        danger = (self.liste[x][y], x+2, y)  # couleur, x, y
                        self.liste_danger.append(danger)
                    elif self.liste[x][y] == self.liste[x+2][y] == self.liste[x+3][y] and self.liste[x+1][y] == " "*5 and self.liste[x+1][y-1] != " "*5 :#case en x+1 danger
                        danger = (self.liste[x][y], x+1, y)  # couleur, x, y
                        self.liste_danger.append(danger)
                    elif self.liste[x][y] == self.liste[x+1][y] == self.liste[x+2][y] and self.liste[x-1][y] == " "*5 and self.liste[x-1][y-1] != " "*5  :# case en x danger
                        danger = (self.liste[x][y], x-1, y)  # couleur, x, y
                        self.liste_danger.append(danger)


                # on regarde si y a une ligne de 4 vertical
                if y <= 2 :# la hauteur c'est simple
                    if self.liste[x][y] == self.liste[x][y+1] == self.liste[x][y+2] and self.liste[x][y+3] == ' '*5:
                        danger = (self.liste[x][y], x, y+3)  # couleur, x, y
                        self.liste_danger.append(danger)

                # diagonale droite
                if y <= 2 and x <= 3:

                    if self.liste[x][y] == self.liste[x+1][y+1] == self.liste[x+2][y+2] and self.liste[x+3][y+3] ==  " "*5 and self.liste[x+3][y+2] != " "*5:
                        danger = (self.liste[x][y], x+3, y+3)  # couleur, x, y
                        self.liste_danger.append(danger)
                    elif self.liste[x][y] == self.liste[x+1][y+1] == self.liste[x+3][y+3] and self.liste[x+2][
                        y+2]  == " "*5 and self.liste[x+2][y+1] != " "*5:
                        danger = (self.liste[x][y], x+2, y+2)  # couleur, x, y
                        self.liste_danger.append(danger)
                    elif self.liste[x][y] == self.liste[x+2][y+2] == self.liste[x+3][y+3] and self.liste[x+1][
                        y+1] == ' ' * 5 and self.liste[x+1][y] != " "*5:
                        danger = (self.liste[x][y], x+1, y+1)  # couleur, x, y
                        self.liste_danger.append(danger)
                    elif y>=2:
                        if self.liste[x][y] == self.liste[x+1][y+1] == self.liste[x+2][y+2] and self.liste[x-1][
                            y-1]   ==  ' ' * 5 and self.liste[x-1][y-2] != " "*5:
                            danger = (self.liste[x][y], x-1, y-1)  # couleur, x, y
                            self.liste_danger.append(danger)
                    elif y==1:#on verifie pas si y a une case vide en bas car on est deja en bas
                        if self.liste[x][y] == self.liste[x+1][y+1] == self.liste[x+2][y+2] and self.liste[x-1][
                            y-1] ==  ' ' * 5:
                            danger = (self.liste[x][y], x-1, y-1)  # couleur, x, y
                            self.liste_danger.append(danger)

                #diagonale gauche
                if y <= 2 and x >= 3:
                    if self.liste[x][y] == self.liste[x - 1][y + 1] == self.liste[x - 2][y + 2] and self.liste[x - 3][
                        y + 3]  == " " * 5 and self.liste[x-3][y+2] != " "*5:
                        danger = (self.liste[x][y], x - 3, y + 3)  # couleur, x, y
                        self.liste_danger.append(danger)
                    elif self.liste[x][y] == self.liste[x - 1][y + 1] == self.liste[x - 3][y + 3] and self.liste[x - 2][
                        y + 2]  ==  ' ' * 5 and self.liste[x-2][y+1] != " "*5:
                        danger = (self.liste[x][y], x - 2, y + 2)  # couleur, x, y
                        self.liste_danger.append(danger)
                    elif self.liste[x][y] == self.liste[x - 2][y + 2] == self.liste[x - 3][y + 3] and self.liste[x - 1][
                        y + 1] == ' ' * 5 and self.liste[x-1][y] != " "*5:
                        danger = (self.liste[x][y], x - 1, y + 1)  # couleur, x, y
                        self.liste_danger.append(danger)
                    elif y>=2:
                        if self.liste[x][y] == self.liste[x - 1][y + 1] == self.liste[x - 2][y + 2] and self.liste[x + 1][
                            y - 1]  ==  ' ' * 5 and self.liste[x+1][y-2] != " "*5:
                                danger = (self.liste[x][y], x + 1, y - 1)  # couleur, x, y
                                self.liste_danger.append(danger)
                    elif y==1:
                        if self.liste[x][y] == self.liste[x - 1][y + 1] == self.liste[x - 2][y + 2] and self.liste[x + 1][
                            y - 1] ==  ' ' * 5 :
                                danger = (self.liste[x][y], x + 1, y - 1)  # couleur, x, y
                                self.liste_danger.append(danger)


        self.write_log_verif(f"la liste de danger est :\n {self.liste_danger}")
        return self.liste_danger

    def ia0(self):
        """ia lvl very easy
        this is a random ia with no brain """

        while True:
            liste_backup = list(self.liste)
            if self.play(self.tour, random.randint(0,6), ia="ia random")[0]:
                break
            else:
                self.liste = list(liste_backup)


    def ia1(self):
        """ a ia lvl easy
        this ia prevents the opponent to win and try to win if it can
        if the oppenent can win at the next move the ia block it"""
        self.possible_win()
        if self.liste_danger == []:
            self.ia0()
            return "random"
        print(self.liste_danger)
        print(self.tour)

        for i in self.liste_danger:#permet de voir ou l'ia peut gagner
            if i[0] == self.tour:
                self.play(self.tour, i[1], ia='ia1 win')
                return "ia 1 win"

        for i in self.liste_danger:#l'advesaire peut alors gagner
            if i[0] != self.tour:#si c'est l'adversaire
                self.play(self.tour, i[1], ia='ia1 counter')
                return "ia 1 counter"

    def ia2(self):
        """ a ia lvl good
        c'est l'ia du niveau 1 sauf que si elle joue et le joueur peut gagner apres alors elle ne fais pas cela """
        self.possible_win()
        print("ia2")
        if self.cpt_ia < 4:# les 4 premier coups de l'ia seront au centre
            nb_min = 2
            nb_max = 4
        elif self.cpt_ia < 8: # les coups de 4-8 seront toujours au centre mais moins 
            nb_min = 1
            nb_max = 5
        else:
            nb_min = 0
            nb_max = 6
        color = self.tour 
        if self.liste_danger == []:
            cpt_test_coup = 0 #compteur de tentative de coup si l'ia fais plus de 15 coup on la force a jouer a un endroit
            while True:
                verif = False
                liste_backup = self.copie_list(self.liste)
                cpt_test_coup += 1
                if self.play(self.tour, random.randint(nb_min, nb_max), ia="ia2 random")[0]:
                    lst = self.possible_win()
                    for i in lst:  # l'advesaire peut alors gagner
                        if i[0] == self.tour:  # si c'est l'adversaire
                            verif = True
                else:
                    continue
                if cpt_test_coup >= 15:
                    return "ia play force so lose"
                    break
                if verif:
                    self.liste = self.copie_list(liste_backup)
                    x, y = self.dernier_coup[1]
                    if self.liste[x][y] != " "*5:
                        self.liste[x][y] = " "*5
                    self.tour = color
                else:
                    break

            print("ia2 smart random")
            return "ia2 play"
        print(self.liste_danger)
        print(self.tour)

        for i in self.liste_danger:#permet de voir ou l'ia peut gagner
            if i[0] == self.tour:
                self.play(self.tour, i[1], ia='ia2 win')
                return "ia 2 win"

        for i in self.liste_danger:#l'advesaire peut alors gagner
            if i[0] != self.tour:#si c'est l'adversaire
                self.play(self.tour, i[1], ia='ia2 counter')
                return "ia 2 counter"


    def ia3(self):
        """cette ia est basé sur l'ia 2 en applicant le principe de l'algo de min max
        (refais maison) qui va parcourir un arbre de solution et attribuer une récompense a chaque coup possible"""
        color = self.tour
        l_backup = self.copie_list(self.liste)
        best_coup = (-5,0)
        for i in range(30):# on va tester 30 chemin de coup possible
            l_coup = []
            heuristique = 0
            for p in range(12):# si on veux augmenter la diffuculté il faut augmenter la profondeur
                self.ia2()#couleur jaune
                l_coup.append(self.dernier_coup)
                if self.detect_win():#ia gagne
                    heuristique = 100 - p
                    break
                self.ia2()#couleur rouge
                if self.detect_win():#ia perd
                    heuristique = -1
                    break
            if heuristique > best_coup[0]:
                best_coup = (heuristique, l_coup[0])
            self.liste = self.copie_list(l_backup)
        print('best_coup', end=" "*5)
        print(best_coup[1])
        self.play(best_coup[1][0],best_coup[1][1][0], "ia minmax")
        if self.tour == color:
            if color == "Rouge":
                self.tour = "Jaune"
            else:
                self.tour = "Rouge"
        return "ia3 play"


    def init_ia3_ML(self):
        """inutile"""
        self.liste_bdd = []        
        # [[index0 , etat0, (x0, y0, reward0)], ...
        
    def ia3_ML(self):
        """l'ia du machine learning ne marche pas elle n'a pas été implementé  """
        self.ia2()
        self.dernier_coup()


    def write_bdd(self):
        """inutile """
        self.recompense
        for i in self.liste_bdd:
            index = i[0]
            etat = i[1]
            coup_possible = i[2]
            #coup_possible[2] = reward 
            requette = f"""
            SELECT * FROM Principale WHERE Etat={etat};  
            """
            self.curseur.execute(requette)
            resultat = self.curseur.fetchone()
            
            if not resultat:
                requete = f"""
                INSERT INTO Principale 
                    (Index, Etat, coup_possible)
                VALUES
                    ({index}, {etat}, {coup_possible})
                """
                self.curseur.execute(requete)
                self.close_bdd()
            else:
                if coup_possible[0] not in resultat[0]:
                    resultat[0].append(coup_possible)
                else:
                    self.ajuste_recompense(resultat, coup_possible)
                    
                    
                requete = f"""
                INSERT INTO Principale 
                    (Index, Etat, coup_possible)
                VALUES
                    ({resultat[0]}, {resulat[1]}, {resultat[2]})
                """
                self.curseur.execute(requete)
                self.close_bdd()
   
    def copie_list(self, l):
        print(l)
        l2 = [[] for i in l]
        for i in range(len(l)):
            for j in range(len(l[i])):
                l2[i].append(l[i][j])
        return l2
                
                 
    def ajuste_recompense(self, resultat, coup_possible_var):
        """inutile"""
        coup_possible_bdd = resultat[2] #tupple
        pass
     
    def recompense(self):
        """inutile """
        pass
                            

    def write_log(self, log):
        with open("log/log_coup.txt",
                  "a", encoding="utf-8") as fichier:
            fichier.write(log)
        with open("log/log_coup_last_game.txt", "a",
                  encoding="utf-8") as fichier:
            fichier.write(log)

    def write_log_verif(self, log):
        with open("log/log_verif_win.txt",
                  "a", encoding="utf-8") as fichier:
            fichier.write(log)

    def clean_console(self):
        """ clean la console
         la commande print( "u001B[H\u001B[J") ne marche que sur spyder """
        if socket.gethostname() == "Rayan-Computer": # je suis sur pycharm il utilise un CMD differant
            print("\n" * 100 )
            return 0
        commands = {"Windows": "cls", "Linux": "clear"}
        os.system(comands[platform.system()])

    def __str__(self):
        """ affiche le jeux P4 en cours"""
        return self.txt()

    def txt_print(self):
        """alternative a __str__()"""
        print(self.txt())

    def txt(self):

        txt = f"""
    -----------------------------------------------------------------------
    |  {self.liste[0][5]}  |  {self.liste[1][5]}  |  {self.liste[2][5]}  |  {self.liste[3][5]}  |  {self.liste[4][5]}  |  {self.liste[5][5]} \
|  {self.liste[6][5]}  |
    -----------------------------------------------------------------------
    |  {self.liste[0][4]}  |  {self.liste[1][4]}  |  {self.liste[2][4]}  |  {self.liste[3][4]}  |  {self.liste[4][4]}  |  {self.liste[5][4]} \
|  {self.liste[6][4]}  |
    -----------------------------------------------------------------------
    |  {self.liste[0][3]}  |  {self.liste[1][3]}  |  {self.liste[2][3]}  |  {self.liste[3][3]}  |  {self.liste[4][3]}  |  {self.liste[5][3]} \
|  {self.liste[6][3]}  |
    -----------------------------------------------------------------------
    |  {self.liste[0][2]}  |  {self.liste[1][2]}  |  {self.liste[2][2]}  |  {self.liste[3][2]}  |  {self.liste[4][2]}  |  {self.liste[5][2]} \
|  {self.liste[6][2]}  |
    -----------------------------------------------------------------------
    |  {self.liste[0][1]}  |  {self.liste[1][1]}  |  {self.liste[2][1]}  |  {self.liste[3][1]}  |  {self.liste[4][1]}  |  {self.liste[5][1]} \
|  {self.liste[6][1]}  |
    ----------------------------------------------------------------------
    |  {self.liste[0][0]}  |  {self.liste[1][0]}  |  {self.liste[2][0]}  |  {self.liste[3][0]}  |  {self.liste[4][0]}  |  {self.liste[5][0]} \
|  {self.liste[6][0]}  |
    -----------------------------------------------------------------------
    |    1    |    2    |    3    |    4    |    5    |    6    |    7    | 
           """
        return txt

    def txt_color(self):
        colorama.init()
        liste_color = [[" " * 5 for j in range(6)] for i in range(7)] # le liste_color = list(self.liste) ne fonctionne pas pour backup
        for y in range(6):
            for x in range(7):
                if self.liste[x][y] == "Rouge":
                    liste_color[x][y] = colorama.Fore.RED + "Rouge" + colorama.Style.RESET_ALL
                elif self.liste[x][y] == "Jaune":
                    liste_color[x][y] = colorama.Fore.YELLOW + "Jaune" + colorama.Style.RESET_ALL
                else:
                    liste_color[x][y] = ' '*5
        txt = f"""
    -----------------------------------------------------------------------
    |  {liste_color[0][5]}  |  {liste_color[1][5]}  |  {liste_color[2][5]}  |  {liste_color[3][5]}  |  {liste_color[4][5]}  |  {liste_color[5][5]} \
|  {liste_color[6][5]}  |
    -----------------------------------------------------------------------
    |  {liste_color[0][4]}  |  {liste_color[1][4]}  |  {liste_color[2][4]}  |  {liste_color[3][4]}  |  {liste_color[4][4]}  |  {liste_color[5][4]} \
|  {liste_color[6][4]}  |
    -----------------------------------------------------------------------
    |  {liste_color[0][3]}  |  {liste_color[1][3]}  |  {liste_color[2][3]}  |  {liste_color[3][3]}  |  {liste_color[4][3]}  |  {liste_color[5][3]} \
|  {liste_color[6][3]}  |
    -----------------------------------------------------------------------
    |  {liste_color[0][2]}  |  {liste_color[1][2]}  |  {liste_color[2][2]}  |  {liste_color[3][2]}  |  {liste_color[4][2]}  |  {liste_color[5][2]} \
|  {liste_color[6][2]}  |
    -----------------------------------------------------------------------
    |  {liste_color[0][1]}  |  {liste_color[1][1]}  |  {liste_color[2][1]}  |  {liste_color[3][1]}  |  {liste_color[4][1]}  |  {liste_color[5][1]} \
|  {liste_color[6][1]}  |
    ----------------------------------------------------------------------
    |  {liste_color[0][0]}  |  {liste_color[1][0]}  |  {liste_color[2][0]}  |  {liste_color[3][0]}  |  {liste_color[4][0]}  |  {liste_color[5][0]} \
|  {liste_color[6][0]}  |
    -----------------------------------------------------------------------
    |    1    |    2    |    3    |    4    |    5    |    6    |    7    | 
           """
        print(txt)

    def new_game(self):
        self.liste = [[" " * 5 for j in range(6)] for i in range(7)]
        self.win = False
        self.cpt_ia = 0
        self.egalite = False
        self.tour = "Rouge"