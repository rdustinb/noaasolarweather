import urllib.request, json, datetime

# Error Log Structure
#   dict{
#       "sample name as key" : {
#           "time_tag" : [ list of dates that are logged every time this script is called ]
#           "url_failure_flags" : [ list of booleans for whether a data type server access failed ]
#           "corrupt_flags" : [ list of booleans for whether a data type failed corruption tests ]

###############################################################################
###############################################################################
# TODO
# 1) Run this script with a daemon for a long time and calculate error rates
#   - For the data sets that have different data lengths on the server, run this
#   script for a few days targetting each archive period for errors.
# 2) Add a "new data" status bit to the JSON archive
#   - The GUI will read to check if the data has been updated by this fetching
#   daemon script.
#   - The GUI will clear the bit once it has updated the graphs.
#   - This bit should not be set if ALL of the data happens to fail to fetch from
#   the error conditions in #1 and #2 above.
###############################################################################
###############################################################################
# Completed
# 1) Add Remote Server URL Pull error handling
#   - This happens if the remote URL or Server is inaccessible
#   - This fetch daemon script should NOT overwrite the json archive if this
#   occurs.
# 2) Add Remote Server Data corruption error handling
#   - This happens if the remote Server is updating data at the same time I am
#   pulling the data, a file-based race condition
#   - This fetch daemon script should NOT overwrite the specific data structure
#   where this error occurs, instead rewriting the data that was already in the
#   archive.
# 3) Add error logging in a way that it can be graphed.
#   - JSON archive
#   - Dictionary of keys that are named according to the error
#   - The Error name dictionary will itself be a list of date stamps
#   - The graphing function can simply count the occurences of date stamps for
#   calculating the error rate and frequency
# 4) Add functionality configuration file.
#   - It is not checked into the repo.
#   - It is user-specific on the user's machine
#   - It is checked every time this script is run
#   - If it is not present a default config file is made by this script
# 5) Make the DEBUG parameter passable to all the functions.
###############################################################################
###############################################################################

###############################################################################
# Solar Weather Indices
###############################################################################
def get_kp_index_1m(error_log_in, data_in, date, DEBUGLEVEL):
  # This function calls' error log and data are passed in to be updated, this allows the error handling to "recover" by
  # simply passing back the data that was in the json archive previously, keeping the stored data
  error_log = error_log_in
  # Get the Kp Index
  if DEBUGLEVEL != "none": print("get_kp_index_1m()")
  url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"

  # Create the error dict if necessary
  if "get_kp_index_1m()" not in error_log:
    error_log["get_kp_index_1m()"] = dict()
    error_log["get_kp_index_1m()"]["urlopen"] = list()
    error_log["get_kp_index_1m()"]["corrupt"] = list()
    error_log["get_kp_index_1m()"]["time_tag"] = list()

  # Update the datestamp list
  error_log["get_kp_index_1m()"]["time_tag"].append(date)

  # Make sure we access the server cleanly
  try:
    with urllib.request.urlopen(url) as thisurl:
      tmp_data = json.loads(thisurl.read().decode())
    error_log["get_kp_index_1m()"]["urlopen"].append(False)
  except Exception as e:
    # If Opening the URL is an issue, then append a False flag for the data corruption since it isn't being tested
    error_log["get_kp_index_1m()"]["urlopen"].append(True)
    error_log["get_kp_index_1m()"]["corrupt"].append(False)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If we cannot even fetch the data, just return what was passed to us....
    return (error_log, data_in)
  
  # Test that the data looks valid before passing
  try:
    if DEBUGLEVEL == "info": print("Example kp_index:         %s"%(tmp_data[0]["kp_index"]))
    if DEBUGLEVEL == "info": print("Example time_tag[0]:      %s"%(tmp_data[0]["time_tag"]))
    if DEBUGLEVEL == "info": print("Example time_tag[-1]:     %s"%(tmp_data[-1]["time_tag"]))
    if DEBUGLEVEL == "info": print("Example data[0]:          %s"%(tmp_data[0]))
    if DEBUGLEVEL == "info": print("Example data[-1]:         %s"%(tmp_data[-1]))
    if DEBUGLEVEL == "info": print("Total data points: %d"%(len(tmp_data)))
    if DEBUGLEVEL == "info": print("\n")

    # If this doesn't throw an exception but doesn't meet these conditions, the data is corrupt
    if (len(tmp_data[0]) is not 2) or (len(tmp_data[-1]) is not 2):
      error_log["get_kp_index_1m()"]["corrupt"].append(True)
      if DEBUGLEVEL == "error": print("Corrupt error:")
      if DEBUGLEVEL == "error": print(tmp_data)
      if DEBUGLEVEL == "error": print("\n")
      return (error_log, data_in)

    # Format this data key
    data["get_kp_index_1m()"] = listOfDicts_to_dictOfLists(tmp_data, DEBUGLEVEL)

    error_log["get_kp_index_1m()"]["corrupt"].append(False)
    return (error_log, data)
  except Exception as e:
    error_log["get_kp_index_1m()"]["corrupt"].append(True)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If the data appears corrupt from some basic tests, return the original data
    return (error_log, data_in)

def get_k_index_1m(error_log_in, data_in, date, DEBUGLEVEL):
  # This function calls' error log and data are passed in to be updated, this allows the error handling to "recover" by
  # simply passing back the data that was in the json archive previously, keeping the stored data
  error_log = error_log_in
  # Get the Boulder K Index
  if DEBUGLEVEL != "none": print("get_k_index_1m()")
  url = "https://services.swpc.noaa.gov/json/boulder_k_index_1m.json"

  # Create the error dict if necessary
  if "get_k_index_1m()" not in error_log:
    error_log["get_k_index_1m()"] = dict()
    error_log["get_k_index_1m()"]["urlopen"] = list()
    error_log["get_k_index_1m()"]["corrupt"] = list()
    error_log["get_k_index_1m()"]["time_tag"] = list()

  # Update the datestamp list
  error_log["get_k_index_1m()"]["time_tag"].append(date)

  # Make sure we access the server cleanly
  try:
    with urllib.request.urlopen(url) as thisurl:
      tmp_data = json.loads(thisurl.read().decode())
    error_log["get_k_index_1m()"]["urlopen"].append(False)
  except Exception as e:
    # If Opening the URL is an issue, then append a False flag for the data corruption since it isn't being tested
    error_log["get_k_index_1m()"]["urlopen"].append(True)
    error_log["get_k_index_1m()"]["corrupt"].append(False)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If we cannot even fetch the data, just return what was passed to us....
    return (error_log, data_in)
  
  # Test that the data looks valid before passing
  try:
    if DEBUGLEVEL == "info": print("Example k_index:          %s"%(tmp_data[0]["k_index"]))
    if DEBUGLEVEL == "info": print("Example time_tag[0]:      %s"%(tmp_data[0]["time_tag"]))
    if DEBUGLEVEL == "info": print("Example time_tag[-1]:     %s"%(tmp_data[-1]["time_tag"]))
    if DEBUGLEVEL == "info": print("Example data[0]:          %s"%(tmp_data[0]))
    if DEBUGLEVEL == "info": print("Example data[-1]:         %s"%(tmp_data[-1]))
    if DEBUGLEVEL == "info": print("Length of data[0]:        %d"%(len(tmp_data[0])))
    if DEBUGLEVEL == "info": print("Total data points: %d"%(len(tmp_data)))
    if DEBUGLEVEL == "info": print("\n")

    # If this doesn't throw an exception but doesn't meet these conditions, the data is corrupt
    if (len(tmp_data[0]) is not 2) or (len(tmp_data[-1]) is not 2):
      error_log["get_k_index_1m()"]["corrupt"].append(True)
      if DEBUGLEVEL == "error": print("Corrupt error:")
      if DEBUGLEVEL == "error": print(tmp_data)
      if DEBUGLEVEL == "error": print("\n")
      return (error_log, data_in)

    # Format this data key
    data["get_k_index_1m()"] = listOfDicts_to_dictOfLists(tmp_data, DEBUGLEVEL)

    error_log["get_k_index_1m()"]["corrupt"].append(False)
    return (error_log, data)
  except Exception as e:
    error_log["get_k_index_1m()"]["corrupt"].append(True)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If the data appears corrupt from some basic tests, return the original data
    return (error_log, data_in)
  
