""" Module my_dataproc
A module for processing two-dimensional numpy arrays (i.e. histograms)"""

#! /usr/bin/python
#import math
#import sys, os
#import getopt
#import time
import numpy as np
#from scipy.optimize import curve_fit
#import scipy as sp #import optimize.curve_fit
# for joining&combining structured arrays
#import numpy.lib.recfunctions as rfn

#################################################################

def cut_data(data, cutbins):
  data0 = data[0][cutbins:-cutbins]
  data1 = data[1][cutbins:-cutbins]
  data = np.vstack((data0, data1))
  return data

def get_hist_fraction(data, fraction):
  if fraction <= 0:
    return 0
  if fraction >= 1:
    fraction = 1.
    index_start = 0
    index_end = np.size(data[0])-1
  # set range to fit
  entries_total = calc_entries(data[1]) #print type(entries_total)
  # normalized cumulative sum array
  cumsum_normal = np.cumsum(data[1])/entries_total #print cumsum_normal, type(cumsum_normal)
  index_start = np.where(cumsum_normal > (1.-fraction)/2.)[0][0]
  index_end = np.where(cumsum_normal > fraction+(1.-fraction)/2.)[0][0] #print index_start, index_end
  # set data to fit
  data0 = data[0][index_start:index_end].copy()
  data1 = data[1][index_start:index_end].copy()
  data = np.vstack((data0, data1))
  return data

def calc_entries(data):
  return np.sum(data)

def calc_mean(data):
  return np.mean(data)

def calc_RMS(data):
  return np.sqrt(np.mean(np.square(data)))

def calc_hist_median(data):
  index = np.where(np.cumsum(data[1]) > calc_entries(data[1]) / 2.)
  return data[0][index]

def calc_hist_mean(data):
  weights = np.multiply(data[0], data[1])
  return np.sum(weights)/np.sum(data[1])

def calc_hist_RMS(data):
  weights = np.multiply(np.square(data[0]-calc_hist_mean(data)), data[1])
  return np.sqrt(np.sum(weights)/np.sum(data[1]))

def print_data(data):
  print "xdata:", data[0]
  print "ydata:", data[1]
  print "entries:", calc_entries(data[1])
  # simple mean, rms
  print "mean:", calc_mean(data[1])
  print "rms:", calc_RMS(data[1])
  # Todo: not the same as in ROOT...
  print "hist mean:", calc_hist_mean(data)
  print "hist RMS:", calc_hist_RMS(data)
