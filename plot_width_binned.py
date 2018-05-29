'''plot width of projections

Usage:
    plot_width_binned.py (--configuration=<configuration> --energy=<energy> --thickness=<thickness> --results=<results> --width=<width>) [--plot=<plot>]

Options:
    --configuration=<configuration> yaml file [required]
    --energy=<energy>           energy in GeV [required]
    --thickness=<thickness>     thickness in mm [required]
    --results=<results>         npy file [required]
    --width=<width>             width name [required]: ROOT_rms, rms_frac, aad_frac or with _norm
    --plot=<plot>               single plot [default: True]
    -h --help                   show usage of this script
    -v --version                show the version of this script
'''

import numpy as np
import yaml
from docopt import docopt
import math

import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
#import matplotlib.ticker as ticker
#from matplotlib.ticker import NullFormatter
#import matplotlib.cm as cm
#from mpl_toolkits.axes_grid1 import make_axes_locatable

params = {'text.latex.preamble' : [r'\usepackage{upgreek}']}
plt.rcParams.update(params)

import my_rootread as mrr
import my_fitfuncs as mff
import my_dataproc as mdp
import highland

############################################
# arguments
arguments = docopt(__doc__, version='plot width of projections')
# open yaml configuration file
configuration = yaml.load(open(arguments['--configuration']))
energy = arguments['--energy']
thickness = arguments['--thickness']
width = arguments['--width']
#widths = np.array(['ROOT_rms_norm', 'rms_frac_norm', 'aad_frac_norm'])
#markers = ['s', 'o', 'x']

# Getting  data
data = np.load(arguments['--results']) #print data.dtype.names
#print data['ROOT_rms00'][runindex]

#####################################
# Getting runlist
runlist = mrr.read_csv_runlist(configuration['runlist'])

# Getting runindex and runnr
runindex = np.intersect1d(np.where(runlist['thickness'] == float(thickness)), np.where(runlist['energy'] == float(energy)))[0]
runnr = runlist['runnr'][runindex]



#########################################
# Data 

# output names
title_save = ("x-dependence_width_" + "run" + str(runnr)[:-2] + "_" +
        energy + "GeV" + "_" + thickness + "mm_" + width
        )
title_plot = title_save.replace("_", " ")

# xdata
xstart = -4.5
xstop = 4.5
xstep = abs(xstop-xstart)/configuration['bins']
xdata = np.arange(xstart, xstop, xstep)

def process_and_plot_width(width):
    # getting data from npy-data
    ydata = np.zeros(configuration['bins'])
    ydata_error = np.zeros(configuration['bins'])
    for index, value in enumerate(xdata):
        binned_histo = '%02d'%(index)
        # data
        ydata[index] = data[width + binned_histo][runindex]
        if width[-4:] == 'norm':
            ydata_error[index] = data[width + '_error' + binned_histo][runindex]
        else:
            ydata_error[index] = data[width + binned_histo][runindex] * 0.01



    # fit
    fit_results = mff.fit_linear(np.vstack((xdata, ydata)), ydata_error, 0.0, 0.0)
    print fit_results
    ydata_fit = mff.fitfunc_linear(xdata, fit_results['slope'], fit_results['offset'])

    # in momentum
    #x_data = highland_multi_scatterer_extended_momentum(theta, thickness_sut, x0_sut)

    # plot
    if plot == True:
        ##########################################
        # Plot settings
        fig = plt.figure(figsize=(4, 3))
        fig.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.15)
        # data
        plt.errorbar(xdata, ydata, yerr = ydata_error,
                label = width.replace("_", " "),
                linestyle = 'None',
                color = 'k',
                #marker = markers[np.where(widths == width)[0][0]])
                marker = 'x')
        # fit
        #label_text = r'$\chi^2$/ndf = ' + '{:f}'.format(fit_results['chi2red'])
        label_text = (r'slope$_{\rm fit} = $ ' +
                '({:.1f}'.format(fit_results['slope']*1000) +
                ' $\pm$ {:.1f})'.format(fit_results['dslope']*1000) +
                r'$\frac{\upmu{\rm rad}}{\rm mm}$')
        plt.plot(xdata, ydata_fit,
                label = label_text,
                color = 'k', lw = 1, ls = '-')
        # option
        plt.legend(fontsize=10)
        plt.title(title_plot, fontsize=10)
        plt.xlabel("x-direction [mm]")
        plt.ylabel("width [mrad]")
        margin_percent = 0.1
        ystart = np.min(ydata * (1. - margin_percent))
        yend   = np.max(ydata * (1. + margin_percent))
        plt.ylim(ystart, yend)
        # momentum
        plt.twinx()
        #plt.ylabel(r'particle rate [kHz]')
        #plt.ylim(ystart*rate_factor_rel, yend*rate_factor_rel/rate_factor_abs)
        plt.ylabel(r'momentum [GeV/c]')
        #plt.yticks(np.arange(5))
        ystart_momentum = highland.highland_multi_scatterer_momentum(ystart, runlist['thickness'][runindex], highland.x0alu)
        yend_momentum =   highland.highland_multi_scatterer_momentum(yend, runlist['thickness'][runindex], highland.x0alu)
        plt.ylim(ystart_momentum, yend_momentum)

        # save name in folder
        name_save =  "output/xspread/" + title_save + str(".pdf")
        fig.savefig(name_save)
        print "evince " + name_save + "&"

#process_and_plot_width(widths[0])
#process_and_plot_width(widths[1])
process_and_plot_width(width)


#np.save(outfile, newlist)
