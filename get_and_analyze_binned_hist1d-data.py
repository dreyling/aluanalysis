'''get and analyse 1d histogram data

Usage:
    get_and_analyze_hist1d-data.py (--configuration=<configuration>) [--fraction=<fraction> --rel_error=<rel_error>]

Options:
    --configuration=<configuration> yaml file [required]
    --fraction=<fraction>       central fraction of histogram data [default: 1.0]
    --rel_error=<rel_error>     relative error for error propagation [default: 0.03]
    -h --help                   show usage of this script
    -v --version                show the version of this script
'''

import numpy as np
import math
import yaml
from docopt import docopt

import my_rootread as mrr
import my_fitfuncs as mff
import my_dataproc as mdp

import highland

############################################
# arguments

# reading documentation
arguments = docopt(__doc__, version='get and fit 1d histogram data')
# open yaml configuration file
configuration = yaml.load(open(arguments['--configuration']))
fraction = arguments['--fraction']
rel_error = float(arguments['--rel_error'])


##############################################
# output names
outfile = "data/stats_and_fits_" + arguments['--configuration'][:-5] + "_data-fraction_" + fraction

#####################################
# Start getting data from histograms

# Getting runlist using genfromtxt
runlist = mrr.read_csv_runlist(configuration['runlist'])

newlist = runlist
for bin_index in range(configuration['bins']):
    binned_histo = '%02d'%(bin_index)
    #print 'proc_events'+binned_histo
    newlist = mrr.extend_list(newlist,
        'ROOT_entries'+binned_histo,
        'ROOT_mean'+binned_histo,
        'ROOT_rms'+binned_histo,
        'rms_frac'+binned_histo,
        'aad_frac'+binned_histo,
        )
#print newlist

########################################
# Getting values 
for index, value in enumerate(newlist):
    for bin_index in range(configuration['bins']):
        binned_histo = '%02d'%(bin_index)
        # 0. test
        # 1. get and add ROOT specs
        specs = mrr.getHistSpecs(runlist, index,
                configuration['histogram_collection'] + binned_histo,
                configuration['root_path'],
                configuration['root_suffix'],
                configuration['root_folder'])
        print "Histogram:", binned_histo
        newlist['ROOT_entries' + binned_histo][index] = specs['entries']
        newlist['ROOT_mean' + binned_histo][index] = specs['mean']
        newlist['ROOT_rms' + binned_histo][index] = specs['stddev']

        # 2. get hist data
        data, edges = mrr.getHist1Data(runlist, index,
                configuration['histogram_collection'] + binned_histo,
                configuration['root_path'],
                configuration['root_suffix'],
                configuration['root_folder'])

        # 3a. rms, aad (of data fraction)
        datafrac = mdp.get_hist_fraction(data, float(fraction))
        newlist['rms_frac' + binned_histo][index] = mdp.calc_hist_RMS(datafrac)
        newlist['aad_frac' + binned_histo][index] = mdp.calc_aad(data, float(fraction))

        # 3. gauss fit
        #fitresult = mff.fit_gauss(datafrac, mu0=0.0, sigma0=0.3, height0=50e3)
        #newlist['gauss_mu'     ][index] = fitresult['mu'     ]
        #newlist['gauss_si'     ][index] = fitresult['si'     ]
        #newlist['gauss_si_dev' ][index] = fitresult['dsi'    ]
        #newlist['gauss_height' ][index] = fitresult['height' ]
        #newlist['gauss_chi2red'][index] = fitresult['chi2red']

        # 4. combined fit (with two sigmas)
        #fitresult = mff.fit_combined(data, mu0=0.0, si0=0.3, nu_s0=5.0, si_s0= 0.3, frac0=0.3, height0=50e3)
        #newlist['combined_mu'     ][index] = fitresult['mu'     ]
        #newlist['combined_si_g'   ][index] = fitresult['si'     ]
        #newlist['combined_si_g_dev'][index] = fitresult['dsi'    ]
        #newlist['combined_nu_s'   ][index] = fitresult['nu_s'   ]
        #newlist['combined_si_s'   ][index] = fitresult['si_s'   ]
        #newlist['combined_si_s_dev'][index] = fitresult['dsi_s'  ]
        #newlist['combined_frac'   ][index] = fitresult['frac'   ]
        #newlist['combined_height' ][index] = fitresult['height' ]
        #newlist['combined_chi2red'][index] = fitresult['chi2red']

        # 5. combined fit with one sigma
        #fitresult = mff.fit_combined_one_sigma(data, mu0=0.0, si0=0.3, nu_s0=5.0, frac0=0.3, height0=50e3)
        #newlist['combined_one_mu'     ][index] = fitresult['mu'     ]
        #newlist['combined_one_si'     ][index] = fitresult['si'     ]
        #newlist['combined_one_si_dev' ][index] = fitresult['dsi'    ]
        #newlist['combined_one_nu_s'   ][index] = fitresult['nu_s'   ]
        #newlist['combined_one_frac'   ][index] = fitresult['frac'   ]
        #newlist['combined_one_height' ][index] = fitresult['height' ]
        #newlist['combined_one_chi2red'][index] = fitresult['chi2red']

if False:
    ##########################################
    # Normalizing width values
    # TODO: normalizing
    #for bin_index in range(configuration['bins']):
    #    binned_histo = '%02d'%(bin_index)

    def normalize_by_air_measurement(keyword, relative_error=True):
        # getting zero values
        cut_zero = (newlist['thickness'] == 0.0)
        data_zero_energy = newlist[cut_zero]['energy']
        data_zero_keyword = newlist[cut_zero][keyword]
        for index, value in enumerate(newlist):
            # normalized value
            theta_meas = newlist[keyword][index]
            theta_air0 = data_zero_keyword[data_zero_energy == newlist['energy'][index]][0]
            if theta_meas <= theta_air0:
                newlist[keyword+'_norm'][index] = 0.0
            else:
                newlist[keyword+'_norm'][index] = math.sqrt(theta_meas**2 - theta_air0**2)
            # propagated error
            if relative_error == True:
                theta_meas_error = rel_error * theta_meas
                theta_air0_error = rel_error * theta_air0
            else:
                theta_meas_error = newlist[keyword+'_dev'][index]
                theta_air0_error = newlist[cut_zero][keyword+'_dev'][data_zero_energy == newlist['energy'][index]][0]
            # result/return
            if newlist[keyword+'_norm'][index] == 0.0:
                newlist[keyword+'_norm_error'][index] = 0.0
            else:
                newlist[keyword+'_norm_error'][index] = math.sqrt(
                        (theta_meas/newlist[keyword+'_norm'][index] * theta_meas_error)**2 +
                        (theta_air0/newlist[keyword+'_norm'][index] * theta_air0_error)**2 )

    # rms ROOT
    normalize_by_air_measurement('ROOT_rms', relative_error=True)
    # rms frac
    normalize_by_air_measurement('rms_frac', relative_error=True)
    # aad frac
    normalize_by_air_measurement('rms_frac', relative_error=True)

############################################
# Save in npy format
print "saving npy-data in:", outfile
print "including these values:", newlist.dtype.names
np.savetxt(outfile+'.csv', newlist, delimiter=',', header=str(newlist.dtype.names[:]))
np.save(outfile, newlist)
