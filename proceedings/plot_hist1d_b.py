#! /usr/bin/python
import inspect, os
import sys
import matplotlib.pyplot as plt
import numpy as np
#from scipy.optimize import curve_fit
#import math

sys.path.insert(0, '../')
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
runlist = mrr.readRunlist("../" + name_runlist)

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

# Getting analysis data
entries   = data_analysis['proc_events'][runindex]
gauss_mu  = data_analysis['gauss_mu'][runindex]
gauss_si  = data_analysis['gauss_si'][runindex]
gauss_dmu = data_analysis['gauss_dmu'][runindex]
gauss_dsi = data_analysis['gauss_dsi'][runindex]
gauss_he  = data_analysis['gauss_height'][runindex]
gauss_c2  = data_analysis['gauss_chi2'][runindex]
gauss_c2r = data_analysis['gauss_chi2red'][runindex]
gauss_sin = data_analysis['gauss_si_norm'][runindex]


#####################
# output names
title_save = "run" + str(runnr)[:-2] + "_" + energy + "GeV" + "_" + thickness + "mm" + "_" + input_file[5:-4] 
title_plot = title_save.replace("_", " ")


##########################################
# Plotting Data
fig, ax = plt.subplots(figsize=(5, 5))#, dpi=100)
fig.subplots_adjust(left=0.14, bottom=0.12, right=0.97, top=0.97)

# grids and lines
#plt.axvspan(datafrac[0][0], datafrac[0][-1], color='yellow', alpha=0.3, label='98\%')
#plt.axvline(0, color='0.5')

# normalization factor
norm = np.max(data[1]) #; print norm

# plot data

# line
#plt.plot(data[0], data[1]/norm, 'k', label='k')

# histogram, bar-style
plt.bar(edges[:-1], data[1]/norm, width=data[0][1]-data[0][0], linewidth=0, color='0.5', label='data') # tested: , yerr=np.sqrt(data[1])/norm

# plot fit
x_fit = datafrac[0]
para = [gauss_mu, gauss_si, gauss_he/norm]
y_fit = mff.fitfunc_gauss(x_fit, *para)
plt.plot(x_fit, y_fit, ls='--', lw=3, color='k', label = 'fit')

# limits and labels
#plt.yscale("log"), plt.ylim(5e-5, 5)
plt.xlim(-1.2, 1.2), plt.ylim(0, 1.3)

#plt.title(title_plot)
plt.xlabel(r'kink angle $\alpha_{\rm eff}$ [mrad]', fontsize=14, labelpad=16)
plt.ylabel("entries (normalized)", fontsize=14, labelpad=16)

####################
# legend and text

# Legend
handles, labels = ax.get_legend_handles_labels()
# reverse order
ax.legend(handles[::-1], labels[::-1], loc='upper left', prop={'size':12}, frameon=False)

# fit results
textbox = (
	r'$\theta_{\rm meas} =$ (' + '{:.3f}'.format(gauss_si) + r'$\pm$' + '{:.3f}'.format(gauss_dsi) + ') mrad' + '\n' + 
#	r'entries$_{98\%} = $ ' + '{:.2e}'.format(np.sum(datafrac[1])) + ' ({:.2f} \%)'.format(100*np.sum(datafrac[1])/np.sum(data[1]))  + '\n' +
        r'$\chi^2/{\rm ndf} = $ ' + '{:.1f}'.format(gauss_c2r)
  )
props = dict(boxstyle='square,pad=0.6', facecolor='white', alpha=1.0)
ax.text(0.04, 0.84, textbox, transform=ax.transAxes, fontsize=10, #linespacing=1.5,
        verticalalignment='top', horizontalalignment='left')#, bbox=props)

textbox = '{0} GeV/c, {1} mm'.format(energy, thickness)
ax.text(0.955, 0.97, textbox, transform=ax.transAxes, 
        fontsize=12, fontweight='heavy', color='k', 
        verticalalignment='top', horizontalalignment='right')#, bbox=props)

# save name in folder
name_save =  "output/" + title_save + str("_b.pdf") 
fig.savefig(name_save)
print "evince " + name_save + "&"
