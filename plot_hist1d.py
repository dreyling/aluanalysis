#! /usr/bin/python
import inspect, os
import sys
import matplotlib.pyplot as plt
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
#print np.size(runlist['runnr'])
#print np.size(nameRootHistos)

# Getting histogram data
runindex = 0 
histindex = np.where(nameRootHistos == "gblprb")[0][0] #print histindex
data = mrl.getHist1Data(runlist, runindex, nameRootHistos, histindex, namePath, nameSuffix, nameRootFolder)

# Plotting Data
fig, ax = plt.subplots(figsize=(6, 6))#, dpi=100)

plt.plot(data[0], data[1])
plt.yscale("log")

plt.title(str(runlist[runindex]) + " " + nameRootHistos[histindex])
plt.xlabel("[mu]")
plt.ylabel("[events]")

plt.show()

nameSave =  "output/" + sys.argv[0][:-3] + str(".pdf") 
fig.savefig(nameSave)
print "evince " + nameSave + "&"
