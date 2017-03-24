#! /usr/bin/python
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import math

import x0py 

datapath = "/home/jande/Documents/ownCloud/X0/"#"histograms/"

# Start reading the runlists

runlistfileData = 'runlist-x0d.csv'
runlistfileSim = 'runlist-x0.csv'
whichHisto = "kinkxduttotalx0"

runlistData = x0py.readRunlist(runlistfileData)
runlistSim = x0py.readRunlist(runlistfileSim)


data = x0py.getDataFromRootFiles(runlistData, datapath, whichHisto)
sim = x0py.getDataFromRootFiles(runlistSim, datapath, whichHisto)

plt.ion()
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(10, 9))

plt.rc('text', usetex=True)
plt.rc('font', family='serif')

ax1.set_title(r"$\displaystyle\sigma_{\theta,corr}^2$ Measurement vs. Highland")
ax1.set_xlabel(r"$\displaystyle\sigma_{\theta,corr,calc}^2$")
ax1.set_ylabel(r"$\displaystyle\sigma_{\theta,corr,meas}^2$")
ax1.plot(data[...,5],data[...,4], linestyle='', marker='o')
ax1.set_ylim([0,2.])
ax1.set_xlim([0,2.])

fopt, fcov = curve_fit(x0py.linfunc,data[...,5],data[...,4])
print "Fit rms^2 vs prediction (Meas): " + str(fopt[0]) + "*x + " + str(fopt[1])
xp1 = np.linspace(0., np.amax(data[...,5])*1.1, 200)  # define values to plot the function for
ax1.plot(xp1, x0py.linfunc(xp1, fopt[0], fopt[1]), 'r-')
ax1.text(0.95, 0.05, r'm='+str('{:.3f} $\pm$ {:.3f}'.format(fopt[0],math.sqrt(fcov[0,0]))), fontsize=15, verticalalignment='bottom', horizontalalignment='right',transform=ax1.transAxes)

ax2.set_title(r"$\displaystyle\sigma_{\theta,corr}^2$ Simulation vs. Highland")
ax2.set_xlabel(r"$\displaystyle\sigma_{\theta,corr,calc}^2$")
ax2.set_ylabel(r"$\displaystyle\sigma_{\theta,corr,meas}^2$")
ax2.plot(sim[...,5],sim[...,4], linestyle='', marker='o', c='r')

fopts, fcovs = curve_fit(x0py.linfunc,sim[...,5],sim[...,4])
print "Fit rms^2 vs prediction (Sim): " + str(fopts[0]) + "*x + " + str(fopts[1])
xp2 = np.linspace(0., np.amax(sim[...,5])*1.1, 200)  # define values to plot the function for
ax2.plot(xp2, x0py.linfunc(xp2, fopts[0], fopts[1]), 'r-')
ax2.text(0.95, 0.05, r'm='+str('{:.3f} $\pm$ {:.3f}'.format(fopts[0],math.sqrt(fcovs[0,0]))), fontsize=15, verticalalignment='bottom', horizontalalignment='right',transform=ax2.transAxes)
ax2.set_ylim([0,2.])
ax2.set_xlim([0,2.])

ax3.set_title("Meas \& Sim")
ax3.set_xlabel(r"$\displaystyle\sigma_{\theta,corr,calc}^2$")
ax3.set_ylabel(r"$\displaystyle\sigma_{\theta,corr,meas}^2$")
ax3.plot(data[...,5],data[...,4], linestyle='', marker='o', c='b')
ax3.plot(sim[...,5],sim[...,4], linestyle='', marker='o', c='r')
ax3.set_ylim([0,2.])
ax3.set_xlim([0,2.])


# Correlation plot

