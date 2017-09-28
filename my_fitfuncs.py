""" Module my_fitfuncs
A module collecting fitting functions and methods"""

#! /usr/bin/python
#import math
#import sys, os
#import getopt
#import time
import numpy as np
from scipy.optimize import curve_fit
from scipy.stats import t
from scipy.special import gamma
#import scipy as sp #import optimize.curve_fit
# for joining&combining structured arrays
#import numpy.lib.recfunctions as rfn

#################################################################
# functions

def fitfunc_linear(xdata, *para):
    slope  = para[0]
    offset = para[1]
    return slope * xdata + offset

def fitfunc_linear_zero(xdata, *para):
    slope  = para[0]
    return slope * xdata

def fitfunc_gauss(xdata, *para):
    # para = [mu, sigma, height]
    mu      = para[0]
    si      = para[1]
    height  = para[2]
    return height / (si*np.sqrt(2.*np.pi)) * np.exp(-0.5*(xdata-mu)**2/si**2)

def fitfunc_gauss_normed(xdata, *para):
    mu  = para[0]
    si  = para[1]
    return 1./(si*np.sqrt(2.*np.pi)) * np.exp(-0.5*(xdata-mu)**2/si**2)

def fitfunc_studentt(xdata, *para):
    mu      = para[0]
    nu      = para[1]
    height  = para[2]
    return height * t.pdf(xdata, nu, loc=mu)

def fitfunc_studentt_nonstand_normed(xdata, *para):
    mu      = para[0]
    nu_s    = para[1]
    si_s    = para[2]
    gamma_factor = gamma((nu_s+1.)/2.) / gamma(nu_s/2.)
    return gamma_factor / (np.sqrt(nu_s*np.pi)*si_s) * (1. + ((xdata - mu)**2. / (nu_s * si_s**2.)))**(-(nu_s+1.)/2.)

def fitfunc_studentt_nonstand(xdata, *para):
    mu      = para[0]
    nu_s    = para[1]
    si_s    = para[2]
    height  = para[3]
    return height * fitfunc_studentt_nonstand_normed(xdata, mu, nu_s, si_s)

def fitfunc_combined_gauss_studentt(xdata, *para):
    # para = [mu, si_g, nu_s, si_s, frac, height]
    mu      = para[0]
    si_g    = para[1]
    nu_s    = para[2]
    si_s    = para[3]
    frac    = para[4]
    height  = para[5]
    return height * ( (1-frac)*fitfunc_gauss_normed(xdata, mu, si_g) + frac*fitfunc_studentt_nonstand_normed(xdata, mu, nu_s, si_s))

def fitfunc_combined_gauss_studentt_one_sigma(xdata, *para):
    # para = [mu, si, nu_s, frac, height]
    mu      = para[0]
    si    = para[1]
    nu_s    = para[2]
    frac    = para[3]
    height  = para[4]
    return height * ( (1-frac)*fitfunc_gauss_normed(xdata, mu, si) + frac*fitfunc_studentt_nonstand_normed(xdata, mu, nu_s, si))

###############################################
# methods 

def fit_linear(data, dydata, slope0, offset0):
  xdata = data[0]
  ydata = data[1]
  if np.mean(dydata) == 0.:
      print "linear fit using sqrt(n) deviation"
      dydata = np.sqrt(ydata); dydata = np.where(dydata > 0.0, dydata, 1) #; print dy 
  # start parameter
  para0 = [slope0, offset0] # slope, offset
  para, cov = curve_fit(fitfunc_linear, xdata, ydata, p0=para0, sigma=dydata)
  slope = para[0]
  offset = para[1]
  dslope = np.sqrt(cov[0][0])
  doffset = np.sqrt(cov[1][1])
  # chi**2
  print "y data",  ydata
  print "y fit", fitfunc_linear(xdata, *para)
  print "d y data", dydata
  print "data freedoms", len(ydata)
  print "parameter freedoms", len(para)
  chi2 = np.sum(((ydata - fitfunc_linear(xdata, *para)) / dydata)**2)
  chi2red = chi2 / (len(ydata)-len(para))
  fit_results = {'slope':slope, 'offset':offset, 'dslope':dslope, 'doffset':doffset, 'chi2':chi2, 'chi2red':chi2red}
  return fit_results

