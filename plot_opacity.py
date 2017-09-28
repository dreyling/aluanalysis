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
from scipy.optimize import curve_fit

import highland
import my_fitfuncs as mff

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
#width = data['combined_si_g_norm'][data['thickness']>0.0]
#opac_standard = data['opacity_highland_standard'][data['thickness']>0.0]
opac_electron =  data['opacity_highland_electron'][data['thickness']>0.0]
thickness = data['thickness'][data['thickness']>0.0]
energy = data['energy'][data['thickness']>0.0]

# highland x data
opacity = np.logspace(-3, 1., 100)
highland_electron = highland.highland_opacity_electrons(opacity)
ax1.plot(opacity, highland_electron,
            lw=1, label='Highland (electron)')

# data
ax1.plot(opac_electron, width, 'kx')
#ax1.plot(opac_standard, width, 'rx')

# fit 
fitfunc = mff.fitfunc_linear #_zero
para0 = [13.0, 0.0]
xdata = opac_electron
ydata = width
para, cov = curve_fit(fitfunc, xdata, ydata, p0=para0)
print para
highland_fit = fitfunc(opacity, *para)
ax1.plot(opacity, highland_fit,
        lw=1, label='Highland (electron) fit\nslope = {:.3f}, offset = {:.3f}'.format(para[0], para[1]))


# label
for index, value in enumerate(thickness):
    label = '\,\,\,\,' + str(thickness[index]) + 'mm / ' + str(energy[index]) + 'GeV'
    ax1.text(opac_electron[index], width[index]*1.07, label,
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

#ax1.set_title(title_plot)
ax1.set_xlabel(r'opacity $\epsilon^{0.555}/p$ [1/GeV]')
ax1.set_ylabel(r'scattering angle $\theta$ [mrad]')

################################################
# save name in folder
name_save =  "output/" + title_save + str(".pdf")
fig.savefig(name_save)
print "evince " + name_save + "&"
