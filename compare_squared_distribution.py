#! /usr/bin/python
import inspect, os
import sys
import matplotlib.pyplot as plt
#import matplotlib.gridspec as gridspec
#import matplotlib.ticker as ticker
#from matplotlib.ticker import NullFormatter
#import matplotlib.cm as cm
from scipy.optimize import curve_fit
import numpy as np
import math

import my_rootread as mrr
import my_fitfuncs as mff
import my_dataproc as mdp

from myparams import * 

############################################
# setting which data
print "Starting script:", sys.argv[0]
title_save = sys.argv[0][:-3]

name_path = "/home/jande/Documents/fhl-wgs01/data/data_datura/161128_scatalu/EUTelescope_root_files/kappa075_2kink/" 
name_suffix = "-GBLKinkEstimator_kappa075_2kink"

energy 		= 1.
thickness = 0.0
print "selected energy:", energy
print "selected thickness:", thickness

#####################################

# getting runlist
runlist = mrr.read_csv_runlist(name_runlist)

# getting run
runindex = np.intersect1d(np.where(runlist['thickness'] == float(thickness)), np.where(runlist['energy'] == float(energy)))[0]
runnr = runlist['runnr'][runindex]
print "selected run:", runnr, 

# getting 1d Histo normal
data, edges = mrr.getHist1Data(runlist, runindex, 'gblsumkxandsumky', name_path, name_suffix, name_rootfolder)
histo_specs = mrr.getHistSpecs(runlist, runindex, 'gblsumkxandsumky', name_path, name_suffix, name_rootfolder)

# getting 1d Histo squared
data2, edges2 = mrr.getHist1Data(runlist, runindex, 'gblsumkx2andsumky2', name_path, name_suffix, name_rootfolder)
histo_specs2 = mrr.getHistSpecs(runlist, runindex, 'gblsumkx2andsumky2', name_path, name_suffix, name_rootfolder)

# getting 2d Profile
contents2, counts2, bincenters_x2, bincenters_y2, edges_x2, edges_y2, errors2 = mrr.getProfile2Data(runlist, runindex, 'gblsumkx2andsumky2_xyP', name_path, name_suffix, name_rootfolder)

# getting 2d Profile
contents2b, counts2b, bincenters_x2b, bincenters_y2b, edges_x2b, edges_y2b, errors2b = mrr.getProfile2Data(runlist, runindex, 'gblsumkx2andsumky2_xybP', name_path, name_suffix, name_rootfolder)

# getting 2d Profile
contents, counts, bincenters_x, bincenters_y, edges_x, edges_y, errors = mrr.getProfile2Data(runlist, runindex, 'gblsumkxandsumky_xyP', name_path, name_suffix, name_rootfolder)

######################################################3
# analyse

print ""
############
print "histo ROOT specs (gblsumkxandsumky):\n", histo_specs
print "histo mean (entries, gblsumkxandsumky):\n", mdp.calc_hist_mean(data)
print "histo RMS (entries, gblsumkxandsumky):\n", mdp.calc_hist_RMS(data)
frac = 0.98
datafrac = mdp.get_hist_fraction(data, frac)
para0 = [0., 0.5, 10000.] # mu, sigma, norm
para, cov = curve_fit(mff.fitfunc_gauss, datafrac[0], datafrac[1], p0=para0, sigma=np.sqrt(datafrac[1]))
print "histo sigma gauss fit (entries, gblsumkxandsumky):\n", para[1], "frac", frac
frac = 0.955
datafrac = mdp.get_hist_fraction(data, frac)
para0 = [0., 0.5, 10000.] # mu, sigma, norm
para, cov = curve_fit(mff.fitfunc_gauss, datafrac[0], datafrac[1], p0=para0, sigma=np.sqrt(datafrac[1]))
print "histo sigma gauss fit (entries, gblsumkxandsumky):\n", para[1], "frac", frac

print ""
############
print "histo ROOT specs (gblsumkx2andsumky2):\n", histo_specs2
print "histo mean (squared entries, gblsumkx2andsumky2):\n", mdp.calc_hist_mean(data2), "(sqrt: ", math.sqrt(mdp.calc_hist_mean(data2)), ")"

print ""
############
content_mean2 = np.mean(contents2[(contents2 != 0.) & (contents2 < 7.8)])
content_median2 = np.median(contents2[contents2 != 0.])
print "mean of 2d profile (squared entries, gblsumkx2andsumky2_xyP):\n", content_mean2, "(sqrt: ", math.sqrt(content_mean2), ")"
print "median of 2d profile (squared entries, gblsumkx2andsumky2_xyP):\n", content_median2, "(sqrt: ", math.sqrt(content_median2), ")"
print "entries", np.nansum(counts2)
print "max", np.max(contents2)
print "entries >100", np.size(contents2[contents2 > 100])

print ""
############
content_mean2b = np.mean(contents2b[contents2b != 0.])
print "mean of 2d profile b (squared entries, gblsumkx2andsumky2_xybP):\n", content_mean2b, "(sqrt: ", math.sqrt(content_mean2b), ")"
print "entries", np.nansum(counts2b)
print "max", np.max(contents2b)
print "entries >100", np.size(contents2b[contents2b > 100])


print ""
############
contents_mean = np.mean(contents[contents != 0.])
errors_mean = np.mean(errors[errors != 0.])
print "mean mean of 2d profile (entries, gblsumkxandsumky_xyP):\n", contents_mean
print "mean error of 2d profile (entries, gblsumkxandsumky_xyP):\n", errors_mean

