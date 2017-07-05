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
#import math

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

#####################################
# Start

info = True#False

# Getting runlist
runlist = mrr.readRunlist(name_runlist)

# getting right runindex
runindex = np.intersect1d(np.where(runlist['thickness'] == float(thickness)), np.where(runlist['energy'] == float(energy)))[0]
runnr = runlist['runnr'][runindex]
print "selected run:", runnr

# Getting histogram data
contents, counts, bincenters_x, bincenters_y, edges_x, edges_y = mrr.getProfile2Data(runlist, runindex, coll_name, name_path, name_suffix, name_rootfolder)


#if coll_name == "gblsumkx2andsumky2_xybP":
#    contents = np.sqrt(contents)

data = mrr.getHist1Data(runlist, runindex, "gblsumkx2andsumky2", name_path, name_suffix, name_rootfolder)


print "histo mean", mdp.calc_hist_mean(data)



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
fig.subplots_adjust(left=0.13, right=0.97, top=0.97, bottom=0.14)
# subplots-grid: rows, columns
grid = gridspec.GridSpec(3, 5, hspace=0.05, wspace=0.05)

# settings
# image
ax1 = plt.subplot(grid[1:, :4])
ax1.set_xlim(edges_x.min(), edges_x.max())
ax1.set_ylim(edges_y.min(), edges_y.max())
ax1.set_xlabel(r'x triplet pos. at $z_{\rm SUT}$ [mm]')
ax1.set_ylabel(r'y triplet pos. at $z_{\rm SUT}$ [mm]')
# test views
if False:
    # bottom left corner
    ax1.set_xlim(edges_x.min()+2.9, edges_x.min()+3.5), ax1.set_ylim(edges_y.min()+1.9, edges_y.min()+2.5)
    # top right corner
    ax1.set_xlim(edges_x.min()+2.5+18, edges_x.min()+3+18), ax1.set_ylim(edges_y.min()+1.5+8, edges_y.min()+2.3+8)

# x-projection
ax2 = plt.subplot(grid[:1, :4], sharex=ax1) 
ax2.tick_params(labelbottom='off')    
ax2.set_xlim(edges_x.min(), edges_x.max())
ax2.set_ylim(np.min(projection_x[1]), np.max(projection_x[1]))
if coll_name == "gblsumkx2andsumky2_xybP":
    ax2.set_ylabel(r'$\theta_{\rm meas}$ [mrad]')
if coll_name == "gblsumkxandsumky_xyP":
    ax2.set_ylabel(r'$\alpha_{\rm eff}$ [mrad]')
tick_spacing_x = 0.05 
ax2.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing_x))

# y-projection
ax3 = plt.subplot(grid[1:, 4:], sharey=ax1) 
ax3.set_ylim(edges_y.min(), edges_y.max())
ax3.tick_params(labelleft='off')    
ax3.set_xlim(np.min(projection_y[1]), np.max(projection_y[1]))
if coll_name == "gblsumkx2andsumky2_xybP":
    ax3.set_xlabel(r'$\theta_{\rm meas}$ [mrad]')
if coll_name == "gblsumkxandsumky_xyP":
    ax3.set_xlabel(r'$\alpha_{\rm eff}$ [mrad]')
tick_spacing_y = 0.05 
ax3.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing_y))

# data window
if True:
    ax1.set_xlim(-9.5, 9.5)
    ax1.set_ylim(-4.5, 4.5)
    ax2.set_xlim(-9.5, 9.5)
    ax3.set_ylim(-4.5, 4.5)

# image
# for the right view 
# - content Matrix has to be transposed
# - and the y-edges has to be switched
# proofed by comparing with root visualization
image = ax1.imshow(contents.T, 
        # nominal: extent = (left, right, bottom, top)
        # y edges switched
        extent=(edges_x.min(), edges_x.max(), edges_y.max(), edges_y.min()), 
        interpolation="none", 
        # for automatic color map
        vmin=content_mean - content_std, vmax=content_mean + content_std, 
        # manual color map
        #vmin=0.5, vmax=0.75, 
        cmap=cm.bone_r
        )
#plt.colorbar()#, ax=ax1)

# x-projection
ax2.plot(projection_x[0], projection_x[1], color='k', lw=1, alpha=0.25)

# y-projection
# reverse here also the order of "y" values
ax3.plot(projection_y[1][::-1], projection_y[0], color='k', lw=1, alpha=0.25)

###############
# binned representation
number_merged_points = 50  

# x-projection
projection_x_means_pos_binned = projection_x[0].reshape(-1, number_merged_points).mean(axis=1)
projection_x_means_val_binned = projection_x[1].reshape(-1, number_merged_points).mean(axis=1)
projection_x_stds_val_binned = projection_x[1].reshape(-1, number_merged_points).std(axis=1)
#print np.size(projection_x[0])
#print np.size(projection_x_means_pos_binned)
ax2.errorbar(projection_x_means_pos_binned, projection_x_means_val_binned, 
        xerr=(projection_x_means_pos_binned[1]-projection_x_means_pos_binned[0])/2.,
        yerr=projection_x_stds_val_binned,
        capsize=0,
        marker='+',
        ls='None', 
        color='k'
        )

# x-projection
projection_y_means_pos_binned = projection_y[0].reshape(-1, number_merged_points).mean(axis=1)
projection_y_means_val_binned = projection_y[1].reshape(-1, number_merged_points).mean(axis=1)
projection_y_stds_val_binned = projection_y[1].reshape(-1, number_merged_points).std(axis=1)
#print np.size(projection_x[0])
#print np.size(projection_x_means_pos_binned)
ax3.errorbar(projection_y_means_val_binned[::-1], projection_y_means_pos_binned, 
        yerr=(projection_y_means_pos_binned[1]-projection_y_means_pos_binned[0])/2.,
        xerr=projection_y_stds_val_binned,
        capsize=0,
        marker='+',
        ls='None', 
        color='k'
        )



# save name in folder
#plt.show()
name_save =  "output/" + title_save + str(".pdf") 
fig.savefig(name_save)
print "evince " + name_save + "&"
