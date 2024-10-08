# Support definitions
import json
from urllib.request import urlopen
from pathlib import Path

################################
# Fetch the URL data and return, or use the local raw data and return (fetching a storing once if needed)
def remoteOrLocal(dataSourceURL: str, localDataFolder: str, pullAndUseLocalData: bool):
    ################
    # Store and use a local copy of the data
    if pullAndUseLocalData:
        ########
        # Only fetch the file once...
        # Use the original filename as the local filename
        localDataFilename = dataSourceURL.split("/")[-1]
        localDataFilePath = Path(localDataFolder+"/"+localDataFilename)
        # If there is no local data file, fetch and create it
        if not localDataFilePath.is_file():
            # Fetch the file from the server...
            jsonData = fetchRemoteData(dataSourceURL=dataSourceURL)
            # Store the data local
            setLocalData(localDataFolder=localDataFolder, localDataFilename=localDataFilename, jsonData=jsonData)
        else:
            print("Local data file present, skipping remote fetch...")
        # Read the data from the local file...
        jsonData = getLocalData(localDataFolder=localDataFolder, localDataFilename=localDataFilename)
    else:
        ########
        # Fetch the file from the server...
        jsonData = fetchRemoteData(dataSourceURL=dataSourceURL)
    # Return the JSON Data Object
    return jsonData

################################
# Fetch the remote data
def fetchRemoteData(dataSourceURL: str):
    print("Fetching remote data from %s"%(dataSourceURL))
    # Open the URL
    response = urlopen(dataSourceURL)
    # Fetch the Data
    jsonData = json.load(response)
    return jsonData

################################
# Store the data to a local file
def setLocalData(localDataFolder: str, localDataFilename: str, jsonData):
    localDataFilePath = Path(localDataFolder+"/"+localDataFilename)
    print("Setting data to %s"%(localDataFilePath))
    # Store the data local
    with open(localDataFilePath, "w") as fh:
        json.dump(jsonData, fh)

################################
# Get the data from a local file
def getLocalData(localDataFolder: str, localDataFilename: str):
    localDataFilePath = Path(localDataFolder+"/"+localDataFilename)
    print("Getting data from %s"%(localDataFilePath))
    # Read the data from the local file...
    with open(localDataFilePath, "r") as fh:
        jsonData = json.load(fh)
    return jsonData