###############################################################################
# Solar Weather Measurements
###############################################################################
def get_measurement_differential_electrons(period, error_log_in, data_in, date, DEBUGLEVEL):
  # This function calls' error log and data are passed in to be updated, this allows the error handling to "recover" by
  # simply passing back the data that was in the json archive previously, keeping the stored data
  error_log = error_log_in
  # "time_tag"
  # "satellite"
  # "flux"
  # "energy"
  if DEBUGLEVEL != "none": print("get_measurement_differential_electrons(%s)"%(period))
  if period == "6h": url = "https://services.swpc.noaa.gov/json/goes/primary/differential-electrons-6-hour.json"
  if period == "1d": url = "https://services.swpc.noaa.gov/json/goes/primary/differential-electrons-1-day.json"
  if period == "3d": url = "https://services.swpc.noaa.gov/json/goes/primary/differential-electrons-3-day.json"
  if period == "7d": url = "https://services.swpc.noaa.gov/json/goes/primary/differential-electrons-7-day.json"

  # Create the error dict if necessary
  if "get_measurement_differential_electrons()" not in error_log:
    error_log["get_measurement_differential_electrons()"] = dict()
    error_log["get_measurement_differential_electrons()"]["urlopen"] = list()
    error_log["get_measurement_differential_electrons()"]["corrupt"] = list()
    error_log["get_measurement_differential_electrons()"]["time_tag"] = list()

  # Update the datestamp list
  error_log["get_measurement_differential_electrons()"]["time_tag"].append(date)

  # Make sure we access the server cleanly
  try:
    with urllib.request.urlopen(url) as thisurl:
      tmp_data = json.loads(thisurl.read().decode())
    error_log["get_measurement_differential_electrons()"]["urlopen"].append(False)
  except Exception as e:
    # If Opening the URL is an issue, then append a False flag for the data corruption since it isn't being tested
    error_log["get_measurement_differential_electrons()"]["urlopen"].append(True)
    error_log["get_measurement_differential_electrons()"]["corrupt"].append(False)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If we cannot even fetch the data, just return what was passed to us....
    return (error_log, data_in)
  
  # Test that the data looks valid before passing
  try:
    if DEBUGLEVEL == "info": print("Example satellite    : %s"%(tmp_data[0]["satellite"]))
    if DEBUGLEVEL == "info": print("Example flux         : %s"%(tmp_data[0]["flux"]))
    if DEBUGLEVEL == "info": print("Example energy       : %s"%(tmp_data[0]["energy"]))
    if DEBUGLEVEL == "info": print("Example time_tag[0]  : %s"%(tmp_data[0]["time_tag"]))
    if DEBUGLEVEL == "info": print("Example time_tag[-1] : %s"%(tmp_data[-1]["time_tag"]))
    if DEBUGLEVEL == "info": print("Total data points: %d"%(len(tmp_data)))
    if DEBUGLEVEL == "info": print("\n")
  
    # If this doesn't throw an exception but doesn't meet these conditions, the data is corrupt
    if (len(tmp_data[0]) is not 4) or (len(tmp_data[-1]) is not 4):
      error_log["get_measurement_differential_electrons()"]["corrupt"].append(True)
      if DEBUGLEVEL == "error": print("Corrupt error:")
      if DEBUGLEVEL == "error": print(tmp_data)
      if DEBUGLEVEL == "error": print("\n")
      return (error_log, data_in)

    # Format this data key
    data["get_measurement_differential_electrons()"] = listOfDicts_to_dictOfLists(tmp_data, DEBUGLEVEL)

    error_log["get_measurement_differential_electrons()"]["corrupt"].append(False)
    return (error_log, data)
  except Exception as e:
    error_log["get_measurement_differential_electrons()"]["corrupt"].append(True)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If the data appears corrupt from some basic tests, return the original data
    return (error_log, data_in)

