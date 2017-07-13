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

params = {'text.latex.preamble' : [r'\usepackage{upgreek}']}
plt.rcParams.update(params)

sys.path.insert(0, '../')
import my_rootread as mrr
import my_fitfuncs as mff
import my_dataproc as mdp

from myparams import * 

############################################
# setting which data
print "Starting script:", sys.argv[0]

name_path = "/home/jande/Documents/fhl-wgs01/afs/desy.de/user/h/hjansen/public/JDE/"
name_file = "run001017-GBLKinkEstimator_kappa100_highres_fixedalign.root"
root_file = name_path + name_file
root_folder = "Fitter06/GBL/"
coll_name = "gblsumkxandsumky_xyP"

# Getting  data
contents, counts, bincenters_x, bincenters_y, edges_x, edges_y, errors = mrr.getProfile2DataRaw(
        root_file, root_folder, coll_name)


#########################################
# calculate sigmas from ROOT content
sigmas = np.multiply(np.sqrt(counts), errors)
#print np.shape(sigmas)
#print np.isnan(sigmas)

# setting nan to 0
#sigmas[np.isnan(sigmas)] = 0.0
#print np.shape(sigmas)
#print np.isnan(sigmas)

# cut window 
if True:
    window_xmin = np.where(bincenters_x < -9.0)[0][-1]+1
    window_xmax = np.where(bincenters_x > 9.0)[0][0]
    window_ymin = np.where(bincenters_y < -4.0)[0][-1]+1
    window_ymax = np.where(bincenters_y > 4.0)[0][0]
    #print window_xmin, window_xmax
    #print window_ymin, window_ymax
    #print np.shape(sigmas[window_xmin:window_xmax, window_ymin:window_ymax])
    sigmas[:window_xmin, :] = 0.0
    sigmas[:, :window_ymin] = 0.0
    sigmas[window_xmax:, :] = 0.0
    sigmas[:, window_ymax:] = 0.0

# define as content to keep names
contents = sigmas

# data analysis
content_mean = np.mean(contents[contents != 0.])
content_std = np.std(contents[contents != 0.])
if True:
    print "content not zero"
    print contents[contents != 0.]
    print np.shape(contents[contents != 0.])
    print "mean", content_mean
    print "std", content_std
    print "min", np.min(contents[contents != 0.])
    print "max", np.max(contents[contents != 0.])


#####################
# output names
data_type = 'error'
title_save = "tomography_example_run001017"
title_plot = title_save.replace("_", " ")


##########################################
# Plotting Data
fig = plt.figure(figsize=(5, 3))
fig.subplots_adjust(left=0.11, right=0.91, bottom=0.2)

# subplot
grid = gridspec.GridSpec(1, 1)

# settings
ax1 = plt.subplot(grid[:, :])
xmin, xmax = -9.5, 9.5
ax1.set_xlim(xmin=xmin, xmax=xmax)
ymin, ymax = -5.05, 5.05
ax1.set_ylim(ymin=ymin, ymax=ymax)
ax1.set_xlabel(r'$x_{\rm triplet}$ [mm]')
ax1.set_ylabel(r'$y_{\rm triplet}$ [mm]')
tick_spacing_2d = 2.
ax1.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing_2d))
ax1.yaxis.set_major_locator(ticker.MultipleLocator(tick_spacing_2d))

# image
# for the right view 
# - content Matrix has to be transposed
# - and the y-edges has to be switched
# proofed by comparing with root visualization
vmin = content_mean - 1.*content_std 
vmax = content_mean + 2.0*content_std 

# mask zero entries white
contents = np.ma.masked_where(contents == 0., contents)
cmap = cm.viridis_r
cmap.set_bad(color='white')

# imshow
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
#ax1.autoscale(True)

# for colorbar position, has to be after ax1 creation
# make axis beside, in order to scale colorbar
from mpl_toolkits.axes_grid1 import make_axes_locatable
divider = make_axes_locatable(plt.gca())
cax = divider.append_axes("right", size="5%", pad="0%")
# shape colorbar
cb = fig.colorbar(image, cax=cax)
#cb.set_ticks([0.5, 0.7, 0.9, 1.1])
cax.tick_params(labelsize=8)
textbox = r'$\theta_{\rm meas}$ [mrad]'
cb.set_label(textbox, fontsize=8, labelpad=5)

################################
# save name in folder
name_save =  "output/" + title_save + "_" + data_type + str(".eps") 
fig.savefig(name_save)
print "evince " + name_save + "&"
