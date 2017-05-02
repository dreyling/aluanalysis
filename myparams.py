#! /usr/bin/python
import numpy as np

##################################################
# Names, Folders, Histograms
nameRunlist = "runlistX0meas.csv"
namePath = "/home/jande/Documents/ownCloud/X0_hendrik/measurement/"
nameSuffix = "-GBLKinkEstimator_kappa100" 
nameRootFolder = "Fitter06/GBL/"
nameRootHistos = np.array([
"gblrx0", "gblry0", "gblrx1", "gblry1", "gblrx2", "gblry2", "gblrx3", "gblry3", "gblrx4", "gblry4", "gblrx5", "gblry5",
"gblpx0", "gblpy0", "gblpx1", "gblpy1", "gblpx2", "gblpy2", "gblpx3", "gblpy3", "gblpx4", "gblpy4", "gblpx5", "gblpy5",
"gbltx1", "gbltx2", "gbltx3", "gbltx4",
"gblprb"
])

##################################################
# Physical constants

x0alu = 88.97 # mm
