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
data = "/home/jande/Documents/ownCloud/X0_hendrik/measurement/run000046-GBLKinkEstimator_kappa100.root" 


# Open a file using python-like context
with root_open(data) as input_file:

  for path, dirs, objects in input_file.walk():
    print "path:", path
  #  print "dirs:", dirs
    print "objects:", objects

  print "list all:", input_file.ls()

  ######################

  # getting data 
  histdata = input_file.Fitter06.GBL.gblprbx
  print "output input_file.TH2"
  print histdata
	
  # Make a new figure (or you could clear the old one)
  figure, axes = plt.subplots(figsize=(6, 6))#, dpi=100)

  # Plot a 2D histogram with a colour-bar key
  counts, xedges, yedges, image = root2matplotlib.hist2d( histdata, cmap="cool" )
  print "output root2matplolib.hist"
  print np.shape(counts), np.size(counts), counts
  print np.size(xedges), xedges  # dimension + 1 
  print np.size(yedges), yedges  # dimension + 1 
  #print np.shape(counts) # dimension
  #print np.size(counts)  # total entries
  #print np.sum(counts)   # sum
  #print np.mean(counts)  # mean
  #print np.std(counts)   # std
  #print np.max(counts)   # max
  #print np.min(counts)   # min
  # print image 				   # image imformation 
  plt.colorbar(image, ax=axes)
  
  # Draw axes with labels at the ends
  plt.xlabel("x")#, ha="right", position=(1, 0) )
  plt.ylabel("y")#, ha="right", position=(0, 1))

  # Convert a ROOT 2d histogram into a NumPy array
  counts = hist2array(histdata)
  print "output hist2array"
  print np.shape(counts), np.size(counts) ,counts
  #print np.sum(counts)   # sum
  #print np.mean(counts)  # mean
  #print np.std(counts)   # std
  #print np.max(counts)   # max
  #print np.min(counts)   # min

  plt.show()
  
  figure.savefig( sys.argv[0][:-3] + str(".pdf") )
  plt.close(figure)

