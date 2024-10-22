# This is the master data agent, it will enable and disable different data agents.
from support import filehandling, timestamp
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
urlMaxRetries               = int(config.get('data', 'url_max_retries'))

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
    thisJsonData = filehandling.remoteOrLocal(dataSourceURL=thisDataSourceURL, localDataFolder=localRawDataFolder, pullAndUseLocalData=pullAndUseLocalData, urlMaxRetries=urlMaxRetries)
    ################
    # Create an array of the energies...
    thisFirstEntryIndicator = ""
    captureDataKeys = 1
    for thisElement in thisJsonData:
        if "energy" in thisElement:
            # Dictionary:
            #   "last_update": string
            #   "time_tag": list()
            #   "data_keys": list()
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
                # After one set of keys have been capture, disable the capturing of the data unique keys
                captureDataKeys = 0
            # Create the data_keys list at the beginning
            if "data_keys" not in dataDict:
                dataDict["data_keys"] = list()
            # Only capture the first set of data keys, as they repeat in the data set from the NOAA JSON files
            if captureDataKeys == 1:
                dataDict["data_keys"].append(thisElement["energy"])
            # Create the dictionary element of this energy level as a list
            if thisElement["energy"] not in dataDict:
                dataDict[thisElement["energy"]] = list()
            # Append the data sample to the list
            dataDict[thisElement["energy"]].append(float(dataPrecisionFormatter.format(thisElement["flux"])))
            # Append the data key to the list
        else:
            # Dictionary (Magnetometer only):
            #   "last_update": string
            #   "time_tag": list()
            #   "data_keys": list()
            #   "data_name": string
            #   "He": list()
            #   "Hn": list()
            #   "Hp": list()
            #   "total": list()
            # If the time_tag hasn't been created in the dictionary yet, create it
            if "time_tag" not in dataDict:
                dataDict["time_tag"] = list()
            # Create the data_keys list at the beginning
            if "data_keys" not in dataDict:
                dataDict["data_keys"] = list()
            dataDict["time_tag"].append(thisElement["time_tag"])
            # Create the dictionary element of this energy level as a list
            if "He" not in dataDict:
                dataDict["He"] = list()
                dataDict["data_keys"].append("He")
            if "Hn" not in dataDict:
                dataDict["Hn"] = list()
                dataDict["data_keys"].append("Hn")
            if "Hp" not in dataDict:
                dataDict["Hp"] = list()
                dataDict["data_keys"].append("Hp")
            if "total" not in dataDict:
                dataDict["total"] = list()
                dataDict["data_keys"].append("total")
            # Append to the list
            dataDict["He"].append(float(dataPrecisionFormatter.format(thisElement["He"])))
            dataDict["Hn"].append(float(dataPrecisionFormatter.format(thisElement["Hn"])))
            dataDict["Hp"].append(float(dataPrecisionFormatter.format(thisElement["Hp"])))
            dataDict["total"].append(float(dataPrecisionFormatter.format(thisElement["total"])))
    # After the data has been formatted and appended, add the last_update string
    dataDict["last_update"] = timestamp.getTimestamp()
    ################
    # Trim data to a small set
    if trimData:
        for thisKey in dataDict:
            dataDict[thisKey] = dataDict[thisKey][:5]
    ################
    # Store the Formatted Data
    filehandling.setLocalData(localDataFolder=localFormattedDataFolder, localDataFilename=thisDataFilename, jsonData=dataDict)

