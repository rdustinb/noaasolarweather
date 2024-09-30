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
allDataSourceURLs           = config.get('sources', 'urls').split()

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

