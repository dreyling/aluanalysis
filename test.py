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

#print data[0][98], data[1][98]
#print data[0][99], data[1][99]
#print data[0][100], data[1][100]
#print data[0][101], data[1][101]

#data = mrl.cutData(data, 5)
print "mean 100    :", mrl.calcHistMean(data)
print "rms 100     :", mrl.calcHistRMS(data)


data98 = mrl.getHistFraction(data, 0.98)
print "mean 98  :", mrl.calcHistMean(data98)
print "rms 98   :", mrl.calcHistRMS(data98)

#specs = mrl.getHistSpecs(runlist, runindex, nameRootHistos, histindex, namePath, nameSuffix, nameRootFolder)
#print specs

#print "gauss fit:", mrl.fitGaussHisto1d(data98, 0.0, 1.0, 2.e5)

if False:
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
