'''plot comparison of 2d distributions

Usage:
    plot_2d_comparison.py (--results=<results> --data_type=<data_type>)

Options:
    --results=<results>         npy file [required]
    --data_type=<data_type>     'mean' or 'sigma' [required]
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

arguments = docopt(__doc__, version='plot 2d comparison')
# open npy result file
data = np.load(arguments['--results'])
data_type = arguments['--data_type']

############################################
# output names
title_save = 'compare_' + arguments['--results'][20:-4] + '_vs_opacity'
title_plot = title_save.replace("_", " ")

############################################
# Plotting Data
fig, ax = plt.subplots(figsize=(8, 8))#, dpi=100)
fig.subplots_adjust(left=0.10, right=0.98, top=0.98, bottom=0.10)
grid = gridspec.GridSpec(2, 2, hspace=0.1, wspace=0.2)
ax1 = plt.subplot(grid[:1, :1])
ax2 = plt.subplot(grid[1:, :1], sharex=ax1)
ax3 = plt.subplot(grid[:1, 1:])#, sharey=ax1)
ax4 = plt.subplot(grid[1:, 1:], sharex=ax3)
# grid test
#ax1.text(0.5, 0.5, 'ax1', transform=ax1.transAxes)
#ax2.text(0.5, 0.5, 'ax2', transform=ax2.transAxes)
#ax3.text(0.5, 0.5, 'ax3', transform=ax3.transAxes)
#ax4.text(0.5, 0.5, 'ax4', transform=ax4.transAxes)

# zero lines
ax2.axhline(y=0.0, color='0.25')
ax4.axhline(y=0.0, color='0.25')

# xdata: vs. opacity
opac_electron =  (data['thickness'][data['thickness']>0.0]/highland.x0alu)**(0.555) / data['energy'][data['thickness']>0.0]
# xdata: vs. thickness
thickness = data['thickness'][data['thickness']>0.0]
# xdata: vs. energy
energy = data['energy'][data['thickness']>0.0]

xdata = opac_electron

# ydata:
# ax1
ax1.errorbar(xdata, data['projection_x_mean'][data['thickness']>0.0],
        yerr=data['projection_x_rms'][data['thickness']>0.0],
        ls='None', marker='o', markersize=2, color='k')
# ax2 
ax2.errorbar(xdata, data['projection_x_fit_slope'][data['thickness']>0.0],
        yerr=data['projection_x_fit_dslope'][data['thickness']>0.0],
        ls='None', marker='o', markersize=2, color='k')
# ax3
ax3.errorbar(xdata, data['projection_y_mean'][data['thickness']>0.0],
        yerr=data['projection_y_rms'][data['thickness']>0.0],
        ls='None', marker='o', markersize=2, color='k')
# ax4 
ax4.errorbar(xdata, data['projection_y_fit_slope'][data['thickness']>0.0],
        yerr=data['projection_y_fit_dslope'][data['thickness']>0.0],
        ls='None', marker='o', markersize=2, color='k')


if data_type == 'sigma':
    # highland x data
    opacity = np.logspace(-3, 0., 100)
    highland_electron = highland.highland_opacity_electrons(opacity)
    ax1.plot(opacity, highland_electron,
                lw=1, color='k', label='Highland (electron)')
    ax3.plot(opacity, highland_electron,
                lw=1, color='k', label='Highland (electron)')

# label
for index, value in enumerate(thickness):
    label = '\,\,\,\,' + str(thickness[index]) + 'mm / ' + str(energy[index]) + 'GeV'
    ax1.text(xdata[index], data['projection_x_mean'][data['thickness']>0.0][index]*1.07,
            label, verticalalignment='bottom', horizontalalignment='left',
            rotation=80, fontsize=4, color='0.5')
    ax2.text(xdata[index], data['projection_x_fit_slope'][data['thickness']>0.0][index]*1.07,
            label, verticalalignment='bottom', horizontalalignment='left',
            rotation=80, fontsize=4, color='0.5')
    ax3.text(xdata[index], data['projection_y_mean'][data['thickness']>0.0][index]*1.07,
            label, verticalalignment='bottom', horizontalalignment='left',
            rotation=80, fontsize=4, color='0.5')
    ax4.text(xdata[index], data['projection_y_fit_slope'][data['thickness']>0.0][index]*1.07,
            label, verticalalignment='bottom', horizontalalignment='left',
            rotation=80, fontsize=4, color='0.5')

# scales
ax1.set_xscale("log")
ax3.set_xscale("log")
if data_type == 'sigma':
    ax1.set_yscale("log")
    ax3.set_yscale("log")
    ax1.set_ylim(0.1, 20)
    ax3.set_ylim(0.1, 20)

# axis labels
ax1.set_ylabel(r'total mean [mrad]')
ax2.set_xlabel(r'x-projection, opacity $\epsilon^{0.555}/p$ [1/GeV]')
ax2.set_ylabel(r'slope along axis [mrad/mm]')
ax4.set_xlabel(r'y-projection, opacity $\epsilon^{0.555}/p$ [1/GeV]')

# hiding axis names
#ax1.set_xticklabels([])
#ax3.set_xticklabels([])
#ax3.set_yticklabels([])
#ax4.set_yticklabels([])

################################################
# save name in folder
name_save =  "output/" + title_save + str(".pdf")
fig.savefig(name_save)
print "evince " + name_save + "&"
