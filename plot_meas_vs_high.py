'''plot measurement vs. highland-prediction

Usage:
    plot_meas_vs_high.py (--results=<results>) [--width=<width> --thickness=<thickness>]

Options:
    --results=<results>         npy file [required]
    --width=<width>             width name [default: combined_one_si_norm]
    --thickness=<thickness>     thickness, defalut all [default: all]
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

arguments = docopt(__doc__, version='plot measurement vs. highland')
# open npy result file
data = np.load(arguments['--results'])

############################################
# output names
title_save = "meas_vs_highland_" + arguments['--width'] + "_" + arguments['--thickness']
title_plot = title_save.replace("_", " ")

##############################################
# Processing
if arguments['--thickness'] == 'all':
    width_meas = data[arguments['--width']][data['thickness']>0.0]
    energy = data['energy'][data['thickness']>0.0]
    thickness = data['thickness'][data['thickness']>0.0]
else:
    width_meas = data[arguments['--width']][data['thickness']==float(arguments['--thickness'])]
    energy = data['energy'][data['thickness']==float(arguments['--thickness'])]
    thickness = data['thickness'][data['thickness']==float(arguments['--thickness'])]

width_high = highland.highland_multi_scatterer(energy, thickness, highland.x0alu)

############################################
# Plotting Data
fig, ax = plt.subplots(figsize=(4, 4))#, dpi=100)
fig.subplots_adjust(left=0.17, right=0.96, top=0.96, bottom=0.12)
grid = gridspec.GridSpec(3, 1, hspace=0.0)
ax1 = plt.subplot(grid[:, :])

# data
ax1.plot(width_high, width_meas,
        marker='x',
        color='k',
        ls='None', label='datapoints')

# prediction 
width_pred = np.linspace(0.8 * np.min(width_high), 1.2 * np.max(width_high), 100)
ax1.plot(width_pred, width_pred,
        color='0.5',
        label='prediction', ls='--')

# fit
if False:
    fitfunc = mff.fitfunc_linear
    para0 = [1.0, 0.0]
    xdata = width_high
    ydata = width_meas
    para, cov = curve_fit(fitfunc, xdata, ydata, p0=para0)
    highland_fit = fitfunc(width_pred, *para)
    ax1.plot(width_pred, highland_fit,
            lw=1, label='Fit slope = {:.3f}\noffset = {:.3f}mrad'.format(para[0], para[1]))


# label

bbox = {'fc': 'none', 'ec': 'none', 'pad': 0}
for index, value in enumerate(thickness):
    label = str(thickness[index]) + 'mm / ' + str(energy[index]) + 'GeV' + '$\hspace{50pt}$ \,'
    ax1.text(width_high[index], width_meas[index], label,
            verticalalignment='bottom', horizontalalignment='right',
#            bbox=bbox,
            color='0.5',
            rotation=-30,
            fontsize=6)

# legend
ax1.legend(loc='lower right')

# scales
ax1.set_xscale("log")
#ax1.set_xlim(0.0011, 0.45)
ax1.set_yscale("log")
#ax1.set_ylim(0.015, 15)

#ax1.set_title(title_plot)
ax1.set_xlabel(r'prediction Highland $\theta$ [mrad]')
ax1.set_ylabel(r'measurement $\theta$ [mrad]')

################################################
# save name in folder
name_save =  "output/" + title_save + str(".pdf")
fig.savefig(name_save)
print "evince " + name_save + "&"