nRunsD = np.size(runlistData,0)
nRunsS = np.size(runlistSim,0)
corr = np.zeros((np.maximum(nRunsD,nRunsS),2))
ind = 0
for i in range(0, nRunsD):
    for j in range(0, nRunsS):
        if(data[i,1] == sim[j,1]):
            if(data[i,2] == sim[j,2]):
                corr[ind,0] = data[i,4]
                corr[ind,1] = sim[j,4]
                ind = ind + 1

foptc, fcovc = curve_fit(x0py.linfunc,corr[...,0],corr[...,1])
print "Fit Correlation: " + str(foptc[0]) + "*x + " + str(foptc[1])

ax4.set_title("Meas vs Sim (aka correlation)")
ax4.set_xlabel(r"$\displaystyle\sigma_{\theta,corr,sim}^2$")
ax4.set_ylabel(r"$\displaystyle\sigma_{\theta,corr,meas}^2$")
ax4.plot(corr[...,1],corr[...,0], linestyle='', marker='o', c='k')
xp3 = np.linspace(0., np.amax(corr[...,0])*1.1, 200)  # define values to plot the function for
ax4.plot(xp3, x0py.linfunc(xp3, foptc[0], foptc[1]), 'r-')
ax4.text(0.95, 0.05, r'm='+str('{:.3f} $\pm$ {:.3f}'.format(foptc[0],math.sqrt(fcovc[0,0]))), fontsize=15, verticalalignment='bottom', horizontalalignment='right',transform=ax4.transAxes)
ax4.set_ylim([0,2.])
ax4.set_xlim([0,2.])

fig.subplots_adjust(hspace=0.4, wspace=0.5)
plt.show()


fig2, a = plt.subplots(2, 4, figsize=(13, 8))

ratioVsTh = np.zeros((7,2))

def plotOneOfTheseMFs(m,k,thickness):
    
    pbounds = ([0,-np.inf],[np.inf,np.inf])
    xps = np.linspace(1., 5., 200)

    d1 = x0py.oneThicknessDataset(thickness, data)
    popt, pcov = curve_fit(x0py.highfunc,d1[...,1],d1[...,0], bounds=pbounds)

    a[m,k].set_title(r"$\displaystyle\sigma_{\theta,corr}$ vs momentum, th = " + str(thickness))
    a[m,k].set_xlabel("p [GeV]")
    a[m,k].set_ylabel(r"$\displaystyle\sigma_{\theta,corr} [mrad]$")
            
    a[m,k].plot(d1[:,1],d1[:,0], linestyle='', marker='o')
    a[m,k].plot(xps, x0py.highfunc(xps, popt[0], popt[1]), 'r-')
    a[m,k].set_ylim([0,np.amax(d1[...,0]*1.1)])
    a[m,k].text(0.95, 0.05, r'd='+str('{:.3f} $\pm$ {:.3f}'.format(popt[0],math.sqrt(pcov[0,0]))), fontsize=15, verticalalignment='bottom', horizontalalignment='right',transform=a[m,k].transAxes)

    ratioVsTh[m*4+k,0] = popt[0]/thickness
    ratioVsTh[m*4+k,1] = thickness/x0py.x0alu

plotOneOfTheseMFs(0,0,0.013)
plotOneOfTheseMFs(0,1,0.025)
plotOneOfTheseMFs(0,2,0.050)
plotOneOfTheseMFs(0,3,0.1)
plotOneOfTheseMFs(1,0,0.2)
plotOneOfTheseMFs(1,1,1.0)
plotOneOfTheseMFs(1,2,10.0)

a[1,3].set_title("Measurement error")
a[1,3].set_xlabel("nom. thickness [t/X0]")
a[1,3].set_ylabel(r"$\displaystyle th_{meas.}/th_{nom.}$")
a[1,3].semilogx(ratioVsTh[...,1],ratioVsTh[...,0], marker='o', linestyle='')

fig2.subplots_adjust(hspace=0.4, wspace=0.5)
plt.show()

raw_input("Drueck mich!")

#plt.semilogx(data[...,2],data[...,6], linestyle='', marker='o')
#plt.show()
