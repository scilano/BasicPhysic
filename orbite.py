import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button




#Paramètres d'affichage du graphique Ep=f(x)
ylim1=-800
ylim2=1000

#Paramètres généraux
m = 1800 #kg masse de l'astrer en rotation
C = 100 #m2/s constante des aires
K=150000 #Constante K
r = np.arange(0.1, 10000, 1)
Em0=0.1
Em=-13

t0, t1, n = 0, 200, 5000

t=np.linspace(t0,t1,n) #axe des temps



#Force centrale attractive :
def signal(r, K):
    return -K/r

def signal2(r, m):
    return 0.5*m*(C**2)/(r**2)

def signal3(r, m, K):
    return 0.5*m*(C**2)/(r**2)-K/r

def derivee_signal3(r,m,K) :
    return -m*(C**2)/(r**3)+K/(r**2)

#Détermination énergie minimale

def dichotomie(f,a,b,e):
    delta = 1
    while delta > e:
        m = (a + b) / 2
        delta = abs(b - a)
        if f(m) == 0:
            return m
        elif f(a) * f(m)  > 0:
            a = m
        else:
            b = m
    return a, b
func = lambda r: -m*(C**2)/(r**3)+K/(r**2)

a,b = dichotomie(lambda r: -m*(C**2)/(r**3)+K/(r**2), 0.1, 400, 0.001)
minimum=(a+b)/2

def Emecanique(Em) :
    return Em*np.ones(len(r))

#Détermination des intersections
def intersection(Em,K,m) :
    r1 = []
    delta = (K**2)+2*Em*(C**2)*m
    if delta == 0 :
        r1.append(-K/(2*Em))
        return minimum
    else :
        r1.append(-K/(2*Em)-(np.sqrt(delta)/(2*Em)))
        r1.append(-K/(2*Em)+(np.sqrt(delta)/(2*Em)))
        #print(r1)
        return r1

def coordonneesx1(Em,K,m) :
    r=intersection(Em, K, m)
    x1=[]
    x1.append(r[0])
    x1.append(r[0])
    return x1

def coordonneesy1(Em,K,m) :
    r=intersection(Em, K, m)
    x1=[0]
    x1.append(0.5*m*(C**2)/(r[0]**2)-K/r[0])
    return x1

def coordonneesx2(Em,K,m) :
    r=intersection(Em, K, m)
    x2=[]
    x2.append(r[1])
    x2.append(r[1])
    return x2

def coordonneesy2(Em,K,m) :
    r=intersection(Em, K, m)
    x2=[0]
    x2.append(0.5*m*(C**2)/(r[1]**2)-K/r[1])
    return x2

def etiquette(Em,K,m) :
    r=intersection(Em, K, m)
    plt.text(r[0], 1, "$r_1$")
    plt.text(r[1], 1, "$r_1$")


fig, ax = plt.subplots(1,2)
lines, = ax[0].plot(r, signal(r,K), label=r"$-\frac{K}{r}$")
lines2, = ax[0].plot(r, signal2(r,m), label=r"$-\frac{1}{2}m\frac{C^2}{r^2}$")
lines4, = ax[0].plot(r, signal3(r, m, K), label=r"$-\frac{1}{2}m\frac{C^2}{r^2}-\frac{K}{r}$")
lines3, = ax[0].plot(r,Emecanique(Em), label='Em')
coordo1, = ax[0].plot(coordonneesx1(Em,K,m),coordonneesy1(Em,K,m), '--')
coordo2, = ax[0].plot(coordonneesx2(Em,K,m),coordonneesy2(Em,K,m), '--')


ax[0].set_ylim(ylim1, ylim2)

ax[0].set_xlim(0, 1000)
ax[0].legend()
ax[0].set_xticks([]) #effacer les graduations
ax[0].set_yticks([])
axfreq = plt.axes([0.25, 0.10, 0.65, 0.03])

ax[0].spines["bottom"].set_position(("data",0)) # pour avoir l'axe des abscisses en zéro
ax[0].set_ylabel("Énergie")
ax[0].set_xlabel("Distance")
ax[0].set_title('Énergie potentielle en fonction de la distance')
plt.subplots_adjust(bottom=0.25)

# Tracé des trajectoires


def F_vec(Vec, t):
    theta, r, rp = Vec
    return np.array([1/r**2, rp, 1/r**3-1/r**2])

def alpha(Em,Em0):
    return(Em/Em0)

def trajectoire(alpha, t) :
    if alpha==0 :
        CI = np.array([0,0.5,0])
    else :
        CI = np.array([0,(-1+np.sqrt(1+alpha))/alpha,0])
    Sol = odeint(F_vec,CI,t)
    theta= Sol[:,0]
    r2 = Sol[:,1]
    x, y = r2*np.cos(theta), r2*np.sin(theta)
    return x,y



traj1, = ax[1].plot(trajectoire(alpha(Em,-signal3(minimum, m, K)), t)[0],trajectoire(alpha(Em,-signal3(minimum, m, K)), t)[1],'k')
traj2, = ax[1].plot(trajectoire(alpha(Em,-signal3(minimum, m, K)), t)[0],-trajectoire(alpha(Em,-signal3(minimum, m, K)), t)[1],'k')
ini = ax[1].plot(0,0, 'o', color='red')

ax[1].set_title('Trajectoire en fonction de l\'énergie mécanique du système')
ax[1].set_xticks([]) #effacer les graduations
ax[1].set_yticks([])

ax[1].set_xlim(-20, 10)
ax[1].set_ylim(-15, 15)

# Partie intéraction

sEm = Slider(axfreq, "Em", signal3(minimum, m, K), ylim2,valinit=Em0)


def update(val):
    lines3.set_ydata(Emecanique(sEm.val))
    coordo1.set_xdata(coordonneesx1(sEm.val,K,m))
    coordo1.set_ydata(coordonneesy1(sEm.val,K,m))
    coordo2.set_xdata(coordonneesx2(sEm.val,K,m))
    coordo2.set_ydata(coordonneesy2(sEm.val,K,m))
    traj1.set_xdata(trajectoire(alpha(sEm.val,-signal3(minimum, m, K)), t)[0])
    traj1.set_ydata(trajectoire(alpha(sEm.val,-signal3(minimum, m, K)), t)[1])
    traj2.set_xdata(trajectoire(alpha(sEm.val,-signal3(minimum, m, K)), t)[0])
    traj2.set_ydata(-trajectoire(alpha(sEm.val,-signal3(minimum, m, K)), t)[1])
    intersection(sEm.val, K, m)
    fig.canvas.draw_idle()

sEm.on_changed(update)

plt.show()