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
# options
energy = arguments['--energy']
thickness = arguments['--thickness']
width = arguments['--width']
plot = arguments['--plot']
# open yaml configuration file
configuration = yaml.load(open(arguments['--configuration']))
aad_correction_factor = math.pi/2. #configuration['add_correction_factor']
# Getting  data
data = np.load(arguments['--results']) #print data.dtype.names, data['ROOT_rms00'][runindex]

######################################################3

def process_and_plot_width(width, runindex):
    # xdata
    xstart = -9.
    xstop = 9.
    xdata = np.linspace(xstart, xstop, num=configuration['bins'], endpoint=True)
    # getting data from npy-data
    ydata = np.zeros(configuration['bins'])
    ydata_error = np.zeros(configuration['bins'])
    for index, value in enumerate(xdata):
        binned_histo = '%02d'%(index)
        # data
        ydata[index] = data[width + binned_histo][runindex]
        if width[-4:] == 'norm':
            ydata_error[index] = data[width + '_error' + binned_histo][runindex]
        elif width == 'gauss_si_norm' or width == 'combined_one_si_norm':
            ydata_error[index] = data[width + '_dev' + binned_histo][runindex] * 0.01
        else:
            ydata_error[index] = data[width + binned_histo][runindex] * 0.01
    # correction for aad values
    if width == 'aad_frac_norm' or width == 'aad_frac':
        ydata = ydata * aad_correction_factor
        ydata_error = ydata_error * aad_correction_factor

    # fit
    fit_results = mff.fit_linear(np.vstack((xdata, ydata)), ydata_error, 0.0, 0.0)
    ydata_fit = mff.fitfunc_linear(xdata, fit_results['slope'], fit_results['offset'])

    # plot
    if bool(plot) == True:
        # output names
        title_save = ("x-dependence_width_" + "run" + str(data['runnr'][runindex])[:-2] + "_" +
                str(data['energy'][runindex]) + "GeV" + "_" + 
                str(data['thickness'][runindex]) + "mm_" + width
                )
        title_plot = title_save.replace("_", " ")
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
                '({:.2f}'.format(fit_results['slope']*1000) +
                ' $\pm$ {:.2f})'.format(fit_results['dslope']*1000) +
                r'$\frac{\upmu{\rm rad}}{\rm mm}$')
        plt.plot(xdata, ydata_fit,
                label = label_text,
                color = 'k', lw = 1, ls = '-')
        # option
        plt.legend(fontsize=10)
        plt.title(title_plot, fontsize=10)
        plt.xlabel("x-direction [mm]")
        plt.ylabel("width [mrad]")
        margin_percent = 0.025
        ystart = np.min(ydata * (1. - margin_percent**2))
        yend   = np.max(ydata * (1. + margin_percent))
        plt.ylim(ystart, yend)
        # momentum
        ax2 = plt.twinx()
        #plt.ylabel(r'particle rate [kHz]')
        #plt.ylim(ystart*rate_factor_rel, yend*rate_factor_rel/rate_factor_abs)
        ax2.set_ylabel(r'momentum [GeV/c]')
        #plt.yticks(np.arange(5))
        # Highland assumption
        if False:
            ystart_momentum = highland.highland_multi_scatterer_momentum(ystart, data['thickness'][runindex], highland.x0alu)
            yend_momentum = highland.highland_multi_scatterer_momentum(yend, data['thickness'][runindex], highland.x0alu)
            plt.ylim(ystart_momentum, yend_momentum)
        #TODO: correction to nominal energy
        else:
            ymiddle = ydata[np.where(xdata == 0.0)[0]]
            #ymiddle_momentum = highland.highland_multi_scatterer_momentum(ymiddle, data['thickness'][runindex], highland.x0alu)

            momentum_tick_locations = np.array([ydata[0], ydata[9], ydata[18]]) # mrad
            momentum_tick_values = highland.highland_multi_scatterer_momentum(momentum_tick_locations, data['thickness'][runindex], highland.x0alu)

            ax2.set_yticks(momentum_tick_locations)

            ax2.set_yticklabels(('high', '3.0', 'low'))
            ax2.set_yticklabels((momentum_tick_values))
            ax2.set_ylim(ystart, yend)
            ax2.axhline(momentum_tick_locations[1], color='k')

        # save name in folder
        name_save =  "output/xspread/" + title_save + str(".pdf")
        fig.savefig(name_save)
        print "evince " + name_save + "&"

    return fit_results

##################################################3

# loop over all
if energy == 'all' and thickness == 'all':
    slopes = np.zeros(len(data['runnr']))
    dslopes = np.zeros(len(data['runnr']))
    for runindex, value in enumerate(data['runnr']):
        #print runindex, value
        # Getting runindex and runnr
        #runindex = np.intersect1d(np.where(data['thickness'] == float(thickness)), np.where(data['energy'] == float(energy)))[0]
        # process and plot
        fit_results = process_and_plot_width(width, runindex)
        slopes[runindex] = fit_results['slope']
        dslopes[runindex] = fit_results['dslope']
    print data['runnr']
    print data['energy']
    print data['thickness']
    print slopes
    print dslopes
    #np.save(outfile, newlist)

# single plot
else:
    # Getting runindex and runnr
    runindex = np.intersect1d(np.where(data['thickness'] == float(thickness)), np.where(data['energy'] == float(energy)))[0]
    # process and plot
    print process_and_plot_width(width, runindex)
