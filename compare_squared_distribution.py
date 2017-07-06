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
thickness = 0.1
print "selected energy:", energy
print "selected thickness:", thickness

#####################################

# getting runlist
runlist = mrr.readRunlist(name_runlist)

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
sigmas_mean = np.nanmean(sigmas)
#print np.size(sigmas), np.shape(sigmas), sigmas
# alternative
#print np.size(counts[~np.isnan(counts)])
sigmas2 = np.multiply(np.sqrt(counts[~np.isnan(counts)]), errors[errors != 0.])
sigmas_mean2 = np.mean(sigmas2)
print "mean sigma of 2d profile (entries, gblsumkxandsumky_xyP):\n", sigmas_mean
print "mean sigma of 2d profile (entries, gblsumkxandsumky_xyP), check:\n", sigmas_mean2

print sigmas2

if True:
    #######################################33
    fig, ax = plt.subplots(figsize=(5, 3))
    fig.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.15)

    plt.hist(sigmas2, 1000, histtype='step')

    plt.yscale('log')
    plt.xlim(0, 5)
    plt.xlabel("bine x sqrt(binn)")
    plt.ylabel("counts bine x sqrt(binn)")

    plt.text(0.4, 0.9, 'mean (bine x sqrt(binn)) = {:.6f}'.format(sigmas_mean2), transform=ax.transAxes, fontsize=10, verticalalignment='top', horizontalalignment='left')


    # save name in folder
    name_save =  "output/" + title_save + str(".pdf") 
    fig.savefig(name_save)
    print "evince " + name_save + "&"

