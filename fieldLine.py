import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
from matplotlib.patches import Circle

#Compute the electric field of a charge q at position r0 = (x0, y0) at the point (x, y)
def E(q, r0, x, y):

    r = np.hypot(x-r0[0], y-r0[1])**3
    return q * (x - r0[0]) / r, q * (y - r0[1]) / r
#Vector with the position of the charges (q, x, y)

charges = []
for i in range(8):
    theta = i * np.pi/4
    if i % 2 == 0:
        charges.append((1, np.cos(theta), np.sin(theta)))
    else:
        charges.append((-1, np.cos(theta), np.sin(theta)))




N = 1000 # Number of points in each direction
limit = 0.1 # Size of the charges
density = 2# Density of the field lines (augment to have more lines, decrease to have less)
cmapname = 'viridis' # Colormap name
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
    
#Mask the field lines inside the charges (to avoid singluarities)
mask = (mask > 0)
Ex[mask] = np.nan
Ey[mask] = np.nan
EAmplitude = np.sqrt(Ex**2 + Ey**2)

#Plot the field lines and the charges
fig, ax = plt.subplots()

charge_colors = {True: '#aa0000', False: '#0000aa'}
for c in charges:
    ax.add_artist(Circle(c[1:], limit, color=charge_colors[c[0]>0]))

ax.streamplot(X, Y, Ex, Ey, color=EAmplitude,cmap = cmapname,broken_streamlines=False,density=density)
map = colors.LogNorm(vmin=np.min(EAmplitude[~mask]), vmax=np.max(EAmplitude[~mask]))
cbar = plt.colorbar(cm.ScalarMappable(norm=map, cmap=cmapname), ax=ax)
cbar.set_label('Electric Field Amplitude (Arbitrary Units)')

ax.set_aspect('equal')

plt.show()