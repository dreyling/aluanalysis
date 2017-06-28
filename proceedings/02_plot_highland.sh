#!/bin/bash

export RMSGAUSS0980="data/kappa075_2kink_gblsumkx_0.98.npy"

python plot_data_highland.py $RMSGAUSS0980 gauss_si_norm all
