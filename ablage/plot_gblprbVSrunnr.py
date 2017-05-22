#! /usr/bin/python
import inspect, os
import sys
import matplotlib.pyplot as plt
import matplotlib.ticker
import numpy as np
#from scipy.optimize import curve_fit
#import math

import myrootlib as mrl
from myparams import *

nameScript = inspect.getfile(inspect.currentframe()) 
print "Starting script:", sys.argv[0]

#####################################
# Start

# Getting runlist
runlist = mrl.readRunlist(nameRunlist)
#print runlist['runnr'], runlist['thickness'], runlist['energy'] 

# Getting histogram data
histindex = np.where(nameRootHistos == "gblprb")[0][0]
data = mrl.loopRunAndSum(runlist, nameRootHistos, histindex, namePath, nameSuffix, nameRootFolder)

# Plotting Data
fig, ax = plt.subplots(figsize=(8, 5))#, dpi=100)

plt.plot(data[0], data[1], 'kx')
plt.yscale("log")

plt.title(nameRootHistos[histindex])
plt.xlabel("[runnr]")
plt.ylabel("[events]")
plt.grid(True)
ax.yaxis.set_major_formatter(matplotlib.ticker.LogFormatter())


#plt.show()

nameSave =  "output/" + sys.argv[0][:-3] + str(".pdf") 
fig.savefig(nameSave)
print "evince " + nameSave + "&"
