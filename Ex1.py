# -*- coding: utf-8 -*-

from math import cos, sin, pi, degrees, exp
from tkinter import Tk, Canvas, Button, Frame, Label, StringVar, LEFT, RIGHT, TOP, BOTTOM, NORMAL, DISABLED


#Constantes utiles
dt = 10 #Variation du temps
l = 100 #Longueur du fil
omega = (9.81/l)**2 #fréquence d'oscillation
Theta0 = 40*(2*pi/360) #Angle du fil initial
r = 5 #Rayon des boules
[x,y] = [100,20] #Position de la boule centrale
m = 100 #masse du poids
k = 1 #Coeff frottements visqeux
lambd = k*omega/(2*m*l)


#Variables globales changeant au fil du programme 
t = 0 #Variable de temps
Theta = Theta0 #Angle du fil au temps t
cpt = 1 #Compteur pour l'enregistrement d'image


""" Fonctions """

# Exercice 1 : Fonction d'étape
def DoStep(Canvas):
    global Theta
    global t
    global cpt
    t = t + dt
    Theta = Theta0 * cos(omega*t)
    
    Canvas.delete("all")
    x2 = x + l * sin(Theta)
    y2 = y + l * cos(Theta)
    Canvas.create_line(x, y, x2, y2, fill='black', width=3)
    Canvas.create_oval(x-r, y-r, x+r, y+r, fill = 'red', outline = 'black')
    Canvas.create_oval(x2-r, y2-r, x2+r, y2+r, fill = 'red', outline = 'black')
    
    Texte_Theta.set('Theta = %.2f' % degrees(Theta))
    Texte_t.set('t = ' + str(t))
    
    Canvas.postscript(file="filename_%04d.ps" % cpt, colormode='color')
    cpt += 1

# Exercice 2 :Fonctions d'enchaînement
RunActif = False

def DoIteration():
    if RunActif == True :
        DoStep(Image)
        fen.after(50, DoIteration)

def DoRun():
    global RunActif
    Run.config(state=DISABLED)
    Run_amorti.config(state=DISABLED)
    RunActif = True
    DoIteration()

def DoStop():
    global RunActif
    RunActif = False
    Run.config(state=NORMAL)

# Exercice 4 : Version pendule amorti

def DoRun_amorti():
    global RunActif
    Run.config(state=DISABLED)
    Run_amorti.config(state=DISABLED)
    RunActif = True
    DoIteration_amorti()

def DoIteration_amorti():
    if RunActif == True :
        DoStep_amorti(Image)
        fen.after(50, DoIteration)

def DoStep_amorti(Canvas):
    global Theta
    global t
    global cpt
    t = t + dt
    Theta = Theta0 * exp(-lambd*omega*t) * cos( ( (1-lambd)**0.5 )*omega*t )
    
    Canvas.delete("all")
    x2 = x + l * sin(Theta)
    y2 = y + l * cos(Theta)
    Canvas.create_line(x, y, x2, y2, fill='black', width=3)
    Canvas.create_oval(x-r, y-r, x+r, y+r, fill = 'red', outline = 'black')
    Canvas.create_oval(x2-r, y2-r, x2+r, y2+r, fill = 'red', outline = 'black')
    
    Texte_Theta.set('Theta = %.2f' % degrees(Theta))
    Texte_t.set('t = ' + str(t))
    
    Canvas.postscript(file="filename_%04d.ps" % cpt, colormode='color')
    cpt += 1

""" Affichage """

fen = Tk()


Image = Canvas(fen, width=200, height=150, bg='ivory')
Image.pack(side=TOP)

#Initialisation
Image.delete("all")
x2 = x + l * sin(Theta)
y2 = y + l * cos(Theta)
Image.create_line(x, y, x2, y2, fill='black', width=3)
Image.create_oval(x-r, y-r, x+r, y+r, fill = 'red', outline = 'black')
Image.create_oval(x2-r, y2-r, x2+r, y2+r, fill = 'red', outline = 'black')
#Fin initiation


#Infos variables sur thêta et t
infos = Frame(fen)
infos.pack(side=LEFT)

Texte_Theta = StringVar()
Info_Theta = Label(fen, textvariable = Texte_Theta)
Info_Theta.pack(in_=infos, side=BOTTOM)
Texte_Theta.set('Theta = %.2f' % degrees(Theta))

Texte_t = StringVar()
Info_t = Label(fen, textvariable = Texte_t)
Info_t.pack(in_=infos, side=TOP)
Texte_t.set('t = ' + str(t))


#Boutons
boutons = Frame(fen)
boutons.pack(side=RIGHT)

Quit = Button(fen, text='Quitter', command=fen.destroy)
Quit.pack(in_=boutons, side=BOTTOM, padx=3, pady=3)
    
Step = Button(fen, text='Step', command=lambda: DoStep(Image))
Step.pack(in_=boutons, side=TOP, padx=3, pady=3)

Stop = Button(fen, text='Stop', command=DoStop)
Stop.pack(in_=boutons, side=RIGHT, padx=3, pady=3)

Run = Button(fen, text='Run', command=DoRun)
Run.pack(in_=boutons, side=RIGHT, padx=3, pady=3)


Step_amorti = Button(fen, text='Step Amorti', command=lambda: DoStep_amorti(Image))
Step_amorti.pack(in_=boutons, side=TOP, padx=3, pady=3)

Run_amorti = Button(fen, text='Run Amorti', command=DoRun_amorti)
Run_amorti.pack(in_=boutons, side=RIGHT, padx=3, pady=3)



fen.mainloop()
fen.destroy()