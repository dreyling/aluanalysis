#! /usr/bin/python
import inspect, os
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
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

# Getting runlist
runlist = mrr.readRunlist(name_runlist)

# getting right runindex
runindex = np.intersect1d(np.where(runlist['thickness'] == float(thickness)), np.where(runlist['energy'] == float(energy)))[0]
runnr = runlist['runnr'][runindex]
print "selected run:", runnr

# Getting histogram data
contents, counts, bincenters_x, bincenters_y, edges_x, edges_y = mrr.getProfile2Data(runlist, runindex, coll_name, name_path, name_suffix, name_rootfolder)



print bincenters_x, bincenters_y
print edges_x, edges_y
print np.size(bincenters_x), np.size(bincenters_y)
print np.size(edges_x), np.size(edges_y)


index = np.where(bincenters_x == -9.02)
print index
print np.size(contents)
print np.shape(contents)

print np.size(contents[74])
print contents[75]






# plot
print contents[contents != 0.]
print np.shape(contents[contents != 0.])
print np.mean(contents[contents != 0.])
print np.min(contents[contents != 0.])
print np.max(contents[contents != 0.])

projection_x, projection_y = mdp.get_projections(contents, bincenters_x, bincenters_y)



#print projection_x, projection_y
print np.shape(projection_x)
print np.shape(projection_y)
print np.shape(contents)


print bincenters_x
print contents[:100]





#####################
# output names
title_save = "run" + str(runnr)[:-2] + "_" + energy + "GeV" + "_" + thickness + "mm" + "_" + coll_name 
title_plot = title_save.replace("_", " ")


##########################################
# Plotting Data
#fig = plt.subplots(figsize=(6, 4))#, dpi=100)
#fig.subplots_adjust(left=0.11, right=0.99, top=0.94, bottom=0.12)

fig = plt.figure(1, figsize=(5, 3))
fig.subplots_adjust(left=0.10, right=0.99, top=0.97, bottom=0.14)
# subplots-grid: rows, columns
grid = gridspec.GridSpec(3, 5, hspace=0.05, wspace=0.05)

# image
ax1 = plt.subplot(grid[1:, :4])
ax1.set_xlim(edges_x.min(), edges_x.max())
ax1.set_xlim(edges_x.min()+2.5, edges_x.min()+3.5)
ax1.set_ylim(edges_y.min(), edges_y.max())
ax1.set_ylim(edges_y.min()+1.5, edges_y.min()+2.5)
ax1.set_xlabel("x [mm]")
ax1.set_ylabel("y [mm]")

# x-Histogram
ax2 = plt.subplot(grid[:1, :4])#, sharex=ax1) 
#ax2.tick_params(labelbottom='off')    
ax2.set_xlim(edges_x.min(), edges_x.max())
ax2.set_ylabel("[mrad^2]")

# y-Histogram
ax3 = plt.subplot(grid[1:, 4:])#, sharey=ax1) 
ax3.set_ylim(edges_y.min(), edges_y.max())
#ax3.tick_params(labelleft='off')    


print edges_x.min(), edges_x.max(), edges_y.min(), edges_y.max()


# image

print np.size(bincenters_x)
print np.size(bincenters_y)

print np.shape(contents)
X, Y = np.meshgrid(bincenters_x, bincenters_y)
print X, Y
#ax1.contourf(bincenters_x, bincenters_y, contents.T, 
#        vmin=-1, vmax=75, 
 #       )
image = ax1.imshow(contents.T, 
        extent=(edges_x.min(), edges_x.max(), edges_y.min(), edges_y.max()), 
        interpolation="none", 
        vmin=-1, vmax=75, 
        cmap=cm.bone_r
        )
#plt.colorbar()#, ax=ax1)

#ax1.set_xlim(-9.2, -8.8), ax1.set_ylim(-6.5, 6.5)

# x-Histogram
ax2.plot(projection_x[0], projection_x[1])

# y-Histogram
ax3.plot(projection_y[1], projection_y[0])

# save name in folder
#plt.show()
name_save =  "output/" + title_save + str(".pdf") 
fig.savefig(name_save)
print "evince " + name_save + "&"
