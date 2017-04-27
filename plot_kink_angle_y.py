#! /usr/bin/python
import inspect, os
import sys
import matplotlib.pyplot as plt
import numpy as np
import math

import myrootlib2 as mrl
from myparams import * 

nameScript = inspect.getfile(inspect.currentframe()) 
print "Starting script:", sys.argv[0], nameScript

#####################################
# Open npy file
input_file = sys.argv[0][5:-3] # without plot_ and .py
data = np.load(input_file + '.npy')
#print data.dtype; print data

#exit()

#########################################
# Plotting Data
fig, ax = plt.subplots(figsize=(8, 5))#, dpi=100)

plt.plot(data['energy'], data['rms98_norm'], 'kx')

# scaling and range
plt.yscale("log")
plt.xlim([0.5, 5.5])

# labeling
plt.title("kink angle (gblayprime6, 1 scatterer)")
plt.xlabel("beam energy [GeV]")
plt.ylabel(r'$\sqrt{\theta_{rms_{98}}^2 - \theta_{0,rms_{98}}^2}$')
plt.grid(True)
#ax.yaxis.set_major_formatter(matplotlib.ticker.LogFormatter())

#plt.show()

nameSave =  "output/" + sys.argv[0][:-3] + str(".pdf") 
fig.savefig(nameSave)
print "evince " + nameSave + "&"




exit()
