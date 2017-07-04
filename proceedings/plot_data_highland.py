#! /usr/bin/python
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
import math

from matplotlib import rcParams
rcParams['xtick.direction'] = 'in'
rcParams['ytick.direction'] = 'in'

sys.path.insert(0, '../')
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
#markers = ['^', 'd', 's', 'p', '*', 'h', 'o'][start_sample:end_sample]
markers = ['o', 'o', 'o', 'o', 'o', 'o', 'o'][start_sample:end_sample]
#markers = ['x', 'x', 'x', 'x', 'x', 'x', 'x'][start_sample:end_sample]
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
fig = plt.figure(figsize=(8, 4), dpi=100)
fig.subplots_adjust(left=0.10, right=0.99, top=0.97, bottom=0.12)
# subplots-grid: rows, columns
grid = gridspec.GridSpec(3, 2, hspace=0.03, wspace=0.35)
# layout
ax1 = plt.subplot(grid[:2, :1])
ax2 = plt.subplot(grid[2:, :1], sharex=ax1) 
#ax3 = plt.subplot(grid[:, 2:3])
ax4 = plt.subplot(grid[:2, 1:])
ax5 = plt.subplot(grid[2:, 1:], sharex=ax4) 

# element order
ax1.set_axisbelow(True)
ax2.set_axisbelow(True)
ax4.set_axisbelow(True)
ax5.set_axisbelow(True)

# grids
ax1.grid(True, color='k', lw='0.2', ls='-')
ax2.grid(True, color='k', lw='0.2', ls='-')
ax2.yaxis.grid(False)
ax2.axhline(0, color='k', lw='0.5')
#ax2.axhspan(-0.11, 0.11, alpha=0.5, color='yellow')
ax2.axhline(-0.11, color='k', lw='0.5', ls=':')
ax2.axhline(+0.11, color='k', lw='0.5', ls=':')




# highland x data
highland_energy = np.linspace(0.0, 6, 100)

for index, thickness in enumerate(thicknesses):
  ###########
  # highland 
  highland_y = highland_multi_scatterer(highland_energy, thickness, x0alu)
  ax1.plot(highland_energy, highland_y, 
			color='k', 
                        ls=':'
			)

  ######
  # data
  cut = (data['thickness'] == thickness)
  # data, markers, greyscaled 
  data_energy = data[cut]['energy']
  data_scattering = data[cut][scattering_data] 
  for index2, energy in enumerate(energies):
  	ax1.errorbar(data_energy[index2], data_scattering[index2], 
                        #yerr=0.05*data[cut][scattering_data],
      			color=colors[int(data_energy[index2]-1)],
      			markeredgecolor=colors[int(data_energy[index2]-1)],
			marker=markers[index], 
			linestyle='None')
  
  ########################
  # deviation: measurement - theory
  highland_points = highland_multi_scatterer(data[cut]['energy'], thickness, x0alu)
  deviation = (data[cut][scattering_data] - highland_points) / highland_points
  # line
  ax2.plot(data[cut]['energy'], deviation,
    			color='k',
    			ls='-', lw=0.5)
  # markers
  for index2, energy in enumerate(energies):
  	# points
	ax2.plot(data_energy[index2], deviation[index2],
      			color=colors[int(data_energy[index2]-1)],
      			markeredgecolor=colors[int(data_energy[index2]-1)],
			ls = 'None',
			marker=markers[index],
                        markersize=5,
			)

  # thickness text
  thick_text = str(thickness) + ' mm' # print thick_text
  props = dict(boxstyle='square', pad=0.1, facecolor='white', edgecolor='none', alpha=0.8)
  x_position = 3.5
  y_position = highland_multi_scatterer(x_position, thickness, x0alu)
  ax1.text(x_position, y_position, thick_text, rotation=-9, fontsize=6.5, #linespacing=1.5,
        verticalalignment='center', horizontalalignment='center', bbox=props)

##################
# highland text
highland_text = "Highland's\n11\% accuracy"
props = dict(boxstyle='square', pad=0.1, facecolor='white', edgecolor='none', alpha=0.8)
x_position = 0.5
y_position = 0.0
ax2.text(x_position, y_position, highland_text, rotation=90, fontsize=6.5, #linespacing=1.5,
      verticalalignment='center', horizontalalignment='center', bbox=props)


# data point for legend
ax1.errorbar(data[cut]['energy']+10, data[cut][scattering_data], 
			color='0.3', 
                        markeredgecolor='0.3',
			label=r'$\theta_{\rm Al}$' , 
			marker=markers[index], 
			linestyle='None')
# HL legend
highland_y = highland_multi_scatterer(highland_energy, 10000., x0alu)
ax1.plot(highland_energy, highland_y, 
			color='k',#0.7',
			ls = ':', lw=1,
			label=r'$\theta_{\rm HL}$')


# scaling and range
ax1.set_yscale("log")
ax1.set_xlim([0.0, 5.75])
#ax1.set_ylim([0.02, 5.0])
ax1.set_ylim([0.01, 10.0])
ax2.set_ylim([-0.19, 0.26])

