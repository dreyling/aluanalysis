#! /usr/bin/env python
import inspect, os
import sys
from matplotlib import rcParams
import matplotlib.pyplot as plt
from rootpy.plotting import set_style, root2matplotlib
from rootpy.io import root_open # Look at http://www.rootpy.org/ for full documentation
import ROOT
import numpy as np

from root_numpy import root2array, tree2array, hist2array
from root_numpy.testdata import get_filepath

script_name = inspect.getfile(inspect.currentframe()) 
print "Starting script:", sys.argv[0]
#data = sys.argv[1]
data = "/opt/paper2/GBLKinkEvaluator/bin/output_measurement.root"

# Open a file using python-like context
with root_open(data) as input_file:

  for path, dirs, objects in input_file.walk():
    print "path:", path
  #  print "dirs:", dirs
    print "objects:", objects

  print "list all:", input_file.ls()

  ######################

  # getting data 
  histdata = input_file.m26fitter_5.gblrx0 #kinkx
  print "output input_file."
  print histdata
 
  # Convert a ROOT histogram into a NumPy array
  counts, edges = root2array(histdata)
  print "output hist2array"
  print np.size(counts), counts
  print np.size(edges), edges   # size(counts) + 1 
  
  exit()
	

  # Make a new figure (or you could clear the old one)
  figure, axes = plt.subplots(figsize=(6, 6))#, dpi=100)

  # Plot a 1D histogram TH1
  counts, edges = root2matplotlib.hist( histdata )
  print "output root2matplolib.hist"
  print counts
  print edges

  # Convert a ROOT histogram into a NumPy array
  counts, edges = hist2array(histdata, include_overflow=True, return_edges=True)
  print "output hist2array"
  print np.size(counts), counts
  print np.size(edges), edges   # size(counts) + 1 
  #print np.shape(counts) # dimension
  #print np.size(counts)  # total entries
  #print np.sum(counts)   # sum
  #print np.mean(counts)  # mean
  #print np.std(counts)   # std
  #print np.max(counts)   # max
  #print np.min(counts)   # min

  # Draw axes with labels at the ends
  plt.xlabel("x")#, ha="right", position=(1, 0) )
  plt.ylabel("y")#, ha="right", position=(0, 1))

  plt.show()
 
  figure.savefig( sys.argv[0][:-3] + str(".pdf") )
  plt.close(figure)