def get_measurement_differential_protons(period, error_log_in, data_in, date, DEBUGLEVEL):
  # This function calls' error log and data are passed in to be updated, this allows the error handling to "recover" by
  # simply passing back the data that was in the json archive previously, keeping the stored data
  error_log = error_log_in
  # "time_tag"
  # "satellite"
  # "flux"
  # "energy"
  # "yaw_flip"
  # "channel"
  if DEBUGLEVEL != "none": print("get_measurement_differential_protons(%s)"%(period))
  if period == "6h": url = "https://services.swpc.noaa.gov/json/goes/primary/differential-protons-6-hour.json"
  if period == "1d": url = "https://services.swpc.noaa.gov/json/goes/primary/differential-protons-1-day.json"
  if period == "3d": url = "https://services.swpc.noaa.gov/json/goes/primary/differential-protons-3-day.json"
  if period == "7d": url = "https://services.swpc.noaa.gov/json/goes/primary/differential-protons-7-day.json"

  # Create the error dict if necessary
  if "get_measurement_differential_protons()" not in error_log:
    error_log["get_measurement_differential_protons()"] = dict()
    error_log["get_measurement_differential_protons()"]["urlopen"] = list()
    error_log["get_measurement_differential_protons()"]["corrupt"] = list()
    error_log["get_measurement_differential_protons()"]["time_tag"] = list()

  # Update the datestamp list
  error_log["get_measurement_differential_protons()"]["time_tag"].append(date)

  # Make sure we access the server cleanly
  try:
    with urllib.request.urlopen(url) as thisurl:
      tmp_data = json.loads(thisurl.read().decode())
    error_log["get_measurement_differential_protons()"]["urlopen"].append(False)
  except Exception as e:
    # If Opening the URL is an issue, then append a False flag for the data corruption since it isn't being tested
    error_log["get_measurement_differential_protons()"]["urlopen"].append(True)
    error_log["get_measurement_differential_protons()"]["corrupt"].append(False)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If we cannot even fetch the data, just return what was passed to us....
    return (error_log, data_in)
  
  # Test that the data looks valid before passing
  try:
    if DEBUGLEVEL == "info": print("Example satellite    : %s"%(tmp_data[0]["satellite"]))
    if DEBUGLEVEL == "info": print("Example flux         : %s"%(tmp_data[0]["flux"]))
    if DEBUGLEVEL == "info": print("Example energy       : %s"%(tmp_data[0]["energy"]))
    if DEBUGLEVEL == "info": print("Example yaw_flip     : %s"%(tmp_data[0]["yaw_flip"]))
    if DEBUGLEVEL == "info": print("Example channel      : %s"%(tmp_data[0]["channel"]))
    if DEBUGLEVEL == "info": print("Example time_tag[0]  : %s"%(tmp_data[0]["time_tag"]))
    if DEBUGLEVEL == "info": print("Example time_tag[-1] : %s"%(tmp_data[-1]["time_tag"]))
    if DEBUGLEVEL == "info": print("Total data points: %d"%(len(tmp_data)))
    if DEBUGLEVEL == "info": print("\n")
  
    # If this doesn't throw an exception but doesn't meet these conditions, the data is corrupt
    if (len(tmp_data[0]) is not 6) or (len(tmp_data[-1]) is not 6):
      error_log["get_measurement_differential_protons()"]["corrupt"].append(True)
      if DEBUGLEVEL == "error": print("Corrupt error:")
      if DEBUGLEVEL == "error": print(tmp_data)
      if DEBUGLEVEL == "error": print("\n")
      return (error_log, data_in)

    # Format this data key
    data["get_measurement_differential_protons()"] = listOfDicts_to_dictOfLists(tmp_data, DEBUGLEVEL)

    error_log["get_measurement_differential_protons()"]["corrupt"].append(False)
    return (error_log, data)
  except Exception as e:
    error_log["get_measurement_differential_protons()"]["corrupt"].append(True)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If the data appears corrupt from some basic tests, return the original data
    return (error_log, data_in)

def get_measurement_integral_electrons(period, error_log_in, data_in, date, DEBUGLEVEL):
  # This function calls' error log and data are passed in to be updated, this allows the error handling to "recover" by
  # simply passing back the data that was in the json archive previously, keeping the stored data
  error_log = error_log_in
  # "time_tag"
  # "satellite"
  # "flux"
  # "energy"
  if DEBUGLEVEL != "none": print("get_measurement_integral_electrons(%s)"%(period))
  if period == "6h": url = "https://services.swpc.noaa.gov/json/goes/primary/integral-electrons-6-hour.json"
  if period == "1d": url = "https://services.swpc.noaa.gov/json/goes/primary/integral-electrons-1-day.json"
  if period == "3d": url = "https://services.swpc.noaa.gov/json/goes/primary/integral-electrons-3-day.json"
  if period == "7d": url = "https://services.swpc.noaa.gov/json/goes/primary/integral-electrons-7-day.json"

  # Create the error dict if necessary
  if "get_measurement_integral_electrons()" not in error_log:
    error_log["get_measurement_integral_electrons()"] = dict()
    error_log["get_measurement_integral_electrons()"]["urlopen"] = list()
    error_log["get_measurement_integral_electrons()"]["corrupt"] = list()
    error_log["get_measurement_integral_electrons()"]["time_tag"] = list()

  # Update the datestamp list
  error_log["get_measurement_integral_electrons()"]["time_tag"].append(date)

  # Make sure we access the server cleanly
  try:
    with urllib.request.urlopen(url) as thisurl:
      tmp_data = json.loads(thisurl.read().decode())
    error_log["get_measurement_integral_electrons()"]["urlopen"].append(False)
  except Exception as e:
    # If Opening the URL is an issue, then append a False flag for the data corruption since it isn't being tested
    error_log["get_measurement_integral_electrons()"]["urlopen"].append(True)
    error_log["get_measurement_integral_electrons()"]["corrupt"].append(False)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If we cannot even fetch the data, just return what was passed to us....
    return (error_log, data_in)
  
  # Test that the data looks valid before passing
  try:
    if DEBUGLEVEL == "info": print("Example satellite    : %s"%(tmp_data[0]["satellite"]))
    if DEBUGLEVEL == "info": print("Example flux         : %s"%(tmp_data[0]["flux"]))
    if DEBUGLEVEL == "info": print("Example energy       : %s"%(tmp_data[0]["energy"]))
    if DEBUGLEVEL == "info": print("Example time_tag[0]  : %s"%(tmp_data[0]["time_tag"]))
    if DEBUGLEVEL == "info": print("Example time_tag[-1] : %s"%(tmp_data[-1]["time_tag"]))
    if DEBUGLEVEL == "info": print("Total data points: %d"%(len(tmp_data)))
    if DEBUGLEVEL == "info": print("\n")
  
    # If this doesn't throw an exception but doesn't meet these conditions, the data is corrupt
    if (len(tmp_data[0]) is not 4) or (len(tmp_data[-1]) is not 4):
      error_log["get_measurement_integral_electrons()"]["corrupt"].append(True)
      if DEBUGLEVEL == "error": print("Corrupt error:")
      if DEBUGLEVEL == "error": print(tmp_data)
      if DEBUGLEVEL == "error": print("\n")
      return (error_log, data_in)

    # Format this data key
    data["get_measurement_integral_electrons()"] = listOfDicts_to_dictOfLists(tmp_data, DEBUGLEVEL)

    error_log["get_measurement_integral_electrons()"]["corrupt"].append(False)
    return (error_log, data)
  except Exception as e:
    error_log["get_measurement_integral_electrons()"]["corrupt"].append(True)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If the data appears corrupt from some basic tests, return the original data
    return (error_log, data_in)

