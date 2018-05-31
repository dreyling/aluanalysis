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
        else:
            ydata_error[index] = data[width + binned_histo][runindex] * 0.01
    # correction for aad values
    if width == 'aad_frac_norm' or width == 'aad_frac':
        ydata = ydata * aad_correction_factor
        ydata_error = ydata_error * aad_correction_factor

    # fit
    fit_selection = 3
    fit_results = mff.fit_linear(np.vstack((xdata[fit_selection:-(1+fit_selection)], ydata[fit_selection:-(1+fit_selection)])), ydata_error[fit_selection:-(1+fit_selection)], 0.0, 0.0)
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
                #r'$\frac{\mu{\rm rad}}{\rm mm}$')
        plt.plot(xdata, ydata_fit,
                label = label_text,
                color = 'k', lw = 1, ls = '-')
        # option
        plt.legend(fontsize=10)
        plt.title(title_plot, fontsize=10)
        plt.xlabel("x-direction [mm]")
        plt.ylabel("width [mrad]")
        margin_percent = 0.05
        ystart = np.min(ydata * (1. - margin_percent**2))
        yend   = np.max(ydata * (1. + margin_percent))
        plt.ylim(ystart, yend)

        # 2nd y-axis: momentum axis
        ax2 = plt.twinx()
        ax2.set_ylabel(r'momentum [GeV/c]')
        # Highland assumption
        if False:
            ystart_momentum = highland.highland_multi_scatterer_momentum(ystart, data['thickness'][runindex], highland.x0alu)
            yend_momentum = highland.highland_multi_scatterer_momentum(yend, data['thickness'][runindex], highland.x0alu)
            plt.ylim(ystart_momentum, yend_momentum)
        # correction to nominal energy and 1/p dependency
        else:
            ymiddle = ydata_fit[9] #ydata[np.where(xdata == 0.0)[0]]
            # calculate dep. factor
            depend_factor = data['energy'][runindex] * ymiddle # GeV mm
            # start, middle, end point
            momentum_tick_locations = np.array([ydata_fit[0], ymiddle, ydata_fit[18]]) # mrad
            momentum_tick_values = depend_factor / momentum_tick_locations
            #print momentum_tick_locations, momentum_tick_values
            ax2.set_yticks(momentum_tick_locations)
            ax2.set_yticklabels((np.round(momentum_tick_values, 2)))
            ax2.set_ylim(ystart, yend)
            ax2.axhline(momentum_tick_locations[1], color='k', ls='--')

        # save name in folder
        name_save =  "output/xspread/" + title_save + str(".pdf")
        fig.savefig(name_save)
        print "evince " + name_save + "&"

        #################
        # 2nd plot
        fig = plt.figure(figsize=(4, 3))
        fig.subplots_adjust(left=0.2, right=0.8, top=0.9, bottom=0.15)

        # calculate assumption
        ymiddle = ydata_fit[9] #ydata[np.where(xdata == 0.0)[0]]
        # calculate dep. factor
        if True:
            depend_factor = data['energy'][runindex] * ymiddle # GeV mm
            # ydata 
            ydata_momentum = depend_factor / ydata
            ydata_error_momentum = depend_factor / ydata_error
            ydata_fit_momentum = depend_factor / ydata_fit
        else:
            depend_factor = data['energy'][runindex] / ymiddle # array, [GeV]
            # ydata 
            ydata_momentum = depend_factor * ydata
            ydata_error_momentum = depend_factor * ydata_error
            ydata_fit_momentum = depend_factor * ydata_fit

        # data
        plt.errorbar(xdata, ydata_momentum,
                yerr = ydata_error,
                label = width.replace("_", " "),
                linestyle = 'None',
                color = 'k',
                #marker = markers[np.where(widths == width)[0][0]])
                marker = 'x')
        # fit
        #label_text = (r'slope$_{\rm fit} = $ ' +
        label_text = (r'slope = ' +
                '{:.1f}'.format((ydata_fit_momentum[-1] - ydata_fit_momentum[0]) / (xdata[-1] - xdata[0]) * 1000) +
                #' $\pm$ {:.2f})'.format(depend_factor / (fit_results['dslope']*1000)) +
                r'$\frac{{\rm MeV/c}}{\rm mm}$')
        plt.plot(xdata, ydata_fit_momentum,
                label = label_text,
                color = 'k', lw = 1, ls = '-')
        # option
        plt.legend(loc='lower right', fontsize=10)
        plt.title(title_plot, fontsize=10)
        plt.xlabel("x-direction [mm]")
        plt.ylabel("momentum [GeV/c]")
        plt.axhline(ydata_fit_momentum[9], color='k', ls='--')
        margin_percent = 0.05
        #ystart = np.min(ydata * (1. - margin_percent**2))
        #yend   = np.max(ydata * (1. + margin_percent))
        #plt.ylim(ystart, yend)

        # save name in folder
        name_save =  "output/xspread/" + title_save + '_momentum' + str(".pdf")
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
