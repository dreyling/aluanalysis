""" Module myrootlib
A module for accesing and processing ROOT files"""

#! /usr/bin/python
#import math
#import sys, os
#import getopt
#import time
import numpy as np
#from scipy.optimize import curve_fit

# for joining&combining structured arrays
import numpy.lib.recfunctions as rfn

from ROOT import TFile #, TF1, TCanvas, TH1
#from rootpy.io import root_open # Look at http://www.rootpy.org/ for full documentation
from root_numpy import hist2array #, root2array, tree2array

#################################################################
# reading csv file and extend

def readRunlist(filename):
  print "opening...", filename
  return np.genfromtxt(filename, delimiter='\t', names=True)

def extendList(runlist, *newcol_name):
    newlist = runlist
    for index, value in enumerate(newcol_name):
        newcol = np.zeros(np.size(runlist), dtype = {'names': [value], 'formats': ['f8']} )
        newlist = rfn.merge_arrays((newlist, newcol), flatten = True, usemask = False)
    return newlist

################################################################
# reading root files

# get Data
# runlist: csv file (same folder)
# runindex: index to loop, max. is  length of runlist['runnr'] e.g.
# histname: string, name of Root Histogram
# path: path of rrot files
# suffix: filename: run000X + suffix + .root
# rootfolder: folder name in root file
def getHist1Data(runlist, runindex, histname, path, suffix, rootfolder):
  rootfile = path + "run0"+'{:05d}'.format(int(runlist['runnr'][runindex])) + suffix + ".root"
  print "opening...", rootfile
  # open root file
  histfile = TFile(rootfile)
  # get hist data
  histdata = histfile.Get(rootfolder + histname) #print histdata
  # write as numpy array
  counts, edges = hist2array(histdata, include_overflow=False, return_edges=True) #print counts, edge
  # shift hist data by half of the binwidth, checked with np.where(data[0] > 0.)[0][0]
  binwidth = abs(edges[0][1]-edges[0][0])
  edges = np.array(edges) + binwidth/2. # root probably adds a whole binwidth, irrelevant for rms
  # return x and y data
  data0 = edges[0][:-1]
  data1 = counts
  data = np.vstack((data0, data1))
  return data

def getHistSpecs(runlist, runindex, histname, path, suffix, rootfolder):
  rootfile = path + "run0"+'{:05d}'.format(int(runlist['runnr'][runindex])) + suffix + ".root"
  print "opening...", rootfile
  # open root file
  histfile = TFile(rootfile)
  # get hist data
  histdata = histfile.Get(rootfolder + histname) #print histdata
  return {'mean':histdata.GetMean(1), 'stddev':histdata.GetStdDev(1), 'integral':histdata.Integral(), 'entries':histdata.GetEntries()}

def loopRunAndSum(runlist, histname, path, suffix, rootfolder):
  data = np.zeros((2, np.size(runlist['runnr'])))
  counts = 1 
  for index, value in enumerate(runlist['runnr']):
    data[0][index] = value
    data[1][index] = np.sum(getHist1Data(runlist, index, histname, path, suffix, rootfolder)[counts])
  return data

def getHist2Data(runlist, runindex, histname, path, suffix, rootfolder):
  rootfile = path + "run0"+'{:05d}'.format(int(runlist['runnr'][runindex])) + suffix + ".root"
  print "opening...", rootfile
  # open root file
  histfile = TFile(rootfile)
  # get hist data
  histdata = histfile.Get(rootfolder + histname) #print histdata
  # write as numpy array
  counts, edges = hist2array(histdata, include_overflow=False, return_edges=True) #print counts, edge
  # shift hist data by half of the binwidth, checked with access_th2.py
  binwidth_x = abs(edges[0][1]-edges[0][0])
  bincenters_x = np.array(edges[0][:-1]) + binwidth_x/2. 
  binwidth_y = abs(edges[1][1]-edges[1][0])
  bincenters_y = np.array(edges[1][:-1]) + binwidth_y/2. 
  # return counts (x, y)-array, x_edges and y_edges data
  return counts, bincenters_x, bincenters_y

