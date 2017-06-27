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

# save name in folder
outfile = "data/" + name_kappa + "_" + name_kinks + "_" + name_hist
print outfile

#####################################
# Start getting data from histograms

# Getting runlist using genfromtxt
runlist = mrr.readRunlist(name_runlist)

# hard-coded margins for projections
margin_x = 6
margin_y = 3

# Adding new columns
newlist = mrr.extendList(runlist, 
        'total_sum', 
        'total_mean', 
        'total_rms', 
        'projection_x_sum', 
        'projection_x_mean', 
        'projection_x_rms', 
        'projection_y_sum', 
        'projection_y_mean', 
        'projection_y_rms', 
        'projection_x_fit_slope', 
        'projection_x_fit_offset', 
        'projection_x_fit_dslope', 
        'projection_x_fit_doffset', 
        'projection_x_fit_chi2', 
        'projection_x_fit_chi2red',
        'projection_y_fit_slope', 
        'projection_y_fit_offset', 
        'projection_y_fit_dslope', 
        'projection_y_fit_doffset', 
        'projection_y_fit_chi2', 
        'projection_y_fit_chi2red'
        )

########################################
# Getting values 
for index, value in enumerate(newlist):
    # 0. test
    #print index, value['energy']
    # 1. get 2d hist data
    counts, bincenters_x, bincenters_y = mrr.getHist2Data(runlist, index, name_hist, name_path, name_suffix, name_rootfolder)
    newlist['total_sum'][index] = np.sum(counts)
    newlist['total_mean'][index] = np.mean(counts)
    newlist['total_rms'][index] = np.std(counts)
    # 2. calculate projections
    data_x, data_y = mdp.projections(counts, bincenters_x, bincenters_y, margin_x, margin_y)
    # fill x
    newlist['projection_x_sum'][index] = np.sum(data_x[1])   # sum
    newlist['projection_x_mean'][index] = np.mean(data_x[1])  # mean
    newlist['projection_x_rms'][index] = np.std(data_x[1])   # std
    # fill y
    newlist['projection_y_sum'][index] = np.sum(data_y[1])   # sum
    newlist['projection_y_mean'][index] = np.mean(data_y[1])  # mean
    newlist['projection_y_rms'][index] = np.std(data_y[1])   # std
    # 3. fit projections
    fitresults_x = mff.fit_linear(data_x, 0.0, 5000)
    newlist['projection_x_fit_slope'  ][index] = fitresults_x['slope'  ]
    newlist['projection_x_fit_offset' ][index] = fitresults_x['offset' ]
    newlist['projection_x_fit_dslope' ][index] = fitresults_x['dslope' ]
    newlist['projection_x_fit_doffset'][index] = fitresults_x['doffset']
    newlist['projection_x_fit_chi2'   ][index] = fitresults_x['chi2'   ]
    newlist['projection_x_fit_chi2red'][index] = fitresults_x['chi2red']
    fitresults_y = mff.fit_linear(data_y, 0.0, 5000)
    newlist['projection_y_fit_slope'  ][index] = fitresults_y['slope'  ]
    newlist['projection_y_fit_offset' ][index] = fitresults_y['offset' ]
    newlist['projection_y_fit_dslope' ][index] = fitresults_y['dslope' ]
    newlist['projection_y_fit_doffset'][index] = fitresults_y['doffset']
    newlist['projection_y_fit_chi2'   ][index] = fitresults_y['chi2'   ]
    newlist['projection_y_fit_chi2red'][index] = fitresults_y['chi2red']


#print newlist.dtype.names
#print newlist

print newlist['total_mean']
print newlist['projection_x_fit_slope']
print newlist['projection_x_fit_dslope']
print newlist['projection_y_fit_slope']
print newlist['projection_y_fit_dslope']

############################################
# Save in npy format
print "saving npy-data in:", outfile 
np.save(outfile, newlist)
