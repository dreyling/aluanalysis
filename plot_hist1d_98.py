#! /usr/bin/python
import inspect, os
import sys
import matplotlib.pyplot as plt
import numpy as np
#from scipy.optimize import curve_fit
#import math

import myrootlib2 as mrl
from myparams import * 

############################################
# setting which data
print "Starting script:", sys.argv[0]

# 1st argument
scatterer = sys.argv[1]
if scatterer 		== '1':
  name_path 	= name_path_1scatterer
  name_suffix = name_suffix_1scatterer
elif scatterer 	== '2':
  name_path 	= name_path_2scatterer
  name_suffix = name_suffix_2scatterer
else:
  print "1st argument wrong...no valid data!"
  exit()
print "scatterer number:", scatterer

# 2nd argument
histname 	= sys.argv[2]
print "histogram collection:", histname
# 3rd/4th argument
energy 		= sys.argv[3]
print "selected energy:", energy
thickness = sys.argv[4]
print "selected thickness:", thickness

#####################################
# Start

# Getting runlist
runlist = mrl.readRunlist(name_runlist)
print "Reading...", name_runlist

# getting right runindex
runindex = np.intersect1d(np.where(runlist['thickness'] == float(thickness)), np.where(runlist['energy'] == float(energy)))[0]
runnr = runlist['runnr'][runindex]
print "selected run:", runnr

# Getting histogram data
data = mrl.getHist1Data(runlist, runindex, histname, name_path, name_suffix, name_rootfolder)
data98 = mrl.getHistFraction(data, 0.98)
#print np.sum(data[1])
#print np.sum(data98[1])
#print mrl.calcHistRMS(data98)
#print mrl.calcHistMean(data98)

##########################################
# Plotting Data
fig, ax = plt.subplots(figsize=(6, 4))#, dpi=100)
fig.subplots_adjust(left=0.1, right=0.99, top=0.94, bottom=0.12)

#plt.axvline(data98[0][0],  color='0.5', ls='--')
#plt.axvline(data98[0][-1], color='0.5', ls='--')
plt.axvspan(data98[0][0], data98[0][-1], color='yellow', alpha=0.2)
plt.axvline(0, color='0.5')

plt.plot(data[0], data[1], 'k', label='k')

# text box
textbox = (
	r'$\theta_{{\rm rms}_{100}} =$ ' + '{:.4f}'.format(mrl.calcHistRMS(data)) + ' mrad' + '\n' + 
	r'$\theta_{{\rm rms}_{98}} =$ ' + '{:.4f}'.format(mrl.calcHistRMS(data98)) + ' mrad' + '\n' + 
	r'$\theta_{{\rm mean}_{98}} =$ ' + '{:.4f}'.format(mrl.calcHistMean(data98)) + ' mrad' + '\n' + 
	r'events$_{98} = $ ' + '{:.2e}'.format(np.sum(data98[1])) + ' ({:.2f} \%)'.format(100*np.sum(data98[1])/np.sum(data[1])) 
  )
props = dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9)
ax.text(0.5, 0.05, textbox, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom', horizontalalignment='center', bbox=props)

plt.yscale("log")
plt.xlim(-4.2, 4.2)
plt.ylim(2e1, 9e5)

texttitle = (scatterer + " scatterer model, " + histname + ", " + energy + " GeV, " + thickness + " mm, " + "run " + str(runnr)[:-2])
plt.title(texttitle)
plt.xlabel(r'$\theta$ [mrad]')
plt.ylabel("events")

# save name in folder
outfile = "output/" + sys.argv[1] + "_scatterer_" + sys.argv[2] + "_" + energy + "gev_" + thickness + "mm_" + "run" + str(runnr)[:-2] + ".pdf"
fig.savefig(outfile)
print "evince " + outfile + "&"
