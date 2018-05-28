'''plot width of projections

Usage:
    plot_width_binned.py (--configuration=<configuration> --energy=<energy> --thickness=<thickness> --results=<results>)

Options:
    --configuration=<configuration> yaml file [required]
    --energy=<energy>           energy in GeV [required]
    --thickness=<thickness>     thickness in mm [required]
    --results=<results>         npy file [required]
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
arguments = docopt(__doc__, version='plot width of projections')
# open yaml configuration file
configuration = yaml.load(open(arguments['--configuration']))
energy = arguments['--energy']
thickness = arguments['--thickness']

#####################################
# Getting runlist
runlist = mrr.read_csv_runlist(configuration['runlist'])

# Getting runindex and runnr
runindex = np.intersect1d(np.where(runlist['thickness'] == float(thickness)), np.where(runlist['energy'] == float(energy)))[0]
runnr = runlist['runnr'][runindex]

# Getting  data
#contents, counts, bincenters_x, bincenters_y, edges_x, edges_y, errors = mrr.getProfile2Data(runlist, runindex,
#        configuration['profile_collection'],
#        configuration['root_path'],
#        configuration['root_suffix'],
#        configuration['root_folder'])

data = np.load(arguments['--results'])
#print data.dtype.names

print data['ROOT_rms00'][runindex]


width = ['ROOT_rms', 'rms_frac', 'aad_frac']

# output names

title_save = ("x-dependence_width_" + "run" + str(runnr)[:-2] + "_" +
        energy + "GeV" + "_" + thickness + "mm_" +
        arguments['--configuration'][:-5])
title_plot = title_save.replace("_", " ")

#########################################
# Data 

##########################################
# Plot settings
fig = plt.figure(figsize=(5, 3))
fig.subplots_adjust(left=0.2, right=0.99, top=0.99, bottom=0.2)
# subplots-grid: rows, columns
#grid = gridspec.GridSpec(3, 6, hspace=0.05, wspace=0.0)

xdata = range(configuration['bins'])

for index, value in enumerate(xdata):
    binned_histo = '%02d'%(index)
    # data
    plt.plot(value, data[width[2] + binned_histo][runindex],
            #label=ydata.replace("_", " "),
            color = 'k',
            marker='x')

for index, value in enumerate(xdata):
    binned_histo = '%02d'%(index)
    # data
    plt.plot(value, data[width[1] + binned_histo][runindex],
            #label=ydata.replace("_", " "),
            color = 'k',
            marker='o')


plt.xlabel("x-direction [\# bin]")
plt.ylabel("width, add [mrad ?]")

# save name in folder
name_save =  "output/" + title_save + str(".pdf")
fig.savefig(name_save)
print "evince " + name_save + "&"
