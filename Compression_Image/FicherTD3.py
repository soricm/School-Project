#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 13:47:06 2022

@author: marijansoric
"""
from PIL import Image # importation de la librairie d’image PILLOW
from math import sqrt, log10 # fonctions essentielles de la librairie math
from memory_profiler import profile
#import requests

# 1.1
def remplir(px, r1, w, h, col):
    for x in range(r1[0], r1[0] + h):
        for y in range(r1[1], r1[1] + w):
            px[x, y]= col
    im.show()
    
# 1.2
@profile
def moyenne(px, r1, w, h):
    moy = [0,0,0]
    aire = h*w
    for x in range(r1[0], r1[0] + h):
        for y in range(r1[1], r1[1] + w):
            for i in range(3):
                moy[i] += px[x, y][i]/aire
    return tuple(moy)

# 1.3
def ecarttype(px, r1, w, h):
    moy = moyenne(px, r1, w, h)
    ect = [0,0,0]
    n = h*w
    for x in range(r1[0], r1[0] + h):
        for y in range(r1[1], r1[1] + w):
            for i in range(3):
                ect[i] += px[x, y][i]**2 /n
    for i in range(3):
        ect[i] = sqrt(ect[i] -moy**2)
    return tuple(ect)

# 1.4



def homogeneite(px, x, y, w, h, seuil):
    e = ecarttype(px, x, y, w, h)
    if seuil > e[0]:
        if seuil > e[1]:
            return seuil > e[2]
    return False
    

def homogeneite2(x,y,w,h,seuil):
    R,G,B=ecarttype(px, x,y,w,h) 
    Y = 0.299 * R + 0.587 * G + 0.114 * B
    return (Y<seuil)

# 1.5
def partition(x, y, w, h):
    return (
        (x, y, w//2, h//2),
        (x+ w//2, y, w-w//2, h//2),
        (x, y+ h//2, w//2, h-h//2),
        (x+w//2, y + h//2, w-w//2, h-h//2)
        )

# 2.1
class Noeud:
    def __init__(self, px, x, y, w, h, seuil=100):
        self.px = px
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.enfants = []
        self.couleur = None
        
        if (homogeneite2(x, y, w, h, seuil) ==True) or (w<2 or h<2):
            mr, mv, mb = moyenne(px, x, y, w, h)
            self.couleur = (round(mr), round(mv), round(mb))
        else:
            for x1, y1, w1, h1 in partition(x, y, w, h):
                self.enfants.append(Noeud(px, x1, y1, w1, h1, seuil))
        
    def __str__(self, depth=0):
        tabs = " " *depth
        line = f"{tabs}{{x={self.x}, y={self.y}, w={self.w}, h={self.h}, couleur={self.couleur}}}"
        lines = (line, *(e.__str__(depth+1) for e in self.enfants))


    def PSNR(self):
        W, H = im.size
        EQ = 0
        return 20*log10(225)-10*log10(EQ/(3*W*H))

if __name__ == '__main__':
    im = Image.open("lyon.png") # ouverture du fichier d’image
    W, H = im.size #attribut public
    print(W, H)
    px = im.load() # importation des pixels de l’image
    print(px[30, 55])
    im.show()
    #im = remplir(px, [0,0], 100, 100, (0,0,0))
    #im.save('lyon1.png')
    print('Fin')
    # racine = Noeud(0, 0, 4, 4, 128, 128, 128,
    #     Noeud(0, 0, 2, 2, 255, 255, 255, None, None, None, None),
    #     Noeud(2, 0, 2, 2, 128, 128, 128, None, None, None, None),
    #     Noeud(2, 2, 2, 2, 128, 128, 128, None, None, None, None),
    #     )