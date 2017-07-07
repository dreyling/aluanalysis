#! /usr/bin/python
import inspect, os
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.ticker as ticker
from matplotlib.ticker import NullFormatter
import matplotlib.cm as cm
import numpy as np
#from scipy.optimize import curve_fit
import math

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
coll_name 	= sys.argv[2]
print "collection:", coll_name

# 3rd/4th argument
energy 		= sys.argv[3]
print "selected energy:", energy
thickness = sys.argv[4]
print "selected thickness:", thickness


data_type = 'mean'

#####################################
# Start

info = False

# Getting runlist
runlist = mrr.readRunlist("../" + name_runlist)

# getting right runindex
runindex = np.intersect1d(np.where(runlist['thickness'] == float(thickness)), np.where(runlist['energy'] == float(energy)))[0]
runnr = runlist['runnr'][runindex]
print "selected run:", runnr

# Getting  data
contents, counts, bincenters_x, bincenters_y, edges_x, edges_y, errors = mrr.getProfile2Data(runlist, runindex, coll_name, name_path, name_suffix, name_rootfolder)





# data test
if info:
    print np.size(bincenters_x), np.size(bincenters_y)
    print np.size(edges_x), np.size(edges_y)
    print np.shape(contents), np.size(contents)
    print np.shape(contents[0]), np.size(contents[0])

    x_index = np.where(bincenters_x > -9.)[0][0:5]
    print x_index
    y_index = np.where(bincenters_y > -4.)[0][0:5]
    print y_index

    print bincenters_x[x_index] 
    print bincenters_y[y_index]
    print edges_x.min(), edges_x.max(), edges_y.min(), edges_y.max()
    print contents[x_index[0]:x_index[-1], y_index[0]:y_index[-1]]

# data analysis
content_mean = np.mean(contents[contents != 0.])
content_std = np.std(contents[contents != 0.])
if info:
    print "content not zero"
    print contents[contents != 0.]
    print np.shape(contents[contents != 0.])
    print "mean", content_mean
    print "std", content_std
    print "min", np.min(contents[contents != 0.])
    print "max", np.max(contents[contents != 0.])


# projections
projection_x, projection_y = mdp.get_projections(contents, bincenters_x, bincenters_y)

if info:
    #print projection_x, projection_y
    print np.shape(projection_x), projection_x
    print np.shape(projection_y), projection_y



#####################
# output names
title_save = "run" + str(runnr)[:-2] + "_" + energy + "GeV" + "_" + thickness + "mm" + "_" + coll_name 
title_plot = title_save.replace("_", " ")


##########################################
# Plotting Data
#fig = plt.subplots(figsize=(6, 4))#, dpi=100)
#fig.subplots_adjust(left=0.11, right=0.99, top=0.94, bottom=0.12)

fig = plt.figure(figsize=(5, 3))
fig.subplots_adjust(left=0.12, right=0.99, top=0.99, bottom=0.17)
# subplots-grid: rows, columns
grid = gridspec.GridSpec(3, 6, hspace=0.05, wspace=0.0)

# settings
# image
ax1 = plt.subplot(grid[1:, :4])
# image
#ax1.set_xlim(edges_x.min(), edges_x.max())
#ax1.set_ylim(edges_y.min(), edges_y.max())
ax1.set_xlabel(r'$x_{\rm triplet}$ [mm]')
ax1.set_ylabel(r'$y_{\rm triplet}$ [mm]')
tick_spacing_2d = 2.
ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing_2d))
ax1.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing_2d))
# test views
if False:
    # bottom left corner
    ax1.set_xlim(edges_x.min()+2.9, edges_x.min()+3.5), ax1.set_ylim(edges_y.min()+1.9, edges_y.min()+2.5)
    # top right corner
    ax1.set_xlim(edges_x.min()+2.5+18, edges_x.min()+3+18), ax1.set_ylim(edges_y.min()+1.5+8, edges_y.min()+2.3+8)

# x-projection
ax2 = plt.subplot(grid[:1, :4], sharex=ax1) 
ax2.tick_params(labelbottom='off')    
#ax2.set_xlim(edges_x.min(), edges_x.max())
ax2.set_ylabel(r'$\mu_{\alpha_{\rm eff}}$ [$\mu$rad]', fontsize=8)#, labelpad=0)

