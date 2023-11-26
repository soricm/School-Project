#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 19:31:14 2022

@author: marijansoric
"""
import sqlite3
import matplotlib.pyplot as plt
import numpy             as np

class Ouvrir:
    
    def __init__(self, nom):
        self.__DBname = nom
        self.__conn = sqlite3.connect(self.__DBname)
    
    def __str__(self):
        return 'Base de données :'+self.__DBname
    
    def requete_2(self):
        curseur = self.__conn.cursor()
        liste = []
        try:
            S = "SELECT cName,decision, count(*) \
                FROM Student JOIN Apply  ON Apply.sID = Student.sID \
                GROUP BY cName, decision"
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
    
    def __del__(self):
        self.__conn.close() 
        
        
if __name__ == '__main__':
    
    aBase = Ouvrir('base-stanford.db')
    req2 = aBase.requete_1()
    print(req2)
    
    TauxAcceptation = []
    College = []
    for tup in req4:
        if tup[0] not in College:
            College.append(tup[0])
            
    Demande = [0 for i in range(len(College))]
    
    for j in range(len(College)):
        for i in range(len(req4)):
            if req4[i][0] == College[j]:
                Demande[j] += req4[i][2] 
                
    for cName in College:
        for tup in req4:
            if tup[0] == cName and tup[1] == 'Y':
                TauxAcceptation.append(tup[2])
                
    for i in range(len(TauxAcceptation)):
        TauxAcceptation[i] = TauxAcceptation[i]/Demande[i]*100
    
    print(TauxAcceptation)
        

    labels = College
    men_means = TauxAcceptation
    width = 0.5       
    fig, ax = plt.subplots()
    ax.bar(labels, men_means, width, color = ['blue', 'purple', 'black', 'red'])
    ax.set_ylabel('Taux d\'acceptation (en %)')
    ax.set_xlabel('Universités')
    ax.set_title('Taux d\'accepation pour l\'échantillon observé')
    ax.legend()
    plt.show()
    plt.savefig('TauxAcceptation.png')
            