# calculation of sigma
sigmas = np.multiply(np.sqrt(counts), errors)
#print np.size(sigmas), np.shape(sigmas), sigmas
sigmas_mean = np.nanmean(sigmas)
print "mean sigma of 2d profile (entries, gblsumkxandsumky_xyP):\n", sigmas_mean
#sigmas[np.isnan(sigmas)] = 0.0
#print "mean sigma of 2d profile (entries, gblsumkxandsumky_xyP), check:\n", np.mean(sigmas[sigmas != 0.0])

# alternative for check
sigmas_2 = np.multiply(np.sqrt(counts[~np.isnan(counts)]), errors[errors != 0.])
#print np.size(counts[~np.isnan(counts)])
sigmas_mean_2 = np.mean(sigmas_2)
sigmas_std_2 = np.std(sigmas_2)
sigmas_rms_2 = np.sqrt(np.mean(np.square(sigmas_2)))
print "sigmas:", np.size(sigmas_2), len(sigmas_2)
print "mean sigma of 2d profile (entries, gblsumkxandsumky_xyP), check:\n", sigmas_mean_2
print "std sigma of 2d profile (entries, gblsumkxandsumky_xyP), check:\n", sigmas_std_2
print np.sqrt(np.mean((sigmas_2 - sigmas_mean_2)**2))
print "rms sigma of 2d profile (entries, gblsumkxandsumky_xyP), check:\n",  sigmas_rms_2
# alternative for check
sigmas_3 = np.multiply(np.sqrt(counts[75:525, 50:250]), errors[75:525, 50:250])
#print np.size(counts[~np.isnan(counts)])
sigmas_mean_3 = np.mean(sigmas_3)
print "mean sigma of 2d profile (entries, gblsumkxandsumky_xyP), check 2:\n", sigmas_mean_3
print np.average(sigmas_3)

# weigted mean
counts_w = counts[75:525, 50:250]
errors_w = errors[75:525, 50:250]
sigmas_w = sigmas[75:525, 50:250]
sigmas_sigmas_w = np.divide( np.multiply(np.sqrt(counts_w), errors_w), np.sqrt(2*counts_w-2) )
sigmas_weighted_mean = np.average(sigmas_w, weights=sigmas_sigmas_w)
print "weigthed mean sigma of 2d profile (entries, gblsumkxandsumky_xyP):\n", sigmas_weighted_mean


#####################################
if True:
    #######################################33
    fig, ax = plt.subplots(figsize=(5, 3))
    fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)

    plt.hist(sigmas_2, 1000, histtype='step')

    plt.yscale('log')
    plt.xlim(0, 5)
    plt.xlabel("$\sigma_i$ = bine x sqrt(binn) from 2DProfile")
    plt.ylabel("counts")

    plt.text(0.4, 0.9, 'mean($\sigma_i$) = {:.6f}'.format(sigmas_mean_2), transform=ax.transAxes, fontsize=10, verticalalignment='top', horizontalalignment='left')
    plt.text(0.4, 0.8, 'std($\sigma_i$) = {:.6f}'.format(sigmas_std_2), transform=ax.transAxes, fontsize=10, verticalalignment='top', horizontalalignment='left')
    plt.text(0.4, 0.7, 'rms($\sigma_i$) = {:.6f}'.format(sigmas_rms_2), transform=ax.transAxes, fontsize=10, verticalalignment='top', horizontalalignment='left')


    # save name in folder
    name_save =  "output/" + title_save + "_sigmas_sumkxandsumky" + str(".pdf") 
    fig.savefig(name_save)
    print "evince " + name_save + "&"

    #######################################33
    fig, ax = plt.subplots(figsize=(5, 3))
    fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)

    plt.hist(counts[~np.isnan(counts)], 1000, histtype='step')

    #plt.yscale('log')
    #plt.xlim(0, 5)
    plt.xlabel("binn")
    plt.ylabel("counts (=binn)")


    # save name in folder
    name_save =  "output/" + title_save + "_counts_sumkxandsumky" + str(".pdf") 
    fig.savefig(name_save)
    print "evince " + name_save + "&"

    #######################################33
    fig, ax = plt.subplots(figsize=(5, 3))
    fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)

    plt.hist(counts2[~np.isnan(counts2)], 1000, histtype='step')

    #plt.yscale('log')
    #plt.xlim(0, 5)
    plt.xlabel("binn")
    plt.ylabel("counts (=binn)")


    # save name in folder
    name_save =  "output/" + title_save + "_counts_sumkx2andsumky2" + str(".pdf") 
    fig.savefig(name_save)
    print "evince " + name_save + "&"

    #######################################33
    fig, ax = plt.subplots(figsize=(5, 3))
    fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)

    plt.hist(contents[contents != 0.], 1000, histtype='step')

    #plt.yscale('log')
    plt.xlim(-1, 1)
    plt.xlabel("contents (=binc)")
    plt.ylabel("counts")


    # save name in folder
    name_save =  "output/" + title_save + "_contents_sumkxandsumky" + str(".pdf") 
    fig.savefig(name_save)
    print "evince " + name_save + "&"

    #######################################33
    fig, ax = plt.subplots(figsize=(5, 3))
    fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)

    plt.hist(errors[errors != 0.], 1000, histtype='step')

    plt.yscale('log')
    plt.xlim(0, 0.55)
    plt.xlabel("errors (=bine)")
    plt.ylabel("counts")



    # save name in folder
    name_save =  "output/" + title_save + "_errors_sumkxandsumky" + str(".pdf") 
    fig.savefig(name_save)
    print "evince " + name_save + "&"

