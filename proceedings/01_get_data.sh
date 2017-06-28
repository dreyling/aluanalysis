#!/bin/bash

# root files
export ROOTDATASET="/home/jande/Documents/fhl-wgs01/data/data_datura/161128_scatalu/EUTelescope_root_files/kappa075_2kink/"

# get RMS and Gauss
python get_hist_data.py $ROOTDATASET gblsumkx 0.98

return

# get 2d profile data
python get_2d_data.py $KAPPA075KINK2 gblsumkxandsumky_xyP 
python get_2d_data.py $KAPPA075KINK2 gblsumkx2andsumky2_xyP
