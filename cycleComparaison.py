import matplotlib.axes
import matplotlib.axis
import numpy as np
import matplotlib.pyplot as plt
import matplotlib


class Cycle:
   
    def __init__(self,name:str,nSteps:int,legend:dict=None):
        self.name = name
        if nSteps!=len(legend):
            raise ValueError("The number of steps is wrong")
        self.nSteps = nSteps
        if not (legend is None):
            self.legend = legend
        self.axes = None

        
    def addToFig(self,figure:matplotlib.figure.Figure,axis:matplotlib.axes.Axes,marker:str='-'):
        d_legend={0:"upper right",1:"center right",2:"lower right"}
        l = []
        for i in range(self.nSteps):
            v = self.axes[i,0]
            p = self.axes[i,1]
            N = len(p)//2
            nl, = axis.plot(v,p,label=self.legend[i],linestyle=marker)
            axis.annotate("",xy=(v[N],p[N]),arrowprops=dict(arrowstyle="->"))
            #axis.arrow(v[N],p[N],v[N+10]-v[N],p[N+10]-p[N],shape='full', lw=0, length_includes_head=True, head_width=0.01,head_length=0.05)
            l.append(nl)
        
        leg = axis.legend(handles=l,loc=d_legend[len(axis.artists)],title = self.name)
        axis.add_artist(leg)
        return 0



# Carnot Cycle
def carnot(p_min,p_max,v_max,r,gma=1.4):
    '''Carnot cycle
    The arguments are as follows:
    p_min: minimum pressure (Pa)
    p_max: Maximum pressure (Pa)
    v_max: Maximum volume (m3)
    r: compression ratio
    gma: Adiabatic exponent O2 at 20°C:1.400 '''
    leg = {0:"Isotherme réversible",1:"Adiabatique réversible",2:"Isotherme réversible",3:"Adiabatique réversible"}
    if p_max/p_min < r:
        raise ValueError("p_max/p_min < r, you fucking idiot! What do you think? If you divide a volume by two, the pression will at minimum be multiplied by two.\nReduce r or increase p_max")
    carnotCycle = Cycle("Carnot",4,leg)
    n = 100
    carnotCycle.axes = np.zeros((4,2,n))
    p1=p_min
    v1=v_max
    v2=v_max/r
    c1=p1*v1

    # Process 1-2
    v=np.linspace(v2,v1,n)
    carnotCycle.axes[0] = np.flip(v),np.flip(c1/v)


    # Process 2-3
    p3=p_max
    c2=c1*v2**(gma-1.)
    v3=(c2/p3)**(1/gma)
    v=np.linspace(v3,v2,n)
    carnotCycle.axes[1] = np.flip(v),np.flip(c2/v**gma)

    # Process 3-4
    c3=p3*v3
    c4=p1*v1**gma
    v4=(c4/c3)**(1/(gma-1.))
    v=np.linspace(v3,v4,n)
    carnotCycle.axes[2]= v,c3/v


    # Process 4-1
    v=np.linspace(v4,v1,n)
    carnotCycle.axes[3]= v,c4/v**gma
    return carnotCycle


def otto(p_min,p_max,v_max,r,gma=1.4):
    '''Otto cycle
    The arguments are as follows:
    p_min: minimum pressure (Pa)
    p_max: Maximum pressure (Pa)
    v_max: Maximum volume (m3)
    r: compression ratio
    gma: Adiabatic exponent O2 at 20°C:1.400 '''
    if p_max/p_min < r:
        raise ValueError("p_max/p_min < r, you fucking idiot! You pression will increase because of the compression AND the rise in temperature. Reduce r or increase p_max")

    leg = {0:"Admission d'air",1:"Compression adiabatique",2:"Combustion",3:"Décompression adiabatique",4:"Refroidissement",5:"Echappement des gaz"}
    ottoCycle = Cycle("Otto",6,leg)
    n=100
    ottoCycle.axes = np.zeros((6,2,n))

    #Admission d'air
    v_min = v_max/r
    V0 = np.linspace(v_min,v_max,n)
    P0 = np.ones_like(V0)*p_min
    ottoCycle.axes[0] = V0,P0

    #Compression adiabatique
    c1 = p_min*v_max**gma
    V1 = np.linspace(v_min,v_max,n)
    P1 = c1/V1**gma
    ottoCycle.axes[1] = np.flip(V1),np.flip(P1)

    #Combustion:
    P2 = np.linspace(P1[0],p_max,n)
    V2 = np.ones_like(P2)*v_min
    ottoCycle.axes[2] = V2,P2

    #Décompression
    c3 = p_max*v_min**gma
    V3 = np.copy(V1)
    P3 = c3/V3**gma
    ottoCycle.axes[3] = V3,P3

    #Refroidissement
    P4 = np.linspace(P3[-1],p_min,n)
    V4 = np.ones_like(P4)*v_max
    ottoCycle.axes[4] = np.flip(V4),np.flip(P4)

    #Echappement
    V5 = np.copy(V1)
    P5 = np.ones_like(V5)*p_min
    ottoCycle.axes[5] = np.flip(V5),np.flip(P5)

    return ottoCycle



    
    





fig,ax = plt.subplots()
carnotCycle = carnot(2*10**5,8*10**5,0.5,2,1.4)
carnotCycle.addToFig(fig,ax,'-')

ottoCycle = otto(2*10**5,8*10**5,0.5,2,1.4)
ottoCycle.addToFig(fig,ax,'--')


fig.show()
input()