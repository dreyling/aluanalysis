#! /usr/bin/env python
import inspect, os
import sys
from matplotlib import rcParams
import matplotlib.pyplot as plt
from rootpy.plotting import set_style, root2matplotlib
from rootpy.io import root_open # Look at http://www.rootpy.org/ for full documentation
#import ROOT
from ROOT import TFile, TProfile2D
import numpy as np

from root_numpy import root2array, tree2array, hist2array, array
from root_numpy.testdata import get_filepath

sys.path.insert(0, '../')
import my_fitfuncs as mff
import my_rootread as mrr
import myparams as mpm

script_name = inspect.getfile(inspect.currentframe()) 
print "Starting script:", sys.argv[0]
#data = sys.argv[1]
data = "/home/jande/Documents/fhl-wgs01/data/data_datura/161128_scatalu/EUTelescope_root_files/kappa075_2kink/run000024-GBLKinkEstimator_kappa075_2kink.root" 


# Open a file using python-like context a la James
if(False): 
    with root_open(data) as input_file:
      ########
      # Show all content of ROOT file

      #for path, dirs, objects in input_file.walk():
        #print "path:", path
        #print "dirs:", dirs
        #print "objects:", objects
      #print "list all:", input_file.ls()

      ########
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


########
# Using PyROOT and root_numpy (1d style)
if(True):
  print "output 1d style"
  histfile = TFile(data)
  
  # get hist data
  histdata = histfile.Get('Fitter06/GBL/gblsumkx2andsumky2_xyP') #print histdata
  #histdata = histfile.Get('Fitter06/GBL/gblsumkx_xyh') #print histdata

  print "stats of ROOT repr."
  print histdata.GetEntries() # In ROOT repr.: Entries
  print histdata.GetMean(1)   # In ROOT repr.: Mean x
  print histdata.GetMean(2)   # In ROOT repr.: Mean y
  print histdata.GetStdDev(1) # In ROOT repr.: RMS x
  print histdata.GetStdDev(2) # In ROOT repr.: RMS y
  print histdata.Integral()   # In ROOT repr.: Integral (here Sum over the bin_content = binc)

  # write as numpy array
  counts, edges = hist2array(histdata, include_overflow=False, return_edges=True) #print counts, edge
  # counts array
  print np.shape(counts), np.size(counts)#, counts
  # stats
  print np.sum(counts), np.mean(counts), np.std(counts)
  # 
  print np.shape(counts[0]), np.size(counts[0])#, counts[0]
  print np.shape(counts.T[0]), np.size(counts.T[0])#, counts.T[0]
  print np.size(edges)#, edges  # dimension + 1 
  print np.size(edges[0])#, edges[0]  # dimension + 1 
  print np.size(edges[1])#, edges[1]  # dimension + 1

  #print counts[0], edges[1]
  print np.size(counts[0]), np.size(edges[1])
  index_x = np.where(edges[0] == -9.00)[0][0]
  index_y = np.where(edges[1] == -4.00)[0][0]
  print index_x, edges[0][index_x]
  print index_y, edges[1][index_y]
  print counts[index_x][index_y]
  
  bin_x = 76 + 447
  bin_y = 51

  print "ROOT access to bin content" 
  print histdata.GetBin(bin_x, bin_y)  # 1dim. binnumber 
  print histdata.GetBinContent(bin_x, bin_y)  # binc, for Profile the mean-value
  print histdata.GetBinErrorLow(bin_x, bin_y) # bine, for Profile the error-value
  print counts[bin_x-1][bin_y-1]                # the sum of the N-bincontents
  print counts[bin_x-1][bin_y-1]/histdata.GetBinContent(bin_x, bin_y) # = N = sum / mean
  print edges[0][bin_x-1], edges[1][bin_y-1]

  print "test", histdata.GetBinContent(600, 100)  # binc, for Profile the mean-value
 
  print np.size(counts[0])
  print np.size(counts.T[0])

  contents = np.zeros(shape=np.shape(counts))
  for y_index, y_value in enumerate(counts[0]):
    for x_index, x_value in enumerate(counts.T[0]):
      contents[x_index][y_index] = histdata.GetBinContent(x_index+1, y_index+1)
  print contents
  print counts[bin_x-1][bin_y-1]/contents[bin_x-1][bin_y-1] # real counts
  counts_real = np.divide(counts, contents)
  print type(counts_real)
  print counts_real[bin_x-1][bin_y-1]  # cross check
  print counts_real[bin_x-1, bin_y-1]  # cross check


  # submatrix
  print counts_real[bin_x-1-1:bin_x-1+4, bin_y-1-1:bin_y-1+4]  # cross check
  print contents[bin_x-1-1:bin_x-1+4, bin_y-1-1:bin_y-1+4]  # cross check
  print edges[0][bin_x-1-1:bin_x-1+4]  # cross check
  print edges[1][bin_y-1-1:bin_y-1+4]  # cross check

  runlist = mrr.readRunlist("../" + mpm.name_runlist)

  contents, counts, bincenters_x, bincenters_y, edges_x, edges_y = mrr.getProfile2Data(runlist, int(17), "gblsumkx2andsumky2_xyP", "/home/jande/Documents/fhl-wgs01/data/data_datura/161128_scatalu/EUTelescope_root_files/kappa075_2kink/", "-GBLKinkEstimator_kappa075_2kink", mpm.name_rootfolder)

  print counts[bin_x-1-1:bin_x-1+4, bin_y-1-1:bin_y-1+4]  # cross check
  print contents[bin_x-1-1:bin_x-1+4, bin_y-1-1:bin_y-1+4]  # cross check
  print edges[0][bin_x-1-1:bin_x-1+4]  # cross check
  print edges[1][bin_y-1-1:bin_y-1+4]  # cross check

  print np.size(edges_x), np.size(edges_y)
  print np.size(bincenters_x), np.size(bincenters_y)











  exit()
  
  # getting bincenters
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
  print np.size(projection_x)#, projection_x
  print np.size(projection_y)#, projection_y
  # x-cut zeroes plus safety margin of ~1%
  margin_x = 6
  index_x_non_zero = np.where(projection_x != 0.)
  data_projection_x = projection_x[index_x_non_zero][margin_x+1:-margin_x-1]
  pos_projection_x = bincenters_x[index_x_non_zero][margin_x+1:-margin_x-1]
  print np.size(data_projection_x)#, data_projection_x
  print np.size(pos_projection_x)#, pos_projection_x
  # y-cut zeroes
  margin_y = 3
  index_y_non_zero = np.where(projection_y != 0.)
  data_projection_y = projection_y[index_y_non_zero][margin_y+1:-margin_y-1]
  pos_projection_y = bincenters_y[index_y_non_zero][margin_y+1:-margin_y-1]
  print np.size(data_projection_y)#, data_projection_y
  print np.size(pos_projection_y)#, pos_projection_y
  # normalize
  print np.size(data_projection_x), np.size(counts[1])
  data_projection_x = data_projection_x/np.size(data_projection_x)
  data_projection_y = data_projection_y/np.size(data_projection_y)
  # stack data
  data_x = np.vstack((pos_projection_x, data_projection_x))
  data_y = np.vstack((pos_projection_y, data_projection_y))
  #print np.size(data_x), np.size(data_y)

  print mff.fit_linear(data_x, 0.0, 5000)
  print mff.fit_linear(data_y, 0.0, 5000)
