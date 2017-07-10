#!/bin/bash

# for the mean
python plot_profile2d_mean.py $ROOTDATASET gblsumkxandsumky_xyP 1 0.1
# for the sigma
python plot_profile2d_error.py $ROOTDATASET gblsumkxandsumky_xyP 1 0.1
