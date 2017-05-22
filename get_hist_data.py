#! /usr/bin/python
import inspect, os
import sys
import math
import numpy as np

import myrootlib2 as mrl
from myparams import * 

############################################
# setting which data
name_script = inspect.getfile(inspect.currentframe()) 
print "Starting script:", name_script


# 1st argument
name_path = sys.argv[1]
print "path:", name_path
name_kappa = name_path[-15:-7]
name_kinks = name_path[-6:-1]
name_suffix = "-GBLKinkEstimator_" + name_kappa + "_" + name_kinks

# 2nd argument
name_hist = sys.argv[2]
print "histogram collection", name_hist

# 3rd argument
fraction = sys.argv[3]
print "fraction", fraction


# save name in folder
outfile = "data/" + name_kappa + "_" + name_kinks + "_" + name_hist + "_" + fraction
print outfile

#####################################
# Start getting data from histograms

# Getting runlist using genfromtxt
print "Reading...", name_runlist
runlist = mrl.readRunlist(name_runlist)

# Adding new columns
newlist = mrl.extendList(runlist, 
        'proc_events', 
        'rmsROOT', 
        'rmsfrac', 
        'rmsfrac_norm',
        'gauss_mu',
        'gauss_si',
        'gauss_height',
        'gauss_dmu',
        'gauss_dsi',
        'gauss_chi2',
        'gauss_chi2red',
        'gauss_si_norm'
        )

########################################
# Getting values 
for index, value in enumerate(newlist):
    # 0. test
    #print index, value['energy']
    # 1./2. add ROOT entries and rms ('stddev')
    specs = mrl.getHistSpecs(runlist, index, name_hist, name_path, name_suffix, name_rootfolder)
    #print specs['entries']
    newlist['proc_events'][index] = specs['entries']
    #print specs['stddev']
    newlist['rmsROOT'][index] = specs['stddev']
    # 3. add rmsfrac
    data = mrl.getHist1Data(runlist, index, name_hist, name_path, name_suffix, name_rootfolder)
    datafrac = mrl.getHistFraction(data, float(fraction))
    #print mrl.calcHistRMS(datafrac)
    newlist['rmsfrac'][index] = mrl.calcHistRMS(datafrac)
    # 4. Gauss fit
    fitresult = mrl.fitGaussHisto1d(datafrac, mu0=0.0, sigma0=0.3, height0=50e3)
    #print fitresult['mu']
    newlist['gauss_mu'     ][index] = fitresult['mu'     ]
    newlist['gauss_si'     ][index] = fitresult['si'     ]
    newlist['gauss_height' ][index] = fitresult['height' ]
    newlist['gauss_dmu'    ][index] = fitresult['dmu'    ]
    newlist['gauss_dsi'    ][index] = fitresult['dsi'    ]
    newlist['gauss_chi2'   ][index] = fitresult['chi2'   ]
    newlist['gauss_chi2red'][index] = fitresult['chi2red']

# Normalize RMS values
# Getting Zero values
cut_zero = (newlist['thickness'] == 0.0)
data_zero_energy = newlist[cut_zero]['energy']
data_zero_rmsfrac = newlist[cut_zero]['rmsfrac']
# Calculate normalized value
for index, value in enumerate(newlist):
    newlist['rmsfrac_norm'][index] = math.sqrt(newlist['rmsfrac'][index]**2 - data_zero_rmsfrac[data_zero_energy == newlist['energy'][index]][0]**2)

# Normalize Gauss values
# Getting Zero values
cut_zero = (newlist['thickness'] == 0.0)
data_zero_energy = newlist[cut_zero]['energy']
data_zero_rmsfrac = newlist[cut_zero]['gauss_si']
# Calculate normalized value
for index, value in enumerate(newlist):
    newlist['gauss_si_norm'][index] = math.sqrt(newlist['gauss_si'][index]**2 - data_zero_rmsfrac[data_zero_energy == newlist['energy'][index]][0]**2)







print newlist.dtype.names
print newlist

############################################
# Save in npy format
print "saving npy-data in:", outfile 
np.save(outfile, newlist)
