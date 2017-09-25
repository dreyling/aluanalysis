#! /usr/bin/python
import sys
import math
import numpy as np

sys.path.insert(0, '../')
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
outfile = "data/" + name_kappa + "_" + name_kinks + "_" + name_hist + "_" + fraction #print outfile

#####################################
# Start getting data from histograms

# Getting runlist using genfromtxt
runlist = mrr.readRunlist("../" + name_runlist)

# Adding new columns
newlist = mrr.extendList(runlist, 
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
        'gauss_si_norm',
        'd_gauss_si_norm'
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
    data, edges = mrr.getHist1Data(runlist, index, name_hist, name_path, name_suffix, name_rootfolder)
    datafrac = mdp.get_hist_fraction(data, float(fraction))
    newlist['rmsfrac'][index] = mdp.calc_hist_RMS(datafrac)
    # 4. Gauss fit
    fitresult = mff.fit_gauss(datafrac, mu0=0.0, sigma0=0.3, height0=50e3)
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
data_zero_gauss_si = newlist[cut_zero]['gauss_si']
# assumption of error 
rel_error = 0.03
# Calculate normalized value
for index, value in enumerate(newlist):
    theta_meas = newlist['gauss_si'][index]
    theta_air0 = data_zero_gauss_si[data_zero_energy == newlist['energy'][index]][0]
    newlist['gauss_si_norm'][index] = math.sqrt(theta_meas**2 - theta_air0**2)
    # propagated error, here for each measurement 3% uncertainty
    d_theta_meas = rel_error * theta_meas
    d_theta_air0 = rel_error * theta_air0
    newlist['d_gauss_si_norm'][index] = math.sqrt(
            (theta_meas/newlist['gauss_si_norm'][index] * d_theta_meas)**2 + 
            (theta_air0/newlist['gauss_si_norm'][index] * d_theta_air0)**2 ) 







print newlist.dtype.names
print newlist

############################################
# Save in npy format
print "saving npy-data in:", outfile 
np.save(outfile, newlist)
