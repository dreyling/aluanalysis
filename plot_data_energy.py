#! /usr/bin/python
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import math

from myparams import * 

print "Starting script:", sys.argv[0]


#####################################
# Open npy file
if len(sys.argv) < 2:
  print "No data input. Run get_hist_data.py or select npy-file in data/..."
  exit()
input_file = sys.argv[1]
data = np.load(input_file)

# scattering angle, y-axis data
if len(sys.argv) < 3:
  print "please select data..."
  print data.dtype
  exit()
scattering_data = sys.argv[2]


####################
# iterators
# seven elements
thicknesses = np.array([0.013, 0.025, 0.05, 0.1, 0.2, 1.0, 10.0])
markers = ['^', 'd', 's', 'p', '*', 'h', 'o']
markersizes = [6, 6, 6, 8, 10, 10, 10]
# five
colors = ['0.0', '0.15', '0.3', '0.45', '0.6']
energies = [1., 2., 3., 4., 5.]

#####################
# output names
title_save = "kinkangle_" + input_file[5:-4] + "_" + scattering_data
title_plot = title_save.replace("_", " ")


#########################################
# Plotting
plotname = "energy"
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
for index, thickness in enumerate(thicknesses):
  # data
  cut = (data['thickness'] == thickness)
  ax1.plot(data[cut]['energy'], data[cut][scattering_data], 
			color='k', 
			label=r'$\theta_{\rm Al}(d_{\rm Al} = $' + str(thickness) + ' mm)' , 
			marker=markers[index], 
			markersize=markersizes[index] 
			)#linestyle='None')
  
# scaling and range
ax1.set_yscale("log")
ax1.set_xlim([0.5, 5.5])
#ax1.set_ylim([0.02, 5.0])
#ax2.set_ylim([-0.25, 0.19])

# labeling
ax1.set_title(title_plot)
ax1.set_xlabel("beam energy [GeV]")
ax1.set_ylabel(scattering_data.replace("_", " "))

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

name_save =  "output/" + title_save + "_" + plotname + str(".pdf") 
fig.savefig(name_save)
print "evince " + name_save + "&"

