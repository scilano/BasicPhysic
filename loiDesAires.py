import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi
from matplotlib.patches import Circle
from scipy.interpolate import CubicSpline
import matplotlib.colors

#Fonctions utiles:
def r(a,e,th):
    return a*(1-e**2)/(1+e*np.cos(th))

#Calcul les points de l'orbite pour les paramètres a et e
def orbit(a,e):
    theta = np.linspace(0,2*np.pi)
    T = np.zeros_like(theta)
    R = r(a,e,theta)
    for i,th in enumerate(theta):
        T[i] = MSatellite/L*spi.quad(lambda alpha:r(a,e,alpha)**2,0,th)[0]
    return R,theta,T


def demiGrandaxe(T,G,M):
    return (T**2*G*M/(4*np.pi**2))**(1/3)

#Paramètres
G = 6.67430e-11
MTerre = 5.972e24
MSatellite = 1
RTerre = 6.371e6
periode = 3600*24*10

th1 = 0.1 #Angle de la première aire (en rad)
th3 = np.pi*1.1 #Angle de la seconde aire (en rad)
inter = 0.10*periode #Longeure de l'aire (en s)
e = 0.7

a = demiGrandaxe(periode,G,MTerre)
b = a*np.sqrt(1-e**2)
L = np.sqrt(G*MTerre*MSatellite**2*(a*(1-e**2)))


R,Theta,T = orbit(a,e)

#interpole les fonctions à partir des points précédents
fradius = CubicSpline(T,R)
fradius_theta = CubicSpline(Theta,R,extrapolate="periodic")
fangle = CubicSpline(T,Theta)
ftemps = CubicSpline(Theta,T,extrapolate="periodic")
angle = np.linspace(0,np.pi*2,10000)

#Défini les zones des aires
th2 = fangle(ftemps(th1)+inter)
th4 = fangle(ftemps(th3)+inter)
t1 = ftemps(th1)
t2 = ftemps(th2)
t3 = ftemps(th3)
t4 = ftemps(th4)

mask1 = th1 < angle
mask2 = th2 > angle 
mask3 = th3 < angle
mask4 = th4 > angle
mask = mask1*mask2 + mask3*mask4


#Calcul les aires
A1 = spi.quad(lambda th: 1/2*fradius_theta(th)**2,th1,th2)[0]
A2 = spi.quad(lambda th: 1/2*fradius_theta(th)**2,th3,th4)[0]


#Fait un beau plot
fig,ax = plt.subplots()

cmap = cmap = matplotlib.colors.ListedColormap(['blue', 'red'])
X = fradius_theta(angle)*np.cos(angle)
Y = fradius_theta(angle)*np.sin(angle)
ax.scatter(X,Y,s=0.2,c=mask,cmap=cmap)
ax.plot((0,fradius_theta(th1)*np.cos(th1)),(0,fradius_theta(th1)*np.sin(th1)),c='red',ls='--')
ax.plot((0,fradius_theta(th2)*np.cos(th2)),(0,fradius_theta(th2)*np.sin(th2)),c='red',ls='--')
ax.plot((0,fradius_theta(th3)*np.cos(th3)),(0,fradius_theta(th3)*np.sin(th3)),c='red',ls='--')
ax.plot((0,fradius_theta(th4)*np.cos(th4)),(0,fradius_theta(th4)*np.sin(th4)),c='red',ls='--')
ax.plot((-a*(1+e),a*(1-e)),(0,0),c='black',ls='-')
ax.plot((-a*e,-a*e),(-b,b),c='black',ls='-')
ax.add_artist(Circle((0,0),RTerre,color='brown'))
ax.scatter(-a*e,0)

xdata1 = fradius_theta((th1+th2)/2)*np.cos((th1+th2)/2)/2
ydata1 = fradius_theta((th1+th2)/2)*np.sin((th1+th2)/2)/2

xdata2 = fradius_theta((th3+th4)/2)*np.cos((th3+th4)/2)/2
ydata2 = fradius_theta((th3+th4)/2)*np.sin((th3+th4)/2)/2

ax.text(xdata1,ydata1,"A1",transform=ax.transData,fontsize=20)
ax.text(xdata2,ydata2,"A2",transform=ax.transData,fontsize=20)
ax.text(xdata2*2,ydata1,f"A1/A2 = {A1/A2:.4f}",fontsize=20)



ax.axis("equal")
plt.show()
