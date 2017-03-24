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
histindex = np.where(nameRootHistos == "gbltx1")[0][0] #print histindex
data = mrl.getHist1Data(runlist, runindex, nameRootHistos, histindex, namePath, nameSuffix, nameRootFolder)

#mrl.printData(data)

data98 = mrl.getHistFraction(data, 0.98)

print mrl.fitGaussHisto1d(data98, 0.0, 1.0, 2.e5)

print mrl.calcHistMean(data98)
print mrl.calcHistRMS(data98)
print mrl.calcHistMean(data)
print mrl.calcHistRMS(data)

# Plotting Data
fig, ax = plt.subplots(figsize=(8, 5))#, dpi=100)

plt.plot(data[0], data[1])
plt.yscale("log")

plt.title(str(runlist[runindex]) + " " + nameRootHistos[histindex])
plt.xlabel("[mu]")
plt.ylabel("[events]")

#plt.show()

nameSave =  "output/" + sys.argv[0][:-3] + str(".pdf") 
fig.savefig(nameSave)
print "evince " + nameSave + "&"
