# Support definitions
import json
from urllib.request import urlopen
from pathlib import Path

################################
# Fetch the URL data and return, or use the local raw data and return (fetching a storing once if needed)
def remoteOrLocal(dataSourceURL: str, localDataFolder: str, pullAndUseLocalData: bool, urlMaxRetries: int):
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
            jsonData = fetchRemoteData(dataSourceURL=dataSourceURL, urlMaxRetries=urlMaxRetries)
            # Store the data local
            setLocalData(localDataFolder=localDataFolder, localDataFilename=localDataFilename, jsonData=jsonData)
        else:
            print("Local data file present, skipping remote fetch...")
        # Read the data from the local file...
        jsonData = getLocalData(localDataFolder=localDataFolder, localDataFilename=localDataFilename)
    else:
        ########
        # Fetch the file from the server...
        jsonData = fetchRemoteData(dataSourceURL=dataSourceURL, urlMaxRetries=urlMaxRetries)
    # Return the JSON Data Object
    return jsonData

################################
# Fetch the remote data
def fetchRemoteData(dataSourceURL: str, urlMaxRetries: int):
    initialDelay = 1
    backoffMultiplier = 2
    thisDelay = 1
    #print("Fetching remote data from %s"%(dataSourceURL))
    for thisRetry in range(urlMaxRetries):
        try:
            # Open the URL
            response = urlopen(dataSourceURL)
            # Fetch the Data
            jsonData = json.load(response)
            # Return if everything above succeeds...
            return jsonData
        except Exception as e:
            print("URL data fetch failed, retrying in %d second(s)..."%(thisDelay))
            thisDelay *= backoffMultiplier
            time.sleep(thisDelay)
    raise ExceededRetries("Failed to poll %s within %d retries."%(dataSourceURL, urlMaxRetries))

################################
# Store the data to a local file
def setLocalData(localDataFolder: str, localDataFilename: str, jsonData):
    localDataFilePath = Path(localDataFolder+"/"+localDataFilename)
    #print("Setting data to %s"%(localDataFilePath))
    # Store the data local
    with open(localDataFilePath, "w") as fh:
        json.dump(jsonData, fh)

################################
# Get the data from a local file
def getLocalData(localDataFolder: str, localDataFilename: str):
    localDataFilePath = Path(localDataFolder+"/"+localDataFilename)
    #print("Getting data from %s"%(localDataFilePath))
    # Read the data from the local file...
    with open(localDataFilePath, "r") as fh:
        jsonData = json.load(fh)
    return jsonData
