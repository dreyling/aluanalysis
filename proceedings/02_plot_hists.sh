#!/bin/bash

export RMSGAUSS0980="data/kappa075_2kink_gblsumkx_0.98.npy"

python plot_hist1d.py $ROOTDATASET gblsumkx 3 0.1 $RMSGAUSS0980
python plot_hist1d.py $ROOTDATASET gblsumkx 3 0.0 $RMSGAUSS0980
