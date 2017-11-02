'''plot 2d profile

Usage:
    plot_and_analyze_profile2d.py (--configuration=<configuration> --energy=<energy> --thickness=<thickness> --data_type=<data_type>) [--rebin=<rebin>]

Options:
    --configuration=<configuration> yaml file [required]
    --energy=<energy>           energy in GeV [required]
    --thickness=<thickness>     thickness in mm [required]
    --data_type=<data_type>     'mean' or 'sigma' [required]
    --rebin=<rebin>             rebinning [default: 1]
    -h --help                   show usage of this script
    -v --version                show the version of this script
'''
import numpy as np
import yaml
from docopt import docopt
import math

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
from matplotlib.ticker import NullFormatter
import matplotlib.cm as cm
from mpl_toolkits.axes_grid1 import make_axes_locatable

params = {'text.latex.preamble' : [r'\usepackage{upgreek}']}
plt.rcParams.update(params)

import my_rootread as mrr
import my_fitfuncs as mff
import my_dataproc as mdp

############################################
# arguments
arguments = docopt(__doc__, version='plot 2d comparison')
# open yaml configuration file
configuration = yaml.load(open(arguments['--configuration']))
energy = arguments['--energy']
thickness = arguments['--thickness']
data_type = arguments['--data_type']


#####################################
# Getting runlist

runlist = mrr.read_csv_runlist(configuration['runlist'])

# Getting runindex
runindex = np.intersect1d(np.where(runlist['thickness'] == float(thickness)), np.where(runlist['energy'] == float(energy)))[0]
runnr = runlist['runnr'][runindex]

# Getting  data
contents, counts, bincenters_x, bincenters_y, edges_x, edges_y, errors = mrr.getProfile2Data(runlist, runindex,
        configuration['profile_collection'],
        configuration['root_path'],
        configuration['root_suffix'],
        configuration['root_folder'])

# output names

title_save = ("profile2d_" + data_type + "_run" + str(runnr)[:-2] + "_" +
        energy + "GeV" + "_" + thickness + "mm_" +
        "rebin" + arguments['--rebin'] + "_" + arguments['--configuration'][:-5])
title_plot = title_save.replace("_", " ")

#########################################
# Data 

if data_type == 'sigma':
    sigmas = np.multiply(np.sqrt(counts), errors)
    sigmas[np.isnan(sigmas)] = 0
    contents = sigmas

content_mean = np.mean(contents[contents != 0.])
content_std = np.std(contents[contents != 0.])

# projections
projection_x, projection_y = mdp.get_projections(contents, bincenters_x, bincenters_y)


##########################################
# Plot settings

fig = plt.figure(figsize=(5, 3))
fig.subplots_adjust(left=0.12, right=0.99, top=0.99, bottom=0.17)
# subplots-grid: rows, columns
grid = gridspec.GridSpec(3, 6, hspace=0.05, wspace=0.0)

# image
ax1 = plt.subplot(grid[1:, :4])
ax1.set_xlabel(r'$x_{\rm triplet}$ [mm]')
ax1.set_ylabel(r'$y_{\rm triplet}$ [mm]')
tick_spacing_2d = 2.
ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing_2d))
ax1.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing_2d))

# x-projection
ax2 = plt.subplot(grid[:1, :4], sharex=ax1)
ax2.tick_params(labelbottom='off')
ax2.set_ylabel(r'$\theta_{\rm meas}$ [mrad]', fontsize=8)

# y-projection
ax3 = plt.subplot(grid[1:, 5:], sharey=ax1)
ax3.tick_params(labelleft='off')
ax3.set_xlim(np.min(projection_y[1]), np.max(projection_y[1]))
ax3.set_xlabel(r'$\theta_{\rm meas}$ [mrad]', fontsize=8)

#################################################################3
# image
# for the right view 
# - content Matrix has to be transposed
# - and the y-edges has to be switched
# proofed by comparing with root visualization
factor = math.sqrt(0.5)
vmin = content_mean - factor*content_std
vmax = content_mean + factor*content_std

# mask zero entries white
contents = np.ma.masked_where(contents == 0., contents)
cmap = cm.viridis_r
cmap.set_bad(color='white')

image = ax1.imshow(contents.T,
        # nominal: extent = (left, right, bottom, top)
        # y edges switched
        extent=(edges_x.min(), edges_x.max(), edges_y.max(), edges_y.min()),
        interpolation="none",
        # for automatic color map
        vmin=vmin,
        vmax=vmax,
        cmap=cmap
        )

# for colorbar position, has to be after ax1 creation
ax4 = plt.subplot(grid[1:, 4:5])
ax4.set_axis_off()
# make axis beside, in order to scale colorbar
divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("left", "30%", pad="10%")
# shape colorbar
cb = fig.colorbar(image, cax=cax)
cax.tick_params(labelsize=8)
textbox = r'$\theta_{\rm meas}$ [mrad]'
cb.set_label(textbox, fontsize=8, labelpad=5)

###############
# binned representation
#number_merged_points = 1
number_merged_points = int(arguments['--rebin'])
#if int(arguments['--rebin']) > 1.:
#    title_save = ("profile2d_" + data_type + "_run" + str(runnr)[:-2] + "_" +
#            energy + "GeV" + "_" + thickness + "mm_" +
#            "rebin" + arguments['--rebin'])
#    title_plot = title_save.replace("_", " ")


