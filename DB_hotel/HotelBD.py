#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar  4 13:51:43 2022

@author: marijansoric
"""
import sqlite3
#Ce ne sont pas les méthodes qui impriment les résultats (pas de print)

class HotelDB:
    
    def __init__(self, nom):
        self.__DBname = nom
        self.__conn = sqlite3.connect(self.__DBname)
    
    def __str__(self):
        return 'Base de données :'+self.__DBname
    
    def get_name_hotel_etoile(self, nbEtoiles):
        curseur = self.__conn.cursor()
        liste = []
        try:
            if nbEtoiles <= 0:
                raise ValueError("Le nbr d'étoiles doit être stric. positif.")
            S = "SELECT nom, etoiles FROM hotel WHERE etoiles = {};".format(nbEtoiles)
            # S1 = 'SELCT nom FROM hotel WHERE etoiles=%d', % nbEtoiles     #obso
            # S2 = 'SELCT nom FROM hotel WHERE etoiles=?', (nbEtoiles)      #secur
            curseur.execute(S)
        except sqlite3.OperationalError as sqlerr:
            print('{} in {}'.format(str(sqlerr), self.__DBname))
        except TypeError as typerr:
            print('TypeError : ',str(typerr))
        except ValueError as valerr:
            print('ValueError :',str(valerr))
        else:
            liste = curseur.fetchall()
        
        return liste
    
    def NewClient(self, nom, prenom):
        curseur = self.__conn.cursor()
        try:
            curseur.execute("SELECT nom, prenom FROM client WHERE nom ='{}' \
                             AND prenom = '{}'".format(nom, prenom))
        except sqlite3.OperationalError as sqlerr:
            print('{} in {}'.format(str(sqlerr), self.__DBname))
            return None
        
        liste = curseur.fetchall()
        if len(liste) != 0:
            print('Le client existe déjà.')
            return liste[0][0]
        try:
            curseur.execute("INSERT INTO client(nom, prenom) VALUES  \
                            ('{}','{}')".format(nom, prenom))
        except sqlite3.OperationalError as sqlerr:
            print('{}' in '{}'.format(str(sqlerr), self.__DBname))
            return None
        return curseur.lastrowid
            
    def __del__(self):
        self.__conn.close() 
        

if __name__ == '__main__':
    aHotelDB = HotelDB('hotellerie.db')
    nbEtoiles = 2
    resultat = aHotelDB.get_name_hotel_etoile(nbEtoiles)
    print("Liste des noms d'hotel", nbEtoiles, "étoiles : ", resultat)
    IDClient = aHotelDB.NewClient('Soric','Marijan')
    print('ID Client:', IDClient)