# labeling
#ax1.set_title(title_plot)
ax1.tick_params(labelbottom='off')    
ax2.set_xlabel("beam momentum [GeV/c]", fontsize=14)
ax1.set_ylabel(r'$\theta_{\rm Al} = \sqrt{\theta_{{\rm meas}}^2 - \theta_{\rm meas, air}^2}$ [mrad]')
#ax2.set_ylabel(r'$\sigma_{\rm norm.} = $ measured / Highland - 1')
ax2.set_ylabel('meas / HL $-$ 1')




# legend energy
ax1.legend()
handles, labels = ax1.get_legend_handles_labels()
# reverse to keep order consistent
ax1.legend(reversed(handles), reversed(labels), 
			loc='upper right', 
			#bbox_to_anchor=(1, 0.5), 	
			prop={'size':10})  

# legend thickness
ax4.legend(reversed(handles), reversed(labels), 
			loc='upper left', 
			#bbox_to_anchor=(1, 0.5), 	
			prop={'size':10})  



#######################################################3
# highland thickness data

# grids
ax4.grid(True, color='k', lw='0.2', ls='-')
ax5.grid(True, color='k', lw='0.2', ls='-')
ax5.yaxis.grid(False)
ax5.axhline(0, color='k', lw='0.5')
#ax5.axhspan(-0.11, 0.11, alpha=0.5, color='yellow')
ax5.axhline(-0.11, color='k', lw='0.5', ls=':')
ax5.axhline(+0.11, color='k', lw='0.5', ls=':')

# x data
highland_thickness = np.logspace(-3, 2, 100)

for index, energy in enumerate(energies):
  # highland theory 
  highland_y = highland_multi_scatterer(energy, highland_thickness, x0alu)
  ax4.plot(highland_thickness, highland_y, 
     color='k', 
     linestyle = ':',
     linewidth = 1
     )
  # 2nd loop
  thickness_order = np.array([])
  deviations = np.array([])
  for index2, thickness in enumerate(thicknesses):
    cut  = (data['thickness'] == thickness)
    cut2 = (data[cut]['energy'] == energy)
    # data
    ax4.errorbar(data[cut][cut2]['thickness'], data[cut][cut2][scattering_data], 
      #yerr=0.05*data[cut][cut2][scattering_data],
      color=colors[index],
      markeredgecolor=colors[index], 
      marker=markers[index2], 
      linestyle='None')
    # deviation points
    highland_point = highland_multi_scatterer(energy, data[cut][cut2]['thickness'], x0alu)
    deviation = (data[cut][cut2][scattering_data] - highland_point) / highland_point
    deviations = np.append(deviations, deviation)
    thickness_order = np.append(thickness_order, data[cut][cut2]['thickness'])
  # deviation line per energy
  ax5.plot(thickness_order, deviations,
    color='k',
    ls='-', lw=0.5)
  # deviation points
  for index2, thickness in enumerate(thicknesses):
    cut  = (data['thickness'] == thickness)
    cut2 = (data[cut]['energy'] == energy)
    highland_point = highland_multi_scatterer(energy, data[cut][cut2]['thickness'], x0alu)
    deviation = (data[cut][cut2][scattering_data] - highland_point) / highland_point
    ax5.plot(data[cut][cut2]['thickness'], deviation,
      color=colors[index],
      markeredgecolor=colors[index], 
      marker=markers[index2], 
      markersize=5,
      linestyle='None')
  
  # energy text
  erg_text = str(energy) + ' GeV/c' # print thick_text
  props = dict(boxstyle='square', pad=0.1, facecolor='white', edgecolor='none', alpha=0.8)
  x_position = 3
  if energy == 5.0:
      y_position = highland_multi_scatterer(energy, x_position, x0alu)*0.95
  else:
      y_position = highland_multi_scatterer(energy, x_position, x0alu)
  ax4.text(x_position, y_position, erg_text, rotation=29, fontsize=6.5, #linespacing=1.5,
        verticalalignment='center', horizontalalignment='center', bbox=props)

##################
# highland text
highland_text = "Highland's\n11\% accuracy"
props = dict(boxstyle='square', pad=0.1, facecolor='white', edgecolor='none', alpha=0.8)
x_position = 5e-3
y_position = 0.0
ax5.text(x_position, y_position, highland_text, rotation=90, fontsize=6.5, #linespacing=1.5,
      verticalalignment='center', horizontalalignment='center', bbox=props)
   
# scaling and range
ax4.set_yscale("log")
ax4.set_xscale("log")
ax4.set_xlim([0.002, 50])
ax4.set_ylim([0.01, 10.0])
ax5.set_ylim([-0.19, 0.26])

# labeling
#ax4.set_title(title_plot)
ax4.tick_params(labelbottom='off')    
ax5.set_xlabel("Al thickness [mm]", fontsize=14)
ax4.set_ylabel(r'$\theta_{\rm Al} = \sqrt{\theta_{\rm meas}^2 - \theta_{\rm meas, air}^2}$ [mrad]')
ax5.set_ylabel('meas / HL $-$ 1')

########################
#name_save = "output/" + title_save + str(".pdf") 
name_save = "output/" + 'highland' + str(".pdf") 
fig.savefig(name_save)
print "evince " + name_save + "&"
