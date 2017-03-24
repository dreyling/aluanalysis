#! /usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import math
from ROOT import TH1, TFile, TF1, TCanvas

from rootpy.plotting import set_style, root2matplotlib
from root_numpy import root2array, tree2array, hist2array

import x0py 

# access Hendriks output file
data = "/opt/paper2/GBLKinkEvaluator/bin/output_measurement.root"

rootfile = TFile(data)
print rootfile
rootfile.ls()

canvas = rootfile.Get("m26fitter_5")
print canvas
canvas.ls()

tlist = canvas.GetPrimitive("m26fitter_5_1")
print tlist
tlist.ls()

th1d = tlist.GetPrimitive("gblrx0")
print th1d
th1d.ls()

# root_numpy
test = hist2array(th1d)
print test

