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

sys.path.insert(0, '../')
import my_fitfuncs as mff

script_name = inspect.getfile(inspect.currentframe()) 
print "Starting script:", sys.argv[0]
#data = sys.argv[1]
data = "/home/jande/Documents/fhl-wgs01/data/data_datura/161128_scatalu/EUTelescope_root_files/kappa100_2kink/run000024-GBLKinkEstimator_kappa100_2kink.root" 


# Open a file using python-like context
with root_open(data) as input_file:

  for path, dirs, objects in input_file.walk():
    print "path:", path
  #  print "dirs:", dirs
    print "objects:", objects

  print "list all:", input_file.ls()

  ######################

  # getting data 
  #histdata = input_file.Fitter06.GBL.gblprbx
  #histdata = input_file.Fitter06.GBL.gblsumkx2andsumky2_xyP
  histdata = getattr(input_file.Fitter06.GBL, 'gblsumkx2andsumky2_xyP')
  print "output input_file.TH2"
  print histdata
	
  # Make a new figure (or you could clear the old one)
  figure, axes = plt.subplots(figsize=(6, 6))#, dpi=100)

  # Plot a 2D histogram with a colour-bar key
  counts, xedges, yedges, image = root2matplotlib.hist2d( histdata, cmap="cool" )
  print "output root2matplolib.hist"
  print np.shape(counts), np.size(counts)#, counts
  print np.size(xedges)#, xedges  # dimension + 1 
  print np.size(yedges)#, yedges  # dimension + 1 
  #print np.shape(counts) # dimension
  #print np.size(counts)  # total entries
  print np.sum(counts)   # sum
  print np.mean(counts)  # mean
  print np.std(counts)   # std
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
  print np.shape(counts), np.size(counts)#, counts
  print np.sum(counts)   # sum
  print np.mean(counts)  # mean
  print np.std(counts)   # std
  #print np.max(counts)   # max
  #print np.min(counts)   # min
  figure.savefig( sys.argv[0][:-3] + str(".pdf") )
  plt.close(figure)

  # 1d style 
  print "output 1d style"
  histfile = ROOT.TFile(data)
  # get hist data
  histdata = histfile.Get('Fitter06/GBL/gblsumkx2andsumky2_xyP') #print histdata
  # write as numpy array
  counts, edges = hist2array(histdata, include_overflow=False, return_edges=True) #print counts, edge
  print np.shape(counts), np.size(counts)#, counts
  print np.shape(counts[0]), np.size(counts[0])#, counts
  print np.shape(counts.T[0]), np.size(counts.T[0])#, counts
  print np.size(edges), edges  # dimension + 1 
  print np.size(edges[0])#, edges  # dimension + 1 
  print np.size(edges[1])#, edges  # dimension + 1 
  #print np.size(yedges)#, yedges  # dimension + 1 
  binwidth_x = abs(edges[0][1]-edges[0][0])
  bincenters_x = np.array(edges[0][:-1]) + binwidth_x/2. # root probably adds a whole binwidth, irrelevant for rms
  binwidth_y = abs(edges[1][1]-edges[1][0])
  bincenters_y = np.array(edges[1][:-1]) + binwidth_y/2. # root probably adds a whole binwidth, irrelevant for rms
  print np.size(bincenters_x), bincenters_x  # dimension + 1 
  print np.size(bincenters_y), bincenters_y  # dimension + 1 
  #print np.sum(counts)   # sum
  #print np.mean(counts)  # mean
  #print np.std(counts)   # std

  # projection in x and y
  projection_x = counts.sum(axis=1)
  projection_y = counts.sum(axis=0)
  #print np.size(projection_x), projection_x
  #print np.size(projection_y), projection_y
  # cut zeroes plus safety margin of ~1%
  margin_x = 6
  index_x_non_zero = np.where(projection_x != 0.)
  data_projection_x = projection_x[index_x_non_zero][margin_x+1:-margin_x-1]
  pos_projection_x = bincenters_x[index_x_non_zero][margin_x+1:-margin_x-1]
  print np.size(data_projection_x), data_projection_x
  print np.size(pos_projection_x), pos_projection_x
  margin_y = 3
  index_y_non_zero = np.where(projection_y != 0.)
  data_projection_y = projection_y[index_y_non_zero][margin_y+1:-margin_y-1]
  pos_projection_y = bincenters_y[index_y_non_zero][margin_y+1:-margin_y-1]
  print np.size(data_projection_y), data_projection_y
  print np.size(pos_projection_y), pos_projection_y
  data_x = np.vstack((pos_projection_x, data_projection_x))
  data_y = np.vstack((pos_projection_y, data_projection_y))
  #print np.size(data_x), np.size(data_y)

  print mff.fit_linear(data_x, 0.0, 5000)
  print mff.fit_linear(data_y, 0.0, 5000)











  

