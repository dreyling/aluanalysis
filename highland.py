#! /usr/bin/python
import numpy as np

##################################################
# Physical constants
x0alu = 88.97	# mm
x0sil = 93.65	# mm
x0kap = 285.6	# mm
x0air = 3.042e5 # mm

# Telescope material budget, 20mm configuration
thickness_mimosa_total = 6. * 55e-3       # mm
thickness_kapton_total = 10. * 25e-3      # mm
thickness_air_total    = 4. * 20. + 15.   # mm

# Material for measuring kink angle
thickness_mimosa_kink = 2* 0.5 * 55e-3  # mm
thickness_kapton_kink = 2* 25e-3        # mm
thickness_air_kink    = 15.             # mm


# Highland standard
def highland(momentum, thickness, x0):
    epsilon = thickness/x0
    if epsilon < 1e-3:
      print "Warning! epsilon < 0.001 for thickness", thickness
    if epsilon > 100.:
      print "Warning! epsilon > 100 for thickness", thickness
    # 13.6 MeV / 1 GeV = 10-3 --> mrad
    return 13.6/momentum*np.sqrt(epsilon)*(1.+0.038*np.log(epsilon))

# Highland GBL multi scatterer plus sut_meas which includes material to the next scatteres
# not using for this analysis, sonce the extend kink epsilon would taking this contribution into account twice
def highland_multi_scatterer_extended(momentum, thickness_sut, x0_sut):
    epsilon_kink = (thickness_sut/x0_sut +
            thickness_mimosa_kink/x0sil +
            thickness_kapton_kink/x0kap +
            thickness_air_kink/x0air)
    print 'SUT_eff = ', epsilon_kink
    print 'SUT / SUT_eff = ', thickness_sut/x0_sut / epsilon_kink
    epsilon_total = (thickness_sut/x0_sut +
            thickness_mimosa_total/x0sil +
            thickness_kapton_total/x0kap +
            thickness_air_total/x0air)
    #print epsilon_total, thickness_dut
    if epsilon_kink < 1e-3:
        print "Warning! epsilon < 0.001 for thickness", thickness_sut
    if epsilon_kink > 100.:
        print "Warning! epsilon > 100 for thickness", thickness_sut
    return 13.6/momentum*np.sqrt(epsilon_kink)*(1.+0.038*np.log(epsilon_total))

def highland_multi_scatterer_extended_momentum(theta, thickness_sut, x0_sut):
    epsilon_kink = (thickness_sut/x0_sut +
            thickness_mimosa_kink/x0sil +
            thickness_kapton_kink/x0kap +
            thickness_air_kink/x0air)
    print 'SUT_eff = ', epsilon_kink
    print 'SUT / SUT_eff = ', thickness_sut/x0_sut / epsilon_kink
    epsilon_total = (thickness_sut/x0_sut +
            thickness_mimosa_total/x0sil +
            thickness_kapton_total/x0kap +
            thickness_air_total/x0air)
    #print epsilon_total, thickness_dut
    if epsilon_kink < 1e-3:
        print "Warning! epsilon < 0.001 for thickness", thickness_sut
    if epsilon_kink > 100.:
        print "Warning! epsilon > 100 for thickness", thickness_sut
    return 13.6/theta*np.sqrt(epsilon_kink)*(1.+0.038*np.log(epsilon_total))

# Highland GBL multi scatterer only SUT material
def highland_multi_scatterer(momentum, thickness_sut, x0_sut):
    epsilon_kink = thickness_sut/x0_sut
    epsilon_total = (epsilon_kink +
            thickness_mimosa_total/x0sil +
            thickness_kapton_total/x0kap +
            thickness_air_total/x0air)
    return 13.6/momentum * np.sqrt(epsilon_kink)*(1.+0.038*np.log(epsilon_total))

def highland_multi_scatterer_momentum(theta, thickness_sut, x0_sut):
    epsilon_kink = thickness_sut/x0_sut
    epsilon_total = (epsilon_kink +
            thickness_mimosa_total/x0sil +
            thickness_kapton_total/x0kap +
            thickness_air_total/x0air)
    return 13.6/theta * np.sqrt(epsilon_kink)*(1.+0.038*np.log(epsilon_total))

# Highland for electrons
def highland_electrons(momentum, thickness_sut, x0_sut):
    epsilon_kink = thickness_sut/x0_sut
    return 13.6/momentum * np.power(epsilon_kink, 0.555)


# Highland GBL multi scatterer only SUT material
def highland_opacity_multi_scatterer_raw(opacity, thickness_sut, x0_sut):
    epsilon_total = (thickness_sut/x0_sut +
            thickness_mimosa_total/x0sil +
            thickness_kapton_total/x0kap +
            thickness_air_total/x0air)
    print len(epsilon_total)
    print epsilon_total
    return 13.6 * np.multiply(opacity, 1.+0.038*np.log(epsilon_total))

# Highland for electrons
def highland_opacity_electrons(opacity):
    return 13.6 * opacity
