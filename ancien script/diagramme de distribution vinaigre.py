import numpy as np #importation des bibiolthèques
import matplotlib.pyplot as plt

def pA(pH,pKa):
    return 1/(1+10**(pH-pKa)) #pourcentage de l'acide en fonction du pH
pH = np.linspace(0,14,100)
pKa=4.6 #Valeur du pKa à entrer

plt.plot(pH,pA(pH,pKa),label='CH3COOH') #Tracé de la courbe de % d'acide
plt.plot(pH,1-pA(pH,pKa),label='CH3COO-') #Tracé de la courbe de % de base
plt.grid(True) #Affichage du quadrillage
plt.xlabel('pH') #Titre de l'axe des abscisses
plt.ylabel("proportions") #Titre de l'axe des ordonnées
plt.legend() #Édition de la légende
plt.show() #Indispensable pour afficher la courbe