# y-projection
ax3 = plt.subplot(grid[1:, 5:], sharey=ax1) 
#ax3.set_ylim(edges_y.min(), edges_y.max())
ax3.tick_params(labelleft='off')    
ax3.set_xlim(np.min(projection_y[1]), np.max(projection_y[1]))
ax3.set_xlabel(r'$\mu_{\alpha_{\rm eff}}$ [$\mu$rad]', fontsize=8)#, labelpad=0)
#ax3.set_xticklabels(ax3.xaxis.get_majorticklabels(), rotation=90)


#################################################################3
# image
# for the right view 
# - content Matrix has to be transposed
# - and the y-edges has to be switched
# proofed by comparing with root visualization
vmin=content_mean - content_std 
vmax=content_mean + content_std 

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
        #vmin = 0.,
        vmax=vmax, 
        cmap=cmap
        )

# for colorbar position, has to be after ax1 creation
ax4 = plt.subplot(grid[1:, 4:5]) 
ax4.set_axis_off()
# make axis beside, in order to scale colorbar
from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("left", "30%", pad="10%")
# shape colorbar
cb = fig.colorbar(image, cax=cax)
cb.set_ticks([round(vmin, 2), round(vmin, 2)/2, 0, round(vmax, 2)/2, round(vmax, 2)])
cax.tick_params(labelsize=8)
textbox = r'$\mu_{\alpha_{\rm eff}}$ [mrad]'
cb.set_label(textbox, fontsize=8, labelpad=0)
#ax4.text(-0.3, -0.15, textbox, transform=ax4.transAxes, fontsize=8,
#        verticalalignment='bottom', horizontalalignment='left')#, bbox=props)
#tick_spacing_cm = 0.02 #round((np.max(projection_y[1]) - np.min(projection_y[1]))/3., 2)
#cax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing_cm))
#cax.tick_params(labelsize=10)

# x-projection
#ax2.plot(projection_x[0], projection_x[1], color='k', lw=1, alpha=0.25)

# y-projection
# reverse here also the order of "y" values
#ax3.plot(projection_y[1][::-1], projection_y[0], color='k', lw=1, alpha=0.25)

###############
# binned representation
number_merged_points = 50  

#########################################
# x-projection, rebinned --> position, value/mean, value/std
projection_x_means_pos_binned = projection_x[0].reshape(-1, number_merged_points).mean(axis=1)
projection_x_means_val_binned = projection_x[1].reshape(-1, number_merged_points).mean(axis=1)
projection_x_n_binned = np.size(projection_x[1]) * number_merged_points
projection_x_stds_val_binned = projection_x[1].reshape(-1, number_merged_points).std(axis=1)/math.sqrt(projection_x_n_binned)
#print np.size(projection_x_stds_val_binned)

ax2.errorbar(projection_x_means_pos_binned, projection_x_means_val_binned*1000, 
        xerr=(projection_x_means_pos_binned[1]-projection_x_means_pos_binned[0])/2.,
        yerr=projection_x_stds_val_binned*1000,
        capsize=0,
        marker='+',
        ls='None', 
        color='k'
        )
# scaling
projection_x_min = np.min(projection_x_means_val_binned)-np.min(projection_x_stds_val_binned)*5.
projection_x_max = np.max(projection_x_means_val_binned)+np.max(projection_x_stds_val_binned)*5.
projection_x_min = projection_x_means_val_binned[0] - projection_x_stds_val_binned[0]*5.
projection_x_max = projection_x_means_val_binned[0] + projection_x_stds_val_binned[0]*5.
ax2.set_ylim(projection_x_min, projection_x_max)
ax2.set_ylim(-0.0035*1000, 0.005*1000)
tick_spacing_x = 0.002*1000 #round(abs(projection_x_max - projection_x_min)/3., 2)
#round((np.max(projection_x_means_val_binned)+np.max(projection_x_stds_val_binned) - np.min(projection_x_means_val_binned)-np.min(projection_x_stds_val_binned))/3., 2)
ax2.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing_x))
ax2.tick_params(labelsize=8)
# fit
projection_x_fit_results = mff.fit_linear(np.vstack((projection_x_means_pos_binned, projection_x_means_val_binned)),
        projection_x_stds_val_binned, 0.0, 0.0)
print projection_x_fit_results
projection_x_fit_x = projection_x[0]
projection_x_fit_y = mff.fitfunc_linear(projection_x_fit_x, projection_x_fit_results['slope'], projection_x_fit_results['offset'])
ax2.plot(projection_x_fit_x, projection_x_fit_y*1000,
    color='r', lw=1, ls='-')
