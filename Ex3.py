# -*- coding: utf-8 -*-

from tkinter import *

#Récupération du code
nom = 'Smiley-256-couleurs.ppm'
ppm = open(nom, 'rb')
dataTotal = ppm.read()
ppm.close()

values = dataTotal.split(maxsplit=4)
codage = values[0]
l = int(values[1])
h = int(values[2])
cc = int(values[3])

#Ecriture du code

TexteCode = str( '%02X' % dataTotal[0])
for i in range(1000): #On peut remplacer 1000 par len(dataTotal) pour tout avoir
    TexteCode = TexteCode + ' ' + str( '%02X' % dataTotal[i])

TexteCodage = 'P6 ' + str(l) + ' ' + str(h) + ' ' + str(cc)


#Affichage

fen1 = Tk()

b1 = Button(fen1, text = 'Quitter', command = fen1.quit)
b1.pack(side=BOTTOM, padx = 3, pady = 3)

S = Scrollbar(fen1)
S.pack(side=RIGHT, fill=Y)

code = Text(fen1, font='Courier', height=20, width=48) #Pour accueillir le code général
code.pack(side=LEFT, fill=Y)

code2 = Text(fen1, font='Courier', height=20, width=15) #Pour accueillir le codage
code2.pack(side=LEFT, fill=Y)

S.config(command=code.yview)
code.config(yscrollcommand=S.set)

code.insert(END, TexteCode)
code2.insert(END, TexteCodage)


mainloop()
fen1.destroy()