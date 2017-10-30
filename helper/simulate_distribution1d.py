'''simulate distribution along an axis

Usage:
    simulate_distribution1d.py

Options:
    -h --help                   show usage of this script
    -v --version                show the version of this script
'''

from docopt import docopt
import numpy as np
import math
import matplotlib.pyplot as plt

import sys
sys.path.insert(0, '../')
import my_fitfuncs as mff
import my_dataproc as mdp

def position_dependent_mean(position, distribution, *para):
    mu_start = -math.atan((position + 10.)/40) #rad
    mu_end = math.atan((10. - position)/40) #rad
    # print mu_start, mu_end
    mu_data = np.linspace(mu_start, mu_end, 1000) # rad
    if distribution == 'gauss':
        # para = [mu, sigma, height]
        count_data = mff.fitfunc_gauss(mu_data, *para)
    elif distribution == 'combined':
        # para = [mu, si, nu_s, frac, height]
        count_data = mff.fitfunc_combined_gauss_studentt_one_sigma(mu_data, *para)
    else:
        print "no valid distribution!!"
        exit()
    return mdp.calc_hist_mean(np.vstack((mu_data, count_data)))

def distribution1d(x_data, distribution, *para):
    y_data = np.zeros(len(x_data))
    for index, value in enumerate(x_data):
        y_data[index] = position_dependent_mean(value, distribution, *para)
        #print y_data[index]
    return y_data

############################################
# arguments
arguments = docopt(__doc__, version='simulate 1d distribution')


############################################
# Plots
fig, ax = plt.subplots(1, 1)

distribution = 'gauss'
distribution = 'combined'

sigmas = np.array([0.005, 0.001]) # rad
#sigmas = np.array([0.995, 1.23, 1.62, 2.37, 4.01]) # mrad from 10mm measurements

nu = np.array([2.83, 1.45])
frac = np.array([0.53, 0.42])


x_data = np.linspace(-10, 10, 1000)
x_fit = np.linspace(-10, 10, 500)
for index, value in enumerate(sigmas):
    if distribution == 'gauss':
        y_data = distribution1d(x_data, distribution, 0.15, value, 1.0)
    elif distribution == 'combined':
        y_data = distribution1d(x_data, distribution, 0.15, value, nu[0], frac[0], 1.0)
    plt.plot(x_data, y_data, label='sigma {}'.format(value))
    #fitresults = mff.fit_linear(np.vstack((x_data, y_data)), 0.0, 1.0, 0.0)
    #y_fit = mff.fitfunc_linear(x_fit, fitresults['slope'], fitresults['offset'])
    #plt.plot(x_fit, y_fit, label='slope {} offset {}'.format(fitresults['slope'], fitresults['offset']))


plt.legend()
plt.xlabel('x-position at SUT [mm]')
plt.ylabel('mean of distribution [rad]')
#plt.xlim(-9., 9.)
#plt.ylim(-0.001, 0.001)

############################################
# output names
title_save = 'simulate_distribution1d_' + distribution
plt.savefig(title_save + '.pdf')
