""" Module myrootlib
A module for accesing and processing ROOT files"""

#! /usr/bin/python
import math
import sys, os
import getopt
import time
import numpy as np
from scipy.optimize import curve_fit
#import scipy as sp #import optimize.curve_fit
# for joining&combining structured arrays
import numpy.lib.recfunctions as rfn

from ROOT import TFile #, TF1, TCanvas, TH1

from rootpy.io import root_open # Look at http://www.rootpy.org/ for full documentation

from root_numpy import root2array, tree2array, hist2array

#################################################################

def readRunlist(filename):
  return np.genfromtxt(filename, delimiter='\t', names=True)

def extendList(runlist, newcol_name):
  newcol = np.zeros(np.size(runlist), dtype = {'names': [newcol_name], 'formats': ['f8']} )
  newlist = rfn.merge_arrays((runlist, newcol), flatten = True, usemask = False)
  return newlist
  



# get Data
# runlist: csv file (same folder)
# runindex: index to loop, max. is  length of runlist['runnr'] e.g.
# histname: string, name of Root Histogram
# path: path of rrot files
# suffix: filename: run000X + suffix + .root
# rootfolder: folder name in root file
def getHist1Data(runlist, runindex, histname, path, suffix, rootfolder):
  rootFile = path + "run0"+'{:05d}'.format(int(runlist['runnr'][runindex])) + suffix + ".root"
  print "opening...", rootFile
  # open root file
  histfile = TFile(rootFile)
  # get hist data
  histdata = histfile.Get(rootfolder + histname) #print histdata
  # write as numpy array
  counts, edges = hist2array(histdata, include_overflow=False, return_edges=True)
  #print counts, edges
  #print np.size(counts), np.size(edges)
  # shorten length by guess in this direction
  #counts = counts[1:]
  # shift hist data by half of the binwidth, checked with np.where(data[0] > 0.)[0][0]
  binwidth = abs(edges[0][1]-edges[0][0])
  edges = np.array(edges) + binwidth/2. # root probably adds a whole binwidth, irrelevant for rms
  # return x and y data
  #print edges[0][:-1]
  data0 = edges[0][:-1]
  data1 = counts
  data = np.vstack((data0, data1))
  return data
  #return edges[0][:-1], counts

def cutData(data, cutbins):
  data0 = data[0][cutbins:-cutbins]
  data1 = data[1][cutbins:-cutbins]
  data = np.vstack((data0, data1))
  return data

def getHistFraction(data, fraction):
  if fraction <= 0:
    return 0
  if fraction >= 1:
    fraction = 1.
    indexStart = 0
    indexEnd = np.size(data[0])-1
  # set range to fit
  entriesTotal = calcEntries(data[1])
  #print type(entriesTotal)
  cumsumNormal = np.cumsum(data[1])/entriesTotal # normalized cumulative sum array
  #print cumsumNormal
  #print type(cumsumNormal)
  indexStart = np.where(cumsumNormal > (1.-fraction)/2.)[0][0]
  indexEnd = np.where(cumsumNormal > fraction+(1.-fraction)/2.)[0][0]# print indexStart, indexEnd
  # set data to fit
  data0 = data[0][indexStart:indexEnd].copy()
  data1 = data[1][indexStart:indexEnd].copy()
  data = np.vstack((data0, data1))
  return data

def getHistSpecs(runlist, runindex, histname, path, suffix, rootfolder):
  rootFile = path + "run0"+'{:05d}'.format(int(runlist['runnr'][runindex])) + suffix + ".root"
  print "opening...", rootFile
  # open root file
  histfile = TFile(rootFile)
  # get hist data
  histdata = histfile.Get(rootfolder + histname) #print histdata
  #print histdata.GetBin(1)
  #print histdata.GetBinCenter(1)
  #print histdata.GetStats(1)
  #print histdata.GetXaxis().SetRange(50, 100)
  return {'mean':histdata.GetMean(1), 'stddev':histdata.GetStdDev(1), 'integral':histdata.Integral(), 'entries':histdata.GetEntries()}


#########33

def getHistSpecsMod(runlist, runindex, histname, path, suffix, rootfolder, mod):
  rootFile = path + "run0"+'{:05d}'.format(int(runlist['runnr'][runindex])) + suffix + ".root"
  # open root file
  histfile = TFile(rootFile)
  # get hist data
  histdata = histfile.Get(rootfolder + histname) #print histdata
  return {'mean':histdata.GetMean(), 'stddev':histdata.GetStdDev(), 'integral':histdata.Integral(), 'entries':histdata.GetEntries()}

