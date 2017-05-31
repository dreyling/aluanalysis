#!/bin/bash

# general comparison
python get_hist_data.py $KAPPA075KINK1 gblsumkx 0.98
python get_hist_data.py $KAPPA075KINK2 gblsumkx 0.98
python get_hist_data.py $KAPPA100KINK1 gblsumkx 0.98
python get_hist_data.py $KAPPA100KINK2 gblsumkx 0.98

# fraction comparison, also for fit
python get_hist_data.py $KAPPA100KINK2 gblsumkx 0.90
python get_hist_data.py $KAPPA075KINK2 gblsumkx 0.90
python get_hist_data.py $KAPPA100KINK2 gblsumkx 0.955
python get_hist_data.py $KAPPA075KINK2 gblsumkx 0.955


# old commands
#python get_hist_data.py 2 gblsumkx 0.98
#python get_hist_data.py 2 gblsumkx 0.90

