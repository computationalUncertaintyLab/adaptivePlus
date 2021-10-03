#mcandrew

import sys
sys.path.append("../")

import numpy as np
import pandas as pd

from mods.index import index

if __name__ == "__main__":

    idx = index("../data/")
    forecasts = idx.grabForecasts()

    EWs = sorted(list(forecasts.EW.unique()))

    EWandMW = pd.DataFrame( { "EW":EWs, "MW":np.arange(0,len(EWs)) } )
    EWandMW.to_csv("EWsandMWs.csv",index=False)
   
 
