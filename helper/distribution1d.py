import sys
import numpy as np
import math
import matplotlib.pyplot as plt

sys.path.insert(0, '../')
import my_fitfuncs as mff
import my_dataproc as mdp

def calculate_position_dependent_distribution_mean(position, sigma, misaligned):
    mu_start = -math.atan((position + 10.)/50) - misaligned
    mu_end = math.atan((10. - position)/50) - misaligned
    #print mu_start, mu_end
    mu_data = np.linspace(mu_start, mu_end, 100)
    count_data = mff.fitfunc_gauss_normed(mu_data, 0.0, sigma)
    return mdp.calc_hist_mean(np.vstack((mu_data, count_data)))

#print calculate_position_dependent_distribution_mean(10, 1.0)

def distribution1d(x_data, sigma, misaligned):
    y_data = np.zeros(len(x_data))
    for index, value in enumerate(x_data):
        y_data[index] = calculate_position_dependent_distribution_mean(
                value, sigma, misaligned)
        #print y_data[index]
    return y_data

fig, ax = plt.subplots(1, 1)

misaligned = 0.05

x_data = np.linspace(-10, 10, 1000)
for index, value in enumerate([0.01, 0.05, 0.1, 0.2, 0.4, 1.0]):
    y_data = distribution1d(x_data, value, misaligned)
    plt.plot(x_data, y_data, label='sigma {}'.format(value))

plt.legend()
plt.xlabel('x-position at SUT [mm]')
plt.ylabel('mean of distribution [rad]')

plt.savefig(sys.argv[0][:-3] + '_' + str(misaligned).replace('.','-') + '.pdf')
