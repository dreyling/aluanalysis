'''10mm mean distribution

Usage:
    plot_10mm_mean_distribution.py (--results=<results>) [--width=<width> --thickness=<thickness>]

Options:
    --results=<results>         npy file [required]
    --width=<width>             width name [default: combined_one_si_norm]
    --thickness=<thickness>     thickness, defalut all [default: 10.0]
    -h --help                   show usage of this script
    -v --version                show the version of this script
'''

import numpy as np
from docopt import docopt

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit

import highland
import my_fitfuncs as mff

############################################
# arguments

arguments = docopt(__doc__, version='plot 10mm mean distribuiton')
# open npy result file
data = np.load(arguments['--results'])

############################################
# output names
title_save = "mean_distribution_" + arguments['--thickness']
title_plot = title_save.replace("_", " ")

##############################################
# Processing
sample = (data['thickness']==float(arguments['--thickness']))

# xdata
thickness = data['thickness'][sample]
energy = data['energy'][sample]
opacity =  (thickness/highland.x0alu)**(0.555) / energy


############################################
# Plotting Data
fig, ax = plt.subplots(figsize=(6, 6))#, dpi=100)
fig.subplots_adjust(left=0.15, right=0.98, top=0.98, bottom=0.15)
grid = gridspec.GridSpec(2, 2, hspace=0.02, wspace=0.02)
'''
ax1 = plt.subplot(grid[:1, :1])
ax2 = plt.subplot(grid[1:, :1], sharex=ax1)
ax3 = plt.subplot(grid[:1, 1:], sharey=ax1)
ax4 = plt.subplot(grid[1:, 1:], sharex=ax3, sharey=ax2)
'''
ax3 = plt.subplot(grid[:1, 1:])
ax4 = plt.subplot(grid[1:, 1:], sharex=ax3)
ax1 = plt.subplot(grid[:1, :1], sharey=ax3)
ax2 = plt.subplot(grid[1:, :1], sharex=ax1, sharey=ax4)

# ax1
#ax1.errorbar(energy, data['projection_x_mean'][sample],
#        yerr=data['projection_x_rms'][sample],
#        ls='None', marker='x', markersize=5, color='k')
#ax1.errorbar(energy, data['projection_x_fit_offset'][sample],
#        yerr=data['projection_x_fit_doffset'][sample],
#        ls='None', marker='x', markersize=5, color='k')
ax1.errorbar(energy, -1.*data['projection_x_fit_offset'][sample]/data['projection_x_fit_slope'][sample],
        yerr=data['projection_x_fit_doffset'][sample],
        ls='None', marker='x', markersize=5, color='k')
# ax2 
ax2.errorbar(energy, data['projection_x_fit_slope'][sample],
        yerr=data['projection_x_fit_dslope'][sample],
        ls='None', marker='x', markersize=5, color='k')
# ax3
#ax3.errorbar(energy, data['projection_y_mean'][sample],
#        yerr=data['projection_y_rms'][sample],
#        ls='None', marker='x', markersize=5, color='k')
#ax3.errorbar(energy, data['projection_y_fit_offset'][sample],
#        yerr=data['projection_y_fit_doffset'][sample],
#        ls='None', marker='x', markersize=5, color='k')
ax3.errorbar(energy, -1.*data['projection_y_fit_offset'][sample]/data['projection_y_fit_slope'][sample],
        yerr=data['projection_y_fit_doffset'][sample],
        ls='None', marker='x', markersize=5, color='k')
# ax4 
ax4.errorbar(energy, data['projection_y_fit_slope'][sample],
        yerr=data['projection_y_fit_dslope'][sample],
        ls='None', marker='x', markersize=5, color='k')

# axis labels
ax1.set_ylabel(r'offset/zero-point at axis [mm]')
ax2.set_xlabel(r'x-projection, energy [GeV]')
ax2.set_ylabel(r'slope along axis [mrad/mm]')
ax4.set_xlabel(r'y-projection, energy [GeV]')

ax1.axhline(0.0, lw=0.5, color='k')
ax2.axhline(0.0, lw=0.5, color='k')
ax3.axhline(0.0, lw=0.5, color='k')
ax4.axhline(0.0, lw=0.5, color='k')


# hiding axis names
#ax1.set_xticklabels([])
#ax3.set_xticklabels([])
#ax3.set_yticklabels([])
#ax4.set_yticklabels([])

# legend
#ax1.legend(loc='upper left')

# scales
#ax1.set_xscale("log")
#ax1.set_xlim(0.0011, 0.45)
#ax1.set_yscale("log")
#ax1.set_ylim(0.015, 15)

#ax1.set_title(title_plot)
#ax1.set_xlabel(r'prediction Highland $\theta$ [mrad]')
#ax1.set_ylabel(r'measurement $\theta$ [mrad]')

################################################
# save name in folder
name_save =  "output/" + title_save + str(".pdf")
fig.savefig(name_save)
print "evince " + name_save + "&"
