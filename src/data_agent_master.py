# This is the master data agent, it will enable and disable different data agents.
from support import filehandling
import configparser
import os 

################################
# Get the configuration
# Create a config parser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Access values from the configuration file
pullAndUseLocalData         = config.getboolean('data', 'use_local')
localRawDataFolder          = config.get('data', 'local_raw')
localFormattedDataFolder    = config.get('general', 'local_formatted')
trimData                    = config.getboolean('data', 'trim_data')
dataPrecision               = config.get('data', 'precision')
baseUrl                     = config.get('data', 'base_url')
dataTypes                   = config.get('data', 'data_types').split()
allDataSpan                 = config.get('data', 'all_data_span').split()

# Generate the full URLs
allDataSourceURLs           = [baseUrl+thisType+"-"+thisSpan+".json" for thisType in dataTypes for thisSpan in allDataSpan]

# Generate the precision formatter
dataPrecisionFormatter = "{:.%sf}"%(dataPrecision)

################################
# Create the local folders if needed
for thisFolder in (localRawDataFolder, localFormattedDataFolder):
    if not os.path.exists(thisFolder): 
        os.makedirs(thisFolder) 

################################
# Fetch the data
for thisDataSourceURL in allDataSourceURLs:
    dataDict = dict()
    ################
    # Generate the local filename based off the URL... (is this a good idea?)
    thisDataFilename = thisDataSourceURL.split("/")[-1]
    ################
    # Get the data...
    # This is in the support/filehandling.py file, a local library:
    thisJsonData = filehandling.remoteOrLocal(dataSourceURL=thisDataSourceURL, localDataFolder=localRawDataFolder, pullAndUseLocalData=pullAndUseLocalData)
    ################
    # Create an array of the energies...
    thisFirstEntryIndicator = ""
    for thisElement in thisJsonData:
        if "energy" in thisElement:
            # Dictionary:
            #   "time_tag": string
            #   "data_name": string
            #   "<energy val 0>": list()
            #   "<energy val 1>": list()
            #       ...
            #   "<energy val 2>": list()
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
        else:
            # Dictionary (Magnetometer only):
            #   "time_tag": string
            #   "data_name": string
            #   "He": list()
            #   "Hn": list()
            #   "Hp": list()
            #   "total": list()
            # If the time_tag hasn't been created in the dictionary yet, create it
            if "time_tag" not in dataDict:
                dataDict["time_tag"] = list()
            dataDict["time_tag"].append(thisElement["time_tag"])
            # Create the dictionary element of this energy level as a list
            if "He" not in dataDict:
                dataDict["He"] = list()
            if "Hn" not in dataDict:
                dataDict["Hn"] = list()
            if "Hp" not in dataDict:
                dataDict["Hp"] = list()
            if "total" not in dataDict:
                dataDict["total"] = list()
            # Append to the list
            dataDict["He"].append(float(dataPrecisionFormatter.format(thisElement["He"])))
            dataDict["Hn"].append(float(dataPrecisionFormatter.format(thisElement["Hn"])))
            dataDict["Hp"].append(float(dataPrecisionFormatter.format(thisElement["Hp"])))
            dataDict["total"].append(float(dataPrecisionFormatter.format(thisElement["total"])))
    ################
    # Trim data to a small set
    if trimData:
        for thisKey in dataDict:
            dataDict[thisKey] = dataDict[thisKey][:5]
    ################
    # Store the Formatted Data
    filehandling.setLocalData(localDataFolder=localFormattedDataFolder, localDataFilename=thisDataFilename, jsonData=dataDict)

