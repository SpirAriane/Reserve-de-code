# -*- coding: utf-8 -*-

from PIL import Image, ImageTk, ImageFile
from tkinter import *
ImageFile.LOAD_TRUNCATED_IMAGES = True


# Récupération du code
nom = 'Smiley_gris.pgm'

pgm = open(nom, 'rb')
dataTotal = pgm.read()
pgm.close()


# Récupération des données
values = dataTotal.split(maxsplit=4)
codage = values[0]
l = int(values[1])
h = int(values[2])
cc = int(values[3])
data = values[4]


#Forgeage des outils
def get_pixel(i,j,image,largeur): #Extraction
    indice = largeur*j + i
    return image[indice]

def set_pixel(i,j,g,image): #Remplacement
    image[i][j] = bytes([g])


# Réécriture des données pour extraire les contours
pixels = [ [0]*h for i in range(l) ]

#Définition des couleurs des bords (la couleur par défaut est grise)
for kl in range(l):
    pixels[kl][0] = bytes([128])
    pixels[kl][h-1] = bytes([128])
for kh in range(h):
    pixels[0][kh] = bytes([128])
    pixels[l-1][kh] = bytes([128])

#Détermination des pixels centraux
for kl in range(1, l-1):
    for kh in range(1, h-1):
        VoisinsHautGauche = 2*get_pixel(kl-1,kh-1,data,l) + 2*get_pixel(kl,kh-1,data,l) + 2*get_pixel(kl-1,kh,data,l)
        VoisinsBasDroite = 2*get_pixel(kl+1,kh+1,data,l) + 2*get_pixel(kl,kh+1,data,l) + 2*get_pixel(kl+1,kh,data,l)
        NewValeur = 128 - VoisinsHautGauche + VoisinsBasDroite
        
        if NewValeur > 255 :
            NewValeur = 255
        elif NewValeur < 0 :
            NewValeur = 0
        #Inversion de la couleur
        set_pixel(kl,kh,NewValeur,pixels)
        


# Ecriture des nouvelles donnée dans une nouvelle image
pgm2 = open('Smiley_embossage.pgm','wb')
pgm2.write(('P5\n%s %s\n%s\n' % (l,h,cc)).encode('utf-8'))
for kh in range(h):
    for kl in range (l):
        pgm2.write(pixels[kl][kh])

pgm2.close()


# Affichage de l'image
fen1 = Tk()
b1=Button(fen1, text = 'Quitter', command = fen1.quit)
b1.pack(side=RIGHT, padx = 3, pady = 3)

photo = ImageTk.PhotoImage(file ='Smiley_embossage.pgm')
can1 = Canvas(fen1, width =photo.width(), height =photo.height())
can1.create_image(photo.width(), photo.height(), anchor = 'se', image = photo) #pour une obscure raison, "anchor='nw'" case l'image en bas à droite en la coupant, je fais donc sans
can1.pack()

fen1.mainloop()
fen1.destroy()