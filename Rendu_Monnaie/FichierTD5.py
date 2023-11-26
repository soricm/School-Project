#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May  6 14:01:43 2022

@author: marijansoric
# """


# 3.1
infty = float('inf') #'infini'#'infini'
# S est le stock des pièces, M est le montant 
def Monnaie(S,M): 
    mat=[[0]*(M+1) for _ in range(len(S)+1)]
    for i in range(len(S)+1):
        for m in range(M+1):
            if m == 0:
                mat[i][m] = 0
            elif i==0:
                mat[i][m] = infty
            else:
                mat[i][m] = min(
                            1 + mat[i][m - S[i-1]] if m - S[i-1] >= 0 else infty,
                            mat[i-1][m] if i >= 1  else infty)
    return mat[len(S)][M]

# 3.2
def Monnaie2(S,M):
    mat=[[0]*(M+1) for _ in range(len(S)+1)]
    L = [[[]]*(M+1) for _ in range(len(S)+1)] 
    # matrice des pièces utilisées pour chaque cellule (matrice de liste)
    for i in range(len(S)+1):
        for m in range(M+1):
            if m == 0:
                mat[i][m] = 0 # la liste L[i][m] reste vide
            elif i==0:
                mat[i][m] = infty # la liste L[i][m] reste vide
            else:
                mat[i][m] = min(
                    1 + mat[i][m - S[i-1]] if m - S[i-1] >= 0 else infty,
                    mat[i-1][m] if i >= 1 else infty)
                
                if mat[i][m] == mat[i-1][m]:
                    L[i][m] = L[i-1][m]
                else:
                    m1 = m-1
                    while mat[i][m1] >= mat[i][m]: 
                    # on cherche un nombre de pièce inférieur à mat[i][m] dans la ligne
                        m1 -= 1
                    L[i][m] = L[i][m1] + [m-m1] 
                    # (m-m1) est la pièce utilisée pour passer de [i][m] à [i][m1]
    return mat[len(S)][M], L[len(S)][M]

#3
def Dynamique(S, M, D):
    mat=[[0]*(M+1) for _ in range(len(S)+1)]
    for i in range(len(S)+1):
        for m in range(M+1):
            if m == 0:
                mat[i][m] = 0
            elif i==0:
                mat[i][m] = infty
            else:
                ma=[infty,mat[i-1][m]]
                for k in range(1, len(S)+1):
                    if D[i-1]>=k and m - k*S[i-1] >= 0:
                        ma.append(k + mat[i-1][m - k*S[i-1]])
                mat[i][m]=min(ma)
    return mat[len(S)][M]
#4
def Poids(S, M, P): 
    mat=[[0]*(M+1) for _ in range(len(S)+1)]
    for i in range(len(S)+1):
        for m in range(M+1):
            if m == 0:
                mat[i][m] = 0
            elif i==0:
                mat[i][m] = infty
            else:
                mat[i][m] = min(
                            P[i-1] + mat[i][m - S[i-1]] if m - S[i-1] >= 0 else infty,
                            mat[i-1][m] if i >= 1  else infty)
    return mat[len(S)][M]
#5
def DynamiqueP(S, M, D, P):
    mat=[[0]*(M+1) for _ in range(len(S)+1)]
    for i in range(len(S)+1):
        for m in range(M+1):
            if m == 0:
                mat[i][m] = 0
            elif i==0:
                mat[i][m] = infty
            else:
                ma=[infty,mat[i-1][m]]
                for k in range(1, len(S)+1):
                    if D[i-1]>=k and m - k*S[i-1] >= 0:
                        ma.append(k*P[i-1] + mat[i-1][m - k*S[i-1]])
                mat[i][m]=min(ma)
    return mat[len(S)][M]
#6
def Poids_Gloutonne(S, P, M):
    L = []
    for i in range(len(S)):
        L.append((P[i]/S[i],S[i],P[i]))
    L.sort()
    Mp = M
    res = 0
    while Mp > 0:
        for (r,s,p) in L:
            if s <=Mp:
                res += p*(Mp//s)
                Mp = Mp%s
    return res
    
if __name__ == "__main__":
    S=[1, 2, 5, 10, 20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
    Sd=[1,3,4,7]
    Pd=[10, 27, 32, 55]
    D=[10]*13
    P=[2.3,3.06,3.92,4.1,5.74,7.8,7.5,8.5,0.6,0.7,0.8,0.9,1]

    # Pour 3.6
    for M in range(1,21): 
        if DynamiqueP(Sd,M,D,Pd) != Poids_Gloutonne(Sd, Pd, M):
            print(M, DynamiqueP(Sd,M,D,Pd),Poids_Gloutonne(Sd, Pd, M))