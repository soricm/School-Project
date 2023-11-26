#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 18 13:39:12 2022

@author: marijansoric
"""
from tkinter import *
from random import randint
from formes import *
from tkinter import colorchooser
import sqlite3

class ZoneAffichage(Canvas):
    def __init__(self, parent, largeur, hauteur, color):
        Canvas.__init__(self, parent, width=largeur, height=hauteur, bg=color) #appel au constructeur
        
        self.__listeShape = []
        # Base, Poteau, Traverse, Corde
        self.__listeShape.append(Rectangle(self, 50,  270, 200,  26, "brown"))
        self.__listeShape.append(Rectangle(self, 87,   83,  26, 200, "brown"))
        self.__listeShape.append(Rectangle(self, 87,   70, 150,  26, "brown"))
        self.__listeShape.append(Rectangle(self, 183,  67,  10,  40, "brown"))
        # Tete, Tronc
        self.__listeShape.append(Rectangle(self, 188, 120,  20,  20, "black"))
        self.__listeShape.append(Rectangle(self, 175, 143,  26,  60, "black"))
        # Bras gauche et droit
        self.__listeShape.append(Rectangle(self, 133, 150,  40,  10, "black"))
        self.__listeShape.append(Rectangle(self, 203, 150,  40,  10, "black"))
        # Jambes gauche et droite
        self.__listeShape.append(Rectangle(self, 175, 205,  10,  40, "black"))
        self.__listeShape.append(Rectangle(self, 191, 205,  10,  40, "black"))

    def cachePendu(self):
        for i in range(len(self.__listeShape)):
            self.__listeShape[i].setState("hidden")
        
    def dessinePiecePendu(self, i):
        if i <= len(self.__listeShape):
            self.__listeShape[i-1].setState("normal")
            
    def cachePenduUndo(self, j):
        if j <= len(self.__listeShape):
            self.__listeShape[j].setState("hidden")

    
     
class MonBoutonLettre(Button):
    def __init__(self, parent, grandparent, t):
        Button.__init__(self, parent, text=t, state=DISABLED)
        self.__lettre = t
        self.__fenetre = grandparent

    def cliquer(self):
        self.config(state=DISABLED) #savoir où on est : ici self=mon bouton !
        self.__fenetre.traitement(self.__lettre)
        
    

class FenPrincipale(Tk):
    def __init__(self): 
        Tk.__init__(self) #appel constructeur classe mere 
        self.title("Jeu du pendu")
        self.configure(bg="blue")
        self.__conn = sqlite3.connect('pendu.db')
        self.__list = self.requete_joueurs()
        self.__nomjoueur = StringVar()
        self.__nomjoueur.set("Nom joueur")
        
        def show():  # fonction appelée lors de la validation du joueur
            label.config(text = clicked.get()) 
            self.__nomjoueur = clicked.get()
            Score.pack_forget() 

        #barre du haut
        barreOutils = Frame(self)
        MenuCouleur = Frame(self)
        MenuUndo = Frame(self)
        Score = Frame(self)
        newGameButton = Button(barreOutils, text='Nouvelle Partie') 
        QuitButton = Button(barreOutils, text='Quitter') 
        ChoixCouleurFond = Button(MenuCouleur, text='Fond')
        ChoixCouleurFondDessin = Button(MenuCouleur, text='Fond Dessin')
        UndoButton = Button(MenuUndo, text='Annuler') 
        ValiderJ = Button(Score, text = "Valider Joueur", command=show) 
        label = Label(barreOutils , text = " ") 
        EntrerNom = Entry(Score, font=("Arial",20),bg="white", textvariable=self.__nomjoueur)

        #canevas du dessin du pendu
        self.__canevas = ZoneAffichage(self, 600, 400, color="red")
        
        ####################
        # Test menu déroulant


         

        
        options = []
        for joueur in self.__list:
            options.append(joueur[1] + ' ' + joueur[2])

        for a in self.__list: # trouver l'id du joueur
            if self.__nomjoueur == a[1]+' '+a[2]:
                self.__idjoueur = a[0]

        
        clicked = StringVar() 
        clicked.set( "Sélectionnez Joueur") 
        
        drop = OptionMenu(Score, clicked , *options) 
        
        
        #mot
        self.__textelmot = StringVar()
        self.__textelmot.set("Mot : ")
        lmot = Label(self, textvariable=self.__textelmot)
        
        chgcouleur = Label(MenuCouleur, text="Pour changer la couleur : ")
        chgcout = Label(MenuUndo, text="Pour annuler le dernier coup : ")

        #clavier
        Clavier = Frame(self)
        self.__boutons = []
        for i in range(26):
            t = chr(ord('A')+i)
            self.__boutons.append(MonBoutonLettre(Clavier, self, t))
            
        #placement éléments
        barreOutils.pack(side=TOP, padx=5, pady=5)
        Score.pack(side=TOP, padx=5, pady=5)
        newGameButton.pack(side=LEFT, padx=5, pady=5)
        QuitButton.pack(side=LEFT, padx=5, pady=5)
        MenuCouleur.pack(side=RIGHT, padx=5, pady=5)
        MenuUndo.pack(side=LEFT, padx=5, pady=5)
        
        drop.pack(side=TOP, padx=5, pady=5)
        label.pack(side=TOP, padx=5, pady=5)
        ValiderJ.pack(side=TOP, padx=5, pady=5)
        EntrerNom.pack(side=TOP, padx=5, pady=5)

        self.__canevas.pack(side=TOP, padx=50, pady=50)
        
        lmot.pack(side=TOP)
        Clavier.pack(side=TOP, padx=5, pady=5)

        chgcouleur.pack(side=TOP, padx=5, pady=5)
        ChoixCouleurFond.pack(side=TOP, padx=5, pady=5)
        ChoixCouleurFondDessin.pack(side=TOP, padx=5, pady=5)
        chgcout.pack(side=TOP, padx=5, pady=5)
        UndoButton.pack(side=TOP, padx=5, pady=5)

        ChoixCouleurFond.config(command=self.ChoixCoulF)
        ChoixCouleurFondDessin.config(command=self.ChoixCoulFD)
        
        
        for i in range(26):
            self.__boutons[i].config(command=self.__boutons[i].cliquer)
            
        UndoButton.config(command=self.untraitement)
        
        
        for i in range(3):
            for j in range(7):
                self.__boutons[i*7+j].grid(row=i, column=j)
        for j in range(5):
            self.__boutons[21+j].grid(row=3, column=j+1)
        
        
        QuitButton.config(command=self.destroy)
        newGameButton.config(command=self.NouvellePartie)

         
        self.chargeMots() #appel à une méthode interne

    def ChoixCoulF(self):
        #couleur du Fond
        colors = colorchooser.askcolor(color="blue", title="Choissez la couleur")
        self.configure(bg=colors[1])
    
    def ChoixCoulFD(self):
        #couleur du Fond-Dessin
        colors = colorchooser.askcolor(color="red", title="Choissez la couleur")
        self.__canevas.configure(bg=colors[1])
        
        
    def untraitement(self): # fonction pour 'Undo'
        self.__nbUndo += 1
        self.__textelmot.set('Mot : ' + self.__motAffiche[-self.__nbUndo])
        if self.__motAffiche[-self.__nbUndo] == self.__motAffiche[-self.__nbUndo-1]:
            self.__canevas.cachePenduUndo(self.__nbManques - self.__nbUndo)

    def traitement(self, lettre):
        cpt = 0
        lettres = list(self.__motAffiche[-1]) #créer une liste de toutes les lettres
        for i in range(len(self.__mot)):
            if self.__mot[i] == lettre:
                cpt += 1
                lettres[i] = lettre
        
        self.__motAffiche.append(''.join(lettres)) #colle ensemble avec '' qui fait la jointure
        
        if cpt == 0: # si la lettre n'est pas dans le mot
            self.__nbManques += 1
            self.__canevas.dessinePiecePendu(self.__nbManques - self.__nbUndo)
            if self.__nbManques - self.__nbUndo >= 10:
                self.finPartie(False)
        else:
            self.__textelmot.set('Mot : ' + self.__motAffiche[-1])
            if self.__mot == self.__motAffiche[-1]:
                self.finPartie(True)
                
    def finPartie(self, gagne):
        for b in self.__boutons:
            b.config(state=DISABLED)
        if gagne:
            self.__textelmot.set(self.__mot +'- Bravo, vous avez gagné !')
        else:
            self.__textelmot.set('Vous avez perdu, le mot était : '+self.__mot)
        succes=0
        lettres = list(self.__motAffiche[-1]) 
        for i in range(len(self.__mot)):
            if self.__mot[i] == lettres[i]:
                succes += 1
        succes = succes/len(list(self.__mot))
        curseur = self.__conn.cursor()
        curseur.execute("UPDATE Partie SET succes = '{}' WHERE idpartie='{}'".format(succes, self.__idpartie))
        
    def chargeMots(self):
        f = open('mots.txt', 'r')
        s = f.read()
        self.__mots = s.split('\n')
        f.close()
        #return self.__mots
        
    def NouvellePartie(self):
        for i in range(26):
            self.__boutons[i].config(state=NORMAL)
        self.__mot=self.__mots[randint(0, len(self.__mots)-1)]
        self.__motAffiche = [len(self.__mot)*'*', len(self.__mot)*'*'] #pour que liste[-2] existe même au premier coup
        self.__textelmot.set("Mot : " + self.__motAffiche[0]+ ' à {} lettres'.format(len(self.__mot)))
        self.__nbManques = 0
        self.__canevas.cachePendu()
        self.__nbUndo = 0
        self.__nomjoueur = 'Nouveau joueur'
        curseur = self.__conn.cursor()
        curseur.execute("INSERT INTO Partie(idpartie, idjoueur,mot) VALUES ((SELECT MAX(idpartie) FROM Partie)+1,'{}','{}')".format(self.__idjoueur, self.__mot))
        curseur2 = self.__conn.cursor()
        curseur2.execute("SELECT MAX(idpartie) FROM Partie")
        self.__idpartie = curseur2.fetchall() +1
        
    def requete_joueurs(self):
        curseur = self.__conn.cursor()
        try:
            S = "SELECT * FROM Joueur"
            curseur.execute(S)
        except sqlite3.OperationalError:
            return None
        else:
            return curseur.fetchall()
        
    def NewJoueur(self, prenomJ, nomJ): 
        curseur = self.__conn.cursor()
        try:
            curseur.execute("SELECT prenom, nom FROM Joueur WHERE prenom ='{}' \
                            AND nom ='{}'".format(prenomJ, nomJ))
        except sqlite3.OperationalError:
            return None
        liste = curseur.fetchall()
        if len(liste) != 0:
            return None
        try:
            curseur.execute("INSERT INTO client(prenom, nom) VALUES  \
                            ('{}','{}')".format(prenomJ, nomJ))
        except sqlite3.OperationalError:
            return None
        
    
if __name__ == "__main__":
    fen = FenPrincipale()
    fen.mainloop()