'''plot and fit 1d histograms

Usage:
    plot_and_fit_hist1d.py (--configuration=<configuration> --energy=<energy> --thickness=<thickness>) [--fraction=<percentage> --fitfunction=<fitfunc>]

Options:
    --configuration=<configuration> yaml file [required]
    --energy=<energy>           energy in GeV [required]
    --thickness=<thickness>     thickness in mm [required]
    --fitfunction=<fitfunction> fit function: gauss, studentt_standard, studentt, combined_two_sigmas, combined_one_sigma [default: none]
    --fraction=<fraction>       central fraction of histogram data [default: 1.0]
    -h --help                   show usage of this script
    -v --version                show the version of this script
'''

import numpy as np
import yaml
from docopt import docopt

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit

import my_rootread as mrr
import my_fitfuncs as mff
import my_dataproc as mdp

############################################
# arguments

arguments = docopt(__doc__, version='plot and fit 1d histograms 2.0')
# open yaml configuration file
configuration = yaml.load(open(arguments['--configuration']))
energy = arguments['--energy']
thickness = arguments['--thickness']
fraction = arguments['--fraction']
fitfunction = arguments['--fitfunction']

############################################
# getting data

# getting runlist
runlist = mrr.read_csv_runlist(configuration['runlist'])

# getting right runindex
runindex = np.intersect1d(np.where(runlist['thickness'] == float(thickness)), np.where(runlist['energy'] == float(energy)))[0]
runnumber = runlist['runnr'][runindex]
print "selected run:", runnumber

# getting histogram data
data, edges = mrr.getHist1Data(runlist, runindex,
        configuration['histogram_collection'],
        configuration['root_path'],
        configuration['root_suffix'],
        configuration['root_folder'])

# processing central fraction of data 
if float(fraction) == 1.0:
    datafrac = data
else:
    datafrac = mdp.get_hist_fraction(data, float(fraction))

############################################
# output names
title_save = "hist1d" + "_"  + "run" + str(runnumber)[:-2] + "_" + energy + "GeV" + "_" + thickness + "mm" + "_" + fraction + "data_fit-" + fitfunction
title_plot = title_save.replace("_", " ")

############################################
# Plotting Data
fig, ax = plt.subplots(figsize=(6, 6))#, dpi=100)
fig.subplots_adjust(left=0.11, right=0.95, top=0.94, bottom=0.10)
# subplots-grid: rows, columns
grid = gridspec.GridSpec(3, 1, hspace=0.0)
# layout
ax1 = plt.subplot(grid[:2, :])
ax2 = plt.subplot(grid[2:, :], sharex=ax1)

# data
ax1.plot(data[0], data[1], 'k')

# fit
if fitfunction != 'none':

    if fitfunction == 'gauss':
        print "\nGauss fit"
        fitfunc = mff.fitfunc_gauss
        parameters = [r'$\mu$', r'$\sigma_g$', r'$N$']
        para0 = [0.0, 0.3, 50e3]
        para_bounds=([-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf],
                        [+np.inf, np.inf, np.inf, np.inf, np.inf, np.inf])

    if fitfunction == 'studentt_standard':
        print "\nStudentt fit"
        fitfunc = mff.fitfunc_studentt
        parameters = [r'$\mu$', r'$\nu_s$', r'$N$']
        para0 = [0.0, 0.3, 50e3]
        para_bounds=([-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf],
                        [+np.inf, np.inf, np.inf, np.inf, np.inf, np.inf])

    if fitfunction == 'studentt':
        print "\nnon-stand. Studentt fit"
        fitfunc = mff.fitfunc_studentt_nonstand
        parameters = [r'$\mu$', r'$\nu_s$', r'$\sigma_s$', r'$N$']
        para0 = [0.0, 5., 0.3, 50e3]
        para_bounds=([-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf],
                        [+np.inf, np.inf, np.inf, np.inf, np.inf, np.inf])

    if fitfunction == 'combined_two_sigmas':
        print "\nCombined (constraining 0<= frac <= 1) fit"
        fitfunc = mff.fitfunc_combined_gauss_studentt
        parameters = [r'$\mu$', r'$\sigma_G$', r'$\nu_s$', r'$\sigma_S$', r'$a$', r'$N$']
        para0 = [0.0, 0.3, 5., 0.3, 0.3, 50e3]
        para_bounds=([-np.inf, 0.0, 1.0, 0.0, 0.0, 1.0],
                        [+np.inf, np.inf, np.inf, np.inf, 1.0, np.inf])

    if fitfunction == 'combined_one_sigma':
        print "\nCombined plus one sigma (constraining 0<= frac <= 1) fit"
        fitfunc = mff.fitfunc_combined_gauss_studentt_one_sigma
        parameters = [r'$\mu$', r'$\sigma$', r'$\nu_s$', r'$a$', r'$N$']
        para0 = [0.0, 0.3, 100., 0.3, 50e3]
        para_bounds=([-np.inf, 0.0, 1.0, 0.0, 1.0],
                        [+np.inf, np.inf, np.inf, 1.0, np.inf])


    # fit range and zero lines
    ax1.axvspan(datafrac[0][0], datafrac[0][-1], color='yellow', alpha=0.2)
    ax1.axvline(0, color='0.5')
    ax2.axhline(0, color='0.5')

    # fit 
    xdata = datafrac[0]
    ydata = datafrac[1]
    dydata = np.sqrt(ydata); dydata = np.where(dydata > 0.0, dydata, 1) #; print dy 
    para, cov = curve_fit(fitfunc, xdata, ydata, p0=para0, sigma=dydata, bounds=para_bounds)
    # chi**2
    chi2 = np.sum(((ydata - fitfunc(xdata, *para)) / dydata)**2)
    chi2red = chi2 / (len(ydata)-len(para))

    # text
    fitresults = ""
    for index, value in enumerate(parameters):
        fitresults += value + ' = {:.3f}'.format(para[index]) + '\n'
    fitresults += r'$\chi^2$' + ' = {:.3f}'.format(chi2) + '\n'
    fitresults += r'$\chi_{red.}^2$' + ' = {:.3f}'.format(chi2red)
    print fitresults
    ax1.text(0.95, 0.95, fitresults,
                verticalalignment='top', horizontalalignment='right', transform=ax.transAxes,
                fontsize=10)

    # plot fit
    y_fit = fitfunc(data[0], *para)
    ax1.plot(data[0], y_fit, ls='--', lw=2, alpha=0.8, color='red')

    # plot deviation
    deviation = (data[1] - y_fit) / y_fit
    ax2.plot(data[0], deviation, color='k')


# scales
#ax1.set_xlim(-0.5, 0.5)
ax1.set_yscale("log")
ax1.set_ylim(1, 8e5)
#ax2.set_yscale("log")
ax2.set_ylim(-1.2, 1.2)

ax1.set_title(title_plot)
ax2.set_xlabel(r'$\theta$ [mrad]')
ax1.set_ylabel("counts")
ax2.set_ylabel("meas/fit - 1")

################################################
# save name in folder
name_save =  "output/" + title_save + str(".pdf") 
fig.savefig(name_save)
print "evince " + name_save + "&"
