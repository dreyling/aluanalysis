#! /usr/bin/env python
from matplotlib import rcParams
import matplotlib.pyplot as plt
from rootpy.plotting import set_style, root2matplotlib
from rootpy.io import root_open

# Look at http://www.rootpy.org/ for full documentation

# Use ATLAS plotting style
set_style("ATLAS", mpl=True)
rcParams["font.family"] = "sans-serif"
rcParams["font.sans-serif"] = "Helvetica"
rcParams["mathtext.fontset"] = "custom"
rcParams["mathtext.default"] = "sf"
rcParams["mathtext.rm"] = "serif"
rcParams["mathtext.tt"] = "sans"
rcParams["mathtext.it"] = "sans:italic"
rcParams["mathtext.bf"] = "sans:bold"
rcParams["mathtext.fallback_to_cm"] = True

# Set up an array of colours
colours = [ "red", "blue", "green", "magenta" ]

# Open a file using python-like context
with root_open("run000080.raw.root") as input_file:

  # for path, dirs, objects in input_file.walk():
  #   print path, dirs, objects

  # Can't use file.path.to.hist because there are spaces in the histogram names
  timing_histograms = {
    "Data Analysis" : getattr( input_file.MonitorPerformance, "Data Analysis Time"),
    "Histo Filling" : getattr( input_file.MonitorPerformance, "Histo Fill Time"),
    "Clustering" : getattr( input_file.MonitorPerformance, "Clustering Time"),
    "Correlation" : getattr( input_file.MonitorPerformance, "Correlation Time")
  }

  # Set up a matplotlib figure and axes
  figure, axes = plt.subplots(figsize=(6, 6), dpi=100)

  # Plot using rootpy's matplotlib interface
  for colour, (name, histogram) in zip( colours, timing_histograms.items() ) :
    root2matplotlib.hist( histogram, color=colour, label=name )

  # Draw axes with labels at the ends
  plt.xlabel("Time", ha="right", position=(1, 0) )
  plt.ylabel("Number of instances", ha="right", position=(0, 1))

  # Draw a legend
  plt.legend(loc="upper right", fontsize=15)

  # Draw some ATLAS labels
  plt.text(0.03, 0.92, "ATLAS", va="bottom", ha="left", color="black", size=18, fontname="sans-serif", weight="bold", style="oblique", transform=axes.transAxes)
  plt.text(0.22, 0.92, "Internal", va="bottom", ha="left", color="black", size=18, fontname="sans-serif", transform=axes.transAxes)

  # Save to file
  figure.savefig( "example_timing.pdf" )
  plt.close(figure)





  # ... we *can* use the simple histogram retrieval syntax here :)
  correlation_2D = input_file.Correlations.h_corr_X_APIX_0_vs_APIX_2

  # Make a new figure (or you could clear the old one)
  figure, axes = plt.subplots(figsize=(6, 6), dpi=100)

  # Plot a 2D histogram with a colour-bar key
  counts, xedges, yedges, image = root2matplotlib.hist2d( correlation_2D, cmap="cool" )
  plt.colorbar(image, ax=axes)

  # Draw axes with labels at the ends
  plt.xlabel("APIX 0 X", ha="right", position=(1, 0) )
  plt.ylabel("APIX 2 X", ha="right", position=(0, 1))

  figure.savefig( "example_2D.pdf" )
  plt.close(figure)
