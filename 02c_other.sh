#!/bin/bash

python plot_data.py $KAPPA100KINK2FRAC098 rmsfrac_norm gauss_si_norm
python plot_data.py $KAPPA075KINK2FRAC098 rmsfrac_norm gauss_si_norm
#python plot_data.py $KAPPA100KINK2FRAC090 rmsfrac_norm gauss_si_norm

python plot_data_energy.py $KAPPA100KINK2FRAC098 rmsfrac_norm
python plot_data_energy.py $KAPPA100KINK2FRAC098 rmsfrac
python plot_data_energy.py $KAPPA075KINK2FRAC098 rmsfrac
python plot_data_energy.py $KAPPA100KINK2FRAC098 gauss_chi2
python plot_data_energy.py $KAPPA075KINK2FRAC098 gauss_chi2
python plot_data_energy.py $KAPPA100KINK2FRAC098 gauss_chi2red
#python plot_data_energy.py $KAPPA100KINK2FRAC090 gauss_chi2red