def get_measurement_integral_protons(period, error_log_in, data_in, date, DEBUGLEVEL):
  # This function calls' error log and data are passed in to be updated, this allows the error handling to "recover" by
  # simply passing back the data that was in the json archive previously, keeping the stored data
  error_log = error_log_in
  # "time_tag"
  # "satellite"
  # "flux"
  # "energy"
  if DEBUGLEVEL != "none": print("get_measurement_integral_protons(%s)"%(period))
  if period == "6h": url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-6-hour.json"
  if period == "1d": url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-1-day.json"
  if period == "3d": url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-3-day.json"
  if period == "7d": url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-7-day.json"

  # Create the error dict if necessary
  if "get_measurement_integral_protons()" not in error_log:
    error_log["get_measurement_integral_protons()"] = dict()
    error_log["get_measurement_integral_protons()"]["urlopen"] = list()
    error_log["get_measurement_integral_protons()"]["corrupt"] = list()
    error_log["get_measurement_integral_protons()"]["time_tag"] = list()

  # Update the datestamp list
  error_log["get_measurement_integral_protons()"]["time_tag"].append(date)

  # Make sure we access the server cleanly
  try:
    with urllib.request.urlopen(url) as thisurl:
      tmp_data = json.loads(thisurl.read().decode())
    error_log["get_measurement_integral_protons()"]["urlopen"].append(False)
  except Exception as e:
    # If Opening the URL is an issue, then append a False flag for the data corruption since it isn't being tested
    error_log["get_measurement_integral_protons()"]["urlopen"].append(True)
    error_log["get_measurement_integral_protons()"]["corrupt"].append(False)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If we cannot even fetch the data, just return what was passed to us....
    return (error_log, data_in)
  
  # Test that the data looks valid before passing
  try:
    if DEBUGLEVEL == "info": print("Example satellite    : %s"%(tmp_data[0]["satellite"]))
    if DEBUGLEVEL == "info": print("Example flux         : %s"%(tmp_data[0]["flux"]))
    if DEBUGLEVEL == "info": print("Example energy       : %s"%(tmp_data[0]["energy"]))
    if DEBUGLEVEL == "info": print("Example time_tag[0]  : %s"%(tmp_data[0]["time_tag"]))
    if DEBUGLEVEL == "info": print("Example time_tag[-1] : %s"%(tmp_data[-1]["time_tag"]))
    if DEBUGLEVEL == "info": print("Total data points: %d"%(len(tmp_data)))
    if DEBUGLEVEL == "info": print("\n")
  
    # If this doesn't throw an exception but doesn't meet these conditions, the data is corrupt
    if (len(tmp_data[0]) is not 4) or (len(tmp_data[-1]) is not 4):
      error_log["get_measurement_integral_protons()"]["corrupt"].append(True)
      if DEBUGLEVEL == "error": print("Corrupt error:")
      if DEBUGLEVEL == "error": print(tmp_data)
      if DEBUGLEVEL == "error": print("\n")
      return (error_log, data_in)

    # Format this data key
    data["get_measurement_integral_protons()"] = listOfDicts_to_dictOfLists(tmp_data, DEBUGLEVEL)

    error_log["get_measurement_integral_protons()"]["corrupt"].append(False)
    return (error_log, data)
  except Exception as e:
    error_log["get_measurement_integral_protons()"]["corrupt"].append(True)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If the data appears corrupt from some basic tests, return the original data
    return (error_log, data_in)

def get_measurement_magnetometers(period, error_log_in, data_in, date, DEBUGLEVEL):
  # This function calls' error log and data are passed in to be updated, this allows the error handling to "recover" by
  # simply passing back the data that was in the json archive previously, keeping the stored data
  error_log = error_log_in
  # "time_tag"
  # "satellite"
  # "He"
  # "Hp"
  # "Hn"
  # "total"
  # "arcjet_flag"
  if DEBUGLEVEL != "none": print("get_measurement_magnetometers(%s)"%(period))
  if period == "6h": url = "https://services.swpc.noaa.gov/json/goes/primary/magnetometers-6-hour.json"
  if period == "1d": url = "https://services.swpc.noaa.gov/json/goes/primary/magnetometers-1-day.json"
  if period == "3d": url = "https://services.swpc.noaa.gov/json/goes/primary/magnetometers-3-day.json"
  if period == "7d": url = "https://services.swpc.noaa.gov/json/goes/primary/magnetometers-7-day.json"

  # Create the error dict if necessary
  if "get_measurement_magnetometers()" not in error_log:
    error_log["get_measurement_magnetometers()"] = dict()
    error_log["get_measurement_magnetometers()"]["urlopen"] = list()
    error_log["get_measurement_magnetometers()"]["corrupt"] = list()
    error_log["get_measurement_magnetometers()"]["time_tag"] = list()

  # Update the datestamp list
  error_log["get_measurement_magnetometers()"]["time_tag"].append(date)

  # Make sure we access the server cleanly
  try:
    with urllib.request.urlopen(url) as thisurl:
      tmp_data = json.loads(thisurl.read().decode())
    error_log["get_measurement_magnetometers()"]["urlopen"].append(False)
  except Exception as e:
    # If Opening the URL is an issue, then append a False flag for the data corruption since it isn't being tested
    error_log["get_measurement_magnetometers()"]["urlopen"].append(True)
    error_log["get_measurement_magnetometers()"]["corrupt"].append(False)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If we cannot even fetch the data, just return what was passed to us....
    return (error_log, data_in)
  
  # Test that the data looks valid before passing
  try:
    if DEBUGLEVEL == "info": print("Example satellite    : %s"%(tmp_data[0]["satellite"]))
    if DEBUGLEVEL == "info": print("Example He           : %s"%(tmp_data[0]["He"]))
    if DEBUGLEVEL == "info": print("Example Hp           : %s"%(tmp_data[0]["Hp"]))
    if DEBUGLEVEL == "info": print("Example Hn           : %s"%(tmp_data[0]["Hn"]))
    if DEBUGLEVEL == "info": print("Example total        : %s"%(tmp_data[0]["total"]))
    if DEBUGLEVEL == "info": print("Example arcjet_flag  : %s"%(tmp_data[0]["arcjet_flag"]))
    if DEBUGLEVEL == "info": print("Example time_tag[0]  : %s"%(tmp_data[0]["time_tag"]))
    if DEBUGLEVEL == "info": print("Example time_tag[-1] : %s"%(tmp_data[-1]["time_tag"]))
    if DEBUGLEVEL == "info": print("Total data points: %d"%(len(tmp_data)))
    if DEBUGLEVEL == "info": print("\n")
  
    # If this doesn't throw an exception but doesn't meet these conditions, the data is corrupt
    if (len(tmp_data[0]) is not 7) or (len(tmp_data[-1]) is not 7):
      error_log["get_measurement_magnetometers()"]["corrupt"].append(True)
      if DEBUGLEVEL == "error": print("Corrupt error:")
      if DEBUGLEVEL == "error": print(tmp_data)
      if DEBUGLEVEL == "error": print("\n")
      return (error_log, data_in)

    # Format this data key
    data["get_measurement_magnetometers()"] = listOfDicts_to_dictOfLists(tmp_data, DEBUGLEVEL)

    error_log["get_measurement_magnetometers()"]["corrupt"].append(False)
    return (error_log, data)
  except Exception as e:
    error_log["get_measurement_magnetometers()"]["corrupt"].append(True)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If the data appears corrupt from some basic tests, return the original data
    return (error_log, data_in)

