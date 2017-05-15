#! /usr/bin/python
import numpy as np

##################################################
# Names, Folders, Histograms
name_runlist = "runlistX0meas.csv"
name_path_1scatterer = "/home/jande/Documents/ownCloud/X0_hendrik/measurement_1scatterer/"
name_path_2scatterer = "/home/jande/Documents/ownCloud/X0_hendrik/measurement_2scatterer/"
name_suffix_1scatterer = "-GBLKinkEstimator_kappa100" 
name_suffix_2scatterer = "-GBLKinkEstimator_kappa100_test" 
name_rootfolder = "Fitter06/GBL/"

##################################################
# Physical constants
x0alu = 88.97 	# mm
x0sil = 93.65 	# mm
x0kap = 285.6 	# mm
x0air = 3.042e5 # mm

# Telescope material budget, 20mm configuration
thickness_mimosa = 6 * 55e-3 		# mm
thickness_kapton = 10 * 25e-3 	# mm
thickness_air    = 4 * 20 + 15 	# mm

# Highland standard
def highland(momentum, thickness, x0):
    epsilon = thickness/x0
    if epsilon < 1e-3: 
      print "Warning! epsilon < 0.001 for thickness", thickness
    if epsilon > 100.:
      print "Warning! epsilon > 100 for thickness", thickness
    return 13.6/momentum*np.sqrt(epsilon)*(1.+0.038*np.log(epsilon))

# Highland GBL multi scatterer
def highland_multi_scatterer(momentum, thickness_dut, x0_dut):
    epsilon_dut = thickness_dut/x0_dut
    epsilon_total = epsilon_dut + thickness_mimosa/x0sil + thickness_kapton/x0kap + thickness_air/x0air
    #print epsilon_total, thickness_dut
    #if epsilon_dut < 1e-3: 
    #  print "Warning! epsilon < 0.001 for thickness", thickness_dut
    #if epsilon_dut > 100.:
    #  print "Warning! epsilon > 100 for thickness", thickness_dut
    return 13.6/momentum*np.sqrt(epsilon_dut)*(1.+0.038*np.log(epsilon_total))

# Energy loss

 

