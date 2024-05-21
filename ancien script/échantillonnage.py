import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button #outils pour faire des curseurs

# Signal
f = 2.
def signal(t):
    return np.sin(2. * np.pi *f * t )
# Echantillonnage
D = 2. # Duree d'observation
fe = 4. # Frequence d'echantillonnage
N = int(D * fe) + 1 # Nombre de points enregistres
te1=[]# Grille d'echantillonnage
te2=[]
for i in range(N):
    te1+=[1/fe*i,1/fe*i] #pour l'ordonnée
    te2+=[1/fe*i,1/fe*(i+1)] #pour l'abscisse.
tp = np.linspace(0., D, 1000) # Grille plus fine pour tracer l'allure du signal parfait
# Trace du signal
fig,ax=plt.subplots()
plot,=plt.plot(te2, signal(np.array(te1)), 'or-', label = u"Signal échantillonné")
plt.plot(tp, signal(tp), 'b--', label = u"Signal réel")
plt.grid()
plt.xlabel("Temps $t$",fontsize=15)
plt.ylabel("Amplitude $x(t)$",fontsize=15)
plt.legend()
plt.show()

# Ajuste le graphique pour faire de la place pour les curseurs
plt.subplots_adjust(bottom=0.25)

#Création du curseur

axfreq = plt.axes(([0.25, 0.15, 0.65, 0.03]))
freq_slider = Slider(
    ax=axfreq,
    label='Fréquence d\'échantillonage',
    valmin=1,
    valmax=50,
    valinit=4)

freq_slider.label.set_size(15)

# Fonction appelée dès que la valeur de F change
def update(val):
    N = int(D * freq_slider.val) + 1
    te1=[]# Grille d'echantillonnage
    te2=[]
    for i in range(N):
        te1+=[1/freq_slider.val*i,1/freq_slider.val*i] #pour l'ordonnée
        te2+=[1/freq_slider.val*i,1/freq_slider.val*(i+1)] #pour l'abscisse.
    plot.set_data(te1, signal(np.array(te2)))

freq_slider.on_changed(update)