# -*- coding: utf-8 -*-
"""
Code devolopée par
Rayan DRISSI (@rayan_d_10, mail: school@rayan-drissi.com)
assistée par
Dimitri Bohmler (@dis_mitri)
Matthew Bonhomme (@matthewbhe)

"""
#%% import
from tkinter import *
from random import *
import logging  # la gestion d'erreur
from tkinter.font import *  # les polices
from tkinter.messagebox import * # les popup
import sys  # le system pour sys.exit()
from time import sleep
import os
import subprocess # pour ouvrir le fichier index html a l'aide de python sans passer par os si l'invite de commande est desactiver
from lib_plateau import * #local lib


try:  # ce try  est juste pour rayan
    from fonction_recurante import *  # dans le pythonpath ou dans le dossier envoyer
except:
    sys.path.append("C:\\10 rayan\\NSI\\fonction")
    from fonction_recurante import *

    print('importé via sys')

logging.basicConfig(format='line=%(lineno)s %(message)s')  # pour la gestion d'érreur

# %% debut du code

P = Plateau()


class Fenetre:
    """
    Cette Class sert a la gestion de l'interface graphique en tkinter
    tous ce qui est print n'est pas lu par l'utlisateur mais pas le dev il sert donc a debugoger le jeux
    l'interface du taquin commence a la methode init_taquin le reste sert juste a l'interface de base
    """




    def __init__(self):
        """
        on renvoie a init par convention et pour tinker si il veut s'auto debuger avec le debuger tinker et les init separer sont plus utile au debugage
        """
        self.init()

    def init(self):
        """
        initialise notre fenetre avec nos couleur et la resolution ainsi que le pleine écran et d'autre chose
        :return:
        """
        self.epi = False  # mode epileptic (esteregg)
        self.root = Tk()
        self.top_verif = False
        self.bg = "#1e1f29"
        self.root['bg'] = self.bg
        self.root.title("Puissance 4")
        self.resolution(
            mode='auto')  # fonction qui mets la resolution automatiquement en fonction de la resolution de l'ecran 1
        self.root.attributes('-fullscreen', False)
        self.top_verif = False  # si nous souhaiton utiliser des toplevel permet de savoir si ils sont activer ou pas (chez nous non normalement)
        Button(self.root, height=0, relief=FLAT, width=0, highlightthickness=0, command=self.f_epi, bg=self.bg).place(
            x=0, y=0)  # ester egg

        self.bu_fermer = Button(self.root, bg='red', width=10, height=0, relief=FLAT,
                                command=self.root.destroy)
        self.bu_fermer.place(relx=0.988, rely=0.0001)
        self.police_ttg = Font(size=30)
        self.init_p4()


    def init_top(self):
        """
        initialise un top level ( cette fonction n'est pas forcement utiliser)
        :return:
        """
        if self.top_verif:
            return True
        self.top = Toplevel(self.root)
        self.top['bg'] = self.bg
        self.top.title("Top")
        self.top.geometry('1920x1080')
        self.top_verif = True

        #self.bu_fermer_top = Button(self.top, bg='red', width=10, highlightthickness=0, height=0, relief=FLAT,command=self.top.destroy).place(relx=0.988, rely=0.0001)

    def affichage(self, top=0):
        """
        Affiche le root
        ou le top si il est souhaitez
        :param top:
        :return:
        """
        if top == 0:
            self.root.mainloop()
        else:
            self.top.mainloop()

    def rename(self, nom, top=0):
        """
        pour rename les fenêtres
        :param nom:
        :return:
        """
        if top == False:
            self.root.title(nom)
        elif top == True:
            self.top.title(nom)

    def screen_shot(self, nom, extension=".png"):
        """
        effectue un screen shot
        :param nom:
        :return:
        """
        PIL.ImageGrap.grab().sabe(nom + extension)

    def open_image(self, nom):
        """

        :param nom: avec l'extension
        :return:
        """
        photo = PhotoImage(file=nom)

        return photo

    def fond(self, couleur='0', methode=False, top=False, renvoie=False):

        """
        change la couleur du fond
        inutile de lire cette fonction elle permet juste de gérer plein de chose pour l'ester egg
        :param couleur: la couleur souhaiter ou zero pour random
        :param methode: la methode utilisé dans couleur_random()
        :param top: si on veux modifier la couleur du top
        :return: nothing
        """
        if not renvoie:
            if not top:
                if couleur != '0':
                    self.root['bg'] = couleur
                elif methode != 0:
                    self.root['bg'] = couleur_random(methode)
                else:
                    try:
                        self.root['bg'] = couleur
                    except:
                        print('erreur sur le changement de fond couleur')
            elif top:
                if couleur != '0':
                    self.top['bg'] = couleur
                elif methode != 0:
                    self.top['bg'] = couleur_random(methode)
                else:
                    try:
                        self.top['bg'] = couleur
                    except:
                        print('erreur sur le changement de fond couleur')
        else:
            self.couleur_bu = couleur_random(methode)

    def resolution(self, taille='1920x1080', top=False, mode='manuel'):
        """
        change la resolution
        :param mode: manuel or auto
        :param taille: 1920x1080
        :param top: type bool
        :return: nothing
         si le mode est auto cela change la resolution automatiquement par rapport a la resolution de l'écran
        """
        if mode == 'auto':
            x = self.root.winfo_screenwidth()
            y = self.root.winfo_screenheight()
            taille = str(x) + 'x' + str(y)
        if top == False:
            self.root.geometry(taille)
        else:
            self.top.geometry(taille)

    def actualisation(self):
        """
        gere actualisation de la fenetre et s'auto appelle au bout de 50ms
        sert pour le moment au ester egg
        :return:
        """
        if self.epi:
            self.fond(methode=4)
            self.fond(methode=3, renvoie=True)

        self.root.after(50, self.actualisation)

    def f_epi(self):
        """
        ester egg sur le mode épileptique
        :return:
        """

        self.epi = True
        self.actualisation()

    ##############################################################################################################################
    # %%spyderonly debut de la zone du Puissance 4
    ###############################################################################################################################

    def init_p4(self):
        """

        """
        self.root.iconbitmap('puissance4.ico')
        self.couleur_bg = "#404256"
        self.couleur_fg = 'white'
        self.coup = False # pour verif les coup dans actualiser_grille()
        self.police = Font(size=15, family='High Tower text')  # normalement inclus avec office sinon mettez Times news roman
        self.resolution("1400x900")
        self.ia = (False, -1)
        self.attente = False
        self.init_canevas()
        self.init_grille()
        self.init_bouton()
        self.top_new_game()

    def init_canevas(self):
        """initalise le cannevas de jeu """
        self.can = Canvas(self.root, width=1000, height=700, bd=0, bg=self.bg)
        self.can.place(anchor=CENTER, relx=0.4, rely=0.5)
        self.can.bind("<Button-1>", self.recup_click)
        self.image_grille = self.open_image("grille.png")
        self.can.create_image(500, 350, image=self.image_grille)

    def init_bouton(self):
        """nos 100 000 bouton et label"""

        self.new = Button(self.root, text="Nouvelle partie", bg=self.couleur_bg, fg=self.couleur_fg, bd=2,
                            font=self.police, width=12, height=3, command=self.top_new_game)
        self.new.place(anchor = CENTER, relx=0.9, rely=0.5)

        self.tour = Label(self.root, text=" ", bg=self.dico_couleur["Rouge"], fg=self.couleur_fg, bd=2,
              font=self.police, width=7, height=3)
        self.tour.place(relx=0.4, rely=0.05, anchor=CENTER)

        Button(self.root, text="Regle du jeux", bg=self.couleur_bg,
               fg=self.couleur_fg, bd=2, width=10, height=3, command=self.rule).place(relx=0.01, rely=0.01)


        Label(self.root, text="@rayan_d_10", bg=self.bg, fg=self.couleur_fg, bd=2,
              font=self.police, width=10, height=2).place(relx=0.85,rely=0.98,anchor=CENTER)

        Label(self.root, text="@dis_mitri\n@matthewbhe\n@amaury.rbt", bg=self.bg, fg=self.couleur_fg, bd=2, width=11, height=3).place(relx=0.95,rely=0.97,anchor=CENTER)

    def init_grille(self):
        self.colone = [[750] for i in range(7)]
        self.position = [i * 135 + 100 for i in range(7)]
        self.dico_couleur = {"Jaune": "#F1C40F", "Rouge": "#FF0000"}

    def aff_ligne(self, taille):
        """affiche des lignes pour savoir ou cliquer """
        x = -85 # j'incremente au debut
        x2 = 15 # -85 + 100
        for i in range(7):
            x += 135
            x2 += 135
            self.can.create_line(x, 0, x, 700, fill="white", width=taille)
            self.can.create_line(x2, 0, x2, 700, fill="white", width=taille)

    def actualiser_grille(self):
        r = 50
        if self.coup == P.dernier_coup:#si aucun coup n'a été effectue
            return False
        self.coup = P.dernier_coup

        if not (self.coup[0] == "attente"):
            color = self.coup[0]
            x = self.position[self.coup[1][0]]
            y = self.colone[self.coup[1][0]][-1] - 115
            self.colone[self.coup[1][0]].append(y)
            self.can.create_oval(x-r, y-r, x+r, y+r, fill=self.dico_couleur[color], outline=self.dico_couleur[color])
        self.tour.config(bg=self.dico_couleur[P.tour])

    def recup_click(self, event):
        print("on rentre dans recup click")
        if self.attente:
            print('on ne peut pas jouer')
            return False
        self.attente = True
        print('on ne peut plus jouer')
        x, y = event.x, event.y
        x_min = -85  # j'incremente au debut
        x_max = 15  # -85 + 100
        for i in range(7):
            x_min += 135
            x_max += 135
            if x_min <=x<= x_max:
                self.play(i)
                return True
        self.change_attente()


    def play(self, case):
        color = P.tour
        if not P.play(color, case, ia="player")[0]:
            self.change_attente()
            print('coup hors du tableau coté tk')
            return False
        self.actualiser_grille()
        if self.verif_win():
            return True
        elif P.egalite:
            print('egalite')
            self.top_new_game()
        if self.ia[0]:
            self.root.after(500, self.play_ia)
        else:
            self.root.after(500, self.change_attente)



    def play_ia(self):
        if self.ia[1] == 0:
            P.ia0()
        elif self.ia[1] == 1:
            P.ia1()
        elif self.ia[1] == 2:
            P.ia2()
        elif self.ia[1] == 3:
            P.ia3()
        self.actualiser_grille()
        print("l'ia a finis de jouer")
        P.txt_color()
        
        if not self.verif_win():
            self.change_attente()
        elif P.egalite:
            print("egalité")
            self.top_new_game()
        else:
            print("win")

    def change_attente(self):
        print('on peut de nouveau jouer \n')
        self.attente = False

    def verif_win(self):
        self.actualiser_grille()
        verif = P.detect_win()
        if verif[0] == True:
            x_min = self.position[verif[2]]
            x_max = self.position[verif[4]]
            y_min = self.colone[verif[2]][verif[3]]-115
            y_max = self.colone[verif[4]][verif[5]]-115
            print(x_min, y_min, ",  ", x_max, y_max)
            self.can.create_line(x_min, y_min, x_max, y_max, fill="white", width=3)
            self.top_new_game()
            txt_win = f"Le joueur {verif[1]} à gagner"
            self.label_win = Label(self.top, text=txt_win, bg=self.bg, fg=self.couleur_fg, bd=2,
                                   font=self.police, width=25, height=5)
            self.label_win.place(anchor=CENTER, relx=0.5, rely=0.05)
            self.attente = False
            return True



    def top_new_game(self):
        self.init_top()
        self.resolution("500x400", top=True)
        self.init_grille()
        Button(self.top, text="User vs User", bg=self.couleur_bg,
               fg=self.couleur_fg, bd=2, width=10, height=2,
                                   font=self.police, command=self.u2u).place(relx=0.2, rely=0.3, anchor=CENTER)
        Button(self.top, text="ia vs ia", bg=self.couleur_bg,
               fg=self.couleur_fg, font=self.police, bd=2, width=10, height=2, command=self.iavsia).place(relx=0.8, rely=0.3, anchor=CENTER)
        Button(self.top, text="ia tres facile", bg=self.couleur_bg,
               fg=self.couleur_fg, bd=2, width=10, height=2 ,
                                   font=self.police, command=self.lvl0).place(relx=0.2, rely=0.55, anchor=CENTER)
        Button(self.top, text="ia facile", bg=self.couleur_bg,
               fg=self.couleur_fg ,font=self.police, bd=2, width=10, height=2, command=self.lvl1).place(relx=0.8, rely=0.55, anchor=CENTER)
        Button(self.top, text="ia normal", bg=self.couleur_bg,
               fg=self.couleur_fg , font=self.police, bd=2, width=10, height=2, command=self.lvl2).place(relx=0.2, rely=0.8, anchor=CENTER)
        Button(self.top, text="ia difficile", bg=self.couleur_bg,
               fg=self.couleur_fg ,font=self.police, bd=2, width=10, height=2, command=self.lvl3).place(relx=0.8, rely=0.8, anchor=CENTER)


    def u2u(self):
        "user to user"
        P.new_game()
        self.ia = (False, -1)
        self.sup_all()
        self.top.destroy()
        self.top_verif =  False
        self.tour.config(bg=self.dico_couleur[P.tour])

    def lvl0(self):
        P.new_game()
        self.ia = (True, 0)
        self.sup_all()
        self.top.destroy()
        self.top_verif =  False
        self.tour.config(bg=self.dico_couleur[P.tour])

    def lvl1(self):
        P.new_game()
        self.ia = (True, 1)
        self.sup_all()
        self.top.destroy()
        self.top_verif =  False
        self.tour.config(bg=self.dico_couleur[P.tour])

    def lvl2(self):
        P.new_game()
        self.ia = (True, 2)
        self.sup_all()
        self.top.destroy()
        self.top_verif =  False
        self.tour.config(bg=self.dico_couleur[P.tour])

    def lvl3(self):
        P.new_game()
        self.ia = (True, 3)
        self.sup_all()
        self.top.destroy()
        self.top_verif =  False
        self.tour.config(bg=self.dico_couleur[P.tour])

    def iavsia(self):
        P.new_game()
        self.ia = (True, 3)
        self.sup_all()
        self.top.destroy()
        self.top_verif =  False
        self.tour.config(bg=self.dico_couleur[P.tour])
        self.attente = True
        self.play_iavsia()


    def play_iavsia(self):
        """l'ia joue toute les 250ms """
        P.ia3()
        self.actualiser_grille()
        if self.verif_win():
            return True
        self.root.after(100, self.play_iavsia)


    def remplir_a_fond(self):
        """
        fonction uniquement de debugage
        :return:
        """
        for i in range(3):
            for i in range(7):
                P.play("Rouge", i)
                P.txt_color()
                self.actualiser_grille()
            for i in range(7):
                P.play("Jaune", i)
                P.txt_color()
                self.actualiser_grille()

    def remplir_ia(self):
        """
        fonction uniquement de debugage
        :return:
        """
        for i in range(15):
            P.ia1()
            self.actualiser_grille()

    def rule(self):
        """ ouvre dans le navigateur index.html"""
        url = 'regle4/accueil.html'
        try:
            import webbrowser
            import psutil
            
            if psutil.LINUX:
                # Linux
                print('unix')
                chrome_path = '/usr/bin/google-chrome %s'
                webbrowser.get(chrome_path).open(url)
            elif psutil.WINDOWS:
                # Windows
                print('windows')
                try:
                    os.startfile(url)  # windows
                    print('enfin')
                except:
                    print("webbrowser")
                    path_a = os.getcwd()
                    url = path_a + '/' + url
                    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
                    webbrowser.get(chrome_path).open(url)
                    chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'#windows serveur et veille version
                    webbrowser.get(chrome_path).open(url)

            elif psutil.MACOS:
                print('macos')
                # MacOS
                chrome_path = 'open -a /Applications/Google\ Chrome.app %s'
                webbrowser.get(chrome_path).open(url)
        except:#google n'est pas installer
            try:
                os.startfile(url) # windows
                print('enfin')
            except:# lamenais (cmd bloque)
                print('#################################################\n il faut lancer a la main le fichier index.html \n #############################')

    def sup_all(self):
        """ cette fonction vide le canevas
        c'est sale mais fonctionel"""
        for i in self.can.find_all():#parcours tous les elements du canevas
            if i==1:
                continue
            self.can.delete(i)


    def couleur_rond(self):
        """ cette fonction choisis les couleur des ronds
        soit via des couleur predefinis soit via des couleur au hasard qui se base sur une fonction de fonction recurante """
        self.dico_couleur = {"jaune": "#F1C40F", "rouge": "#FF0000"}




