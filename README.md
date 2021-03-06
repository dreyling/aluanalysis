# aluanalysis

Reads root files for plotting and analysing.

## Installation

ROOT compiled with python flag:
- PyROOT for ```from ROOT import TFile```, see https://root.cern.ch/pyroot

Python (try Anaconda or Miniconda or the local python):
- Python 2.7
- numpy, scipy, matplotlib, yaml, docopt
- root_numpy for ```from root_numpy import hist2array```, see http://scikit-hep.org/root_numpy/install.html

## Work flow

Configuration/input parameters are set by a ```yaml``` file and/or arguments.
Plots are saved in ```output```.
Npy arrays are saved in ```data```, see step 2.

Just run the existing scripts or use a single command which are in the scripts:
1. ```01_...sh``` scripts are accesing one root file and content and plot it and to check methods
2. ```02_...sh``` scripts are accesing multiple root files e.g. given by the runlist, fit histograms, extract parameters, 
and produce a npy and csv file for further analysis. The data files are saved in ```data```.
3. ```03_...sh``` scripts are for analyising the data files generated in step 2.
