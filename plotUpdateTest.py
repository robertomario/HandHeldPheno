# -*- coding: utf-8 -*-
"""
Created on Mon Jun 24 14:00:33 2019

@author: ROBERTO MARIO
"""
import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 2*np.pi, 100)
y = np.sin(x)

#plt.ioff()
fig = plt.figure()
ax = fig.add_subplot(111)
line1, = ax.plot(x[:50], y[:50], 'b-')
plt.show(block=False)
oldData=line1.get_data()

input('Press enter to continue...')

line1.set_xdata(np.concatenate((oldData[0],x[51:99]), axis=None))
line1.set_ydata(np.concatenate((oldData[1],y[51:99]), axis=None))
#fig.canvas.draw()
#plt.show()