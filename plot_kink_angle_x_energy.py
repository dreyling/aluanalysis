#! /usr/bin/python
import sys
import matplotlib.pyplot as plt
import numpy as np
import math

from myparams import * 

print "Starting script:", sys.argv[0]

#####################################
# Open npy file
input_file = sys.argv[0][5:17] # without plot_ and .py
data = np.load(input_file + '.npy')
#print data.dtype; print data

# Function

#########################################
# Plotting Data
fig, ax = plt.subplots(figsize=(8, 5))#, dpi=100)
plt.subplots_adjust(left=0.1, right=0.8, top=0.94, bottom=0.1)

# iterators
thicknesses = [0.013, 0.025, 0.05, 0.1, 0.2, 1.0, 10.0]
markers = ['^', 'd', 's', 'p', '*', 'h', 'o']
markersizes = [6, 6, 6, 8, 10, 10, 10]
colors = ['0.2', '0.3', '0.4', '0.5', '0.6']
# highland x data
highland_x = np.linspace(0.5, 6, 50)
for index, thickness in enumerate(thicknesses):
  # highland theory 
  highland_y = highland(highland_x, thickness, x0alu)
  plt.plot(highland_x, highland_y, 
			color='0.8',
			marker=markers[index], 
			markersize=4, 
			label='$\epsilon = ${:.4f}'.format(thickness/x0alu))
  # data
  cut = (data['thickness'] == thickness)
  #print data[cut]['thickness'], data[cut]['energy'], data[cut]['rms98_norm']
  for index2, energy in enumerate(data[cut]['energy']):
    #print colors[int(energy-1)], energy, data[cut]['energy'][index2]
    plt.plot(data[cut]['energy'][index2], data[cut]['rms98_norm'][index2], 
			color=colors[int(energy-1)], 
			#label=thickness, 
			marker=markers[index], 
			markersize=markersizes[index], 
			linestyle='None')
  # for the legend, fake plot
  plt.plot(data[cut]['energy'], data[cut]['rms98_norm']/10000, 
			color='0.6', 
			label=thickness, 
			marker=markers[index], 
			markersize=markersizes[index], 
			linestyle='None')

#exit()

# scaling and range
plt.yscale("log")
plt.xlim([0.5, 5.5])
plt.ylim([0.02, 5.0])

# labeling
plt.title("kink angle (gblaxprime6, 1 scatterer)")
plt.xlabel("beam energy [GeV]")
plt.ylabel(r'$\sqrt{\theta_{rms_{98}}^2 - \theta_{0,rms_{98}}^2}$ [mrad]')
plt.grid(True)
#ax.yaxis.set_major_formatter(matplotlib.ticker.LogFormatter())

# legend
plt.legend()
handles, labels = ax.get_legend_handles_labels()
ax.legend(reversed(handles), reversed(labels), loc='center left', bbox_to_anchor=(1, 0.5))  # reverse to keep order consistent

#plt.show()
nameSave =  "output/" + sys.argv[0][:-3] + str(".pdf") 
fig.savefig(nameSave)
print "evince " + nameSave + "&"


###################################
# 1/E
name = '_quadratic'
fig, ax = plt.subplots(figsize=(8, 5))#, dpi=100)
plt.subplots_adjust(left=0.1, right=0.8, top=0.94, bottom=0.1)

#plt.plot(data['energy'], data['rms98_norm'], 'kx')

thicknesses = [0.013, 0.025, 0.05, 0.1, 0.2, 1.0, 10.0]
markers = ['^', 'd', 's', 'p', '*', 'h', 'o']
markersizes = [6, 6, 6, 8, 10, 10, 10]
colors = ['0.4', '0.5', '0.6', '0.7', '0.8']
for index, thickness in enumerate(thicknesses):
  cut = (data['thickness'] == thickness)
  #print data[cut]['thickness'], data[cut]['energy'], data[cut]['rms98_norm']
  for index2, energy in enumerate(data[cut]['energy']):
    #print colors[int(energy-1)], energy, data[cut]['energy'][index2]
    plt.plot(data[cut]['energy'][index2], data[cut]['rms98_norm'][index2]**2, 
			color=colors[int(energy-1)], 
			#label=thickness, 
			marker=markers[index], 
			markersize=markersizes[index], 
			linestyle='None')
  # for the legend, fake plot
  plt.plot(data[cut]['energy'], data[cut]['rms98_norm']/10000, 
			color='0.6', 
			label=thickness, 
			marker=markers[index], 
			markersize=markersizes[index], 
			linestyle='None')

#exit()

# scaling and range
plt.yscale("log")
plt.xlim([0.5, 5.5])
plt.ylim([0.0005, 10.0])

# labeling
plt.title("kink angle $^2$ (gblaxprime6, 1 scatterer)")
plt.xlabel("beam energy [GeV]")
plt.ylabel(r'${\theta_{rms_{98}}^2 - \theta_{0,rms_{98}}^2}$ [mrad$^2$]')
plt.grid(True)
#ax.yaxis.set_major_formatter(matplotlib.ticker.LogFormatter())

# legend
plt.legend()
handles, labels = ax.get_legend_handles_labels()
ax.legend(reversed(handles), reversed(labels), loc='center left', bbox_to_anchor=(1, 0.5))  # reverse to keep order consistent

#plt.show()
nameSave =  "output/" + sys.argv[0][:-3] + name + str(".pdf") 
fig.savefig(nameSave)
print "evince " + nameSave + "&"
