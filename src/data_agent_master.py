# This is the master data agent, it will enable and disable different data agents.
from support import filehandling

#allDataSourceURLs = {
#    "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"
#}

#allDataSourceURLs = {
#    "https://services.swpc.noaa.gov/json/goes/primary/differential-protons-1-day.json",
#    "https://services.swpc.noaa.gov/json/goes/primary/differential-electrons-1-day.json",
#    "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-1-day.json",
#    "https://services.swpc.noaa.gov/json/goes/primary/integral-electrons-1-day.json",
#    "https://services.swpc.noaa.gov/json/goes/primary/magnetometers-1-day.json",
#    "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"
#}

# Magnetometers uses a vector data value, not the energy key

allDataSourceURLs = {
    "https://services.swpc.noaa.gov/json/goes/primary/differential-protons-1-day.json",
    "https://services.swpc.noaa.gov/json/goes/primary/differential-electrons-1-day.json",
    "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-1-day.json",
    "https://services.swpc.noaa.gov/json/goes/primary/integral-electrons-1-day.json",
    "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"
}

pullAndUseLocalData = True

localRawDataFolder = "localData"
localFormattedDataFolder = "formattedData"

# Fetch the data
for thisDataSourceURL in allDataSourceURLs:
    dataDict = dict()
    print(" ")
    ################
    # Generate the local filename based off the URL... (is this a good idea?)
    thisDataFilename = thisDataSourceURL.split("/")[-1]
    ################
    # Get the data...
    # This is in the support/filehandling.py file, a local library:
    thisJsonData = filehandling.remoteOrLocal(dataSourceURL=thisDataSourceURL, localDataFolder=localRawDataFolder, pullAndUseLocalData=pullAndUseLocalData)
    ################
    # Create an array of the energies...
    print("Formatting data from %s"%(thisDataSourceURL))
    for thisElement in thisJsonData:
        # Create the dictionary element of the date as a list
        if "time_tag" not in dataDict:
            dataDict["time_tag"] = list()
        dataDict["time_tag"].append(thisElement["time_tag"])
        # Create the dictionary element of this energy level as a list
        if thisElement["energy"] not in dataDict:
            dataDict[thisElement["energy"]] = list()
        # Append to the list
        dataDict[thisElement["energy"]].append(thisElement["flux"])
    ################
    # Store the Formatted Data
    filehandling.setLocalData(localDataFolder=localFormattedDataFolder, localDataFilename=thisDataFilename, jsonData=dataDict)

