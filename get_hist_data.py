#! /usr/bin/python
import inspect, os
import sys
import math
import numpy as np

import myrootlib2 as mrl
from myparams import * 

############################################
# setting which data
nameScript = inspect.getfile(inspect.currentframe()) 
print "Starting script:", sys.argv[0], nameScript

# 1st argument
if sys.argv[1] == '1':
  name_path = name_path_1scatterer
  name_suffix = name_suffix_1scatterer
elif sys.argv[1] == '2':
  name_path = name_path_2scatterer
  name_suffix = name_suffix_2scatterer
else:
  print "1st argument wrong...no valid data!"
  exit()
print sys.argv[1], "scatterer"

# 2nd argument
histname = sys.argv[2]
print sys.argv[2], "histogram collecetion"

# save name in folder
outfile = "data/" + sys.argv[1] + "_scatterer_" + sys.argv[2]

#####################################
# Start getting data from histograms

# Getting runlist using genfromtxt
print "Reading...", name_runlist
runlist = mrl.readRunlist(name_runlist)

# Naming empty columns
newcol_name1 = 'proc_events'
newcol_name2 = 'rmsROOT'
newcol_name3 = 'rms98'
newcol_name4 = 'rms98_norm'
# Adding new columns
newlist = mrl.extendList(mrl.extendList(mrl.extendList(mrl.extendList(runlist, newcol_name1), newcol_name2), newcol_name3), newcol_name4) 
#print newlist.dtype; print newlist[0]

########################################
# Getting values 
for index, value in enumerate(newlist):
	# 0. test
	#print index, value['energy']
	# 1./2. add ROOT entries and rms ('stddev')
	specs = mrl.getHistSpecs(runlist, index, histname, name_path, name_suffix, name_rootfolder)
	#print specs['entries']
	newlist['proc_events'][index] = specs['entries']
	#print specs['stddev']
	newlist['rmsROOT'][index] = specs['stddev']
	# 3. add rms98
	data = mrl.getHist1Data(runlist, index, histname, name_path, name_suffix, name_rootfolder)
	data98 = mrl.getHistFraction(data, 0.98)
	#print mrl.calcHistRMS(data98)
	newlist['rms98'][index] = mrl.calcHistRMS(data98)

# Getting Zero values
cut_zero = (newlist['thickness'] == 0.0)
data_zero_energy = newlist[cut_zero]['energy']
data_zero_rms98 = newlist[cut_zero]['rms98']

# Calculate normalized value
for index, value in enumerate(newlist):
  newlist['rms98_norm'][index] = math.sqrt(newlist['rms98'][index]**2 - data_zero_rms98[data_zero_energy == newlist['energy'][index]][0]**2)

print newlist

############################################
# Save in npy format
print "saving npy-data in:", outfile 
np.save(outfile, newlist)
