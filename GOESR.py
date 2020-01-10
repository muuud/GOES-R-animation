#!/usr/bin/env python

import glob
import numpy as np
import matplotlib.pyplot as plt
import netCDF4
import matplotlib as mpl
import time
from matplotlib import animation
from astropy.time import TimeDelta, Time
from astropy import units as u

mpl.rcParams['savefig.pad_inches'] = 0

#find netCDF files
x = glob.glob('/path/to/nc/files/*.nc')

#zip sort in order of increasing time
times = [int(path.split('_')[3][1:]) for path in x]
times, paths = (list(t) for t in zip(*sorted(zip(times, x))))

#read data
path = paths[0]
d = netCDF4.Dataset(path)
data = d['Rad'][:].data
data[np.where(data==np.max(data))] = 0
tsec = d['t'][:].data
tstring = (Time(2000, format='jyear') + TimeDelta(tsec*u.s)).iso
tstring[:-7]

#example plot
fig = plt.figure(figsize=(5,5),dpi=300)
ax = plt.axes([0,0,1,1], frameon=False)
ax.get_xaxis().set_visible(False)
ax.get_yaxis().set_visible(False)
plt.autoscale(tight=True)
im = plt.imshow(data,cmap='Greys_r')
tt = ax.text(10,100,tstring[:-7],color='white',fontsize=8)
plt.show()

def init():
    im.set_array(np.zeros(data.shape))
    tt.set_text('init')
    return im, tt

def updatefig(frame, *args):
    path = paths[frame]
    d = netCDF4.Dataset(path)
    data = d['Rad'][:].data
    tsec = d['t'][:].data
    tstring = (Time(2000, format='jyear') + TimeDelta(tsec*u.s)).iso
    data[np.where(data==np.max(data))] = 0
    tt.set_text(tstring[:-7])
    im.set_array(data)
    return im, tt

#Render Video
LEN = len(paths)
frames = [int(_) for _ in np.round(np.arange(LEN))]
print('frames: {}'.format(len(frames)))
t0 = time.time()
ani = animation.FuncAnimation(fig, updatefig, frames=frames, interval=50, blit=True, init_func=init)
Writer = animation.writers['ffmpeg']
writer = Writer(fps=24, metadata=dict(artist='Me'), bitrate=6000)
ani.save('GOESR.mp4', writer=writer)
t1 = time.time()
print('rendered in {} seconds'.format(t1-t0))
plt.close()