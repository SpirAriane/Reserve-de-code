# -*- utf8 -*-

#!/usr/bin/env python
# -----------------------------------------------------------------------------
# Multi-layer perceptron
# Version d'origine:
# Copyright (C) 2011  Nicolas P. Rougier
#
# Distributed under the terms of the BSD License.
# Modifié par B. Lamiroy
# -----------------------------------------------------------------------------
# This is an implementation of the multi-layer perceptron with retropropagation
# learning.
# -----------------------------------------------------------------------------
import numpy as np

def sigmoid(x):
    ''' Nous utilisons la tangente hyperbolique ... parce qu'elle a une dérivée sympa '''
    return np.tanh(x)

def dsigmoid(x):
    ''' Dérivée de la tangente hyperbolique '''
    return 1.0-sigmoid(x)**2

class Perceptron:
    ''' Classe de perceptron multicouche '''

    # *args = nombre variable d'arguments (stockés dans une structure itérable)
    def __init__(self, *args):
        ''' Initialization du perceptron avec tailles fournies.  '''

        # les arguments définissent le nombre de neurones par couche
        self.forme = args
        
        # n = nombre de couches
        n = len(args)

        # Construction des couches
        self.couches = []
        # La magie des perceptrons : on rajoute un noeud "biais" supplémentaire
        # pour garantir la convergence. 
        self.couches.append(np.ones(self.forme[0]+1))
        # Ensuite on construit les couches intermédiaires et finale
        for i in range(1,n):
            self.couches.append(np.ones(self.forme[i]))

        # Construction des matrices de poids (intialement mis à zéro)
        self.poids = []
        for i in range(n-1):
            self.poids.append(np.zeros((self.couches[i].size,
                                         self.couches[i+1].size)))

        # deltapoids  will hold last change in poids (for inertie)
        '''Mon deltapoids va avoir une forme plus détaillée pour faciliter le gradient amorti '''
        self.deltapoids = []
        for k in range(len(self.poids)):
            self.deltapoids += [np.zeros(np.shape(Test.poids[k]))]

        # Reset matrices poids à des valeurs aléatoires
        self.reset()

    def reset(self):
        ''' Reset poids '''

        for i in range(len(self.poids)):
            Z = np.random.random((self.couches[i].size,self.couches[i+1].size))
            self.poids[i][...] = (2*Z-1)*0.25

    def propagation(self, data):
        ''' Propagation des données "data" depuis la couche d'entrée à la sortie. '''

        # Affectation des données à la couche d'entrée (sauf noeud "biais")
        self.couches[0][0:-1] = data

        # Propagation de la couche 0 à la couche n-1 utilisant la fonction d'activtion
        for i in range(1,len(self.forme)):
            self.couches[i][...] = sigmoid(np.dot(self.couches[i-1],self.poids[i-1]))
            #test fonction identité : self.couches[i][...] = np.dot(self.couches[i-1],self.poids[i-1])

        # Retourne le résultat
        return self.couches[-1]


    def retropropagation(self, target, vitesse=0.1, inertie=0.1):

        # Calcul de l'erreur au niveau de la couche de sortie
        error = target - self.couches[-1]
        delta = error*dsigmoid(self.couches[-1])
        
        # Calcul de l'erreur au niveau des couches intermédiaires
        List_errors = [delta] #à chaque itération, la liste d'erreur de la nouvelle couche sera placée au début
        N = len(self.forme)
        for k in range(2,N+1): #On va parcourir la liste à l'envers avec des -k
            ErrorsNextLayer = List_errors[0]
            ErrorsThisLayer = [0]*self.forme(-k)
            for n in range(len(ErrorsThisLayer)):
                somme = np.dot(Test.poids[-k+1],ErrorsNextLayer)[n]
                delta_n = dsigmoid(self.couches[-k][n])*somme
                ErrorsThisLayer[n] = delta_n
            List_errors = [ErrorsThisLayer] + List_errors
        
        List_errors = np.array(List_errors)    
        
        # Mise à jour des poids
        
        ''' Descente du gradient simple '''
        '''
        new_poids = self.poids
        for k in range(N-1): #Car N-1 matrices de poids
            for i in range(len(self.couche(k))):
                for j in range(len(self.couche(k+1))):
                    gradient_ij = self.couche[k][i]*List_errors[k+1][j]
                    correction_ij = vitesse * gradient_ij + self.poids[k][i][j]
                    new_poids[k][i][j] = correction_ij
        self.poids = new_poids
        '''
        
        ''' Descente du gradient amorti '''
        new_poids = self.poids
        for k in range(N-1): #Car N-1 matrices de poids
            for i in range(len(self.couche(k))):
                for j in range(len(self.couche(k+1))):
                    gradient_ij = self.couche[k][i]*List_errors[k+1][j]
                    correction_ij = vitesse * gradient_ij + inertie * self.deltapoids[k][i][j] + self.poids[k][i][j]
                    self.deltapoids[k][i][j] = gradient_ij
                    new_poids[k][i][j] = correction_ij
        self.poids = new_poids
            
        # Renvoi de l'erreur observé
        return (error**2).sum()


#Test

Test = Perceptron(2,5,1)
print(Test.propagation([0,0]))
print(Test.couches)
print(Test.poids)