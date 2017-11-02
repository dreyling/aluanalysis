'''get and analyse 2d profile data

Usage:
    get_and_analyze_profile2d-data.py (--configuration=<configuration> --data_type=<data_type>) [--rebin=<rebin>]

Options:
    --configuration=<configuration> yaml file [required]
    --data_type=<data_type>     'mean' or 'sigma' [required]
    --rebin=<rebin>             rebinning [default: 1]
    -h --help                   show usage of this script
    -v --version                show the version of this script
'''

#import sys
import math
import numpy as np
import yaml
from docopt import docopt

import my_rootread as mrr
import my_fitfuncs as mff
import my_dataproc as mdp

############################################
# arguments

# reading documentation
arguments = docopt(__doc__, version='get and analyse 2d profile data')
# open yaml configuration file
configuration = yaml.load(open(arguments['--configuration']))
data_type = arguments['--data_type']
number_merged_points = int(arguments['--rebin'])

##############################################
# output names
outfile = ("data/stats_and_fits_2d-profile_" + arguments['--configuration'][:-5] + "_" + 
        data_type + "_" + "rebin" + arguments['--rebin'])

#####################################
# Start getting data from histograms

# Getting runlist using genfromtxt
runlist = mrr.read_csv_runlist(configuration['runlist'])

# hard-coded margins for projections
margin_x = 6
margin_y = 3

# Adding new columns
newlist = mrr.extend_list(runlist,
        'total_sum',
        'total_mean',
        'total_rms',
        # x projection
        'projection_x_sum',
        'projection_x_mean',
        'projection_x_rms',
        'projection_x_fit_slope',
        'projection_x_fit_offset',
        'projection_x_fit_dslope',
        'projection_x_fit_doffset',
        'projection_x_fit_chi2',
        'projection_x_fit_chi2red',
        # y projection
        'projection_y_sum',
        'projection_y_mean',
        'projection_y_rms',
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
    contents, counts, bincenters_x, bincenters_y, edges_x, edges_y, errors = mrr.getProfile2Data(
            runlist, index,
            configuration['profile_collection'],
            configuration['root_path'],
            configuration['root_suffix'],
            configuration['root_folder'])
            #name_hist,
            #name_path,
            #name_suffix,
            #name_rootfolder)
    if data_type == 'sigma':
        # getting sigma from profile: sqrt(N) * err = sigma 
        sigmas = np.multiply(np.sqrt(counts), errors)
        sigmas[np.isnan(sigmas)] = 0
        contents = sigmas
        print 'Getting the sigma-data of run {} with energy {} GeV and thickness {} mm'.format(value['runnr'], value['energy'], value['thickness'])
    elif data_type == 'mean':
        print 'Getting the mean-data of run {} with energy {} GeV and thickness {} mm'.format(value['runnr'], value['energy'], value['thickness'])
    else:
        print 'Please select a data type: mean or sigma'
        exit()
    # calculate specs
    newlist['total_sum'][index] = np.sum(contents[contents != 0.]) #np.sum(contents)
    newlist['total_mean'][index] = np.mean(contents[contents != 0.]) #np.mean(contents)
    newlist['total_rms'][index] = np.std(contents[contents != 0.]) #np.std(contents)

    # 2a. calculate projections
    data_x, data_y = mdp.get_projections(contents, bincenters_x, bincenters_y)
    # fill x
    newlist['projection_x_sum'][index] = np.sum(data_x[1])   # sum
    newlist['projection_x_mean'][index] = np.mean(data_x[1])  # mean
    newlist['projection_x_rms'][index] = np.std(data_x[1])   # std
    # fill y
    newlist['projection_y_sum'][index] = np.sum(data_y[1])   # sum
    newlist['projection_y_mean'][index] = np.mean(data_y[1])  # mean
    newlist['projection_y_rms'][index] = np.std(data_y[1])   # std

    # 2b. rebinning
    # rebinning x-projection
    data_x0_rebinned = mdp.rebin_data(data_x[0], number_merged_points)
    data_x1_rebinned = mdp.rebin_data(data_x[1], number_merged_points)
    data_x_rebinned = np.vstack((data_x0_rebinned, data_x1_rebinned))
    # rebinning y-projection
    data_y0_rebinned = mdp.rebin_data(data_y[0], number_merged_points)
    data_y1_rebinned = mdp.rebin_data(data_y[1], number_merged_points)
    data_y_rebinned = np.vstack((data_y0_rebinned, data_y1_rebinned))

    # 3. fit projections
    fitresults_x = mff.fit_linear(data_x_rebinned, 0, 0.0, 0.0)
    newlist['projection_x_fit_slope'  ][index] = fitresults_x['slope'  ]
    newlist['projection_x_fit_offset' ][index] = fitresults_x['offset' ]
    newlist['projection_x_fit_dslope' ][index] = fitresults_x['dslope' ]
    newlist['projection_x_fit_doffset'][index] = fitresults_x['doffset']
    newlist['projection_x_fit_chi2'   ][index] = fitresults_x['chi2'   ]
    newlist['projection_x_fit_chi2red'][index] = fitresults_x['chi2red']
    fitresults_y = mff.fit_linear(data_y_rebinned, 0, 0.0, 0.0)
    newlist['projection_y_fit_slope'  ][index] = fitresults_y['slope'  ]
    newlist['projection_y_fit_offset' ][index] = fitresults_y['offset' ]
    newlist['projection_y_fit_dslope' ][index] = fitresults_y['dslope' ]
    newlist['projection_y_fit_doffset'][index] = fitresults_y['doffset']
    newlist['projection_y_fit_chi2'   ][index] = fitresults_y['chi2'   ]
    newlist['projection_y_fit_chi2red'][index] = fitresults_y['chi2red']


#print newlist.dtype.names
#print newlist
#print newlist['total_mean']
#print newlist['projection_x_fit_slope']
#print newlist['projection_x_fit_dslope']
#print newlist['projection_y_fit_slope']
#print newlist['projection_y_fit_dslope']

############################################
# Save in npy format
print "saving npy-data in:", outfile
print "including these values:", newlist.dtype.names
np.savetxt(outfile+'.csv', newlist, delimiter=',', header=str(newlist.dtype.names[:]))
np.save(outfile, newlist)
