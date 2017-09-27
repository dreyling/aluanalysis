'''plot opacity

Usage:
    plot_widths.py (--results=<results>)

Options:
    --results=<results>         npy file [required]
    -h --help                   show usage of this script
    -v --version                show the version of this script
'''

import numpy as np
from docopt import docopt

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

import highland

############################################
# arguments

arguments = docopt(__doc__, version='plot opacity')
# open npy result file
data = np.load(arguments['--results'])

############################################
# output names
title_save = "compare_opacity"
title_plot = title_save.replace("_", " ")

############################################
# Plotting Data
fig, ax = plt.subplots(figsize=(6, 6))#, dpi=100)
fig.subplots_adjust(left=0.11, right=0.95, top=0.94, bottom=0.10)
grid = gridspec.GridSpec(3, 1, hspace=0.0)
ax1 = plt.subplot(grid[:, :])

width = data['combined_one_si_norm'][data['thickness']>0.0]
opac_standard = data['opacity_highland_standard'][data['thickness']>0.0]
opac_electron =  data['opacity_highland_electron'][data['thickness']>0.0]
thickness = data['thickness'][data['thickness']>0.0]
energy = data['energy'][data['thickness']>0.0]

# highland x data
opacity = np.linspace(0.0, 0.5, 100)
#highland_standard = highland.highland_opacity_multi_scatterer_raw(opacity, thickness, highland.x0alu)
highland_electron = highland.highland_opacity_electrons(opacity)

#ax1.plot(opacity, highland_standard,
#            lw=1, label='Highland (multi-scattering)')
ax1.plot(opacity, highland_electron,
            lw=1, label='Highland (electron)')
# data
ax1.plot(opac_electron, width, 'kx')

# label
for index, value in enumerate(thickness):
    label = '    ' + str(thickness[index]) + 'mm / ' + str(energy[index]) + 'GeV'
    ax1.text(opac_electron[index], width[index], label,
            verticalalignment='bottom', horizontalalignment='center',
            rotation=90,
            fontsize=6)

# legend
ax1.legend(loc='lower right')

# scales
ax1.set_xscale("log")
ax1.set_xlim(0.0011, 0.45)
ax1.set_yscale("log")
ax1.set_ylim(0.015, 15)

ax1.set_title(title_plot)
ax1.set_xlabel(r'opacity $\epsilon^{0.555}/p$ [1/GeV]')
ax1.set_ylabel(r'scattering angle $\theta$ [mrad]')

################################################
# save name in folder
name_save =  "output/" + title_save + str(".pdf")
fig.savefig(name_save)
print "evince " + name_save + "&"
