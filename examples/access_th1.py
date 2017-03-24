#! /usr/bin/env python
import inspect, os
import sys
from matplotlib import rcParams
import matplotlib.pyplot as plt
from rootpy.plotting import set_style, root2matplotlib
from rootpy.io import root_open # Look at http://www.rootpy.org/ for full documentation
from ROOT import TFile
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
  histdata = input_file.Fitter06.GBL.gblry0 #kinkx
  #histdata = input_file.Fitter06.GBL.gblayprime6  #gblrxvsx0 #gblprb#gblchi2b#selax # okay
  #histdata = input_file.Fitter06.Tracks.sixkxzy #sixx0 # okay
  #histdata = input_file.Fitter06.Downstream.dridxvsy # okay
  #histdata = input_file.Fitter06.Upstream.tridx4b #tridxvsx #tridx # okay
  #histdata = input_file.hEvtProcessingTime # okay
  #histdata = input_file.Fitter06.triddaMindut # okay
  #histdata = input_file.Fitter06.Telescope.dx02 # okay
  print "output input_file.TH1"
  print histdata
	

  # Make a new figure (or you could clear the old one)
  figure, axes = plt.subplots(figsize=(6, 6))#, dpi=100)

  # Plot a 1D histogram TH1
  counts, edges = root2matplotlib.hist( histdata )
  print "output root2matplolib.hist"
  print counts
  print edges

  # Convert a ROOT histogram into a NumPy array
  counts, edges = hist2array(histdata, include_overflow=False, return_edges=True)
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

  #plt.show()


  rootfile = TFile(data)
  histdata = rootfile.Get("Fitter06/GBL/gblry0")
  print histdata
  print histdata.GetMean()
  print histdata.GetStdDev()
  print histdata.Integral()
  print histdata.GetEntries()


  exit() 

  counts, edges = hist2array(histdata, include_overflow=True, return_edges=True)
  print "output hist2array"
  print np.size(counts), counts
  print np.size(edges), edges   # size(counts) + 1 


 
  figure.savefig( sys.argv[0][:-3] + str(".pdf") )
  plt.close(figure)
