#mcandrew

import sys
sys.path.append("../")

import json

import numpy as np
import pandas as pd

from mods.index import index

def writeDataDict(outfl,dct):
    fout = open(outfl,"w")
    json.dump(dct,fout,indent=6)
    fout.close()

if __name__ == "__main__":

    idx = index("../data/")
    epidata = idx.grabEpiData()

    epidata = epidata.drop(columns=["surveillanceWeek"])
    epidata = epidata[epidata.lag>=1]

    epidata = epidata.rename(columns={"region":"Location"})
    
    EW2MW = index("./").grabEW2MW()
    epidata = epidata.merge(EW2MW,on="EW")

    epidata["Location"] = epidata["Location"].replace({loc:n for n,loc in enumerate(epidata.Location.unique())})
    epidata.to_csv("epidataFormated.csv",index=False)
