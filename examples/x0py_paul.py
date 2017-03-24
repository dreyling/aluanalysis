#! /usr/bin/python
import numpy as np
import os

from ROOT import TH1, TFile, TF1, TCanvas

import math
import sys
import getopt
import csv
import time

x0alu = 88.97

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

def highfunc(x, a, b):
    return 1e3*0.0136/x*math.sqrt(a/x0alu)*(1.+0.038*math.log(a/x0alu))+b
    #return 1e3*0.0141/x*math.sqrt(a/x0alu)*(1.+1./9.*math.log(a/x0alu,10))+b

def linfunc(x, a, b):
    return a*x+b

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


def readRunlist(filename):
    runlistIn = np.zeros((2000,3))

    print "opening " + str(filename)

    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile, delimiter='\t')
        i=0
        for word in reader:
            runlistIn[i,0]=word['runnr']
            runlistIn[i,1]=word['energy']
            runlistIn[i,2]=word['thickness']
            i = i+1
    csvfile.close()

    nRunsIn = 0
    for i in range(0,np.size(runlistIn,0)):
        if runlistIn[i,0]!=0:
            nRunsIn = nRunsIn+1
        else:
            break
        
    runlist = runlistIn[:nRunsIn]

    return runlist

def getDataFromRootFiles(runlist, path, histoid):
    
    nRuns = np.size(runlist,0)

    data = np.zeros((nRuns,7))   # runnr, energy, nom. thickness, rms^2, rms^2-rms_0^2, cal. rms^2_corr, meas/calc rms^2_corr
    rmssq0VsEnergy = np.zeros(nRuns)

    if(runlist[0,0] > 80000):
        whichSet = "simulation"
    else:
        whichSet = "measurement"
    print "Reading " + whichSet + " data ..."

    for i in range(0, nRuns):
        if runlist[i,0]!=0:
            rootfile = TFile(path+"run0"+'{:05d}'.format(int(runlist[i,0]))+"-analysis.root")
            
            rms = getFitRMS(runlist[i,0], rootfile, histoid)
            
            rootfile.Close()
            
            rms2 = rms*rms
            data[i,0]=runlist[i,0]
            data[i,1]=runlist[i,1]
            data[i,2]=runlist[i,2]
            data[i,3]=rms2
            
            energy = runlist[i,1]
            thickness = runlist[i,2]

            if(thickness == 0.0): # zero thickness, reference run
                rmssq0VsEnergy[int(energy)]=rms2
                print "Reference for " + whichSet + ", " + str(int(energy)) + " GeV: " + str(rms2)


    for i in range(0, nRuns):
        data[i,4] = data[i,3]-rmssq0VsEnergy[int(data[i,1])]
        data[i,5] = calcRMS2(data[i,2],data[i,1])
        data[i,6] = data[i,4]/data[i,5]

    return data