def loopRunAndSum(runlist, histname, path, suffix, rootfolder):
  data = np.zeros((2, np.size(runlist['runnr'])))
  counts = 1 
  for index, value in enumerate(runlist['runnr']):
    data[0][index] = value
    data[1][index] = np.sum(getHist1Data(runlist, index, histname, path, suffix, rootfolder)[counts])
  return data

fitfunc_gauss = lambda xdata, *para: para[2] * np.exp(-0.5*(xdata-para[0])**2/para[1]**2)



def fitGaussHisto1d(data, mu0, sigma0, height0):
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
  fitResult = {'mu':mu, 'si':si, 'height':height, 'dmu':dmu, 'dsi':dsi, 'chi2':chi2, 'chi2red':chi2red}
  return fitResult

def printData(data):
  print "xdata:", data[0]
  print "ydata:", data[1]
  print "entries:", calcEntries(data[1])
  # simple mean, rms
  print "mean:", calcMean(data[1])
  print "rms:", calcRMS(data[1])
  # Todo: not the same as in ROOT...
  print "hist mean:", calcHistMean(data)
  print "hist RMS:", calcHistRMS(data)

###

def calcEntries(data):
  return np.sum(data)

def calcMean(data):
  return np.mean(data)

def calcRMS(data):
  return np.sqrt(np.mean(np.square(data)))

def calcHistMedian(data):
  index = np.where(np.cumsum(data[1]) > calcEntries(data[1]) / 2.)
  return data[0][index]

def calcHistMean(data):
  weights = np.multiply(data[0], data[1])
  return np.sum(weights)/np.sum(data[1])

def calcHistRMS(data):
  weights = np.multiply(np.square(data[0]-calcHistMean(data)), data[1])
  return np.sqrt(np.sum(weights)/np.sum(data[1]))
  #qsum = np.sqrt (calcRMS(data[0])**2 + calcMean(data[0]))
  #return qsum
  #weight2 = np.multiply(data[0], np.square(data[1]))
  #return np.sqrt(np.sum(weight2))/np.sum(data[1])
  #return np.sqrt(np.sum(np.square(weight)/np.sum(data[1])))
  #return np.sqrt(np.mean(np.square(np.multiply(data[0], data[1]))))

#########

def highfunc(momentum, thickness, x0material, offset):
    energyfactor = 13.6 # in MeV
    return energyfactor/momentum*np.sqrt(thickness/x0material)*(1.+0.038*np.log(thickness/x0material))+offset

def linfunc(xdata, slope, offset):
    return slope * xdata + offset
   

########################################################## 

def getFitRMS(runnr, rootfile, histoid):

    draw = False
    
    if(runnr > 80000):
        rebinning = 2
    else:
        rebinning = 1
            
    
    hist = rootfile.Get("MyEUTelTriplets/" + histoid)
    hist.Rebin(rebinning,"newHist")
    hist2 = rootfile.Get("newHist")
    
    func = TF1("func", "gaus(0)",-10.,10.)
    func.SetParameter(0,10000)
    func.SetParameter(1,0)
    func.SetParameter(2,0.1)

    fitrange = hist2.GetRMS()*5.

    if(fitrange > 10.):
        print "Yep. That really happened! RMS=" + str(hist2.GetRMS())
        hist2 = rootfile.Get("MyEUTelTriplets/kinkxduttotalx0l")
    
    if (draw):
        c = TCanvas()
        hist2.Draw("")
        hist2.SetTitle("Run " + str(runnr))
        hist2.Fit(func,"Wq","",-fitrange,fitrange)
        #raw_input("Press Enter to continue...")
        time.sleep(0.3)
    else:
        hist2.Fit(func,"Wnq","",-fitrange,fitrange)

    return func.GetParameter(2)

def calcRMS2(th, energy):
    if(th > 0.):
        #rms2 = math.pow(1.e3*0.0136/energy*math.sqrt(th/x0alu)*(1.+0.038*math.log(th/x0alu)),2)
        rms2 = math.pow(highfunc(energy,th,0),2)
        #rms2 = math.pow(1.e3*0.0136/energy*math.sqrt(th/x0alu),2)
        #rms2 = math.pow(1.e3*0.0136/energy*math.pow(th/x0alu,0.555),2)
    else:
        rms2 = 0.
    
    return rms2

def oneThicknessDataset(thickness, data):
    dataset = np.zeros((5,2))

    nRuns = np.size(data,0)
    for i in range(0, nRuns):
        if(data[i,2] == thickness):
            dataset[int(data[i,1])-1,0] = math.sqrt(data[i,4])
            dataset[int(data[i,1])-1,1] = data[i,1]
    
    for i in range(np.size(dataset,0)-1,0,-1):
        if(dataset[i,1] == 0.):
            print "yay, delete nr. " + str(i)
            dataset = np.delete(dataset,i,0)

    return dataset
