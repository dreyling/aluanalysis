# analysis of realigned 10mm data
python plot_profile2d.py --configuration=measurement_10mm_realign.yaml --energy=1 --thickness=10.0 --data_type=mean
python plot_profile2d.py --configuration=measurement_10mm_realign.yaml --energy=2 --thickness=10.0 --data_type=mean
python plot_profile2d.py --configuration=measurement_10mm_realign.yaml --energy=3 --thickness=10.0 --data_type=mean
python plot_profile2d.py --configuration=measurement_10mm_realign.yaml --energy=4 --thickness=10.0 --data_type=mean
python plot_profile2d.py --configuration=measurement_10mm_realign.yaml --energy=5 --thickness=10.0 --data_type=mean

python plot_profile2d.py --configuration=measurement_10mm_realign.yaml --energy=1 --thickness=10.0 --data_type=mean --rebin=10
python plot_profile2d.py --configuration=measurement_10mm_realign.yaml --energy=2 --thickness=10.0 --data_type=mean --rebin=10
python plot_profile2d.py --configuration=measurement_10mm_realign.yaml --energy=3 --thickness=10.0 --data_type=mean --rebin=10
python plot_profile2d.py --configuration=measurement_10mm_realign.yaml --energy=4 --thickness=10.0 --data_type=mean --rebin=10
python plot_profile2d.py --configuration=measurement_10mm_realign.yaml --energy=5 --thickness=10.0 --data_type=mean --rebin=10

# analysis of 10mm data
python plot_profile2d.py --configuration=measurement.yaml --energy=1 --thickness=10.0 --data_type=mean
python plot_profile2d.py --configuration=measurement.yaml --energy=2 --thickness=10.0 --data_type=mean
python plot_profile2d.py --configuration=measurement.yaml --energy=3 --thickness=10.0 --data_type=mean
python plot_profile2d.py --configuration=measurement.yaml --energy=4 --thickness=10.0 --data_type=mean
python plot_profile2d.py --configuration=measurement.yaml --energy=5 --thickness=10.0 --data_type=mean

python plot_profile2d.py --configuration=measurement.yaml --energy=1 --thickness=10.0 --data_type=mean --rebin=10
python plot_profile2d.py --configuration=measurement.yaml --energy=2 --thickness=10.0 --data_type=mean --rebin=10
python plot_profile2d.py --configuration=measurement.yaml --energy=3 --thickness=10.0 --data_type=mean --rebin=10
python plot_profile2d.py --configuration=measurement.yaml --energy=4 --thickness=10.0 --data_type=mean --rebin=10
python plot_profile2d.py --configuration=measurement.yaml --energy=5 --thickness=10.0 --data_type=mean --rebin=10

python plot_profile2d.py --configuration=simulation.yaml --energy=1 --thickness=10.0 --data_type=mean
python plot_profile2d.py --configuration=simulation.yaml --energy=2 --thickness=10.0 --data_type=mean
python plot_profile2d.py --configuration=simulation.yaml --energy=3 --thickness=10.0 --data_type=mean
python plot_profile2d.py --configuration=simulation.yaml --energy=4 --thickness=10.0 --data_type=mean
python plot_profile2d.py --configuration=simulation.yaml --energy=5 --thickness=10.0 --data_type=mean

return

# bin analysis for 10mm, 4GeV
python plot_profile2d.py --configuration=measurement.yaml --energy=4 --thickness=10.0 --data_type=mean
python plot_profile2d.py --configuration=measurement.yaml --energy=4 --thickness=10.0 --data_type=mean --rebin=2
python plot_profile2d.py --configuration=measurement.yaml --energy=4 --thickness=10.0 --data_type=mean --rebin=5
python plot_profile2d.py --configuration=measurement.yaml --energy=4 --thickness=10.0 --data_type=mean --rebin=10
python plot_profile2d.py --configuration=measurement.yaml --energy=4 --thickness=10.0 --data_type=mean --rebin=25
python plot_profile2d.py --configuration=measurement.yaml --energy=4 --thickness=10.0 --data_type=mean --rebin=50