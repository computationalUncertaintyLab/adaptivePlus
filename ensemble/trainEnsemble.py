#mcandrew

import sys
sys.path.append("../") # make sure this code can access files one folder up

import numpy as np
import pandas as pd

from mods.ensemble import adaptiveEnsemble # in the mods/ensemble folder, import the class called ensemble
from mods.index import index
from mods.epiTools import fromEW2Season # maps an EW to the season

if __name__ == "__main__":


    idx = index("../analysisdata/") # index needs a root directory to pull data from
    scores = idx.grabComponentModelScores()

    scores = scores.sort_values("releaseEW")
    releaseEWs = list( sorted(scores.releaseEW.unique()) )

    # We will iterate through every week of the season.
    # releaseEW equasl the currently available scores data
    # subsetOfScoresAvailable is the dataset corresponding to that releaseEW

    firstRun = 1
    season = "2010/2011"
    for releaseEW in releaseEWs:
        subsetOfScoresAvailable = scores[scores.releaseEW<=releaseEW]

        mostRecentSeason = subsetOfScoresAvailable.iloc[-1].Season
        subsetOfScoresAvailableWithinSeason = subsetOfScoresAvailable.loc[subsetOfScoresAvailable.Season==mostRecentSeason]

        ae = adaptiveEnsemble( subsetOfScoresAvailableWithinSeason, weight = 0.08 )
        ae.buildProbMatrix()
        ae.train()

        means,quantiles = ae.computeWeightStats()

        means["season"] = season
        means["releaseEW"] = releaseEW

        if firstRun:
            means.to_csv("./meansAdaptiveEnsemble.csv",mode="w",header=True,index=False)
            firstRun=0
        else:
            means.to_csv("./meansAdaptiveEnsemble.csv",mode="a",header=False,index=False)
