#! /usr/bin/python
#import inspect, os
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
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
data = mrr.getHist1Data(runlist, runindex, histname, name_path, name_suffix, name_rootfolder)
datafrac = mdp.get_hist_fraction(data, float(fraction))

# derivative
dx = data[0][1:] - data[0][:-1]
dy = data[1][1:] - data[1][:-1]
deriv_x = data[0][0:-1]
deriv_y = dy / dx

#####################
# output names
title_save = "run" + str(runnr)[:-2] + "_" + energy + "GeV" + "_" + thickness + "mm" + "_" + input_file[5:-4] 
title_plot = title_save.replace("_", " ")


##########################################
# Plotting Data
fig, ax = plt.subplots(figsize=(6, 8))#, dpi=100)
fig.subplots_adjust(left=0.11, right=0.99, top=0.94, bottom=0.12)

# subplots-grid: rows, columns
grid = gridspec.GridSpec(2, 1, hspace=0.05)
# layout
ax1 = plt.subplot(grid[:1, :])
ax2 = plt.subplot(grid[1:, :], sharex=ax1) 

ax1.axvspan(datafrac[0][0], datafrac[0][-1], color='yellow', alpha=0.2)
ax1.axvline(0, color='0.5')

norm = np.max(data[1])
ax1.plot(data[0], data[1]/norm, 'k')

# deriv
ax2.plot(deriv_x, deriv_y, 'k')


# Fit line
fitfunc_gauss = lambda xdata, *para: para[2] * np.exp(-0.5*(xdata-para[0])**2/para[1]**2)
gauss_mu = data_analysis['gauss_mu'][runindex]
gauss_si = data_analysis['gauss_si'][runindex]
gauss_he = data_analysis['gauss_height'][runindex]
gauss_c2 = data_analysis['gauss_chi2red'][runindex]

x_fit = data[0]
para = [gauss_mu, gauss_si, gauss_he/norm]
y_fit = fitfunc_gauss(x_fit, *para)

ax1.plot(x_fit, y_fit, ls='--', lw=2, alpha=0.8, color='red')

# text box
textbox = (
	r'$\theta_{{\rm rms}_{100}} =$ ' + '{:.4f}'.format(mdp.calc_hist_RMS(data)) + ' mrad' + '\n' + 
	r'$\theta_{{\rm rms}_{frac}} =$ ' + '{:.4f}'.format(mdp.calc_hist_RMS(datafrac)) + ' mrad' + '\n' + 
	r'$\theta_{{\rm mean}_{frac}} =$ ' + '{:.4f}'.format(mdp.calc_hist_mean(datafrac)) + ' mrad' + '\n' + 
	r'events$_{frac} = $ ' + '{:.2e}'.format(np.sum(datafrac[1])) + ' ({:.2f} \%)'.format(100*np.sum(datafrac[1])/np.sum(data[1]))  + '\n' +
        r'$\chi^2_{\rm red.} = $ ' + '{:.1f}'.format(gauss_c2)
  )
props = dict(boxstyle='round,pad=0.5', facecolor='white', alpha=0.9)
ax1.text(0.5, 0.05, textbox, transform=ax.transAxes, fontsize=10,
        verticalalignment='bottom', horizontalalignment='center', bbox=props)

ax1.set_yscale("log")
ax1.set_xlim(-0.5, 0.5)
#ax1.set_xlim(-1.9, 1.9)
ax1.set_ylim(5e-7, 5)

ax1.set_title(title_plot)
ax1.set_xlabel(r'$\theta$ [mrad]')
ax1.set_ylabel("events normalized")


# save name in folder
name_save =  "output/" + "deriv_" + title_save + str(".pdf") 
fig.savefig(name_save)
print "evince " + name_save + "&"
