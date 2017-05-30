#! /usr/bin/python
import inspect, os
import sys
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy as np
from scipy.optimize import curve_fit
#import math

import myrootlib2 as mrl
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
runlist = mrl.readRunlist(name_runlist)
print "Reading...", name_runlist

# getting right runindex
runindex = np.intersect1d(np.where(runlist['thickness'] == float(thickness)), np.where(runlist['energy'] == float(energy)))[0]
runnr = runlist['runnr'][runindex]
print "selected run:", runnr

# Getting histogram data
data = mrl.getHist1Data(runlist, runindex, histname, name_path, name_suffix, name_rootfolder)
datafrac = mrl.getHistFraction(data, float(fraction))
#print np.sum(data[1])
#print np.sum(datafrac[1])
#print mrl.calcHistRMS(datafrac)
#print mrl.calcHistMean(datafrac)


fitfuncs = ['gauss', 'studentt', 'nonstand', 'combined']

for index, value in enumerate(fitfuncs[1:2]):
    if value == 'gauss':
        print "\nGauss fit"
        # gauss
        fitfunc = mrl.fitfunc_gauss
        # mu, sigma, norm
        para0 = [0.0, 0.3, 50e3]

    if value == 'studentt':
        print "\nStudentt fit"
        # gauss
        fitfunc = mrl.fitfunc_studentt
        # mu, sigma, norm
        para0 = [0.0, 0.3, 50e3]

    if value == 'nonstand':
        print "\nnon-stand. Studentt fit"
        # gauss
        fitfunc = mrl.fitfunc_gauss
        # mu, sigma, norm
        para0 = [0.0, 0.3, 50e3]

    if value == '\ncombined fit a la Berger':
        print "using combined for fitting"
        # gauss
        fitfunc = mrl.fitfunc_gauss
        # mu, sigma, norm
        para0 = [0.0, 0.3, 50e3]





    #####################
    # output names
    title_save = "fit" + "_" + value + "_"  + "run" + str(runnr)[:-2] + "_" + energy + "GeV" + "_" + thickness + "mm" + "_" + fraction 
    title_plot = title_save.replace("_", " ")

    ##########################################
    # Plotting Data
    fig, ax = plt.subplots(figsize=(6, 8))#, dpi=100)
    fig.subplots_adjust(left=0.11, right=0.99, top=0.94, bottom=0.12)

    # subplots-grid: rows, columns
    grid = gridspec.GridSpec(2, 1, hspace=0.1)
    # layout
    ax1 = plt.subplot(grid[:1, :])
    ax2 = plt.subplot(grid[1:, :], sharex=ax1) 

    # data
    ax1.plot(data[0], data[1], 'k')

    # fit range
    ax1.axvspan(datafrac[0][0], datafrac[0][-1], color='yellow', alpha=0.2)
    # zero line
    ax1.axvline(0, color='0.5')

    # fit 
    xdata = datafrac[0]
    ydata = datafrac[1]
    dydata = np.sqrt(ydata); dydata = np.where(dydata > 0.0, dydata, 1) #; print dy 

    # fit
    para, cov = curve_fit(fitfunc, xdata, ydata, p0=para0, sigma=dydata)

    # fit results
    # chi**2
    chi2 = np.sum(((ydata - fitfunc(xdata, *para)) / dydata)**2)
    chi2red = chi2 / (len(ydata)-len(para))

    print "parameter", para
    print "covariance:", cov
    print "chi2 and chi2red:", chi2, chi2red

    # plot fit
    y_fit = fitfunc(data[0], *para)

    ax1.plot(data[0], y_fit, ls='--', lw=2, alpha=0.8, color='red')

    # plot residual
    residual = data[1] - y_fit

    ax2.plot(data[0], residual, color='k')


    # scales
    #ax1.set_yscale("log")
    #ax2.set_yscale("log")
    #ax1.set_xlim(-0.5, 0.5)
    #ax1.set_ylim(5e-7, 5)
    #ax1.set_ylim(1e0, 1e6)

    ax1.set_title(title_plot)
    ax2.set_xlabel(r'$\theta$ [mrad]')
    ax1.set_ylabel("counts")
    ax2.set_ylabel("data - fit")

    # save name in folder
    name_save =  "output/" + title_save + str(".pdf") 
    fig.savefig(name_save)
    print "evince " + name_save + "&"
