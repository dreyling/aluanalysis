#!/bin/bash

export KAPPA075KINK2="/home/jande/Documents/fhl-wgs01/data/data_datura/161128_scatalu/EUTelescope_root_files/kappa075_2kink/"


# for the mean
#python plot_profile2d_mean.py $KAPPA075KINK2 gblsumkxandsumky_xyP 1 0.1
# for the sigma
python plot_profile2d_error.py $KAPPA075KINK2 gblsumkxandsumky_xyP 1 0.1

return

# for the mean
python plot_profile2d_mean.py $KAPPA075KINK2 gblsumkxandsumky_xyP 3 0.1
# for the sigma
python plot_profile2d_error.py $KAPPA075KINK2 gblsumkxandsumky_xyP 3 0.1

# for the mean
python plot_profile2d_mean.py $KAPPA075KINK2 gblsumkxandsumky_xyP 1 0.0
# for the sigma
python plot_profile2d_error.py $KAPPA075KINK2 gblsumkxandsumky_xyP 1 0.0

############################
# for the sigma
python plot_profile2d.py $KAPPA075KINK2 gblsumkx2andsumky2_xybP 1 0.1
python plot_profile2d.py $KAPPA075KINK2 gblsumkx2andsumky2_xyP 1 0.1
python plot_profile2d.py $KAPPA075KINK2 gblsumkx2andsumky2_xyP 3 0.1
python plot_profile2d.py $KAPPA075KINK2 gblsumkx2andsumky2_xyP 1 0.0
python plot_profile2d.py $KAPPA075KINK2 gblsumkxandsumky_xyP 1 0.1

# test
#python plot_profile2d.py $KAPPA075KINK2 gblsumkx2andsumky2_xyP 1 10.0

#export KAPPA075KINK2FRAC098="data/kappa075_2kink_gblsumkx_0.98.npy"
#python plot_hist1d.py $KAPPA075KINK2 gblsumkx2andsumky2 1 0.1  $KAPPA075KINK2FRAC098

