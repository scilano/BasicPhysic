import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.patches import Circle
from matplotlib.widgets import Button

#Compute the electric field of a charge q at position r0 = (x0, y0) at the point (x, y)
def E(q, r0, x, y):

    r = np.hypot(x-r0[0], y-r0[1])**3
    return q * (x - r0[0]) / r, q * (y - r0[1]) / r
#Vector with the position of the charges (q, x, y)
charge_colors = {True: '#aa0000', False: '#0000aa'}
N = 100 # Number of points in each direction
limit = 0.1 # Size of the charges
density = 1# Density of the field lines (augment to have more lines, decrease to have less)
cmapname = 'viridis' # Colormap name
fig, ax = plt.subplots()
map = colors.LogNorm(vmin=0.1, vmax=1)
cbar = plt.colorbar(cm.ScalarMappable(norm=map, cmap=cmapname), ax=ax)
cbar.set_label('Electric Field Amplitude (Arbitrary Units)')
fig.subplots_adjust(bottom=0.20)
ax.set_aspect('equal')

def plotField(charges):
    global fig, ax, cbar
    ax.clear()
    x = np.linspace(-2, 2, N)
    y = np.linspace(-2, 2, N)
    X,Y = np.meshgrid(x, y)
    Ex, Ey = np.zeros((N,N)), np.zeros((N,N))
    mask = np.zeros((N,N))

    #Compute the electric field lines
    for c in charges:
        c_x,c_y = c[1:]
        ex, ey = E(c[0],(c_x,c_y), x=X, y=Y)
        Ex += ex
        Ey += ey
        mask += (np.sqrt((c_x-X)**2 + (c_y-Y)**2) < limit)
        ax.add_artist(Circle(c[1:], limit, color=charge_colors[c[0]>0]))

    mask = (mask > 0)
    Ex[mask] = np.nan
    Ey[mask] = np.nan
    EAmplitude = np.sqrt(Ex**2 + Ey**2)
    ax.streamplot(X, Y, Ex, Ey, color=EAmplitude,cmap = cmapname,density=density)
    cbar.mappable.set_clim(vmin=np.min(EAmplitude[~mask]), vmax=np.max(EAmplitude[~mask]))
    ax.set_aspect('equal')
    fig.subplots_adjust(bottom=0.20,left=0.01)
    fig.canvas.draw()
    
#Mask the field lines inside the charges (to avoid singluarities)


class Index:
    ind = 0

    def next(self, event):
        self.ind += 1
        charges = []
        for i in range(self.ind):
            theta = 2*i*np.pi/self.ind
            if i % 2 == 0:
                charges.append((1, np.cos(theta), np.sin(theta)))
            else:
                charges.append((-1, np.cos(theta), np.sin(theta)))
        plotField(charges)
        
    def prev(self, event):
        self.ind -= 1
        charges = []
        for i in range(self.ind):
            theta = 2*i*np.pi/self.ind
            if i % 2 == 0:
                charges.append((1, np.cos(theta), np.sin(theta)))
            else:
                charges.append((-1, np.cos(theta), np.sin(theta)))
        plotField(charges)
        




#Plot the field lines and the charges
callback = Index()
axprev = fig.add_axes([0.1, 0.05, 0.2, 0.075])
axnext = fig.add_axes([0.6, 0.05, 0.2, 0.075])
bnext = Button(axnext, 'Add a charge')
bnext.on_clicked(callback.next)
bprev = Button(axprev, 'Remove a charge')
bprev.on_clicked(callback.prev)

plt.show()


