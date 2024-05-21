import numpy as np # importation du module de calcul numpy
import matplotlib.pyplot as plt# importation du module de de tracé
from matplotlib.widgets import Slider, Button #outils pour faire des curseurs

phi=0
T=1 # initialisation de la période
Y1max=2 # initialisation de la valeur maximale du premier signal
Y2max=2

t=[i/100 for i in range(400)] # génération d'une liste de 400 valeurs comprises entre 0 et 4

def f1(t, Y1max, T):
    y1=[]
    for i in t :
        y1.append(Y1max*np.cos(2*np.pi*i/T))
    return y1

def f2(t, Y2max, T, phi):
    y2=[]
    for i in t :
        y2.append(Y2max*np.cos(2*np.pi*i/T+phi))
    return y2

def f(t, Y1max, Y2max, T, phi):
    y=[]
    for i in t :
        y.append(Y1max*np.cos(2*np.pi*i/T)+Y2max*np.cos(2*np.pi*i/T+phi))
    return y

fig, ax = plt.subplots()
lines1,=plt.plot(t,f1(t, Y1max, T),label='premier signal sinusoidal') # génération du tracé de cos(2*pi*t/T) et définition de la légende cos(2*pi*t/T)
lines2,=plt.plot(t,f2(t, Y1max, T, phi),label='deuxi me signal sinusoidal')
lines,=plt.plot(t,f(t, Y1max, Y2max, T, phi),label='somme des deux signaux ')
axphi = plt.axes([0.25, 0.10, 0.65, 0.03])

plt.legend()
ax.set_xlabel("Temps (s)")
ax.set_ylabel("Amplitude (V)")

# Ajuste le graphique pour faire de la place pour le curseur
plt.subplots_adjust(left=0.25, bottom=0.25)

phi = Slider(axphi, label="déphasage", valmin=0, valmax=3*np.pi,valstep=0.01,valinit=0)



def update(val):
    lines2.set_ydata(f2(t, Y1max, T, phi.val))
    lines.set_ydata(f(t, Y1max, Y2max, T, phi.val))

phi.on_changed(update)


plt.show() # affichage de la figure