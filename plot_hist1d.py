#! /usr/bin/python
import inspect, os
import sys
import matplotlib.pyplot as plt
import numpy as np
#from scipy.optimize import curve_fit
#import math

import my_rootread as mrr
import my_fitfuncs as mff
import my_dataproc as mdp

from myparams import * 

############################################
# setting which data
print "Starting script:", sys.argv[0]

# 1st argument, data
name_path = sys.argv[1]
print "path:", name_path
name_kappa = name_path[-15:-7]
name_kinks = name_path[-6:-1]
name_suffix = "-GBLKinkEstimator_" + name_kappa + "_" + name_kinks

# 2nd argument
histname 	= sys.argv[2]
print "histogram collection:", histname

# 3rd/4th argument
energy 		= sys.argv[3]
print "selected energy:", energy
thickness = sys.argv[4]
print "selected thickness:", thickness

# 5th argument, npy results
if len(sys.argv) < 2:
  print "No data input. Run get_hist_data.py or select npy-file in data/..."
  exit()
input_file = sys.argv[5]
data_analysis = np.load(input_file)
#print data_analysis
fraction = input_file[-8:-4]
print "selected data fraction:", fraction

#####################################
# Start

# Getting runlist
runlist = mrr.readRunlist(name_runlist)

# getting right runindex
runindex = np.intersect1d(np.where(runlist['thickness'] == float(thickness)), np.where(runlist['energy'] == float(energy)))[0]
runnr = runlist['runnr'][runindex]
print "selected run:", runnr

# Getting histogram data
data, edges = mrr.getHist1Data(runlist, runindex, histname, name_path, name_suffix, name_rootfolder)
datafrac = mdp.get_hist_fraction(data, float(fraction))
#print np.sum(data[1])
#print np.sum(datafrac[1])
#print mdp.calc_hist_RMS(datafrac)
#print mdp.calc_hist_mean(datafrac)

#####################
# output names
title_save = "run" + str(runnr)[:-2] + "_" + energy + "GeV" + "_" + thickness + "mm" + "_" + input_file[5:-4] 
title_plot = title_save.replace("_", " ")


##########################################
# Plotting Data
fig, ax = plt.subplots(figsize=(6, 4))#, dpi=100)
fig.subplots_adjust(left=0.11, right=0.99, top=0.94, bottom=0.12)

plt.axvspan(datafrac[0][0], datafrac[0][-1], color='yellow', alpha=0.2)
plt.axvline(0, color='0.5')

norm = np.max(data[1]) #; print norm
plt.plot(data[0], data[1]/norm, 'k', label='k')

# Fit line
gauss_mu = data_analysis['gauss_mu'][runindex]
gauss_si = data_analysis['gauss_si'][runindex]
gauss_he = data_analysis['gauss_height'][runindex]
gauss_c2 = data_analysis['gauss_chi2red'][runindex]
#print gauss_mu
#print gauss_si
#print gauss_he
#print gauss_c2

x_fit = data[0]
para = [gauss_mu, gauss_si, gauss_he/norm]
y_fit = mff.fitfunc_gauss(x_fit, *para)

plt.plot(x_fit, y_fit, ls='--', lw=2, alpha=0.8, color='red')

# text box
textbox = (
	r'$\theta_{{\rm rms}_{100}} =$ ' + '{:.4f}'.format(mdp.calc_hist_RMS(data)) + ' mrad' + '\n' + 
	r'$\theta_{{\rm rms}_{frac}} =$ ' + '{:.4f}'.format(mdp.calc_hist_RMS(datafrac)) + ' mrad' + '\n' + 
	r'$\theta_{{\rm mean}_{frac}} =$ ' + '{:.4f}'.format(mdp.calc_hist_mean(datafrac)) + ' mrad' + '\n' + 
	r'events$_{frac} = $ ' + '{:.2e}'.format(np.sum(datafrac[1])) + ' ({:.2f} \%)'.format(100*np.sum(datafrac[1])/np.sum(data[1]))  + '\n' +
        r'$\chi^2_{\rm red.} = $ ' + '{:.1f}'.format(gauss_c2)
  )
props = dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9)
ax.text(0.05, 0.95, textbox, transform=ax.transAxes, fontsize=10,
        verticalalignment='top', horizontalalignment='left', bbox=props)

plt.yscale("log")
#plt.xlim(-4.2, 4.2)
#plt.xlim(-1.9, 1.9)
plt.ylim(5e-5, 5)

plt.title(title_plot)
plt.xlabel(r'$\theta$ [mrad]')
plt.ylabel("events normalized")

# save name in folder
name_save =  "output/" + title_save + str(".pdf") 
fig.savefig(name_save)
print "evince " + name_save + "&"
