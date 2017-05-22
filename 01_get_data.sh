#!/bin/bash
KAPPA075KINK1="/home/jande/Documents/fhl-wgs01/data/data_datura/161128_scatalu/EUTelescope_root_files/kappa075_1kink/"
KAPPA075KINK2="/home/jande/Documents/fhl-wgs01/data/data_datura/161128_scatalu/EUTelescope_root_files/kappa075_2kink/"
KAPPA100KINK1="/home/jande/Documents/fhl-wgs01/data/data_datura/161128_scatalu/EUTelescope_root_files/kappa100_1kink/"
KAPPA100KINK2="/home/jande/Documents/fhl-wgs01/data/data_datura/161128_scatalu/EUTelescope_root_files/kappa100_2kink/"

# general comparison
python get_hist_data.py $KAPPA075KINK1 gblsumkx 0.98
python get_hist_data.py $KAPPA075KINK2 gblsumkx 0.98
python get_hist_data.py $KAPPA100KINK1 gblsumkx 0.98
python get_hist_data.py $KAPPA100KINK2 gblsumkx 0.98

# fraction comparison, also for fit
python get_hist_data.py $KAPPA100KINK2 gblsumkx 0.90
python get_hist_data.py $KAPPA075KINK2 gblsumkx 0.90


# old commands
#python get_hist_data.py 2 gblsumkx 0.98
#python get_hist_data.py 2 gblsumkx 0.90

