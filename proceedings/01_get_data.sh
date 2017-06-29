#!/bin/bash

# get RMS and Gauss
python get_hist_data.py $ROOTDATASET gblsumkx 0.98
python get_hist_data.py $ROOTDATASET gblsumkxandsumky 0.98

return

# get 2d profile data
python get_2d_data.py $ROOTDATASET gblsumkxandsumky_xyP 
python get_2d_data.py $ROOTDATASET gblsumkx2andsumky2_xyP
