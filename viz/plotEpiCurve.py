#mcandrew

import sys
sys.path.append("../")

import json

import numpy as np
import pandas as pd

from mods.index    import index
from mods.tsTools  import tsTools
from mods.plotTools import culpl

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns

if __name__ == "__main__":

    idx = index("../analysisdata/")
    epidata = idx.grabEpiData_f()

    # for each week, plot the most recent ILI value available
    def chooseMostRecentValue(d):
        return d.sort_values(["releaseDate"]).iloc[-1] # bottom row is most recent
    mostRecentEpidata = epidata.groupby(["EW"]).apply( chooseMostRecentValue )

    pl = culpl()
    pl.style()
    
    fig = plt.figure()
    spec = gridspec.GridSpec(ncols=2, nrows=2, figure=fig)
    axs = []

    # plot 1
    ax = fig.add_subplot(spec[0,:])
    axs.append(ax)
    
    ax.plot( mostRecentEpidata.MW,mostRecentEpidata.wili, lw=2 )
    ax.set_xlabel("Epidemic Weeks")
    ax.set_ylabel("ILI (%)")

    xt = mostRecentEpidata.wili.to_numpy()
    
    # plot 2
    ax = fig.add_subplot(spec[1,0])
    axs.append(ax)
    
    ts = tsTools(mostRecentEpidata.wili)
    lags,autoCorrs = ts.computeAutorCorrs()

    ax.plot(lags,autoCorrs, lw=2,alpha=0.5,color="k")
    ax.scatter(lags,autoCorrs, color="k")

    ax.set_xlabel("Lags")
    ax.set_ylabel("Autocorrelation coeff")

    ax.set_xticks(lags)
    ax.set_yticks(np.arange(0,1+0.1,0.1))

    # plot 3
    ax = fig.add_subplot(spec[1,1])
    axs.append(ax)
    
    rmean,resids = ts.computeRunningMean(window=20)
    ax.plot( mostRecentEpidata.MW, resids, lw=2,color="black" )

    ax.set_xlabel("Epidemic weeks")
    ax.set_ylabel("ILI minus running mean")

    pl.styleTicks(axs)
    pl.styleLbls(axs)

    fig.set_tight_layout(True)
    
    plt.show()