#########################################
# x-projection, rebinned --> position, value/mean, value/std
projection_x_means_pos_binned = projection_x[0].reshape(-1, number_merged_points).mean(axis=1)
projection_x_means_val_binned = projection_x[1].reshape(-1, number_merged_points).mean(axis=1)
projection_x_n_binned = np.size(projection_x[1]) * number_merged_points
projection_x_stds_val_binned = projection_x[1].reshape(-1, number_merged_points).std(axis=1)/math.sqrt(projection_x_n_binned)

ax2.errorbar(projection_x_means_pos_binned, projection_x_means_val_binned,
        xerr=(projection_x_means_pos_binned[1]-projection_x_means_pos_binned[0])/2.,
#        yerr=projection_x_stds_val_binned*10,
        capsize=0,
        elinewidth=0.5,
        marker='o',
        markersize=1,
        ls='None',
        color='k'
        )

# scaling
projection_x_min = (np.min(projection_x_means_val_binned)-np.min(projection_x_stds_val_binned)*1.3)
projection_x_max = (np.max(projection_x_means_val_binned)+np.max(projection_x_stds_val_binned)*1.7)
#ax2.set_ylim(projection_x_min, projection_x_max)
tick_spacing_x = round((projection_x_max - projection_x_min)/3., 2)
ax2.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing_x))
ax2.tick_params(labelsize=8)

# fit
projection_x_fit_results = mff.fit_linear(np.vstack((projection_x_means_pos_binned, projection_x_means_val_binned)),
        projection_x_stds_val_binned, 0.0, 0.0)
print projection_x_fit_results
projection_x_fit_x = projection_x[0]
projection_x_fit_y = mff.fitfunc_linear(projection_x_fit_x, projection_x_fit_results['slope'], projection_x_fit_results['offset'])
ax2.plot(projection_x_fit_x, projection_x_fit_y,
    color='r', lw=1, ls='-')
textbox1 = (r'slope$_{\rm fit} = $ ' +
    '({:.1f}'.format(projection_x_fit_results['slope']*1000) +
    ' $\pm$ {:.1f})'.format(projection_x_fit_results['dslope']*1000) +
    r'$\frac{\upmu{\rm rad}}{\rm mm}$')
textbox2 = r'$\chi^2$/ndf = ' + '{:.1f}'.format(projection_x_fit_results['chi2red'])
ax2.text(0.05, 0.87, textbox1, transform=ax2.transAxes, fontsize=7,
        verticalalignment='top', horizontalalignment='left')#, bbox=props)

####################
# y-projection, rebinned --> position, value/mean, value/std
projection_y_means_pos_binned = projection_y[0].reshape(-1, number_merged_points).mean(axis=1)
projection_y_means_val_binned = projection_y[1].reshape(-1, number_merged_points).mean(axis=1)
projection_y_n_binned = np.size(projection_y[1]) * number_merged_points
projection_y_stds_val_binned = projection_y[1].reshape(-1, number_merged_points).std(axis=1)/math.sqrt(projection_y_n_binned)
ax3.errorbar(projection_y_means_val_binned[::-1], -1. * projection_y_means_pos_binned,
        yerr=(projection_y_means_pos_binned[1]-projection_y_means_pos_binned[0])/2.,
#        xerr=projection_y_stds_val_binned*10,
        capsize=0,
        elinewidth=0.5,
        marker='o',
        markersize=1,
        ls='None',
        color='k'
        )
# scaling
projection_y_min = (np.min(projection_y_means_val_binned)-np.min(projection_y_stds_val_binned)*1.2)
projection_y_max = (np.max(projection_y_means_val_binned)+np.max(projection_y_stds_val_binned)*2.6)
#ax3.set_xlim(projection_y_min, projection_y_max)
tick_spacing_y = round((projection_y_max - projection_y_min)/3., 2)
ax3.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing_y))
ax3.tick_params(labelsize=8)
for label in ax3.get_xmajorticklabels():
        label.set_rotation(-90)
# fit
projection_y_fit_results = mff.fit_linear(np.vstack((projection_y_means_pos_binned, projection_y_means_val_binned)),
        projection_y_stds_val_binned, 0.0, 0.0)
print projection_y_fit_results
projection_y_fit_pos = projection_y[0] # position
projection_y_fit_val = mff.fitfunc_linear(projection_y_fit_pos, projection_y_fit_results['slope'], projection_y_fit_results['offset']) # value
ax3.plot(projection_y_fit_val, projection_y_fit_pos,
    color='r', lw=1, ls='-')
textbox1 = (r'slope$_{\rm fit} = $ ' +
    '({:.1f}'.format(projection_y_fit_results['slope']*1000) +
    ' $\pm$ {:.1f})'.format(projection_y_fit_results['dslope']*1000) +
    r'$\frac{\upmu{\rm rad}}{\rm mm}$')
textbox2 = r'$\chi^2$/ndf = ' + '{:.1f}'.format(projection_y_fit_results['chi2red'])
ax3.text(0.86, 0.07, textbox1, transform=ax3.transAxes, fontsize=7,
        verticalalignment='bottom', horizontalalignment='right', rotation=-90)#, bbox=props)

# scaling all
xmin, xmax = -9.8, 9.8
ymin, ymax = -4., 4.
ax1.set_xlim(xmin, xmax)
ax1.set_ylim(ymin, ymax)
ax2.set_xlim(xmin, xmax)
ax3.set_ylim(ymin, ymax)

# save name in folder
name_save =  "output/" + title_save + str(".pdf")
fig.savefig(name_save)
print "evince " + name_save + "&"
