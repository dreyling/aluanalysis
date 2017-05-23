KAPPA075KINK1="/home/jande/Documents/fhl-wgs01/data/data_datura/161128_scatalu/EUTelescope_root_files/kappa075_1kink/"
KAPPA075KINK2="/home/jande/Documents/fhl-wgs01/data/data_datura/161128_scatalu/EUTelescope_root_files/kappa075_2kink/"
KAPPA100KINK1="/home/jande/Documents/fhl-wgs01/data/data_datura/161128_scatalu/EUTelescope_root_files/kappa100_1kink/"
KAPPA100KINK2="/home/jande/Documents/fhl-wgs01/data/data_datura/161128_scatalu/EUTelescope_root_files/kappa100_2kink/"

KAPPA100KINK2FRAC0955="data/kappa100_2kink_gblsumkx_0.955.npy"

python plot_hist1d_deriv.py $KAPPA100KINK2 gblsumkx 5 0.0   $KAPPA100KINK2FRAC0955

