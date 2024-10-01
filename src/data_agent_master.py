# This is the master data agent, it will enable and disable different data agents.
from support import filehandling
import configparser

################################
# Get the configuration
# Create a config parser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Access values from the configuration file
pullAndUseLocalData         = config.getboolean('general', 'use_local')
localRawDataFolder          = config.get('general', 'local_raw')
localFormattedDataFolder    = config.get('general', 'local_formatted')
trimData                    = config.getboolean('data', 'trim_data')
dataPrecision               = config.get('data', 'precision')
allDataSourceURLs           = config.get('sources', 'urls').split()

dataPrecisionFormatter = "{:.%sf}"%(dataPrecision)

################################
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
    thisFirstEntryIndicator = ""
    for thisElement in thisJsonData:
        # If the time_tag hasn't been created in the dictionary yet, create it
        if "time_tag" not in dataDict:
            dataDict["time_tag"] = list()
            thisFirstEntryIndicator = thisElement["energy"]
        # Only append a new time_tag when the list element is the same type as the first one, this prevents duplicate
        # time_tag entries due to multiple data sets in the same file.
        elif thisFirstEntryIndicator == thisElement["energy"]:
            dataDict["time_tag"].append(thisElement["time_tag"])
        # Create the dictionary element of this energy level as a list
        if thisElement["energy"] not in dataDict:
            dataDict[thisElement["energy"]] = list()
        # Append to the list
        dataDict[thisElement["energy"]].append(float(dataPrecisionFormatter.format(thisElement["flux"])))
    ################
    # Trim data to a small set
    if trimData:
        for thisKey in dataDict:
            dataDict[thisKey] = dataDict[thisKey][:5]
    ################
    # Store the Formatted Data
    filehandling.setLocalData(localDataFolder=localFormattedDataFolder, localDataFilename=thisDataFilename, jsonData=dataDict)