#print round(projection_x_fit_results['slope'], 5), round(projection_x_fit_results['dslope'], 5)
#print projection_x_fit_results['chi2red']
#props = dict(boxstyle='square,pad=0.6', facecolor='white', alpha=1.0)
textbox1 = (r'slope$_{\rm fit} = $ ' + 
    '({:.2f}'.format(projection_x_fit_results['slope']*1000) + 
    ' $\pm$ {:.2f})'.format(projection_x_fit_results['dslope']*1000) + 
    r'$\frac{\mu{\rm rad}}{\rm mm}$')
textbox2 = r'$\chi^2$/ndf = ' + '{:.1f}'.format(projection_x_fit_results['chi2red'])
ax2.text(0.92, 0.88, textbox1 + '\n' + textbox2, transform=ax2.transAxes, fontsize=7,
        verticalalignment='top', horizontalalignment='right')#, bbox=props)

####################
# y-projection, rebinned --> position, value/mean, value/std
projection_y_means_pos_binned = projection_y[0].reshape(-1, number_merged_points).mean(axis=1)
projection_y_means_val_binned = projection_y[1].reshape(-1, number_merged_points).mean(axis=1)
projection_y_n_binned = np.size(projection_y[1]) * number_merged_points
projection_y_stds_val_binned = projection_y[1].reshape(-1, number_merged_points).std(axis=1)/math.sqrt(projection_y_n_binned)

ax3.errorbar(projection_y_means_val_binned[::-1]*1000, projection_y_means_pos_binned, 
        yerr=(projection_y_means_pos_binned[1]-projection_y_means_pos_binned[0])/2.,
        xerr=projection_y_stds_val_binned*1000,
        capsize=0,
        marker='+',
        ls='None', 
        color='k'
        )
# scaling
projection_y_min = (np.min(projection_y_means_val_binned)-np.min(projection_y_stds_val_binned))*1.8
projection_y_max = (np.max(projection_y_means_val_binned)+np.max(projection_y_stds_val_binned))*1.8
#ax3.set_xlim(projection_y_min, projection_y_max)
ax3.set_xlim(-0.0035*1000, 0.0058*1000)
tick_spacing_y = 0.002*1000 #round((projection_y_max - projection_y_min)/3., 2)
#round((np.max(projection_x_means_val_binned)+np.max(projection_x_stds_val_binned) - np.min(projection_x_means_val_binned)-np.min(projection_x_stds_val_binned))/3., 2)
ax3.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing_y))
ax3.tick_params(labelsize=8)
for label in ax3.get_xmajorticklabels():
        label.set_rotation(-90)
# fit
projection_y_fit_results = mff.fit_linear(np.vstack((projection_y_means_pos_binned, projection_y_means_val_binned)),
        projection_y_stds_val_binned, 0.0, 0.0)
print projection_y_fit_results
projection_y_fit_x = projection_y[0]
projection_y_fit_y = mff.fitfunc_linear(projection_y_fit_x, projection_y_fit_results['slope'], projection_y_fit_results['offset'])
ax3.plot(projection_y_fit_y*1000, projection_y_fit_x,
    color='r', lw=1, ls='-')
#print round(projection_x_fit_results['slope'], 5), round(projection_x_fit_results['dslope'], 5)
#print projection_x_fit_results['chi2red']
#props = dict(boxstyle='square,pad=0.6', facecolor='white', alpha=1.0)
textbox1 = (r'slope$_{\rm fit} = $ ' + 
    '({:.2f}'.format(projection_y_fit_results['slope']*1000) + 
    ' $\pm$ {:.2f})'.format(projection_y_fit_results['dslope']*1000) +
    r'$\frac{\rm mrad}{\rm mm}$')
textbox2 = r'$\chi^2$/ndf = ' + '{:.1f}'.format(projection_y_fit_results['chi2red'])
ax3.text(0.86, 0.07, textbox1 + '\n' + textbox2, transform=ax3.transAxes, fontsize=7,
        verticalalignment='bottom', horizontalalignment='right', rotation=-90)#, bbox=props)


xmin, xmax = -9.8, 9.8
ymin, ymax = -4., 4.
ax1.set_xlim(xmin, xmax)
ax1.set_ylim(ymin, ymax)
ax2.set_xlim(xmin, xmax)
ax3.set_ylim(ymin, ymax)

# save name in folder
#plt.show()
name_save =  "output/" + title_save + "_" + data_type + str(".pdf") 
fig.savefig(name_save)
print "evince " + name_save + "&"
