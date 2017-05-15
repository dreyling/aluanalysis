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
if sys.argv[1] == None:
  print "No data input. Run get_hist_data.py or select npy-file in data/..."
  exit()
input_file = sys.argv[1]
data = np.load(input_file)

#########################################
# Plotting
plotname = "energy"
# figure
fig = plt.figure(figsize=(8, 8))#, dpi=100)
fig.subplots_adjust(left=0.1, right=0.7, top=0.94, bottom=0.1)
# subplots-grid: rows, columns
grid = gridspec.GridSpec(10, 1, hspace=0.05)
# layout
ax1 = plt.subplot(grid[:7, :])
ax2 = plt.subplot(grid[7:, :], sharex=ax1) 

# iterators
thicknesses = [0.013, 0.025, 0.05, 0.1, 0.2, 1.0, 10.0]
markers = ['^', 'd', 's', 'p', '*', 'h', 'o']
markersizes = [6, 6, 6, 8, 10, 10, 10]
colors = ['0.2', '0.3', '0.4', '0.5', '0.6']
# highland x data
highland_x = np.linspace(0.5, 6, 50)
for index, thickness in enumerate(thicknesses):
  # highland theory 
  highland_y = highland_multi_scatterer(highland_x, thickness, x0alu)
  ax1.plot(highland_x, highland_y, 
			color='0.7',
      markeredgecolor='0.7',
			marker=markers[index], 
			markersize=4, 
			label=r'$\theta_{\rm High.}(\epsilon_{\rm Al} = $' + '{:.4f}'.format(thickness/x0alu) + ')')
  # data
  cut = (data['thickness'] == thickness)
  ax1.plot(data[cut]['energy'], data[cut]['rms98_norm'], 
			color='k', 
			label=r'$\theta_{\rm Al}(d_{\rm Al} = $' + str(thickness) + ' mm)' , 
			marker=markers[index], 
			markersize=markersizes[index], 
			linestyle='None')
  # deviation: theory - measurement
  highland_points = highland_multi_scatterer(data[cut]['energy'], thickness, x0alu)
  deviation = (highland_points - data[cut]['rms98_norm']) / highland_points
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
ax1.set_title("kink angle, (" + input_file[5:-4].replace("_", " ") + ")")
ax2.set_xlabel("beam energy [GeV]")
ax1.set_ylabel(r'$\theta_{\rm Al,\,rms_{98}} = \sqrt{\theta_{\rm tot,\,rms_{98}}^2 - \theta_{0,rms_{98}}^2}$ [mrad]')
ax2.set_ylabel(r'$\sigma_{\rm norm.} = \frac{{\rm Highland}-{\rm meas.}}{\rm Highland}$')

# grids
ax1.grid(True)
ax2.grid(True)
ax2.axhline(0, color='k')
ax2.axhspan(-0.11, 0.11, alpha=0.5, color='yellow')
#ax.yaxis.set_major_formatter(matplotlib.ticker.LogFormatter())

# legend
ax1.legend()
handles, labels = ax1.get_legend_handles_labels()
# reverse to keep order consistent
ax1.legend(reversed(handles), reversed(labels), 
			loc='center left', 
			bbox_to_anchor=(1, 0.5), 	
			prop={'size':12})  

nameSave =  "output/" + sys.argv[1][5:-4] + "_" + plotname + str(".pdf") 
fig.savefig(nameSave)
print "evince " + nameSave + "&"


##########################################################################
# epsilon
plotname = 'epsilon'

# figure
fig = plt.figure(figsize=(8, 8))#, dpi=100)
fig.subplots_adjust(left=0.1, right=0.7, top=0.94, bottom=0.1)
# subplots-grid: rows, columns
grid = gridspec.GridSpec(10, 1, hspace=0.05)
# layout
ax1 = plt.subplot(grid[:7, :])
ax2 = plt.subplot(grid[7:, :], sharex=ax1) 


thicknesses = [0.013, 0.025, 0.05, 0.1, 0.2, 1.0, 10.0]
markers = ['^', 'd', 's', 'p', '*', 'h', 'o']
markersizes = [6, 6, 6, 8, 10, 10, 10]
colors = ['0.4', '0.5', '0.6', '0.7', '0.8']
# highland x data
highland_thickness = np.linspace(0.001, 10, 100)

#print highland_multi_scatterer(1.0, highland_thickness, x0alu)

#exit()


for index, thickness in enumerate(thicknesses):
  cut = (data['thickness'] == thickness)
  #print data[cut]['thickness'], data[cut]['energy'], data[cut]['rms98_norm']
  for index2, energy in enumerate(data[cut]['energy']):
    # highland theory 
    highland_y = highland_multi_scatterer(energy, highland_thickness, x0alu)
    ax1.plot(highland_thickness, highland_y, 
       color='0.7',
       markeredgecolor='0.7',
       marker=markers[index], 
       markersize=4, 
       label=r'$\theta_{\rm High.}(\epsilon_{\rm Al} = $' )#+ '{:.4f}'.format(thickness/x0alu) + ')')
    #data
    #print colors[int(energy-1)], energy, data[cut]['energy'][index2]
    ax1.plot(data[cut]['thickness'][index2], data[cut]['rms98_norm'][index2], 
			color=colors[int(energy-1)], 
			#label=thickness, 
			marker=markers[index], 
			markersize=markersizes[index], 
			linestyle='None')
  # for the legend, fake plot
  plt.plot(data[cut]['thickness'], data[cut]['rms98_norm']/10000, 
			color='0.6', 
			label=thickness, 
			marker=markers[index], 
			markersize=markersizes[index], 
			linestyle='None')

# scaling and range
plt.xscale("log")
plt.yscale("log")
#plt.xlim([0.008, 0.6])
#plt.ylim([0.01, 4.0])

# labeling
ax1.set_title("kink angle (gblaxprime6, 1 scatterer)")
ax1.set_xlabel("$\sqrt{\epsilon}$")
ax1.set_ylabel(r'$\sqrt{\theta_{rms_{98}}^2 - \theta_{0,rms_{98}}^2}$ [mrad]')
plt.grid(True)
#ax.yaxis.set_major_formatter(matplotlib.ticker.LogFormatter())

# legend
ax1.legend()
handles, labels = ax1.get_legend_handles_labels()
# reverse to keep order consistent
ax1.legend(reversed(handles), reversed(labels), 
			loc='center left', 
			bbox_to_anchor=(1, 0.5), 	
			prop={'size':12})  

#plt.show()
nameSave =  "output/" + sys.argv[1][5:-4] + "_" + plotname + str(".pdf") 
fig.savefig(nameSave)
print "evince " + nameSave + "&"