def get_measurement_xrays(period, error_log_in, data_in, date, DEBUGLEVEL):
  # This function calls' error log and data are passed in to be updated, this allows the error handling to "recover" by
  # simply passing back the data that was in the json archive previously, keeping the stored data
  error_log = error_log_in
  # "time_tag"
  # "satellite"
  # "flux"
  # "energy"
  if DEBUGLEVEL != "none": print("get_measurement_xrays(%s)"%(period))
  if period == "6h": url = "https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json"
  if period == "1d": url = "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"
  if period == "3d": url = "https://services.swpc.noaa.gov/json/goes/primary/xrays-3-day.json"
  if period == "7d": url = "https://services.swpc.noaa.gov/json/goes/primary/xrays-7-day.json"

  # Create the error dict if necessary
  if "get_measurement_xrays()" not in error_log:
    error_log["get_measurement_xrays()"] = dict()
    error_log["get_measurement_xrays()"]["urlopen"] = list()
    error_log["get_measurement_xrays()"]["corrupt"] = list()
    error_log["get_measurement_xrays()"]["time_tag"] = list()

  # Update the datestamp list
  error_log["get_measurement_xrays()"]["time_tag"].append(date)

  # Make sure we access the server cleanly
  try:
    with urllib.request.urlopen(url) as thisurl:
      tmp_data = json.loads(thisurl.read().decode())
    error_log["get_measurement_xrays()"]["urlopen"].append(False)
  except Exception as e:
    # If Opening the URL is an issue, then append a False flag for the data corruption since it isn't being tested
    error_log["get_measurement_xrays()"]["urlopen"].append(True)
    error_log["get_measurement_xrays()"]["corrupt"].append(False)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If we cannot even fetch the data, just return what was passed to us....
    return (error_log, data_in)
  
  # Test that the data looks valid before passing
  try:
    if DEBUGLEVEL == "info": print("Example satellite    : %s"%(tmp_data[0]["satellite"]))
    if DEBUGLEVEL == "info": print("Example flux         : %s"%(tmp_data[0]["flux"]))
    if DEBUGLEVEL == "info": print("Example energy       : %s"%(tmp_data[0]["energy"]))
    if DEBUGLEVEL == "info": print("Example time_tag[0]  : %s"%(tmp_data[0]["time_tag"]))
    if DEBUGLEVEL == "info": print("Example time_tag[-1] : %s"%(tmp_data[-1]["time_tag"]))
    if DEBUGLEVEL == "info": print("Total data points: %d"%(len(tmp_data)))
    if DEBUGLEVEL == "info": print("\n")

    # If this doesn't throw an exception but doesn't meet these conditions, the data is corrupt
    if (len(tmp_data[0]) is not 4) or (len(tmp_data[-1]) is not 4):
      error_log["get_measurement_xrays()"]["corrupt"].append(True)
      if DEBUGLEVEL == "error": print("Corrupt error:")
      if DEBUGLEVEL == "error": print(tmp_data)
      if DEBUGLEVEL == "error": print("\n")
      return (error_log, data_in)

    # Format this data key
    data["get_measurement_xrays()"] = listOfDicts_to_dictOfLists(tmp_data, DEBUGLEVEL)

    error_log["get_measurement_xrays()"]["corrupt"].append(False)
    return (error_log, data)
  except Exception as e:
    error_log["get_measurement_xrays()"]["corrupt"].append(True)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If the data appears corrupt from some basic tests, return the original data
    return (error_log, data_in)

