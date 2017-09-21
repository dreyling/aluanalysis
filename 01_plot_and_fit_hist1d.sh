#!/bin/bash

python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=1.0 --fitfunction=combined_one_sigma --fraction=0.98
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=1.0 --fitfunction=combined_two_sigmas --fraction=0.98

python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=1.0 --fitfunction=combined_one_sigma 
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=1.0 --fitfunction=combined_two_sigmas
