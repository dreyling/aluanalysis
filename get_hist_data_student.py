#! /usr/bin/python
import sys
import math
import numpy as np

import my_rootread as mrr
import my_fitfuncs as mff
import my_dataproc as mdp
from myparams import * 

############################################
# setting which data
print "Starting script:", sys.argv[0]

# 1st argument
name_path = sys.argv[1]
print "path:", name_path
name_kappa = name_path[-15:-7]
name_kinks = name_path[-6:-1]
name_suffix = "-GBLKinkEstimator_" + name_kappa + "_" + name_kinks

# 2nd argument
name_hist = sys.argv[2]
print "histogram collection:", name_hist

# 3rd argument
fraction = sys.argv[3]
print "fraction:", fraction

# save name in folder
outfile = "data/comb_" + name_kappa + "_" + name_kinks + "_" + name_hist + "_" + fraction #print outfile

#####################################
# Start getting data from histograms

# Getting runlist using genfromtxt
runlist = mrr.readRunlist(name_runlist)

# Adding new columns
newlist = mrr.extendList(runlist, 
        'proc_events', 
        'rmsROOT', 
        'rmsfrac', 
        'rmsfrac_norm',
        'comb_mu',
        'comb_si',
        'comb_nu_s',
        'comb_si_s',
        'comb_frac',
        'comb_height',
        'comb_chi2',
        'comb_chi2red',
        'comb_si_norm',
        'comb_si_s_norm'
        )

########################################
# Getting values 
for index, value in enumerate(newlist):
    # 0. test
    #print index, value['energy']
    # 1./2. add ROOT entries and rms ('stddev')
    specs = mrr.getHistSpecs(runlist, index, name_hist, name_path, name_suffix, name_rootfolder)
    #print specs['entries']
    newlist['proc_events'][index] = specs['entries']
    #print specs['stddev']
    newlist['rmsROOT'][index] = specs['stddev']
    # 3. add rmsfrac
    data = mrr.getHist1Data(runlist, index, name_hist, name_path, name_suffix, name_rootfolder)
    datafrac = mdp.get_hist_fraction(data, float(fraction))
    newlist['rmsfrac'][index] = mdp.calc_hist_RMS(datafrac)
    # 4. Gauss fit
    fitresult = mff.fit_combined(data, mu0=0.0, si0=0.3, nu_s0=5.0, si_s0= 0.3, frac0=0.4, height0=50e3)
    #print fitresult['mu']
    newlist['comb_mu'     ][index] = fitresult['mu'     ]
    newlist['comb_si'     ][index] = fitresult['si'     ]
    newlist['comb_nu_s'   ][index] = fitresult['nu_s'   ]
    newlist['comb_si_s'   ][index] = fitresult['si_s'   ]
    newlist['comb_frac'   ][index] = fitresult['frac'   ]
    newlist['comb_height' ][index] = fitresult['height' ]
    newlist['comb_chi2'   ][index] = fitresult['chi2'   ]
    print fitresult['chi2red']
    newlist['comb_chi2red'][index] = fitresult['chi2red']

# Normalize RMS values
# Getting Zero values
cut_zero = (newlist['thickness'] == 0.0)
data_zero_energy = newlist[cut_zero]['energy']
data_zero_rmsfrac = newlist[cut_zero]['rmsfrac']
# Calculate normalized value
for index, value in enumerate(newlist):
    newlist['rmsfrac_norm'][index] = math.sqrt(newlist['rmsfrac'][index]**2 - data_zero_rmsfrac[data_zero_energy == newlist['energy'][index]][0]**2)

# Normalize Gauss sigma values
# Getting Zero values
cut_zero = (newlist['thickness'] == 0.0)
data_zero_energy = newlist[cut_zero]['energy']
data_zero_rmsfrac = newlist[cut_zero]['comb_si']
# Calculate normalized value
for index, value in enumerate(newlist):
    newlist['comb_si_norm'][index] = math.sqrt(newlist['comb_si'][index]**2 - data_zero_rmsfrac[data_zero_energy == newlist['energy'][index]][0]**2)

# Normalize Student t sigma values
# Getting Zero values
cut_zero = (newlist['thickness'] == 0.0)
data_zero_energy = newlist[cut_zero]['energy']
data_zero_rmsfrac = newlist[cut_zero]['comb_si_s']
# Calculate normalized value
for index, value in enumerate(newlist):
    if newlist['comb_si_s'][index] > data_zero_rmsfrac[data_zero_energy == newlist['energy'][index]][0]:
        newlist['comb_si_s_norm'][index] = math.sqrt(newlist['comb_si_s'][index]**2 - data_zero_rmsfrac[data_zero_energy == newlist['energy'][index]][0]**2)
    else:
        newlist['comb_si_s_norm'][index] = 0.0


print newlist.dtype.names
print newlist

############################################
# Save in npy format
print "saving npy-data in:", outfile 
np.save(outfile, newlist)
