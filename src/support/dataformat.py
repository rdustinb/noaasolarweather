import statistics
from collections import Counter
import math
from scipy.signal import lfilter

def interquartileMethod(thisDataArray: list):
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

def filterMethod(thisDataArray: list):
    # The larger this is, the longer the b-list is and the smaller the b-list element values are
    n = 10
    # This is a list of floating numbers
    b = [1.0 / n] * n
    a = 1

    # Extrapolate the dataset before x=0
    thisWorkingDataSet = thisDataArray[:10] + thisDataArray

    # Filter the dataset
    #
    # https://docs.scipy.org/doc/scipy-0.14.0/reference/generated/scipy.signal.lfilter.html#scipy.signal.lfilter
    #
    # scipy.signal.lfilter(b, a, x, axis=-1, zi=None)
    # b : array_like
    #   The numerator coefficient vector in a 1-D sequence.
    # a : array_like
    #   The denominator coefficient vector in a 1-D sequence. If a[0] is not 1, then both a and b are normalized by a[0].
    # x : array_like
    #   An N-dimensional input array.
    thisNewDataArray = lfilter(b,a,thisWorkingDataSet)

    # Remove the extrapolated data
    thisNewDataArray = thisNewDataArray[10:]

    # Finally return the new array...
    return thisNewDataArray

def removeZeros(thisDataArray: list):
    thisNewDataArray = list()
    lastValue = thisDataArray[0]

    for thisValue in thisDataArray:
        if thisValue == float(0):
            thisNewDataArray.append(lastValue)
        else:
            thisNewDataArray.append(thisValue)
            lastValue = thisValue

    return thisNewDataArray

# Branch which method to use...
def cleanupData(thisDataArray: list, thisDetectionMethod: str = "Interquartile"):
    filterZeros = True

    if(filterZeros):
        thisNewDataArray = removeZeros(thisDataArray=thisDataArray)
    else:
        thisNewDataArray = thisDataArray

    if(thisDetectionMethod == "Interquartile"):
        return interquartileMethod(thisDataArray=thisNewDataArray)
    elif(thisDetectionMethod == "Filter"):
        return filterMethod(thisDataArray=thisNewDataArray)
    else:
        # No normalization, return original array
        return thisDataArray