###############################################################################
# The Sun Itself
###############################################################################
def get_solar_regions(error_log_in, data_in, date, DEBUGLEVEL):
  # This function calls' error log and data are passed in to be updated, this allows the error handling to "recover" by
  # simply passing back the data that was in the json archive previously, keeping the stored data
  error_log = error_log_in
  # observed_date
  # region
  # latitude
  # longitude
  # location
  # carrington_longitude
  # old_carrington_longitude
  # area
  # spot_class
  # extent
  # number_spots
  # mag_class
  # mag_string
  # status
  # c_xray_events
  # m_xray_events
  # x_xray_events
  # proton_events
  # s_flares
  # impulse_flares_1
  # impulse_flares_2
  # impulse_flares_3
  # impulse_flares_4
  # protons
  # c_flare_probability
  # m_flare_probability
  # x_flare_probability
  # proton_probability
  # first_date
  if DEBUGLEVEL != "none": print("get_solar_regions()")
  url = "https://services.swpc.noaa.gov/json/solar_regions.json"
  
  # Create the error dict if necessary
  if "get_solar_regions()" not in error_log:
    error_log["get_solar_regions()"] = dict()
    error_log["get_solar_regions()"]["urlopen"] = list()
    error_log["get_solar_regions()"]["corrupt"] = list()
    error_log["get_solar_regions()"]["time_tag"] = list()

  # Update the datestamp list
  error_log["get_solar_regions()"]["time_tag"].append(date)

  # Make sure we access the server cleanly
  try:
    with urllib.request.urlopen(url) as thisurl:
      tmp_data = json.loads(thisurl.read().decode())
    error_log["get_solar_regions()"]["urlopen"].append(False)
  except Exception as e:
    # If Opening the URL is an issue, then append a False flag for the data corruption since it isn't being tested
    error_log["get_solar_regions()"]["urlopen"].append(True)
    error_log["get_solar_regions()"]["corrupt"].append(False)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If we cannot even fetch the data, just return what was passed to us....
    return (error_log, data_in)

  # Test that the data looks valid before passing
  try:
    if DEBUGLEVEL == "info": print("Example region                  : %s"%(tmp_data[0]["region"]))
    if DEBUGLEVEL == "info": print("Example latitude                : %s"%(tmp_data[0]["latitude"]))
    if DEBUGLEVEL == "info": print("Example longitude               : %s"%(tmp_data[0]["longitude"]))
    if DEBUGLEVEL == "info": print("Example location                : %s"%(tmp_data[0]["location"]))
    if DEBUGLEVEL == "info": print("Example carrington_longitude    : %s"%(tmp_data[0]["carrington_longitude"]))
    if DEBUGLEVEL == "info": print("Example old_carrington_longitude: %s"%(tmp_data[0]["old_carrington_longitude"]))
    if DEBUGLEVEL == "info": print("Example area                    : %s"%(tmp_data[0]["area"]))
    if DEBUGLEVEL == "info": print("Example spot_class              : %s"%(tmp_data[0]["spot_class"]))
    if DEBUGLEVEL == "info": print("Example extent                  : %s"%(tmp_data[0]["extent"]))
    if DEBUGLEVEL == "info": print("Example number_spots            : %s"%(tmp_data[0]["number_spots"]))
    if DEBUGLEVEL == "info": print("Example mag_class               : %s"%(tmp_data[0]["mag_class"]))
    if DEBUGLEVEL == "info": print("Example mag_string              : %s"%(tmp_data[0]["mag_string"]))
    if DEBUGLEVEL == "info": print("Example status                  : %s"%(tmp_data[0]["status"]))
    if DEBUGLEVEL == "info": print("Example c_xray_events           : %s"%(tmp_data[0]["c_xray_events"]))
    if DEBUGLEVEL == "info": print("Example m_xray_events           : %s"%(tmp_data[0]["m_xray_events"]))
    if DEBUGLEVEL == "info": print("Example x_xray_events           : %s"%(tmp_data[0]["x_xray_events"]))
    if DEBUGLEVEL == "info": print("Example proton_events           : %s"%(tmp_data[0]["proton_events"]))
    if DEBUGLEVEL == "info": print("Example s_flares                : %s"%(tmp_data[0]["s_flares"]))
    if DEBUGLEVEL == "info": print("Example impulse_flares_1        : %s"%(tmp_data[0]["impulse_flares_1"]))
    if DEBUGLEVEL == "info": print("Example impulse_flares_2        : %s"%(tmp_data[0]["impulse_flares_2"]))
    if DEBUGLEVEL == "info": print("Example impulse_flares_3        : %s"%(tmp_data[0]["impulse_flares_3"]))
    if DEBUGLEVEL == "info": print("Example impulse_flares_4        : %s"%(tmp_data[0]["impulse_flares_4"]))
    if DEBUGLEVEL == "info": print("Example protons                 : %s"%(tmp_data[0]["protons"]))
    if DEBUGLEVEL == "info": print("Example c_flare_probability     : %s"%(tmp_data[0]["c_flare_probability"]))
    if DEBUGLEVEL == "info": print("Example m_flare_probability     : %s"%(tmp_data[0]["m_flare_probability"]))
    if DEBUGLEVEL == "info": print("Example x_flare_probability     : %s"%(tmp_data[0]["x_flare_probability"]))
    if DEBUGLEVEL == "info": print("Example proton_probability      : %s"%(tmp_data[0]["proton_probability"]))
    if DEBUGLEVEL == "info": print("Example first_date              : %s"%(tmp_data[0]["first_date"]))
    if DEBUGLEVEL == "info": print("Example observed_date[0]        : %s"%(tmp_data[0]["observed_date"]))
    if DEBUGLEVEL == "info": print("Example observed_date[-1]       : %s"%(tmp_data[-1]["observed_date"]))
    if DEBUGLEVEL == "info": print("Total data points               : %d"%(len(tmp_data)))
    if DEBUGLEVEL == "info": print("\n")
  
    # If this doesn't throw an exception but doesn't meet these conditions, the data is corrupt
    if (len(tmp_data[0]) is not 29) or (len(tmp_data[-1]) is not 29):
      error_log["get_solar_regions()"]["corrupt"].append(True)
      if DEBUGLEVEL == "error": print("Corrupt error:")
      if DEBUGLEVEL == "error": print(tmp_data)
      if DEBUGLEVEL == "error": print("\n")
      return (error_log, data_in)

    # Format this data key
    data["get_solar_regions()"] = listOfDicts_to_dictOfLists(tmp_data, DEBUGLEVEL)

    error_log["get_solar_regions()"]["corrupt"].append(False)
    return (error_log, data)
  except Exception as e:
    error_log["get_solar_regions()"]["corrupt"].append(True)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If the data appears corrupt from some basic tests, return the original data
    return (error_log, data_in)

