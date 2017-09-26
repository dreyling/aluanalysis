#!/bin/bash

python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=3.0 --thickness=0.025 --fitfunction=combined_two_sigmas
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=0.025 --fitfunction=combined_two_sigmas
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=0.05 --fitfunction=combined_two_sigmas
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=5.0 --thickness=0.05 --fitfunction=combined_two_sigmas
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=0.1 --fitfunction=combined_two_sigmas
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=0.2 --fitfunction=combined_two_sigmas
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=5.0 --thickness=1.0 --fitfunction=combined_two_sigmas
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=4.0 --thickness=1.0 --fitfunction=combined_two_sigmas
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=1.0 --fitfunction=combined_two_sigmas
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=10.0 --fitfunction=combined_two_sigmas
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=0.013 --fitfunction=combined_two_sigmas


python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=3.0 --thickness=0.025 --fitfunction=combined_one_sigma
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=0.025 --fitfunction=combined_one_sigma
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=0.05 --fitfunction=combined_one_sigma
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=5.0 --thickness=0.05 --fitfunction=combined_one_sigma
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=0.1 --fitfunction=combined_one_sigma
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=0.2 --fitfunction=combined_one_sigma
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=5.0 --thickness=1.0 --fitfunction=combined_one_sigma
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=4.0 --thickness=1.0 --fitfunction=combined_one_sigma
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=1.0 --fitfunction=combined_one_sigma
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=10.0 --fitfunction=combined_one_sigma
python plot_and_fit_hist1d.py --configuration=measurement.yaml --energy=1.0 --thickness=0.013 --fitfunction=combined_one_sigma
