#mcandrew

import sys             # import "(sys)tem" commands
sys.path.append("../") # make sure this code can access files one folder up

import numpy as np     
import pandas as pd

from mods.ensemble import adaptiveEnsemble # in the mods/ensemble folder, import the class called adaptiveEnsemble
from mods.index import index               # This is a class that makes it easy to import important datasets we need. 
from mods.epiTools import fromEW2Season    # A function that maps an EW to the season

if __name__ == "__main__":

    idx = index("../analysisdata/")          # index needs a root directory to pull data from. Idx can only access data at "../analysisdata/"
    scores = idx.grabComponentModelScores()  # Use the idx class to import logscores for each of the component models across all targets,times,locations

    # Below we will move through epidemic weeks, one by one, and train our adaptive ensemble using 
    # scores that are available at Epidemic Week T, then Epidemic week T+1, and so on.
    
    # Store a list of unique Epidemic Weeks ordered from the earliest epidemic week to the latest epidemic week. 
    scores = scores.sort_values("releaseEW") 
    releaseEWs = list( sorted(scores.releaseEW.unique()) )

    # We will iterate through every week of the season.
    # releaseEW is the currently epidemic week we are in and so we will only have access to scores data 
    # from releaseEW or earlier. 
    # subsetOfScoresAvailable is the dataset corresponding to that releaseEW

    firstRun = 1 # This is used for writing our data out to file. 
    season = "2010/2011"
    for releaseEW in releaseEWs[1:]:
        print("ReleaseEW")
        print(releaseEW)
        
        subsetOfScoresAvailable = scores[scores.releaseEW<=releaseEW]

        mostRecentSeason = subsetOfScoresAvailable.iloc[-1].Season
        subsetOfScoresAvailableWithinSeason = subsetOfScoresAvailable.loc[subsetOfScoresAvailable.Season==mostRecentSeason]

        ae = adaptiveEnsemble( subsetOfScoresAvailableWithinSeason, weight = 0.08 )
        ae.buildProbMatrix()
        ae.train()

        means,quantiles = ae.computeWeightStats()

        means["season"]    = season
        means["releaseEW"] = releaseEW

        if firstRun:
            means.to_csv("./meansAdaptiveEnsemble.csv",mode="w",header=True,index=False)
            firstRun=0
        else:
            means.to_csv("./meansAdaptiveEnsemble.csv",mode="a",header=False,index=False)
