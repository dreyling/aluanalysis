#!/bin/bash

python plot_hist1d_b.py $ROOTDATASET gblsumkxandsumky 3 0.1 $RMSGAUSS0980BOTH
python plot_hist1d_b.py $ROOTDATASET gblsumkxandsumky 3 0.0 $RMSGAUSS0980BOTH
return

python plot_hist1d.py $ROOTDATASET gblsumkxandsumky 3 0.1 $RMSGAUSS0980BOTH
python plot_hist1d.py $ROOTDATASET gblsumkxandsumky 3 0.0 $RMSGAUSS0980BOTH

python plot_hist1d.py $ROOTDATASET gblsumkx 3 0.1 $RMSGAUSS0980
python plot_hist1d.py $ROOTDATASET gblsumkx 3 0.0 $RMSGAUSS0980

