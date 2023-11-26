#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr  1 13:47:06 2022

@author: marijansoric
"""
from PIL import Image
from math import *
import time


# Exo 1.1
def couleur (px,x,y,w,h,r,g,b):
    for i in range(w):
        for j in range (h):
            px[x+i,y+j]=r,g,b
    return px

# Exo 1.2
def moyenne(px, x, y, w, h):
    r,g,b=0,0,0
    for i in range (w):
        for j in range (h):
            a=list(px[x+i,y+j])
            r+=a[0]
            g+=a[1]
            b+=a[2]
    return r/(w*h),g/(w*h),b/(w*h)

# Exo 1.3
def ecarttype(px, x, y, w, h):
    mr,mg,mb=moyenne(px, x, y ,w ,h)
    r,g,b=0,0,0
    for i in range (w):
        for j in range (h):
            a=list(px[x+i,y+j])
            r+=a[0]**2
            g+=a[1]**2
            b+=a[2]**2
    sr=sqrt(r/(w*h)-mr**2)
    sg=sqrt(g/(w*h)-mg**2)
    sb=sqrt(b/(w*h)-mb**2)
    return sr,sg,sb

# Exo 1.4
def homogeneite(x,y,w,h,seuil):
    sigmar,sigmag,sigmab=ecarttype(px, x,y,w,h)
    return sum(ecarttype(px,x,y,w,h))/3<=seuil
    #return (sigmar<seuil and sigmag<seuil and sigmab<seuil)
    
# Exo 3.3
def homogeneite2(x,y,w,h,seuil):
    R,G,B=ecarttype(px, x,y,w,h)
    Y = 0.299 * R + 0.587 * G + 0.114 * B
    Cb = -0.1687*R-0.3313 * G + 0.5 * B
    Cr = 0.5 * R -0.4187 * G - 0.0813 * B
    return (Y<seuil and Cb<seuil and Cr<seuil)

# Exo 1.5
def divisionRectangle(x,y,w,h):
    largeur=w//2
    largeur2=(w-largeur)
    longueur=h//2
    longueur2=h-longueur
    rectangle1=(x,y,largeur,longueur)
    rectangle2=(x+largeur,y,largeur2,longueur)
    rectangle3=(x,y+longueur,largeur,longueur2)
    rectangle4=(x+largeur, y+longueur, largeur2, longueur2)
    return [rectangle1,rectangle2,rectangle3,rectangle4]
    


# Exercice 3.1 – Dans le cas de grandes images, les arbres de quadripartition 
# risquent d’atteindre beaucoup de noeuds, et la limite de m´emoire disponible 
# pourrait ˆetre un probl`eme. On souhaite utiliser une structure d’arbre implicite, 
# comme le tas vu au TD 2, pour stocker les arbres de mani`ere plus compacte.
#  Pour rappel, il s’agit de stocker tous les noeuds dans une liste, de d´eterminer leur 
# position dans l’arbre uniquement par leur position dans la liste, et de n’inclure
#  aucune r´ef´erence explicite entre noeuds. Donnez d’abord les formules permettant 
#  de calculer pour un noeud `a l’indice i les indices de son parent et de ses 4 enfants.

# Par analogie avec les arbres binaire, pour les arbres de quadripartition
# la formules pour obtenir ses 4 enfants est : 4*i+1 ,+2, +3, +4




# Exo 3.2
#  Modiﬁez   maintenant   la   classe   Noeud   ainsi   que   votre   code 
#  pour   g´en´erer   un   arbre  quaternaire  sous  forme  implicite



class Noeud:
    def __init__(self, x, y, w, h, seuil, px):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.couleur = None
        self.enfants = []
        self.px=px
        self.seuil=seuil
        
        if homogeneite2(x, y, w, h, seuil) or (w<2 or h<2): 
            r,g,b=moyenne(px, x, y, w, h)
            self.couleur=( round(r), round(g), round(b))
            
        else :
            L=divisionRectangle(x, y, w, h)
            for l in L:
                self.enfants.append(Noeud(l[0],l[1],l[2],l[3],seuil,px))
            
    def __str__(self, depth=0):
        tabs=" "*depth
        line=f"{tabs}{{x={self.x},y={self.y},w={self.w},h={self.h},couleur={self.couleur}}}"
        lines=(line, *(e.__str__(depth+1) for e in self.enfants))
        return "\n".join(lines)


    def EQ(self):
        if self.couleur!=None:
            eq=0
            for x in range (W):
                for y in range (H): 
                    r1,g1,b1=self.px[x,y]
                    eq+=((r1-r)**2+(g1-g)**2+(b1-b)**2)
            return eq
        else:
            eq=0
            for enfant in self.enfants:
                eq+=enfant.EQ()
            return eq
            
    def PSNR(self):
        eq=self.EQ()
        return 20*log10(255)-10*log10(eq/(3*self.h*self.w))




def compteEnfants(noeud):
    if not noeud.enfants:
        return 1
    else:
        somme=1
        for e in noeud.enfants:
            somme+=compteEnfants(e)
    return somme
            

        
def peint(noeud):
    if compteEnfants(noeud)==1:
        r,g,b=noeud.couleur
        couleur(noeud.px, noeud.x, noeud.y,noeud.w, noeud.h,r,g,b)
    else:
       for e in noeud.enfants:
           peint(e)
           
     
        
def peintProfondeur(noeud, compteur=0):
    if compteEnfants(noeud)==1:
        r,g,b=20*compteur, 20*compteur, 20*compteur
        couleur(noeud.px, noeud.x, noeud.y,noeud.w, noeud.h,r,g,b)
    else:
       for e in noeud.enfants:
           peintProfondeur(e, compteur+1)
    
    
if __name__ == '__main__' :
    tps1 = time.time()
    im = Image.open("lyon.png")
    px = im.load()
    W, H = im.size
    seuil=90 #50
    x,y,w,h=0, 0, W, H
    arbre=Noeud(x,y,w,h,seuil,px)
    #peintProfondeur(arbre,0)
    #print(arbre)
    #print(compteEnfants(arbre))
    
    im.show()
    tps2 = time.time()
    #profile()
    print(tps2-tps1)
# L’ob jectif du rapp ort est de compresser une image
# de    votre    choix    en    appliquant    la    m´etho de    de    
# quadripartition    vue    pr´ec´edemment,    et
# en l’optimisant avec les questions ci-dessous

 