def get_sunspot_report(error_log_in, data_in, date, DEBUGLEVEL):
  # This function calls' error log and data are passed in to be updated, this allows the error handling to "recover" by
  # simply passing back the data that was in the json archive previously, keeping the stored data
  error_log = error_log_in
  # "time_tag":"2020-05-01T05:50:00"
  # "Obsdate":"2020-05-01T00:00:00"
  # "Obstime":"0550"
  # "Station":16320
  # "Observatory":"SVI"
  # "Type":"spt"
  # "Quality":3
  # "Region":2760
  # "Latitude":-8
  # "Report_Longitude":-32
  # "Longitude":-43
  # "Report_Location":"S08W32"
  # "Location":"S08W43"
  # "Carlon":305
  # "Extent":3
  # "Area":0
  # "Numspot":2
  # "Zurich":2
  # "Penumbra":0
  # "Compact":2
  # "Spotclass":"Bxo"
  # "Magcode":2
  # "Magclass":"B"
  # "Obsid":6
  # "Report_Status":2
  # "ValidSpotClass":1}#
  if DEBUGLEVEL != "none": print("get_sunspot_report()")
  url = "https://services.swpc.noaa.gov/json/sunspot_report.json"
  
  # Create the error dict if necessary
  if "get_sunspot_report()" not in error_log:
    error_log["get_sunspot_report()"] = dict()
    error_log["get_sunspot_report()"]["urlopen"] = list()
    error_log["get_sunspot_report()"]["corrupt"] = list()
    error_log["get_sunspot_report()"]["time_tag"] = list()

  # Update the datestamp list
  error_log["get_sunspot_report()"]["time_tag"].append(date)

  # Make sure we access the server cleanly
  try:
    with urllib.request.urlopen(url) as thisurl:
      tmp_data = json.loads(thisurl.read().decode())
    error_log["get_sunspot_report()"]["urlopen"].append(False)
  except Exception as e:
    # If Opening the URL is an issue, then append a False flag for the data corruption since it isn't being tested
    error_log["get_sunspot_report()"]["urlopen"].append(True)
    error_log["get_sunspot_report()"]["corrupt"].append(False)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If we cannot even fetch the data, just return what was passed to us....
    return (error_log, data_in)

  # Test that the data looks valid before passing
  try:
    if DEBUGLEVEL == "info": print("Example Obsdate          : %s"%(tmp_data[0]["Obsdate"]))
    if DEBUGLEVEL == "info": print("Example Obstime          : %s"%(tmp_data[0]["Obstime"]))
    if DEBUGLEVEL == "info": print("Example Station          : %s"%(tmp_data[0]["Station"]))
    if DEBUGLEVEL == "info": print("Example Observatory      : %s"%(tmp_data[0]["Observatory"]))
    if DEBUGLEVEL == "info": print("Example Type             : %s"%(tmp_data[0]["Type"]))
    if DEBUGLEVEL == "info": print("Example Quality          : %s"%(tmp_data[0]["Quality"]))
    if DEBUGLEVEL == "info": print("Example Region           : %s"%(tmp_data[0]["Region"]))
    if DEBUGLEVEL == "info": print("Example Latitude         : %s"%(tmp_data[0]["Latitude"]))
    if DEBUGLEVEL == "info": print("Example Report_Longitude : %s"%(tmp_data[0]["Report_Longitude"]))
    if DEBUGLEVEL == "info": print("Example Longitude        : %s"%(tmp_data[0]["Longitude"]))
    if DEBUGLEVEL == "info": print("Example Report_Location  : %s"%(tmp_data[0]["Report_Location"]))
    if DEBUGLEVEL == "info": print("Example Location         : %s"%(tmp_data[0]["Location"]))
    if DEBUGLEVEL == "info": print("Example Carlon           : %s"%(tmp_data[0]["Carlon"]))
    if DEBUGLEVEL == "info": print("Example Extent           : %s"%(tmp_data[0]["Extent"]))
    if DEBUGLEVEL == "info": print("Example Area             : %s"%(tmp_data[0]["Area"]))
    if DEBUGLEVEL == "info": print("Example Numspot          : %s"%(tmp_data[0]["Numspot"]))
    if DEBUGLEVEL == "info": print("Example Zurich           : %s"%(tmp_data[0]["Zurich"]))
    if DEBUGLEVEL == "info": print("Example Penumbra         : %s"%(tmp_data[0]["Penumbra"]))
    if DEBUGLEVEL == "info": print("Example Compact          : %s"%(tmp_data[0]["Compact"]))
    if DEBUGLEVEL == "info": print("Example Spotclass        : %s"%(tmp_data[0]["Spotclass"]))
    if DEBUGLEVEL == "info": print("Example Magcode          : %s"%(tmp_data[0]["Magcode"]))
    if DEBUGLEVEL == "info": print("Example Magclass         : %s"%(tmp_data[0]["Magclass"]))
    if DEBUGLEVEL == "info": print("Example Obsid            : %s"%(tmp_data[0]["Obsid"]))
    if DEBUGLEVEL == "info": print("Example Report_Status    : %s"%(tmp_data[0]["Report_Status"]))
    if DEBUGLEVEL == "info": print("Example ValidSpotClass   : %s"%(tmp_data[0]["ValidSpotClass"]))
    if DEBUGLEVEL == "info": print("Example time_tag[0]      : %s"%(tmp_data[0]["time_tag"]))
    if DEBUGLEVEL == "info": print("Example time_tag[-1]     : %s"%(tmp_data[-1]["time_tag"]))
    if DEBUGLEVEL == "info": print("Total data points        : %d"%(len(tmp_data)))
    if DEBUGLEVEL == "info": print("\n")
  
    # If this doesn't throw an exception but doesn't meet these conditions, the data is corrupt
    if (len(tmp_data[0]) is not 26) or (len(tmp_data[-1]) is not 26):
      error_log["get_sunspot_report()"]["corrupt"].append(True)
      if DEBUGLEVEL == "error": print("Corrupt error:")
      if DEBUGLEVEL == "error": print(tmp_data)
      if DEBUGLEVEL == "error": print("\n")
      return (error_log, data_in)

    # Format this data key
    data["get_sunspot_report()"] = listOfDicts_to_dictOfLists(tmp_data, DEBUGLEVEL)

    error_log["get_sunspot_report()"]["corrupt"].append(False)
    return (error_log, data)
  except Exception as e:
    error_log["get_sunspot_report()"]["corrupt"].append(True)
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    # If the data appears corrupt from some basic tests, return the original data
    return (error_log, data_in)

###############################################################################
# Support Functions
###############################################################################
def listOfDicts_to_dictOfLists(dataI, DEBUGLEVEL):
  # The purpose of this function is directly tied to the returned data from the NOAA servers
  # The data from NOAA is a list of dictionaries, where one element in the list is a specific
  # sample point, and the list is the set of samples. This is somewhat annoyingly formatted
  # as it would make more sense to return a dictionary of lists instead which is why it is
  # being reformatted here.
  if DEBUGLEVEL != "none": print("listOfDicts_to_dictOfLists()")
  dataO = dict()
  try:
    for sample in dataI:
      for key, value in sample.items():
        if key not in dataO:
          dataO[key] = list()
        dataO[key].append(value)
  except Exception as e:
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")

  if DEBUGLEVEL == "info":
    for key, value in dataO.items():
      print("Example dictionary list of key [%s]: %s"%(key,dataO[key]))

  return dataO

###############################################################################
# File Accesses
###############################################################################
def fetch_archive(file_to_read, DEBUGLEVEL):
  if DEBUGLEVEL != "none": print("fetch_archive()")
  try:
    with open(file_to_read, 'r') as fh:
      data = json.load(fh)
  except Exception as e:
    if DEBUGLEVEL: print("No file %s detected, returning empty dictionary"%(file_to_read))
    if DEBUGLEVEL == "error": print("Exception:")
    if DEBUGLEVEL == "error": print(e)
    if DEBUGLEVEL == "error": print("\n")
    data = dict()
  return data

def store_archive(file_to_write, data, DEBUGLEVEL):
  if DEBUGLEVEL != "none": print("store_archive()")
  with open(file_to_write, 'w') as fh:
    if DEBUGLEVEL == "info": print("Storing to file %s"%(file_to_write))
    json.dump(data, fh)

