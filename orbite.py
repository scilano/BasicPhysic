import numpy as np
import matplotlib.pyplot as plt

G = 6.67430e-11
MTerre = 5.972e24
RTerre = 6.371e6   
#Données (choisies au hasard par un alcoolique notoire)
MSatelitte = 1
C = 3e15

#Energie potentielle effective
def Ep_eff(r):
    return -G*MTerre*MSatelitte/r + MSatelitte*C**2/(2*r**2)

R = np.logspace(6, 10, 1000)

rMin = C**2/(G*MTerre)
v1 = np.sqrt(G*MTerre/RTerre)

print(f"Première vitesse de libération: {v1} m/s")
print(f"Seconde vitesse de libération: {np.sqrt(2)*v1} m/s")
if rMin < RTerre:
    print(f"Le satellite est à l'intérieur de la Terre. rMin = {rMin:.2e} m")
elif rMin < R[0] or R[-1] < rMin:
    print(f"rMin n'appartiens pas à l'intervalle de R. rMin = {rMin:.2e} m, R = [{R[0]:.0e}, {R[-1]:.0e}] m")
#Plot d'un beau graphique
plt.axhline(y=0, color='black', linestyle='--')
plt.plot(R, Ep_eff(R), label = 'Ep_eff')
plt.plot([rMin, rMin], [Ep_eff(rMin), 0], label = 'rMin',linestyle = 'dotted',color='red')
plt.plot([RTerre, RTerre], [Ep_eff(RTerre), 0], label = 'RTerre',linestyle = 'dotted',color='green')
plt.legend()

plt.xlabel('r (m)')
plt.ylabel('Ep_eff (unité SI)')

plt.xscale('log')
plt.show()
    