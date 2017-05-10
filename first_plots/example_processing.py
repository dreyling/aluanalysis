#! /usr/bin/python
import inspect, os
import sys
import matplotlib.pyplot as plt
import numpy as np
# for joining&combining structured arrays
import numpy.lib.recfunctions as rfn

import myrootlib2 as mrl
from myparams import * 

nameScript = inspect.getfile(inspect.currentframe()) 
print "Starting script:", sys.argv[0]

#####################################
# Start

# Getting runlist using genfromtxt
runlist = mrl.readRunlist(nameRunlist)
#print type(runlist); print runlist.dtype; print runlist
# Getting the column
#print runlist['runnr']
# Getting the row
#print runlist[0]

# Cutting data
cut1 = (runlist['thickness'] == 0.013)
cut2 = (runlist['energy'] == 1.)
#print runlist[cut1 & cut2]
# Using np.where
index13mm = np.where(runlist['thickness'] == 0.013)
#print runlist[index13mm]

# Creating a new column
newcol = np.zeros(np.size(runlist), dtype = {'names': ['proc_events'], 'formats': ['f4']} )
#print newcol.dtype; print newcol

# Adding the new column to the array
newlist = rfn.merge_arrays((runlist, newcol), flatten = True, usemask = False)
#print newlist.dtype; print newlist

# Save in npy format
outfile = sys.argv[0][:-3] 
np.save(outfile, newlist)

# Open npy file
loadlist = np.load(outfile + '.npy')
#print loadlist.dtype; print loadlist

# loop over list 
for index, value in enumerate(newlist):
  print index, value['energy']


###################################
# Getting histogram data
runindex = 0 
histname = 'gblaxprime6'
data = mrl.getHist1Data(runlist, runindex, histname, namePath, nameSuffix, nameRootFolder)

print "mean 100    :", mrl.calcHistMean(data)
print "rms 100     :", mrl.calcHistRMS(data)

data98 = mrl.getHistFraction(data, 0.98)
print "mean 98  :", mrl.calcHistMean(data98)
print "rms 98   :", mrl.calcHistRMS(data98)

specs = mrl.getHistSpecs(runlist, runindex, histname, namePath, nameSuffix, nameRootFolder)
print specs['entries']

print "gauss fit:", mrl.fitGaussHisto1d(data98, 0.0, 1.0, 2.e5)
