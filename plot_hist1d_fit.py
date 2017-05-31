#! /usr/bin/python
#import inspect, os
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from scipy.optimize import curve_fit
#import math

import my_rootread as mrr
import my_fitfuncs as mff
import my_dataproc as mdp
from myparams import * 

############################################
# setting which data
print "Starting script:", sys.argv[0]

# 1st argument, data
name_path = sys.argv[1]
print "path:", name_path
name_kappa = name_path[-15:-7]
name_kinks = name_path[-6:-1]
name_suffix = "-GBLKinkEstimator_" + name_kappa + "_" + name_kinks

# 2nd argument
histname 	= sys.argv[2]
print "histogram collection:", histname

# 3rd/4th argument
energy 		= sys.argv[3]
print "selected energy:", energy
thickness = sys.argv[4]
print "selected thickness:", thickness

# 5th argument, npy results
fraction = sys.argv[5]

#####################################
# Start

# Getting runlist
runlist = mrr.readRunlist(name_runlist)

# getting right runindex
runindex = np.intersect1d(np.where(runlist['thickness'] == float(thickness)), np.where(runlist['energy'] == float(energy)))[0]
runnr = runlist['runnr'][runindex]
print "selected run:", runnr

# Getting histogram data
data = mrr.getHist1Data(runlist, runindex, histname, name_path, name_suffix, name_rootfolder)
if fraction == '1':
    datafrac = data
else:
    datafrac = mdp.get_hist_fraction(data, float(fraction))


# loop over fitfuncs
fitfuncs = ['gauss', 'nonstand', 'combined_constrained']

for index, value in enumerate(fitfuncs):
    # Plotting Data
    fig, ax = plt.subplots(figsize=(6, 6))#, dpi=100)
    fig.subplots_adjust(left=0.11, right=0.99, top=0.94, bottom=0.12)
    # subplots-grid: rows, columns
    grid = gridspec.GridSpec(3, 1, hspace=0.0)
    # layout
    ax1 = plt.subplot(grid[:2, :])
    ax2 = plt.subplot(grid[2:, :], sharex=ax1) 

    if value == 'gauss':
        print "\nGauss fit"
        # gauss
        fitfunc = mff.fitfunc_gauss
        print "parameters are [mu, si, height]"
        para0 = [0.0, 0.3, 50e3]
        para_bounds=([-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf],
                        [+np.inf, np.inf, np.inf, np.inf, np.inf, np.inf])

    if value == 'studentt':
        print "\nStudentt fit"
        # gauss
        fitfunc = mff.fitfunc_studentt
        print "parameters are [mu, nu, height]"
        para0 = [0.0, 0.3, 50e3]
        para_bounds=([-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf],
                        [+np.inf, np.inf, np.inf, np.inf, np.inf, np.inf])

    if value == 'nonstand':
        print "\nnon-stand. Studentt fit"
        # gauss
        fitfunc = mff.fitfunc_studentt_nonstand
        print "parameters are [mu, nu, sigma, height]"
        para0 = [0.0, 5., 0.3, 50e3]
        para_bounds=([-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf],
                        [+np.inf, np.inf, np.inf, np.inf, np.inf, np.inf])

    if value == 'combined':
        print "\nCombined fit"
        # gauss
        fitfunc = mff.fitfunc_combined_gauss_studentt
        print "parameters are [mu, si_g, nu_s, si_s, frac, height]"
        # mu, sigma, norm
        para0 = [0.0, 0.3, 5., 0.5, 0.5, 50e3]
        para_bounds=([-np.inf, -np.inf, -np.inf, -np.inf, -np.inf, -np.inf],
                        [+np.inf, np.inf, np.inf, np.inf, np.inf, np.inf])

    if value == 'combined_constrained':
        print "\nCombined (constraining 0<= frac <= 1) fit"
        # gauss
        fitfunc = mff.fitfunc_combined_gauss_studentt
        print "parameters are [mu, si_g, nu_s, si_s, frac, height]"
        # mu, sigma, norm
        para0 = [0.0, 0.3, 100., 0.3, 0.3, 50e3]
        para_bounds=([-np.inf, 0.0, 1.0, 0.0, 0.0, 1.0],
                        [+np.inf, np.inf, np.inf, np.inf, 1.0, np.inf])





    #####################
    # output names
    title_save = "fit" + "_" + value + "_"  + "run" + str(runnr)[:-2] + "_" + energy + "GeV" + "_" + thickness + "mm" + "_" + fraction 
    title_plot = title_save.replace("_", " ")


    # data
    ax1.plot(data[0], data[1], 'k')

    # fit range
    ax1.axvspan(datafrac[0][0], datafrac[0][-1], color='yellow', alpha=0.2)
    # zero line
    ax1.axvline(0, color='0.5')
    # zero line
    ax2.axhline(0, color='0.5')

    # fit 
    xdata = datafrac[0]
    ydata = datafrac[1]
    dydata = np.sqrt(ydata); dydata = np.where(dydata > 0.0, dydata, 1) #; print dy 

    # fit
    para, cov = curve_fit(fitfunc, xdata, ydata, p0=para0, sigma=dydata, bounds=para_bounds)

    # fit results
    # chi**2
    chi2 = np.sum(((ydata - fitfunc(xdata, *para)) / dydata)**2)
    chi2red = chi2 / (len(ydata)-len(para))

    print "parameter", para
    #print "covariance:", cov
    print "chi2 and chi2red:", chi2, chi2red

    # plot fit
    y_fit = fitfunc(data[0], *para)

    ax1.plot(data[0], y_fit, ls='--', lw=2, alpha=0.8, color='red')

    # plot residual
    residual = (data[1] - y_fit) / data[1]

    ax2.plot(data[0], residual, color='k')


    # scales
    #ax1.set_xlim(-0.5, 0.5)
    ax1.set_yscale("log")
    ax1.set_ylim(2e0, 8e5)
    #ax2.set_yscale("log")
    ax2.set_ylim(-1.2, 1.2)

    ax1.set_title(title_plot)
    ax2.set_xlabel(r'$\theta$ [mrad]')
    ax1.set_ylabel("counts")
    ax2.set_ylabel("(data - fit) / data")

    # save name in folder
    name_save =  "output/" + title_save + str(".pdf") 
    fig.savefig(name_save)
    print "evince " + name_save + "&"
