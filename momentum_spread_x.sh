#python get_and_analyze_binned_hist1d-data.py --configuration=measurement_binned.yaml --fraction=0.9

python plot_width_binned.py --configuration=measurement_binned.yaml --energy=3 --thickness=1.0 --results=data/stats_and_fits_measurement_binned_data-fraction_0.9.npy --width=gauss_si_norm

return

python plot_width_binned.py --configuration=measurement_binned.yaml --energy=3 --thickness=1.0 --results=data/stats_and_fits_measurement_binned_data-fraction_0.9.npy --width=combined_one_si_norm
python plot_width_binned.py --configuration=measurement_binned.yaml --energy=3 --thickness=1.0 --results=data/stats_and_fits_measurement_binned_data-fraction_0.9.npy --width=ROOT_rms_norm
python plot_width_binned.py --configuration=measurement_binned.yaml --energy=3 --thickness=1.0 --results=data/stats_and_fits_measurement_binned_data-fraction_0.9.npy --width=rms_frac_norm
python plot_width_binned.py --configuration=measurement_binned.yaml --energy=3 --thickness=1.0 --results=data/stats_and_fits_measurement_binned_data-fraction_0.9.npy --width=aad_frac_norm
python plot_width_binned.py --configuration=measurement_binned.yaml --energy=3 --thickness=1.0 --results=data/stats_and_fits_measurement_binned_data-fraction_0.9.npy --width=ROOT_rms
python plot_width_binned.py --configuration=measurement_binned.yaml --energy=3 --thickness=1.0 --results=data/stats_and_fits_measurement_binned_data-fraction_0.9.npy --width=rms_frac
python plot_width_binned.py --configuration=measurement_binned.yaml --energy=3 --thickness=1.0 --results=data/stats_and_fits_measurement_binned_data-fraction_0.9.npy --width=aad_frac
