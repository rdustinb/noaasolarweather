"""
File handling support functions for NOAA Solar Weather data fetching and local storage
"""

# Support definitions
from urllib import error as urlerror
from urllib.request import urlopen
from pathlib import Path
import json
import time
import socket
import ssl

# Custom Exceptions
class ExceededRetries(Exception):
    """Raised when the maximum number of retries for a URL fetch is exceeded."""

################################
# Fetch the URL data and return, or use the local raw data and return (fetching a storing once if needed)
def remoteOrLocal(dataSourceURL: str, localDataFolder: str, pullAndUseLocalData: bool, urlMaxRetries: int):
    """
    Fetch the URL data and return, or use the local raw data and return (fetching a storing once if needed)
    """
    ################
    # Store and use a local copy of the data
    if pullAndUseLocalData:
        ########
        # Only fetch the file once...
        # Use the original filename as the local filename
        localDataFilename = dataSourceURL.split("/")[-1]
        localDataFilePath = Path(localDataFolder) / localDataFilename
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
    """
    Fetch the remote data, one of the branches used from remoteOrLocal()
    """
    backoffMultiplier = 2
    thisDelay = 1
    #print("Fetching remote data from %s"%(dataSourceURL))
    for _ in range(urlMaxRetries):
        try:
            # Open the URL using a context manager
            with urlopen(dataSourceURL) as response:
                # Fetch the Data
                jsonData = json.load(response)
                # Return if everything above succeeds...
                return jsonData

        except urlerror.HTTPError as e:
            # Retry for server errors (5xx) and some transient client codes like 429/408
            if 500 <= getattr(e, "code", 0) < 600 or getattr(e, "code", 0) in (429, 408):
                print(f"HTTP {e.code} transient error, retrying in {thisDelay}s...")
            else:
                raise

        except urlerror.URLError as e:
            print(f"URLError: {e.reason!s}, retrying in {thisDelay}s...")

        except socket.timeout:
            print(f"Socket timeout, retrying in {thisDelay}s...")

        except ssl.SSLError:
            # TLS issues are usually not transient; surface them to caller
            raise

        except ValueError:
            # Malformed response or URL — don't retry
            raise

        except OSError as e:
            print(f"OSError: {e!s}, retrying in {thisDelay}s...")

        time.sleep(thisDelay)
        thisDelay *= backoffMultiplier

    raise ExceededRetries(f"Failed to poll {dataSourceURL} within {urlMaxRetries} retries.")

################################
# Store the data to a local file
def setLocalData(localDataFolder: str, localDataFilename: str, jsonData):
    """
    Store the data to a local file which allows for the local data to be used later
    """
    local_dir = Path(localDataFolder)
    local_dir.mkdir(parents=True, exist_ok=True)
    localDataFilePath = local_dir / localDataFilename
    #print("Setting data to %s"%(localDataFilePath))
    # Store the data local
    with open(localDataFilePath, "w", encoding='utf-8') as fh:
        json.dump(jsonData, fh)

################################
# Get the data from a local file
def getLocalData(localDataFolder: str, localDataFilename: str):
    """
    Get the data from a local file
    """
    localDataFilePath = Path(localDataFolder) / localDataFilename
    # Read the data from the local file...
    with open(localDataFilePath, "r", encoding='utf-8') as fh:
        jsonData = json.load(fh)
    return jsonData