###############################################################################
# MAIN
###############################################################################
if __name__ == "__main__":
  # Get the current sample datestamp for errors
  now = str(datetime.datetime.now())

  # Pull in the config file or create it if it doesn't exist
  try:
    import fetch_summary_config
  except:
    print("User config file not present, creating...")
    with open("fetch_summary_config.py", "w") as fh:
      fh.write("# none, info, error\n")
      fh.write("DEBUGLEVEL           = \"none\"\n")
      fh.write("ENFILEWRITES         = True\n")
      fh.write("RECORDERRORS         = True\n")
      fh.write("ENINDICESkp          = True\n")
      fh.write("ENINDICESk           = True\n")
      fh.write("ENWEATHERMEASURESd6e = True\n")
      fh.write("ENWEATHERMEASURESd1e = False\n")
      fh.write("ENWEATHERMEASURESd3e = False\n")
      fh.write("ENWEATHERMEASURESd7e = False\n")
      fh.write("ENWEATHERMEASURESd6p = True\n")
      fh.write("ENWEATHERMEASURESd1p = False\n")
      fh.write("ENWEATHERMEASURESd3p = False\n")
      fh.write("ENWEATHERMEASURESd7p = False\n")
      fh.write("ENWEATHERMEASURESi6e = True\n")
      fh.write("ENWEATHERMEASURESi1e = False\n")
      fh.write("ENWEATHERMEASURESi3e = False\n")
      fh.write("ENWEATHERMEASURESi7e = False\n")
      fh.write("ENWEATHERMEASURESi6p = True\n")
      fh.write("ENWEATHERMEASURESi1p = False\n")
      fh.write("ENWEATHERMEASURESi3p = False\n")
      fh.write("ENWEATHERMEASURESi7p = False\n")
      fh.write("ENWEATHERMEASURES6m  = True\n")
      fh.write("ENWEATHERMEASURES1m  = False\n")
      fh.write("ENWEATHERMEASURES3m  = False\n")
      fh.write("ENWEATHERMEASURES7m  = False\n")
      fh.write("ENWEATHERMEASURES6x  = True\n")
      fh.write("ENWEATHERMEASURES1x  = False\n")
      fh.write("ENWEATHERMEASURES3x  = False\n")
      fh.write("ENWEATHERMEASURES7x  = False\n")
      fh.write("ENSUNMEASURES        = True\n")
    import fetch_summary_config

  # Fetch the current data and error log
  if fetch_summary_config.ENFILEWRITES:         data = fetch_archive('data.json', fetch_summary_config.DEBUGLEVEL)
  if fetch_summary_config.RECORDERRORS:         error_log = fetch_archive('errors.json', fetch_summary_config.DEBUGLEVEL)

  # New Data and Error Collection Framework
  # Collect the Data and Errors, if the previous run was logging a type of data and the current run does not contain
  # that type of data, remove it from the error log as it has persistence
  if fetch_summary_config.ENINDICESkp:          # Catch the data and the error log
                           all_info                                           = get_kp_index_1m(error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.RECORDERRORS:       # Strip the data and error log if this data type is no longer being sampled
                           data.pop("get_kp_index_1m()", None)
                           error_log.pop("get_kp_index_1m()", None)

  if fetch_summary_config.ENINDICESk:           # Catch the data and the error log
                           all_info                                           = get_k_index_1m(error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.RECORDERRORS:       # Strip the data and error log if this data type is no longer being sampled
                           data.pop("get_k_index_1m()", None)
                           error_log.pop("get_k_index_1m()", None)

  if fetch_summary_config.ENWEATHERMEASURESd6e: # Catch the data and the error log
                           all_info                                           = get_measurement_differential_electrons("6h", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURESd1e: # Catch the data and the error log
                           all_info                                           = get_measurement_differential_electrons("1d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURESd3e: # Catch the data and the error log
                           all_info                                           = get_measurement_differential_electrons("3d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURESd7e: # Catch the data and the error log
                           all_info                                           = get_measurement_differential_electrons("7d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.RECORDERRORS:       # Strip the data and error log if this data type is no longer being sampled
                           data.pop("get_measurement_differential_electrons()", None)
                           error_log.pop("get_measurement_differential_electrons()", None)

  if fetch_summary_config.ENWEATHERMEASURESd6p: # Catch the data and the error log
                           all_info                                           = get_measurement_differential_protons("6h", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURESd1p: # Catch the data and the error log
                           all_info                                           = get_measurement_differential_protons("1d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURESd3p: # Catch the data and the error log
                           all_info                                           = get_measurement_differential_protons("3d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURESd7p: # Catch the data and the error log
                           all_info                                           = get_measurement_differential_protons("7d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.RECORDERRORS:       # Strip the data and error log if this data type is no longer being sampled
                           data.pop("get_measurement_differential_protons()", None)
                           error_log.pop("get_measurement_differential_protons()", None)

  if fetch_summary_config.ENWEATHERMEASURESi6e: # Catch the data and the error log
                           all_info                                           = get_measurement_integral_electrons("6h", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURESi1e: # Catch the data and the error log
                           all_info                                           = get_measurement_integral_electrons("1d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURESi3e: # Catch the data and the error log
                           all_info                                           = get_measurement_integral_electrons("3d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURESi7e: # Catch the data and the error log
                           all_info                                           = get_measurement_integral_electrons("7d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.RECORDERRORS:       # Strip the data and error log if this data type is no longer being sampled
                           data.pop("get_measurement_integral_electrons()", None)
                           error_log.pop("get_measurement_integral_electrons()", None)

  if fetch_summary_config.ENWEATHERMEASURESi6p: # Catch the data and the error log
                           all_info                                           = get_measurement_integral_protons("6h", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURESi1p: # Catch the data and the error log
                           all_info                                           = get_measurement_integral_protons("1d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURESi3p: # Catch the data and the error log
                           all_info                                           = get_measurement_integral_protons("3d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURESi7p: # Catch the data and the error log
                           all_info                                           = get_measurement_integral_protons("7d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.RECORDERRORS:       # Strip the data and error log if this data type is no longer being sampled
                           data.pop("get_measurement_integral_protons()", None)
                           error_log.pop("get_measurement_integral_protons()", None)

  if fetch_summary_config.ENWEATHERMEASURES6m: # Catch the data and the error log
                           all_info                                           = get_measurement_magnetometers("6h", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURES1m: # Catch the data and the error log
                           all_info                                           = get_measurement_magnetometers("1d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURES3m: # Catch the data and the error log
                           all_info                                           = get_measurement_magnetometers("3d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURES7m: # Catch the data and the error log
                           all_info                                           = get_measurement_magnetometers("7d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.RECORDERRORS:       # Strip the data and error log if this data type is no longer being sampled
                           data.pop("get_measurement_magnetometers()", None)
                           error_log.pop("get_measurement_magnetometers()", None)

  if fetch_summary_config.ENWEATHERMEASURES6x: # Catch the data and the error log
                           all_info                                           = get_measurement_xrays("6h", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURES1x: # Catch the data and the error log
                           all_info                                           = get_measurement_xrays("1d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURES3x: # Catch the data and the error log
                           all_info                                           = get_measurement_xrays("3d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.ENWEATHERMEASURES7x: # Catch the data and the error log
                           all_info                                           = get_measurement_xrays("7d", error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.RECORDERRORS:       # Strip the data and error log if this data type is no longer being sampled
                           data.pop("get_measurement_xrays()", None)
                           error_log.pop("get_measurement_xrays()", None)

  if fetch_summary_config.ENSUNMEASURES: # Catch the data and the error log
                           all_info                                           = get_solar_regions(error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.RECORDERRORS:       # Strip the data and error log if this data type is no longer being sampled
                           data.pop("get_solar_regions()", None)
                           error_log.pop("get_solar_regions()", None)

  if fetch_summary_config.ENSUNMEASURES: # Catch the data and the error log
                           all_info                                           = get_sunspot_report(error_log, data, now, fetch_summary_config.DEBUGLEVEL)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif fetch_summary_config.RECORDERRORS:       # Strip the data and error log if this data type is no longer being sampled
                           data.pop("get_sunspot_report()", None)
                           error_log.pop("get_sunspot_report()", None)

  # Store the updated data and error_log
  if fetch_summary_config.ENFILEWRITES:         store_archive('data.json', data, fetch_summary_config.DEBUGLEVEL)
  if fetch_summary_config.RECORDERRORS:         store_archive('errors.json', error_log, fetch_summary_config.DEBUGLEVEL)
