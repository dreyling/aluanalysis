'''plot widths.py

Usage:
    plot_widths.py (--results=<results>)

Options:
    --results=<results>         npy file [required]
    -h --help                   show usage of this script
    -v --version                show the version of this script
'''

import numpy as np
import math
from docopt import docopt

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

############################################
# arguments

arguments = docopt(__doc__, version='plot widths')
# open npy result file
data = np.load(arguments['--results'])

scattering_xdata = 'energy'

widths = ['rmsROOT_norm', 'rmsfrac_norm', 'gauss_si_norm', 'combined_si_g_norm', 'combined_si_s_norm', 'combined_one_si_norm']

datastart = 5


####################
# iterators
# seven elements
thicknesses = np.array([0.013, 0.025, 0.05, 0.1, 0.2, 1.0, 10.0])[datastart:]
markers = ['^', 'd', 's', 'p', '*', 'h', 'o'][datastart:]
markersizes = [6, 6, 6, 8, 10, 10, 10][datastart:]
# five
colors = ['0.0', '0.15', '0.3', '0.45', '0.6']
energies = [1., 2., 3., 4., 5.]

#####################
# output names
title_save = "kinkangle_" + "width" + "-vs-" + scattering_xdata
title_plot = title_save.replace("_", " ")


#########################################
# Plotting
# figure
fig = plt.figure(figsize=(8, 8))#, dpi=100)
fig.subplots_adjust(left=0.11, right=0.7, top=0.94, bottom=0.1)
# subplots-grid: rows, columns
grid = gridspec.GridSpec(10, 1, hspace=0.05)
# layout
ax1 = plt.subplot(grid[:, :])
#ax2 = plt.subplot(grid[7:, :], sharex=ax1) 

# highland x data
highland_energy = np.linspace(0.5, 6, 50)

for width_index, width_value in enumerate(widths):
    for index, thickness in enumerate(thicknesses):
      # data
      cut = (data['thickness'] == thickness)
      ax1.plot(data[cut][scattering_xdata], data[cut][width_value],
                            label=r'$\theta_{\rm Al}(d_{\rm Al} = $' + str(thickness) + ' mm)\n' + width_value.replace("_", " "),
                            marker=markers[index],
                            markersize=markersizes[index]
                            )

# scaling and range
#ax1.set_yscale("log")
#ax1.set_xlim([0.5, 5.5])
#ax1.set_ylim([0.02, 5.0])
ax1.set_ylim([-0.25, 6.0])

# labeling
ax1.set_title(title_plot)
ax1.set_xlabel(scattering_xdata.replace("_", " "))
ax1.set_ylabel("widths")

# grids
ax1.grid(True)

# legend
ax1.legend()
handles, labels = ax1.get_legend_handles_labels()
# reverse to keep order consistent
ax1.legend(reversed(handles), reversed(labels),
			loc='center left',
			bbox_to_anchor=(1, 0.5),
			prop={'size':12})

name_save =  "output/" + title_save + str(".pdf")
fig.savefig(name_save)
print "evince " + name_save + "&"
