#! /usr/bin/python
import inspect, os
import sys
import matplotlib.pyplot as plt
import numpy as np
# for joining&combining structured arrays
#import numpy.lib.recfunctions as rfn

import myrootlib2 as mrl
from myparams import * 

nameScript = inspect.getfile(inspect.currentframe()) 
print "Starting script:", sys.argv[0], nameScript

#####################################
# Start getting data from histograms

# Getting runlist using genfromtxt
print "Reading...", nameRunlist
runlist = mrl.readRunlist(nameRunlist)

# Naming empty columns
newcol_name1 = 'proc_events'
newcol_name2 = 'rmsROOT'
newcol_name3 = 'rms98'
# Adding new columns
newlist = mrl.extendList(mrl.extendList(mrl.extendList(runlist, newcol_name1), newcol_name2), newcol_name3) 
#print newlist.dtype; print newlist[0]

# Getting histogram data
runindex = 0 


########################################
# Getting values 
histname = 'gblaxprime6'
for runindex, value in enumerate(newlist):
	# 0. test
	#print runindex, value['energy']
	# 1./2. add ROOT entries and rms ('stddev')
	specs = mrl.getHistSpecs(runlist, runindex, histname, namePath, nameSuffix, nameRootFolder)
	#print specs['entries']
	newlist['proc_events'][runindex] = specs['entries']
	#print specs['stddev']
	newlist['rmsROOT'][runindex] = specs['stddev']
	# 3. add rms98
	data = mrl.getHist1Data(runlist, runindex, histname, namePath, nameSuffix, nameRootFolder)
	data98 = mrl.getHistFraction(data, 0.98)
	#print mrl.calcHistRMS(data98)
	newlist['rms98'][runindex] = mrl.calcHistRMS(data98)

print newlist

############################################
# Save in npy format
outfile = sys.argv[0][:-3] 
print "saving... data in", outfile
np.save(outfile, newlist)

# Open npy file
#loadlist = np.load(outfile + '.npy')
#print loadlist.dtype; print loadlist

exit()
