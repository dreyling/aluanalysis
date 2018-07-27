# aluanalysis

Reads root files for plotting and analysing.

## Installation

Based on Python 2.7

Required:
- PyROOT for ```from ROOT import TFile```
- root_numpy for ```from root_numpy import hist2array```
- Python modules: numpy, scipy, matplotlib, yaml, docopt

## Work flow

Configuration/input parameters are set by a ```yaml``` file and/or arguments.
Plots are saved in ```output```.
Npy arrays are saved in ```data```, see step 2.

Just run the existing scripts or use a single command which are in the scripts:
1. ```01_...sh``` scripts are accesing one root file and content and plot it and to check methods
2. ```02_...sh``` scripts are accesing multiple root files e.g. given by the runlist, fit histograms, extract parameters, 
and produce a npy and csv file for further analysis. The data files are saved in ```data```.
3. ```03_...sh``` scripts are for analyising the data files generated in step 2.
