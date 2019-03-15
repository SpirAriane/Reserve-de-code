# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 10:58:55 2019

@author: Spir4u
"""

#Question préliminaire

def shadok2dec(sh):
    if str(sh)==sh: #Cette contrainte ramène tout à l'état de liste, au cas où
        sh = [sh]
    i = 0
    res = 0
    for x in sh:    
        if x=='GA':
            res += 0*(4**i)
        elif x=='BU':
            res += 1*(4**i)
        elif x=='ZO':
            res += 2*(4**i)
        elif x=='MEU':
            res += 3*(4**i)
        else:
            return False
        i += 1 #incrémentation de l'indice pour que la multiplication soit adaptée à la position du chiffre dans la liste
    
    return res
    

#Question 1

def add(sh1,sh2):
    #On s'assure que tout est sous forme de liste
    if str(sh1)==sh1:
        x = [sh1]
    else :
        x = [k for k in sh1]
    if str(sh2)==sh2:
        y = [sh2]
    else :
        y = [k for k in sh2]
    
    addition = {('GA', 'GA') :	(False,'GA'),
            	('GA','BU') : 	(False,'BU'),	('BU', 'GA') : (False,'BU'),
            	('GA', 'ZO') : 	(False, 'ZO'),	('ZO', 'GA') : (False, 'ZO'),
            	('GA', 'MEU') : 	(False, 'MEU'),	('MEU',  'GA') : (False,'MEU'),
            	('BU','BU') : 	(False,'ZO'),
            	('BU', 'ZO') : 	(False, 'MEU'),	('ZO', 'BU') : (False,'MEU'),
            	('BU', 'MEU') : 	(True, 'GA'),	('MEU','BU') : (True,'GA'),
            	('ZO',  'ZO') : 	(True, 'GA'),
            	('ZO', 'MEU') : 	(True, 'BU'),	('MEU',  'ZO') : (True, 'BU'),
            	('MEU',  'MEU') : 	(True, 'ZO')}
    
    resultat = []
    retenue = False
    while len(x)!=0 and len(y)!=0: #Tant qu'il reste des chiffres à calculer
        
        if len(x)==0: #Dans le cas où y est "plus long" que x
            x1='GA'
        else:
            x1 = x.pop(0)
        
        if len(y)==0: #Dans le cas où x est "plus long" que y
            y1='GA'
        else:
            y1 = y.pop(0)
        
        
        (r1, z1) = addition(x1,y1) #On commence par additionner les chiffres récupérés
        if retenue == True: #Si on a une retenue, on ajoute 1 au résultat
            (r2, z1) = addition(z1,'BU')
        
        if r1+r2 == 0: #Si aucun des deux calculs d'amène une retenue
            retenue = False
        else: #Si une retenue apparait, elle est forcément de 1, pas de 2 (car au pire (3+3+1)//4 = 1)
            retenue = True
        
        resultat.append(z1)
        #On ajoute ce qu'on a obtenu et on refait la boucle pour les chiffres suivants
    
    return resultat
    
    

#Question 2

def mult(sh1,sh2):
    #On s'assure que tout est sous forme de liste
    if str(sh1)==sh1:
        x = [sh1]
    else :
        x = [k for k in sh1]
    if str(sh2)==sh2:
        y = [sh2]
    else :
        y = [k for k in sh2]
    
    multiplication = {('GA', 'GA'): 	('GA',),
                      ('GA', 'BU'): 	('GA',), 	('BU', 'GA'): ('GA',),
                      ('GA', 'ZO'): 	('GA',), 	('ZO', 'GA'): ('GA',),
                      ('GA', 'MEU'): ('GA',), 	('MEU', 'GA'): ('GA',),
                      ('BU', 'BU'): 	('BU',),
                      ('BU', 'ZO'): 	('ZO',), 	('ZO', 'BU'): ('ZO',),
                      ('BU', 'MEU'): 	('MEU',),    ('MEU', 'BU'): ('MEU',),
                      ('ZO', 'ZO'): 	('GA', 'BU'),
                      ('ZO', 'MEU'): 	('ZO', 'BU'), 	('MEU', 'ZO'): ('ZO', 'BU'),
                      ('MEU', 'MEU'): 	('BU', 'ZO')}
    
    
    resultat = ['GA']
    i = 0 #incrément indiquant à quelle "dizaine/niveau" de x on en est
    while len(x)!=0 : #Tant qu'il reste des chiffres à calculer
        
        z = ['GA']*i #les 'GA' sont dû à l'avancement du calcul dans les dizaines
        x1 = x.pop(0)
        for yk in y:
            zk = list(multiplication[x1,yk])
            z += zk
        resultat = add(resultat,z) #On ajoute ce qu'on obtient à ce qu'on a déjà
        i += 1 #incrémentation car on passe à la dizaine supérieur
    
    return resultat

    

#Question 3

def moins(sh1,sh2): #On suppose que sh1 > sh2
    #On s'assure que tout est sous forme de liste
    if str(sh1)==sh1:
        x = [sh1]
    else :
        x = [k for k in sh1]
    if str(sh2)==sh2:
        y = [sh2]
    else :
        y = [k for k in sh2]
    
    soustraction = {('GA', 'GA'): 	(False, 'GA'),
                      ('GA', 'BU'): 	(True,'MEU'), 	('BU', 'GA'): (False, 'BU'),
                      ('GA', 'ZO'): 	(True, 'ZO'), 	('ZO', 'GA'): ('GA',),
                      ('GA', 'MEU'): (True, 'BU'), 	('MEU', 'GA'): ('GA',),
                      ('BU', 'BU'): 	(False, 'GA'),
                      ('BU', 'ZO'): 	(True, 'MEU',), 	('ZO', 'BU'): ('ZO',),
                      ('BU', 'MEU'): 	(True, 'ZO',),    ('MEU', 'BU'): ('MEU',),
                      ('ZO', 'ZO'): 	('GA', 'BU'),
                      ('ZO', 'MEU'): 	('ZO', 'BU'), 	('MEU', 'ZO'): ('ZO', 'BU'),
                      ('MEU', 'MEU'): 	('BU', 'ZO')}
    
    


def Karatsuba(sh1,sh2): 
    #je m'asure que tout est sous forme de liste
    if str(sh1)==sh1:
        x = [sh1]
    else :
        x = [k for k in sh1]
    if str(sh2)==sh2:
        y = [sh2]
    else :
        y = [k for k in sh2]
    
    #On va procéder par réccurence, en commençant par déterminer les termes "faibles" et en remontant
    #Cas final : l'un des termes n'a plus qu'un chiffre
    
    
    
    #Cas général : on considère sh = [terme 0] + [termes suivants]*4**1
    x1 = x.pop(0)
    y1 = y.pop(0)
    z0 = mult(x1,y1)
    z2 = Karatsuba(x2,y2)
    z1 = Karatsuba( add(x1,x), add(y1,y) )
    
    z1 = ['GA'] + z1
    z2 = ['GA','GA'] + z2
    z = add(z0,z1)
    resultat = add(z,z2)
    
    return resultat
    
    
    
    
    
    
    
    
    
    
    