'''Moliere package

Usage:
    moliere.py

Options:
    -h --help                   show usage of this script
    -v --version                show the version of this script
'''

import numpy as np
import math
import matplotlib.pyplot as plt
import scipy.integrate as integrate

##################################################
# Physical constants


##################################################
# Moliere scattering




def moliere(theta_scattering, chi_c):
    C = 0.577 # Euler's constant
    b = math.log((chi_c/chi_a)**2.) + 1. - 2.*C
    B = 1.
    theta = theta_scattering / (chi_c * math.sqrt(B))
    return theta



# using ctypes: https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.quad.html


def moliere_distribution(theta, screening_angle=1., theta_0=0.0, normalisation=1.):
    return normalisation * np.exp(-1.*np.power((theta-theta_0)/screening_angle, 2.))

def main():
    #'''running this module as the primary one"""
    # data
    theta = np.linspace(-1, 1, 500)
    height = moliere_distribution(theta)
    # plot
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.plot(theta, height)
    ax.set_xlabel(r'$\theta$ [a.u.]')
    ax.set_ylabel(r'height [a.u.]')
    ax.set_yscale("log")
    # save
    name_save =  "moliere.pdf"
    fig.savefig(name_save)
    print "evince " + name_save + "&"

###################################################
# main
if __name__ == '__main__':
    main()



