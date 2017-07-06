#! /usr/bin/python
import inspect, os
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
#import matplotlib.ticker as ticker
#from matplotlib.ticker import NullFormatter
#import matplotlib.cm as cm
import numpy as np
#from scipy.optimize import curve_fit
import math

import my_fitfuncs as mff
import my_dataproc as mdp

#from myparams import * 

#######################################################

# settings
title_save = sys.argv[0][:-3]
print title_save

# figure
fig = plt.figure(figsize=(5, 3))
fig.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1)
# subplots-grid: rows, columns
grid = gridspec.GridSpec(1, 2, wspace=0.2)
ax1 = plt.subplot(grid[:, :1])
ax2 = plt.subplot(grid[:, 1:])
ax2.set_yscale('log')

# data 
mu, sigma = 0, 0.5 # mean and standard deviation
data = np.random.normal(mu, sigma, 1000000)
print data[0]

# normal histo
count, bins, edges = ax1.hist(data, 1000, normed=True, histtype='step')
bins_cent = bins[:-1] + (bins[1]-bins[0])/2.

# squared histo
data2 = np.power(data, 2)
print data2[0], data[0]**2
count2, bins2, edges2 = ax2.hist(data2, 1000, normed=True, histtype='step')
bins2_cent = bins2[:-1] + (bins2[1]-bins2[0])/2.

# analyse
st_std = mdp.calc_hist_RMS(np.vstack((bins_cent, count)))
print "Gauss: distribution width", st_std
sq_mean = mdp.calc_hist_mean(np.vstack((bins2_cent, count2))) 
print "Gauss2: distribution mean", sq_mean, math.sqrt(sq_mean)
#sq_std = mdp.calc_hist_RMS(np.vstack((bins2_cent, count2))) 
#print "Gauss2: distribution width", sq_std, math.sqrt(sq_std)
print "ratio:", st_std/math.sqrt(sq_mean)

# text
ax1.text(0.05, 0.9, 'RMS: {:.6f}'.format(st_std), transform=ax1.transAxes, fontsize=10, verticalalignment='top', horizontalalignment='left')
ax2.text(0.05, 0.9, 'Mean: {:.6f} \nsqrt(Mean): {:.6f}'.format(sq_mean, math.sqrt(sq_mean)), transform=ax2.transAxes, fontsize=10, verticalalignment='top', horizontalalignment='left')


# save 
name_save =  "output/" + title_save + str(".pdf") 
fig.savefig(name_save)
print "evince " + name_save + "&"
