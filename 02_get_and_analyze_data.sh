# 2d: rebin 10
python get_and_analyze_profile2d-data.py --configuration=measurement.yaml --data_type=mean --rebin=10
python get_and_analyze_profile2d-data.py --configuration=measurement_10mm_realign.yaml --data_type=mean --rebin=10
# simulation window: 371x250
python get_and_analyze_profile2d-data.py --configuration=simulation.yaml --data_type=mean --rebin=1

return

# 1d
python get_and_analyze_hist1d-data.py --configuration=measurement.yaml --fraction=0.98

# 2d
python get_and_analyze_profile2d-data.py --configuration=measurement.yaml --data_type=sigma
python get_and_analyze_profile2d-data.py --configuration=measurement.yaml --data_type=mean

python get_and_analyze_profile2d-data.py --configuration=simulation.yaml --data_type=sigma
python get_and_analyze_profile2d-data.py --configuration=simulation.yaml --data_type=mean

python get_and_analyze_profile2d-data.py --configuration=measurement_10mm_realign.yaml --data_type=sigma
python get_and_analyze_profile2d-data.py --configuration=measurement_10mm_realign.yaml --data_type=mean 
