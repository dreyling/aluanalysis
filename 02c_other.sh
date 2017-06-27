#!/bin/bash

python plot_data_energy.py data/kappa075_2kink_gblsumkx2andsumky2_xyP.npy projection_x_fit_slope lin
python plot_data_energy.py data/kappa075_2kink_gblsumkx2andsumky2_xyP.npy projection_y_fit_slope lin

python plot_data_energy.py data/kappa075_2kink_gblsumkxandsumky_xyP.npy projection_x_fit_slope lin
python plot_data_energy.py data/kappa075_2kink_gblsumkxandsumky_xyP.npy projection_y_fit_slope lin

return


#python plot_data_energy.py $COMBKAPPA100KINK2FRAC098 rmsfrac_norm
#python plot_data_energy.py $COMBKAPPA100KINK2FRAC098 comb_si_norm
#python plot_data_energy.py $COMBKAPPA100KINK2FRAC098 comb_si_s_norm
python plot_data_energy.py $COMBKAPPA100KINK2FRAC098 comb_frac
python plot_data_energy.py $COMBKAPPA100KINK2FRAC098 comb_nu_s

#python plot_data.py $COMBKAPPA100KINK2FRAC098 comb_si_norm comb_si_s_norm
#python plot_data.py $COMBKAPPA100KINK2FRAC098 comb_si comb_si_s
python plot_data.py $COMBKAPPA100KINK2FRAC098 comb_frac comb_nu_s
#python plot_data.py $COMBKAPPA100KINK2FRAC098 comb_frac comb_si_s
python plot_data.py $COMBKAPPA100KINK2FRAC098 comb_frac comb_si
#python plot_data.py $COMBKAPPA100KINK2FRAC098 comb_si_s comb_nu_s
#python plot_data.py $COMBKAPPA100KINK2FRAC098 comb_si comb_nu_s


# vor dem Urlaub

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

