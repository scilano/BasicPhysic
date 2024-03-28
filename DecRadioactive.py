import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi

#On définit 2 fonctions qui représentent les équations différentielles du polonium et du bismuth, telle que NAtome' = F(NAtome,t) avec NAtome le nombre d'atomes de polonium ou de bismuth
def evolution_bismuth(NBismuth, lambdaBismuth):
    return -lambdaBismuth*NBismuth

def evolution_polonium(NBismuth, NPolonium, lambdaBismuth, lambdaPolonium):
    return -lambdaPolonium*NPolonium + lambdaBismuth*NBismuth


#On définit une fonction qui représente le système d'équations différentielles, telle que N' = F(N,t), où N = [NPolonium, NBismuth] à l'instant t et F est une fonction qui renvoie un vecteur de taille 2,
# avec les dérivées de NPolonium, NBismuth
#le paramètre t est important pour que la fonction solve_ivp puisse résoudre le système d'équations différentielles, même si il intervient pas dans les équations
def evolution_systeme(t, N, lambdaPolonium, lambdaBismuth):
    return np.array([evolution_polonium(N[1], N[0], lambdaBismuth, lambdaPolonium), evolution_bismuth(N[1], lambdaBismuth)])
   


t0 = 0    #VALEUR A RENTRER - temps intitial
tf = 600    #VALEUR A RENTRER - temps final
n = 1200    #VALEUR A RENTRER - nombre de pas de temps
tp = 138.4   #VALEUR A RENTRER - temps de demi-vie polonium
N0Bi = 10**6  #VALEUR A REMPLACER - nombre d'atomes de bismuth initialement
tbi = 5.01  #VALEUR A RENTRER - temps de demi-vie du bismuth
N0Po = 0   #VALEUR A REMPLACER - nombre d'atomes de polonium initialement
N0Pb = 0   #VALEUR A REMPLACER - nombre d'atomes de plomb initialement

N0 = np.array([N0Po, N0Bi]) #vecteur contenant les conditions initiales

lambdaPolonium = np.log(2)/tp
lambdaBismuth = np.log(2)/tbi


#Comme on est pas des colossals mongoles, on va utliser scypy pour résoudre le système d'équations différentielles au lieu de le programmer à la main
#Les arguments de la fonction solve_ivp sont les suivants:
#- la fonction qui représente le système d'équations différentielles
#- l'intervalle de temps sur lequel on veut résoudre le système
#- les conditions initiales
#- t_eval est un argument optionnel qui permet de spécifier les temps où on veut connaître la solution

#Comme certains PC sont géré spar des abrutis infoutus de faire une mise à jour, on définit une fonction qui prend en argument t et N et pas lambdaPolonium ni lambdaBismuth,
# et qui renvoie evolution_systeme(t,N,lambdaPolonium,lambdaBismuth),
def evolution_systeme_sans_parametres(t,N):
    return evolution_systeme(t,N,lambdaPolonium,lambdaBismuth)

sol = spi.solve_ivp(evolution_systeme_sans_parametres, [t0, tf], N0, t_eval=np.linspace(t0, tf, n))

N = sol.y #récupérer la solution, c'est un tableau taille 2*n
t = sol.t #récupérer les temps correspondants

NPolonium = N[0] #récupérer le nombre d'atomes de polonium
NBismuth = N[1] #récupérer le nombre d'atomes de bismuth
NPlomb = N0Bi - NBismuth -NPolonium #calculer le nombre d'atomes de plomb

# Tracer le graphique
plt.plot(t, NPolonium, label='Nombre d\'atomes de Polonium')
plt.plot(t, NBismuth, label='Nombre d\'atomes de Bismuth')
plt.plot(t, NPlomb, label='Nombre d\'atomes de Plomb')
plt.title('Evolution du nombre d\'atomes au cours du temps')
plt.xlabel('Temps (jours)')
plt.ylabel('Nombre d\'atomes')
plt.legend()
plt.show()
