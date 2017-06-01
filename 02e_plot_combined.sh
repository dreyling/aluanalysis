#!/bin/bash
python plot_data_highland.py $KAPPA100KINK2FRAC098COMB comb_si_norm all

python plot_data_energy.py   $KAPPA100KINK2FRAC098COMB comb_chi2red 	log
python plot_data_energy.py   $KAPPA100KINK2FRAC098COMB comb_nu_s	lin
python plot_data_energy.py   $KAPPA100KINK2FRAC098COMB comb_si_s	log
python plot_data_energy.py   $KAPPA100KINK2FRAC098COMB comb_frac	lin