def fit_gauss(data, mu0, sigma0, height0):
  xdata = data[0]
  ydata = data[1]
  dydata = np.sqrt(ydata); dydata = np.where(dydata > 0.0, dydata, 1) #; print dy 
  # start parameter
  para0 = [mu0, sigma0, height0] # mu, sigma, norm
  para, cov = curve_fit(fitfunc_gauss, xdata, ydata, p0=para0, sigma=dydata)
  mu = para[0]
  si = abs(para[1])
  height = para[2]
  dmu = np.sqrt(cov[0][0])
  dsi = np.sqrt(cov[1][1])
  # chi**2
  chi2 = np.sum(((ydata - fitfunc_gauss(xdata, *para)) / dydata)**2)
  chi2red = chi2 / (len(ydata)-len(para))
  fit_results = {'mu':mu, 'si':si, 'height':height, 'dmu':dmu, 'dsi':dsi, 'chi2':chi2, 'chi2red':chi2red}
  return fit_results

def fit_combined(data, mu0, si0, nu_s0, si_s0, frac0, height0):
  xdata = data[0]
  ydata = data[1]
  dydata = np.sqrt(ydata); dydata = np.where(dydata > 0.0, dydata, 1) #; print dy 
  # start parameter
  para0 = [mu0, si0, nu_s0, si_s0, frac0, height0]
  para_bounds=([-np.inf, 0.0, 1.0, 0.0, 0.0, 1.0], [np.inf, np.inf, np.inf, np.inf, 1.0, np.inf])
  para, cov = curve_fit(fitfunc_combined_gauss_studentt, xdata, ydata, p0=para0, sigma=dydata, bounds=para_bounds)
  mu = para[0]
  si = abs(para[1])
  dsi = np.sqrt(cov[1][1])
  nu_s = para[2]
  si_s = para[3]
  dsi_s = np.sqrt(cov[3][3])
  frac = para[4]
  height = para[5]
  # chi**2
  chi2 = np.sum(((ydata - fitfunc_combined_gauss_studentt(xdata, *para)) / dydata)**2)
  chi2red = chi2 / (len(ydata)-len(para))
  fit_results = {'mu':mu, 'si':si, 'dsi':dsi, 'nu_s':nu_s, 'si_s':si_s, 'dsi_s':dsi_s, 'frac':frac, 'height':height, 'chi2':chi2, 'chi2red':chi2red}
  return fit_results

def fit_combined_one_sigma(data, mu0, si0, nu_s0, frac0, height0):
  xdata = data[0]
  ydata = data[1]
  dydata = np.sqrt(ydata); dydata = np.where(dydata > 0.0, dydata, 1) #; print dy 
  # start parameter
  para0 = [mu0, si0, nu_s0, frac0, height0]
  para_bounds=([-np.inf, 0.0, 1.0, 0.0, 1.0], [np.inf, np.inf, np.inf, 1.0, np.inf])
  para, cov = curve_fit(fitfunc_combined_gauss_studentt_one_sigma, xdata, ydata, p0=para0, sigma=dydata, bounds=para_bounds)
  mu = para[0]
  si = abs(para[1])
  dsi = np.sqrt(cov[1][1])
  nu_s = para[2]
  frac = para[3]
  height = para[4]
  # chi**2
  chi2 = np.sum(((ydata - fitfunc_combined_gauss_studentt_one_sigma(xdata, *para)) / dydata)**2)
  chi2red = chi2 / (len(ydata)-len(para))
  fit_results = {'mu':mu, 'si':si, 'dsi':dsi, 'nu_s':nu_s, 'frac':frac, 'height':height, 'chi2':chi2, 'chi2red':chi2red}
  return fit_results

