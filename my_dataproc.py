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

def get_projections(counts, bincenters_x, bincenters_y):
  # projection in x and y
  projection_x = counts.sum(axis=1) # sum along the axis, thus it is this way!
  projection_y = counts.sum(axis=0)
  #print np.size(projection_x), np.size(projection_y)
  # x-cut zeroes
  index_x_non_zero = np.where(projection_x != 0.)
  index_x_min = index_x_non_zero[0][0]
  index_x_max = index_x_non_zero[0][-1]
  data_projection_x = projection_x[index_x_min:index_x_max+1]
  pos_projection_x  = bincenters_x[index_x_min:index_x_max+1]
  # y-cut zeroes
  index_y_non_zero = np.where(projection_y != 0.)
  index_y_min = index_y_non_zero[0][0]
  index_y_max = index_y_non_zero[0][-1]
  data_projection_y = projection_y[index_y_min:index_y_max+1]
  pos_projection_y  = bincenters_y[index_y_min:index_y_max+1]
  #print np.size(pos_projection_x), np.size(pos_projection_y)
  # normalize: here take the sum axis!!  
  data_projection_x = data_projection_x/np.size(data_projection_y)
  data_projection_y = data_projection_y/np.size(data_projection_x)
  # stack data
  data_x = np.vstack((pos_projection_x, data_projection_x))
  data_y = np.vstack((pos_projection_y, data_projection_y))
  return data_x, data_y

def projections(counts, bincenters_x, bincenters_y, margin_x, margin_y):
  # projection in x and y
  projection_x = counts.sum(axis=1) # sum along the axis, thus it is this way!
  projection_y = counts.sum(axis=0)
  # x-cut zeroes plus safety margin of ~1%
  index_x_non_zero = np.where(projection_x != 0.)
  data_projection_x = projection_x[index_x_non_zero][margin_x+1:-margin_x-1]
  pos_projection_x = bincenters_x[index_x_non_zero][margin_x+1:-margin_x-1]
  # y-cut zeroes plus safety margin of ~1%
  index_y_non_zero = np.where(projection_y != 0.)
  data_projection_y = projection_y[index_y_non_zero][margin_y+1:-margin_y-1]
  pos_projection_y = bincenters_y[index_y_non_zero][margin_y+1:-margin_y-1]
  # normalize  
  data_projection_x = data_projection_x/np.size(data_projection_y)
  data_projection_y = data_projection_y/np.size(data_projection_x)
  # stack data
  data_x = np.vstack((pos_projection_x, data_projection_x))
  data_y = np.vstack((pos_projection_y, data_projection_y))
  return data_x, data_y

def rebin_data(data, number_merged_points):
    if len(data) % number_merged_points == 0:
        return data.reshape(-1, number_merged_points).mean(axis=1)
    else:
        print "Please choose a proper divider for {}-entries array".format(len(data))
        exit()

def cut_data(data, cutbins):
  data0 = data[0][cutbins:-cutbins]
  data1 = data[1][cutbins:-cutbins]
  data = np.vstack((data0, data1))
  return data

def get_hist_fraction(data, fraction):
  #print data, np.shape(data)
  if fraction <= 0.:
    return 0
  if fraction >= 1.:
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

def calc_aad(data, fraction):
    #print data
    # create original hist data
    # create empty array with right length
    entries_total = calc_entries(data[1])
    hist_origin_abs_values = np.zeros(int(entries_total))
    #print entries_total, len(hist_origin_abs_values)
    # loop over bins and fill array with bin entries * bin x value
    start_index = 0
    for bin_index, bin_entries in enumerate(data[1]):
        if bin_entries != 0.0:
            #print data[0][bin_index], bin_entries
            for index in range(int(bin_entries)):
                fill_index = int(start_index +  index)
                # fill in the absolute value
                hist_origin_abs_values[fill_index] = abs(data[0][bin_index])
            start_index += bin_entries #print start_index
    #print hist_origin_values
    #print np.sort(hist_origin_abs_values)
    # calculate the mean from fraction
    end_fraction_index = int(fraction * entries_total)
    return np.mean(np.sort(hist_origin_abs_values)[:end_fraction_index]) 

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
