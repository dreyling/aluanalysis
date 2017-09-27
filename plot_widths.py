'''plot widths.py

Usage:
    plot_widths.py (--results=<results> --thickness=<thickness>) [--normalized=<True/False>]

Options:
    --results=<results>         npy file [required]
    --thickness=<thickness>     thickness of target
    --normalized=<True/False>   normalized values [default:]
    -h --help                   show usage of this script
    -v --version                show the version of this script
'''

import numpy as np
import math
from docopt import docopt

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import highland

############################################
# arguments

arguments = docopt(__doc__, version='plot widths')
# open npy result file
data = np.load(arguments['--results'])
thickness = float(arguments['--thickness'])

if bool(arguments['--normalized']) == True:
    norm = '_norm'
else:
    norm = ''

xdata = 'energy'
widths = ['rmsROOT', 'rmsfrac', 'gauss_si', 'combined_si_g', 'combined_si_s', 'combined_one_si']

#####################
# output names
title_save = 'kinkangle' + norm + '-vs-' + xdata + '_' + str(thickness) + 'mm'
title_plot = title_save.replace("_", " ")

#########################################
# Plotting
# figure
fig = plt.figure(figsize=(8, 8))#, dpi=100)
fig.subplots_adjust(left=0.11, right=0.7, top=0.94, bottom=0.1)
# subplots-grid: rows, columns
grid = gridspec.GridSpec(10, 1, hspace=0.05)
ax1 = plt.subplot(grid[:, :])

# highland x data
highland_x = np.linspace(0.5, 6, 50)
highland_y = highland.highland_multi_scatterer_extended(highland_x, thickness, highland.x0alu)
ax1.plot(highland_x, highland_y,
            lw=3, label='Highland \n(multi-scattering,\nkink effective)')
highland_y = highland.highland_multi_scatterer(highland_x, thickness, highland.x0alu)
ax1.plot(highland_x, highland_y,
            lw=1, label='Highland \n(multi-scattering)')
highland_y_el = highland.highland_electrons(highland_x, thickness, highland.x0alu)
ax1.plot(highland_x, highland_y_el,
            lw=1, label='Highland \n(electron)')



# data
cut = (data['thickness'] == thickness)
# index sorted by increasing energy 
index_sorted = data[cut][xdata].argsort()
for index, value in enumerate(widths):
    # data
    ydata = value + norm
    ax1.plot(data[cut][xdata][index_sorted], data[cut][ydata][index_sorted],
            label=ydata.replace("_", " "), marker='x')
    # TODO: errorbars
    #ax1.errorbar(data[cut][xdata][index_sorted], data[cut][ydata][index_sorted],
    #        yerr=data[cut][value+'_error'][index_sorted]
    #        label=ydata.replace("_", " "), marker='x')

# scaling and range
ax1.set_xlim([0.5, 5.5])
#ax1.set_yscale("log")
#ax1.set_ylim([0.02, 5.0])
ymax = math.ceil(np.max(data[cut]['rmsROOT'][index_sorted]))
print ymax

ax1.set_ylim([-0.1, ymax])

# labeling
ax1.set_title(title_plot)
ax1.set_xlabel(xdata.replace("_", " "))
ax1.set_ylabel("kinkangle")

# grids
ax1.grid(True)

# legend
#ax1.legend()
#handles, labels = ax1.get_legend_handles_labels()
## reverse to keep order consistent
#ax1.legend(reversed(handles), reversed(labels),
#			loc='center left',
#			bbox_to_anchor=(1, 0.5),
#			prop={'size':12})
ax1.legend(
			loc='center left',
			bbox_to_anchor=(1, 0.5),
			prop={'size':12})

name_save =  "output/" + title_save + str(".pdf")
fig.savefig(name_save)
print "evince " + name_save + "&"
