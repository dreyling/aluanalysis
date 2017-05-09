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
x0alu = 88.97 	# mm
x0sil = 93.65 	# mm
x0kap = 285.6 	# mm
x0air = 3.042e5 # mm

# Telescope material budget, 20mm configuration
thickness_mimosa = 6 * 50e-3 		# mm
thickness_kapton = 12 * 25e-3 	# mm
thickness_air    = 4 * 20 + 15 	# mm

# Function
def highland(momentum, thickness, x0):
    epsilon = thickness/x0
    if epsilon < 1e-3: 
      print "Warning! epsilon < 0.001 for thickness", thickness
    if epsilon > 100.:
      print "Warning! epsilon > 100 for thickness", thickness
    return 13.6/momentum*np.sqrt(epsilon)*(1.+0.038*np.log(epsilon))

# Function
def highland_multi_scatterer(momentum, thickness_dut, x0_dut):
    epsilon_dut = thickness_dut/x0_dut
    epsilon_total = epsilon_dut + thickness_mimosa/x0sil + thickness_kapton/x0kap + thickness_air/x0air
    if epsilon_dut < 1e-3: 
      print "Warning! epsilon < 0.001 for thickness", thickness_dut
    if epsilon_dut > 100.:
      print "Warning! epsilon > 100 for thickness", thickness_dut
    return 13.6/momentum*np.sqrt(epsilon_dut)*(1.+0.038*np.log(epsilon_total))
