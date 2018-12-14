# -*- coding: utf-8 -*-
"""
Created on Thu Dec 13 17:33:06 2018

@author: spir4u
"""

from tkinter import Tk, Canvas, Button, BOTTOM, RIGHT
from random import randrange

colors = ['red','blue','yellow','white','black']

def PopCercle(Canvas):
    global ListeCercles
    NbColor = randrange(0,5)
    Couleur = colors[NbColor]
    Rayon = randrange(10,50)
    Pos = randrange(Rayon,400-Rayon) #Pour éviter un débordement
    Canvas.create_oval(Pos-Rayon, 2*Rayon, Pos+Rayon, 0, fill = Couleur, outline = 'black')
    ListeCercles.append( [ [Pos, 0], Rayon, Couleur ] )
    

def MoveCercle(l, bottom, Canvas): #l = [Position du centre, rayon, couleur], bottom = coordonnés du "sol", compte tenu des cercles déjà arrivés
    [ [PosxCentre, PosyHaut], Rayon, Couleur ] = l
    Canvas.create_oval(PosxCentre-Rayon-1, PosyHaut + 2*Rayon + 1, PosxCentre+Rayon+1, PosyHaut - 1, fill = 'ivory', outline = 'ivory')
    Canvas.create_oval(PosxCentre-Rayon, PosyHaut + 2*Rayon + Vitesse, PosxCentre+Rayon, PosyHaut + Vitesse, fill = l[2], outline = 'black')
    l[0] = [l[0][0], l[0][1]+Vitesse]
    
    
    
    
def NextStep():
    #Détermination de l'apparition d'un nouveau cercle
    global Compteur
    if Compteur == 3:
        PopCercle(Can)
        Compteur = 1
    else :
        Compteur += 1
    
    #Déplacement des cercles
    for l in ListeCercles:
        MoveCercle(l, Bottom, Can)
    
    #Détermination des collisions/arrêt des cercles
    n = len(ListeCercles)
    ListeArrivee = []
    for k in range(n): #Etude de chaque cercle par son numéro
        C1 = ListeCercles(k)
        
        if C1[0][1] + 2*C1[1] >= 400: #Si le cercle touche le fond, PosyHaut+2*Rayon dépasse ou pas 400
            ListeArrivee.append(k) #Si oui on note le numéro du cercle
        
        else : #On cherche si le cercle en touche un autre
            for C2 in CerclesArrives : #Liste des cercles arrêtés
                Distance = (C2[0][0] - C1[0][0])**2 + (C2[0][1] + C2[1] - C1[0][1] - C1[1])**2 #Distance entre les centres
                if Distance <= C2[1]+C1[1]: #Si cette distance est inférieure à celle des rayons, superposition
                    ListeArrivee.append(k)
    
    print(ListeArrivee) #Pour voir pourquoi ça ne marche pas
    
    #Passage des cercles arrivés dans une autre liste
    while len(ListeArrivee) != 0:
        k = ListeArrivee.pop()
        C = ListeCercles.pop(k)
        CerclesArrives.append(C)
                    
    

ListeCercles = []
CerclesArrives = []
Vitesse = 30 #Vitesse de chute, dans [1,50]
 

fen = Tk()

Can = Canvas(fen, width=400, height=400, bg='ivory')
Can.pack()

#Création du premier cercle
NbColor = randrange(0,5)
Couleur = colors[NbColor]
Rayon = randrange(10,50)
Pos = randrange(Rayon,400-Rayon) #Pour éviter un débordement
Can.create_oval(Pos-Rayon, 2*Rayon, Pos+Rayon, 0, fill = Couleur, outline = 'black')
ListeCercles.append( [ [Pos, 0], Rayon, Couleur ] )

Quit = Button(fen, text='Quitter', command=fen.destroy)
Quit.pack(side=BOTTOM, padx=3, pady=3)

Compteur = 1

Bottom = [500]*500 # "sol" initial

Next = Button(fen, text='Next Step', command=NextStep)
Next.pack(side=RIGHT, padx=3, pady=3)


fen.mainloop()
fen.destroy()