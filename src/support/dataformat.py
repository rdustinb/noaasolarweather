import statistics
from collections import Counter
import math

def cleanupData(thisDataArray: list):
    thisNewDataArray = list()

    # Get a list of repeating values
    repeatingValueFence = int(len(thisDataArray) / 10)
    repeatingValues = [k for k,v in Counter(thisDataArray).items() if v>repeatingValueFence]

    thisWorkingDataArray = list()
    lastDataValue = float('nan')

    # Loop through all original data
    for thisDataSample in thisDataArray:
        if thisDataSample in repeatingValues and not(math.isnan(lastDataValue)):
            thisWorkingDataArray.append(lastDataValue)
        else:
            thisWorkingDataArray.append(thisDataSample)
            lastDataValue = thisDataSample

    # Using the Interquartile method for outlier detection
    # https://www.scribbr.com/statistics/outliers/
    #fenceMultiplier = 1.0
    fenceMultiplier = 1.5
    #
    # 1) Sort your data from low to high
    sortedData = sorted(thisWorkingDataArray)
    # 2) Identify the first quartile (Q1), the median, and the third quartile (Q3).
    firstQuartileIndex = int((len(sortedData) + 1)/4)
    thirdQuartileIndex = int(((len(sortedData) + 1)/4)*3)
    medianIndex = int(((len(sortedData) + 1)/4)*2)
    thisQ1 = sortedData[firstQuartileIndex]
    thisQ3 = sortedData[thirdQuartileIndex]
    thisMedian = sortedData[medianIndex]
    # 3) Calculate your IQR = Q3 – Q1
    thisInterQartileRange = thisQ3 - thisQ1
    # 4) Calculate your upper fence = Q3 + (1.5 * IQR)
    thisUpperFence = thisQ3 + (fenceMultiplier*thisInterQartileRange)
    # 5) Calculate your lower fence = Q1 – (1.5 * IQR)
    thisLowerFence = thisQ1 - (fenceMultiplier*thisInterQartileRange)
    # 6) Use your fences to highlight any outliers, all values that fall outside your fences.

    # Loop through all original data
    for thisDataSample in thisWorkingDataArray:
        # Only cap the low end as these could be noise samples
        if thisDataSample <= thisLowerFence:
            thisNewDataArray.append(thisLowerFence)
        else:
            thisNewDataArray.append(thisDataSample)

    # Finally return the new array...
    return thisNewDataArray
