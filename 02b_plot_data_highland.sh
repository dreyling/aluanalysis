#!/bin/bash

#python plot_data_highland.py $KAPPA100KINK1FRAC098 rmsfrac_norm all
#python plot_data_highland.py $KAPPA100KINK1FRAC098 gauss_si_norm all

python plot_data_highland.py $COMBKAPPA100KINK2FRAC098 rmsfrac_norm all
python plot_data_highland.py $COMBKAPPA100KINK2FRAC098 comb_si_norm all
python plot_data_highland.py $COMBKAPPA100KINK2FRAC098 comb_si_s_norm all

exit()


python plot_data_highland.py $KAPPA100KINK2FRAC098 rmsfrac all
python plot_data_highland.py $KAPPA100KINK2FRAC098 rmsfrac_norm all
python plot_data_highland.py $KAPPA100KINK2FRAC098 gauss_si_norm all

python plot_data_highland.py $KAPPA100KINK2FRAC0955 rmsfrac_norm all
python plot_data_highland.py $KAPPA100KINK2FRAC0955 gauss_si_norm all

python plot_data_highland.py $KAPPA100KINK2FRAC090 rmsfrac_norm all
python plot_data_highland.py $KAPPA100KINK2FRAC090 gauss_si_norm all

#python plot_data_highland.py $KAPPA075KINK1FRAC098 rmsfrac_norm all
#python plot_data_highland.py $KAPPA075KINK1FRAC098 gauss_si_norm all

#python plot_data_highland.py $KAPPA075KINK2FRAC098 rmsfrac all
#python plot_data_highland.py $KAPPA075KINK2FRAC098 rmsfrac_norm all
#python plot_data_highland.py $KAPPA075KINK2FRAC098 gauss_si_norm all


############
# should be the same
#python plot_data_highland.py data/2_scatterer_gblsumkx_0.98.npy rmsfrac_norm all
#python plot_data_highland.py data/2_scatterer_gblsumkx_0.98.npy rmsfrac_norm 5samples
#python plot_data_highland.py data/2_scatterer_gblsumkx_0.98.npy gauss_si_norm all
#python plot_data_highland.py data/2_scatterer_gblsumkx_0.98.npy gauss_si_norm 5samples

# ols syntax
#python plot_data_highland.py data/2_scatterer_gblsumkx_0.90.npy
#python plot_data_highland_5samples.py data/2_scatterer_gblsumkx_0.90.npy 

