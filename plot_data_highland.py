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

# scattering data
if len(sys.argv) < 3:
  print "please select data..."
  print data.dtype
  exit()
scattering_data = sys.argv[2]

# only sample
start_sample = 0
end_sample = None
samples = 'all'

if len(sys.argv) < 4:
    print "please select samples: all or 5samples"
    exit()
if sys.argv[3] == '5samples':
    samples = '5samples'
    start_sample = 1
    end_sample = -1


####################
# iterators
# seven elements
thicknesses = np.array([0.013, 0.025, 0.05, 0.1, 0.2, 1.0, 10.0])[start_sample:end_sample]
markers = ['^', 'd', 's', 'p', '*', 'h', 'o'][start_sample:end_sample]
markersizes = [6, 6, 6, 8, 10, 10, 10][start_sample:end_sample]
# five
colors = ['0.0', '0.15', '0.3', '0.45', '0.6']
energies = [1., 2., 3., 4., 5.]

#####################
# output names
title_save = "kinkangle_" + input_file[5:-4] + "_" + scattering_data + "_" + samples
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
ax1 = plt.subplot(grid[:7, :])
ax2 = plt.subplot(grid[7:, :], sharex=ax1) 

# highland x data
highland_energy = np.linspace(0.5, 6, 50)
for index, thickness in enumerate(thicknesses):
  # highland theory 
  highland_y = highland_multi_scatterer(highland_energy, thickness, x0alu)
  ax1.plot(highland_energy, highland_y, 
			color='0.7',
      markeredgecolor='0.7',
			marker=markers[index], 
			markersize=4, 
			label=r'$\theta_{\rm High.}(\epsilon_{\rm Al} = $ ' + '{:.4f}'.format(thickness/x0alu) + ')')
  # data
  cut = (data['thickness'] == thickness)
  ax1.errorbar(data[cut]['energy'], data[cut][scattering_data], 
                        yerr=0.05*data[cut][scattering_data],
			color='k', 
			label=r'$\theta_{\rm Al}(d_{\rm Al} = $' + str(thickness) + ' mm)' , 
			marker=markers[index], 
			markersize=markersizes[index], 
			linestyle='None')
  # deviation: theory - measurement
  highland_points = highland_multi_scatterer(data[cut]['energy'], thickness, x0alu)
  deviation = (highland_points - data[cut][scattering_data]) / highland_points
  ax2.plot(data[cut]['energy'], deviation,
			color='0.5',
      markeredgecolor='0.5',
			marker=markers[index], 
			markersize=markersizes[index])
  
# scaling and range
ax1.set_yscale("log")
ax1.set_xlim([0.5, 5.5])
ax1.set_ylim([0.02, 5.0])
ax2.set_ylim([-0.25, 0.19])

# labeling
ax1.set_title(title_plot)
ax2.set_xlabel("beam energy [GeV]")
ax1.set_ylabel(r'$\theta_{\rm Al} = \sqrt{\theta_{\rm tot}^2 - \theta_{0}^2}$ [mrad]')
ax2.set_ylabel(r'$\sigma_{\rm norm.} = \frac{{\rm Highland}-{\rm meas.}}{\rm Highland}$')

# grids
ax1.grid(True)
ax2.grid(True)
ax2.axhline(0, color='k')
ax2.axhspan(-0.11, 0.11, alpha=0.5, color='yellow')

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

#############################################################
############################################################
plotname = 'thickness'
# figure
fig = plt.figure(figsize=(8, 8))#, dpi=100)
fig.subplots_adjust(left=0.11, right=0.7, top=0.94, bottom=0.1)
# subplots-grid: rows, columns
grid = gridspec.GridSpec(10, 1, hspace=0.05)
# layout
ax1 = plt.subplot(grid[:7, :])
ax2 = plt.subplot(grid[7:, :], sharex=ax1) 


# highland thickness data
highland_thickness = np.logspace(-3, 2, 100)

for index, energy in enumerate(energies):
  # highland theory 
  highland_y = highland_multi_scatterer(energy, highland_thickness, x0alu)
  ax1.plot(highland_thickness, highland_y, 
     color=colors[index],
     #markeredgecolor='0.7',
     #marker=markers[index], 
     #markersize=4, 
     linestyle = '--',
     linewidth = 2,
     label=r'$\theta_{\rm High.}(p = $ ' + '{:.1f}'.format(energy) + ' GeV)')
  # 2nd loop
  thickness_order = np.array([])
  deviations = np.array([])
  for index2, thickness in enumerate(thicknesses):
    cut  = (data['thickness'] == thickness)
    cut2 = (data[cut]['energy'] == energy)
    # data
    ax1.errorbar(data[cut][cut2]['thickness'], data[cut][cut2][scattering_data], 
      yerr=0.05*data[cut][cut2][scattering_data],
      color=colors[index],
      markeredgecolor=colors[index], 
      #label=r'$\theta_{\rm Al}(d_{\rm Al} = $ ' + str(thickness) + ' mm)' , 
      marker=markers[index2], 
      markersize=markersizes[index2], 
      linestyle='None')
    # deviation points
    highland_point = highland_multi_scatterer(energy, data[cut][cut2]['thickness'], x0alu)
    deviation = (highland_point - data[cut][cut2][scattering_data]) / highland_point
    deviations = np.append(deviations, deviation)
    thickness_order = np.append(thickness_order, data[cut][cut2]['thickness'])
    ax2.plot(data[cut][cut2]['thickness'], deviation,
      color=colors[index],
      markeredgecolor=colors[index], 
      marker=markers[index2], 
			markersize=markersizes[index2],
			linestyle='None')
  # deviation line per energy
  ax2.plot(thickness_order, deviations,
    color=colors[index])
  
   
# scaling and range
ax1.set_yscale("log")
ax1.set_xscale("log")
ax1.set_xlim([0.005, 15])
ax1.set_ylim([0.02, 5.0])
ax2.set_ylim([-0.25, 0.19])

# labeling
ax1.set_title(title_plot)
ax2.set_xlabel("thickness [mm]")
ax1.set_ylabel(r'$\theta_{\rm Al} = \sqrt{\theta_{\rm tot}^2 - \theta_{0}^2}$ [mrad]')
ax2.set_ylabel(r'$\sigma_{\rm norm.} = \frac{{\rm Highland}-{\rm meas.}}{\rm Highland}$')

# grids
ax1.grid(True)
ax2.grid(True)
ax2.axhline(0, color='k')
ax2.axhspan(-0.11, 0.11, alpha=0.5, color='yellow')
#ax.yaxis.set_major_formatter(matplotlib.ticker.LogFormatter())

# legend
ax1.legend(loc='center left', 
			bbox_to_anchor=(1, 0.5), 	
			prop={'size':12})  

name_save = "output/" + title_save + "_" + plotname + str(".pdf") 
fig.savefig(name_save)
print "evince " + name_save + "&"
