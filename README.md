# adaptivePlus

**analysisdata/**

from**X**2Number.json
i remapped the 7 targets, 11 locations (10 HHS plus National), and the 21 component models from strings to integers. These jsons present the mapping from string to integers. For example, the target "3 wk ahead" was mapped to the integer 2. 

**EWsandMWs.csv**

Epidemic weeks are formatted using a Year-Week format (i.e. YYYYWW0). Using epidemic week can be difficult during analysis. 
A more natural way to index ILI over time uses a model week, an integer that assigns the value 1 to the first reported epidemic week, 2 to the second week, and so on. This CSV file is a map between epidemic week and model week. 

**epidataFormatted.csv**

This file contains ILI values (wili) for all locations and epidemic weeks, including all potential revisions to an epidemic week. 
You'll find the following columns inside:

```EW,Location,wili,lag,releaseDate,releaseEW,MW```

- EW = Epidemic Week: a standardized way to describe activity within one week. Format is YYYYWW
- Location = ILI is reported for 10 Health and Human Service regions and also at the National level. There are 11 different locations. 
- wili = Percent influenza-like illness within a location and for a specific epidemic week. 
- releaseEW = The week in time when a ILI values was reported for a given epidemic week. For example, an epidemic week of 201243 and releaseEW of 201246 means that during the week of 201246, the reported ILI for Epidemic week 201243 was "X".  
- lag = releaseEW minus EW
- MW = Model week or the number of elapsed weeks from the first reported epidemic week to this EW. 

**scores.csv**

This is a data file where the rows correspond to a component model's log score for a given target, location, epidemic week, and release epidemic week. The range of possible ILI percents from 0 to 100 when a model is scored is discretized into 131 intervals: [0,0.1),[0.1,0.2),...,[12.9,13),[13,100]. In addition to the logscore, this file also includes the probability a component model assigned to the true interval, the true value, and the interval (called a bin).

Columns
```Location,Target,MW,MWtargetWeek,releaseEW,Bin_start_incl,Bin_end_notincl,Value,wili,logscore```


**forecastsFormatted**
This file contains discretized probabilistic predictive distributions for all 21 component models, 11 locations, and 7 targets from the 2011/2012 to 2018/2019 influenza season. A continuous predictive distribution from a component model is discretized into 131 intervals, often called bins: [0,0.1),[0.1,0.2),...[12.9,13.0),[13.0,100.0].  

Columns
```Location,Target,Unit,Bin_start_incl,Bin_end_notincl,Value,component_model_id,EW,MW```

- Location = ILI is reported for 10 Health and Human Service regions and also at the National level. There are 11 different locations.
- Target   = An integer from 0-6 that indicated which of the 7 targets this distribtuion is forecasting. 
- Unit     = Either the string "week" or "percent". The string "week" indicates the forecast assigns probabilities to weeks of the season. The string "percent" indicates the forecast assigns probabilities to ILI percents.
- Bin_start_incl  = For forecasts of ILI, this is one of 0,0.1,0.2,...,13.0 that denotes the lower bound of an interval which was assigned a probability. For forecasts of weeks this is one of 40,41,...,19.
- Bin_end_notincl = For forecasts of ILI, this is one of 0.1,0.2,...,100.0 that denotes the upper bound of an interval which was assigned a probability. For forecasts of weeks this is one of 41,42,...,20.
- Value           = the porbabiliity assigned to the interval [Bin_start_incl, Bin_end_notincl)
- compononet_model_id = An interger in the set 0,1,2,...,20 that indiciates which component model made this forecast.
- EW = Epidemic Week: a standardized way to describe activity within one week. Format is YYYYWW 
- MW = Model week or the number of elapsed weeks from the first reported epidemic week to this EW. 

**viz/**

plotEpiCurve.py
This program plots (top) percent ILI versus model week, (bottom left) the autocorrelation coefficient for lags 1 through 10, and (bottom right) a centered version of ILI versus model. Only the most recent ILI values are reported. The most up to date ILI value is called the **final ILI**. 

**mods/**

The mods folder contains useful code that we may find our selves using over and over.

index.py
This file contain a single object called *index* thats accepts one argument, root, that point to a directory. Index allows the user to load data into a sciript without having to worry about where that file is. Index should be used whenever possible to load data into a script so that the data we use is consistent.

--------------------------------------
**Example**
```
import sys
sys.path.append("../")

from mods.index    import index
idx = index("../analysisdata/")
epidata = idx.grabEpiData_f()
```
--------------------------------------

tsTools.py

Thie file contains the object tsTools and accepts an array representing a time series.
For now, this object computes autocorrealtions and a running mean. 


