import urllib.request, json, datetime

global DEBUG

# Error Log Structure
#   dict{
#       "sample name as key" : {
#           "time_tag" : [ list of dates that are logged every time this script is called ]
#           "url_failure_flags" : [ list of booleans for whether a data type server access failed ]
#           "corrupt_flags" : [ list of booleans for whether a data type failed corruption tests ]

###############################################################################
###############################################################################
# TODO
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
# 4) Add a "new data" status bit to the JSON archive
#   - The GUI will read to check if the data has been updated by this fetching
#   daemon script.
#   - The GUI will clear the bit once it has updated the graphs.
#   - This bit should not be set if ALL of the data happens to fail to fetch from
#   the error conditions in #1 and #2 above.
###############################################################################
###############################################################################
# Completed
###############################################################################
###############################################################################

###############################################################################
# Solar Weather Indices
###############################################################################
def get_kp_index_1m(error_log_in, data_in, date):
  # This function calls' error log and data are passed in to be updated, this allows the error handling to "recover" by
  # simply passing back the data that was in the json archive previously, keeping the stored data
  error_log = error_log_in
  # Get the Kp Index
  if DEBUG: print("get_kp_index_1m()")
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
  except:
    # If Opening the URL is an issue, then append a False flag for the data corruption since it isn't being tested
    error_log["get_kp_index_1m()"]["urlopen"].append(True)
    error_log["get_kp_index_1m()"]["corrupt"].append(False)
    # If we cannot even fetch the data, just return what was passed to us....
    return (error_log, data_in)
  
  # Test that the data looks valid before passing
  try:
    if DEBUG: print("Example kp_index:         %s"%(tmp_data[0]["kp_index"]))
    if DEBUG: print("Example time_tag[0]:      %s"%(tmp_data[0]["time_tag"]))
    if DEBUG: print("Example time_tag[-1]:     %s"%(tmp_data[-1]["time_tag"]))
    if DEBUG: print("Example data[0]:          %s"%(tmp_data[0]))
    if DEBUG: print("Example data[-1]:         %s"%(tmp_data[-1]))
    if DEBUG: print("Total data points: %d"%(len(tmp_data)))
    if DEBUG: print("\n")

    # If this doesn't throw an exception but doesn't meet these conditions, the data is corrupt
    if (len(tmp_data[0]) is not 2) or (len(tmp_data[-1]) is not 2):
      error_log["get_kp_index_1m()"]["corrupt"].append(True)
      return (error_log, data_in)

    # Format this data key
    data["get_kp_index_1m()"] = listOfDicts_to_dictOfLists(tmp_data)

    error_log["get_kp_index_1m()"]["corrupt"].append(False)
    return (error_log, data)
  except:
    error_log["get_kp_index_1m()"]["corrupt"].append(True)
    # If the data appears corrupt from some basic tests, return the original data
    return (error_log, data_in)

def get_k_index_1m(error_log_in, data_in, date):
  # This function calls' error log and data are passed in to be updated, this allows the error handling to "recover" by
  # simply passing back the data that was in the json archive previously, keeping the stored data
  error_log = error_log_in
  # Get the Boulder K Index
  if DEBUG: print("get_k_index_1m()")
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
  except:
    # If Opening the URL is an issue, then append a False flag for the data corruption since it isn't being tested
    error_log["get_k_index_1m()"]["urlopen"].append(True)
    error_log["get_k_index_1m()"]["corrupt"].append(False)
    # If we cannot even fetch the data, just return what was passed to us....
    return (error_log, data_in)
  
  # Test that the data looks valid before passing
  try:
    if DEBUG: print("Example k_index:          %s"%(tmp_data[0]["k_index"]))
    if DEBUG: print("Example time_tag[0]:      %s"%(tmp_data[0]["time_tag"]))
    if DEBUG: print("Example time_tag[-1]:     %s"%(tmp_data[-1]["time_tag"]))
    if DEBUG: print("Example data[0]:          %s"%(tmp_data[0]))
    if DEBUG: print("Example data[-1]:         %s"%(tmp_data[-1]))
    if DEBUG: print("Length of data[0]:        %d"%(len(tmp_data[0])))
    if DEBUG: print("Total data points: %d"%(len(tmp_data)))
    if DEBUG: print("\n")

    # If this doesn't throw an exception but doesn't meet these conditions, the data is corrupt
    if (len(tmp_data[0]) is not 2) or (len(tmp_data[-1]) is not 2):
      error_log["get_k_index_1m()"]["corrupt"].append(True)
      return (error_log, data_in)

    # Format this data key
    data["get_k_index_1m()"] = listOfDicts_to_dictOfLists(tmp_data)

    error_log["get_k_index_1m()"]["corrupt"].append(False)
    return (error_log, data)
  except:
    error_log["get_k_index_1m()"]["corrupt"].append(True)
    # If the data appears corrupt from some basic tests, return the original data
    return (error_log, data_in)
  
###############################################################################
# Solar Weather Measurements
###############################################################################
def get_measurement_differential_electrons(period, error_log_in, data_in, date):
  # This function calls' error log and data are passed in to be updated, this allows the error handling to "recover" by
  # simply passing back the data that was in the json archive previously, keeping the stored data
  error_log = error_log_in
  # "time_tag"
  # "satellite"
  # "flux"
  # "energy"
  if DEBUG: print("get_measurement_differential_electrons(%s)"%(period))
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
  except:
    # If Opening the URL is an issue, then append a False flag for the data corruption since it isn't being tested
    error_log["get_measurement_differential_electrons()"]["urlopen"].append(True)
    error_log["get_measurement_differential_electrons()"]["corrupt"].append(False)
    # If we cannot even fetch the data, just return what was passed to us....
    return (error_log, data_in)
  
  # Test that the data looks valid before passing
  try:
    if DEBUG: print("Example satellite    : %s"%(tmp_data[0]["satellite"]))
    if DEBUG: print("Example flux         : %s"%(tmp_data[0]["flux"]))
    if DEBUG: print("Example energy       : %s"%(tmp_data[0]["energy"]))
    if DEBUG: print("Example time_tag[0]  : %s"%(tmp_data[0]["time_tag"]))
    if DEBUG: print("Example time_tag[-1] : %s"%(tmp_data[-1]["time_tag"]))
    if DEBUG: print("Total data points: %d"%(len(tmp_data)))
    if DEBUG: print("\n")
  
    # If this doesn't throw an exception but doesn't meet these conditions, the data is corrupt
    if (len(tmp_data[0]) is not 4) or (len(tmp_data[-1]) is not 4):
      error_log["get_measurement_differential_electrons()"]["corrupt"].append(True)
      return (error_log, data_in)

    # Format this data key
    data["get_measurement_differential_electrons()"] = listOfDicts_to_dictOfLists(tmp_data)

    error_log["get_measurement_differential_electrons()"]["corrupt"].append(False)
    return (error_log, data)
  except:
    error_log["get_measurement_differential_electrons()"]["corrupt"].append(True)
    # If the data appears corrupt from some basic tests, return the original data
    return (error_log, data_in)

def get_measurement_differential_protons(period, error_log_in, data_in, date):
  # This function calls' error log and data are passed in to be updated, this allows the error handling to "recover" by
  # simply passing back the data that was in the json archive previously, keeping the stored data
  error_log = error_log_in
  # "time_tag"
  # "satellite"
  # "flux"
  # "energy"
  # "yaw_flip"
  # "channel"
  if DEBUG: print("get_measurement_differential_protons(%s)"%(period))
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
  except:
    # If Opening the URL is an issue, then append a False flag for the data corruption since it isn't being tested
    error_log["get_measurement_differential_protons()"]["urlopen"].append(True)
    error_log["get_measurement_differential_protons()"]["corrupt"].append(False)
    # If we cannot even fetch the data, just return what was passed to us....
    return (error_log, data_in)
  
  # Test that the data looks valid before passing
  try:
    if DEBUG: print("Example satellite    : %s"%(tmp_data[0]["satellite"]))
    if DEBUG: print("Example flux         : %s"%(tmp_data[0]["flux"]))
    if DEBUG: print("Example energy       : %s"%(tmp_data[0]["energy"]))
    if DEBUG: print("Example yaw_flip     : %s"%(tmp_data[0]["yaw_flip"]))
    if DEBUG: print("Example channel      : %s"%(tmp_data[0]["channel"]))
    if DEBUG: print("Example time_tag[0]  : %s"%(tmp_data[0]["time_tag"]))
    if DEBUG: print("Example time_tag[-1] : %s"%(tmp_data[-1]["time_tag"]))
    if DEBUG: print("Total data points: %d"%(len(tmp_data)))
    if DEBUG: print("\n")
  
    # If this doesn't throw an exception but doesn't meet these conditions, the data is corrupt
    if (len(tmp_data[0]) is not 6) or (len(tmp_data[-1]) is not 6):
      error_log["get_measurement_differential_protons()"]["corrupt"].append(True)
      return (error_log, data_in)

    # Format this data key
    data["get_measurement_differential_protons()"] = listOfDicts_to_dictOfLists(tmp_data)

    error_log["get_measurement_differential_protons()"]["corrupt"].append(False)
    return (error_log, data)
  except:
    error_log["get_measurement_differential_protons()"]["corrupt"].append(True)
    # If the data appears corrupt from some basic tests, return the original data
    return (error_log, data_in)

def get_measurement_integral_electrons(period, error_log_in, data_in, date):
  # This function calls' error log and data are passed in to be updated, this allows the error handling to "recover" by
  # simply passing back the data that was in the json archive previously, keeping the stored data
  error_log = error_log_in
  # "time_tag"
  # "satellite"
  # "flux"
  # "energy"
  if DEBUG: print("get_measurement_integral_electrons(%s)"%(period))
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
  except:
    # If Opening the URL is an issue, then append a False flag for the data corruption since it isn't being tested
    error_log["get_measurement_integral_electrons()"]["urlopen"].append(True)
    error_log["get_measurement_integral_electrons()"]["corrupt"].append(False)
    # If we cannot even fetch the data, just return what was passed to us....
    return (error_log, data_in)
  
  # Test that the data looks valid before passing
  try:
    if DEBUG: print("Example satellite    : %s"%(tmp_data[0]["satellite"]))
    if DEBUG: print("Example flux         : %s"%(tmp_data[0]["flux"]))
    if DEBUG: print("Example energy       : %s"%(tmp_data[0]["energy"]))
    if DEBUG: print("Example time_tag[0]  : %s"%(tmp_data[0]["time_tag"]))
    if DEBUG: print("Example time_tag[-1] : %s"%(tmp_data[-1]["time_tag"]))
    if DEBUG: print("Total data points: %d"%(len(tmp_data)))
    if DEBUG: print("\n")
  
    # If this doesn't throw an exception but doesn't meet these conditions, the data is corrupt
    if (len(tmp_data[0]) is not 4) or (len(tmp_data[-1]) is not 4):
      error_log["get_measurement_integral_electrons()"]["corrupt"].append(True)
      return (error_log, data_in)

    # Format this data key
    data["get_measurement_integral_electrons()"] = listOfDicts_to_dictOfLists(tmp_data)

    error_log["get_measurement_integral_electrons()"]["corrupt"].append(False)
    return (error_log, data)
  except:
    error_log["get_measurement_integral_electrons()"]["corrupt"].append(True)
    # If the data appears corrupt from some basic tests, return the original data
    return (error_log, data_in)

def get_measurement_integral_protons(period):
  # "time_tag"
  # "satellite"
  # "flux"
  # "energy"
  if DEBUG: print("get_measurement_integral_protons(%s)"%(period))
  if period == "6h": url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-6-hour.json"
  if period == "1d": url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-1-day.json"
  if period == "3d": url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-3-day.json"
  if period == "7d": url = "https://services.swpc.noaa.gov/json/goes/primary/integral-protons-7-day.json"

  with urllib.request.urlopen(url) as thisurl:
    data = json.loads(thisurl.read().decode())
  
  if DEBUG: print("Example satellite    : %s"%(data[0]["satellite"]))
  if DEBUG: print("Example flux         : %s"%(data[0]["flux"]))
  if DEBUG: print("Example energy       : %s"%(data[0]["energy"]))
  if DEBUG: print("Example time_tag[0]  : %s"%(data[0]["time_tag"]))
  if DEBUG: print("Example time_tag[-1] : %s"%(data[-1]["time_tag"]))
  if DEBUG: print("\n")
  
  return data # This is an array of dictionaries

def get_measurement_magnetometers(period):
  # "time_tag"
  # "satellite"
  # "He"
  # "Hp"
  # "Hn"
  # "total"
  # "arcjet_flag"
  if DEBUG: print("get_measurement_magnetometers(%s)"%(period))
  if period == "6h": url = "https://services.swpc.noaa.gov/json/goes/primary/magnetometers-6-hour.json"
  if period == "1d": url = "https://services.swpc.noaa.gov/json/goes/primary/magnetometers-1-day.json"
  if period == "3d": url = "https://services.swpc.noaa.gov/json/goes/primary/magnetometers-3-day.json"
  if period == "7d": url = "https://services.swpc.noaa.gov/json/goes/primary/magnetometers-7-day.json"

  with urllib.request.urlopen(url) as thisurl:
    data = json.loads(thisurl.read().decode())
  
  if DEBUG: print("Example satellite    : %s"%(data[0]["satellite"]))
  if DEBUG: print("Example He           : %s"%(data[0]["He"]))
  if DEBUG: print("Example Hp           : %s"%(data[0]["Hp"]))
  if DEBUG: print("Example Hn           : %s"%(data[0]["Hn"]))
  if DEBUG: print("Example total        : %s"%(data[0]["total"]))
  if DEBUG: print("Example arcjet_flag  : %s"%(data[0]["arcjet_flag"]))
  if DEBUG: print("Example time_tag[0]  : %s"%(data[0]["time_tag"]))
  if DEBUG: print("Example time_tag[-1] : %s"%(data[-1]["time_tag"]))
  if DEBUG: print("\n")
  
  return data # This is an array of dictionaries

def get_measurement_xrays(period):
  # "time_tag"
  # "satellite"
  # "flux"
  # "energy"
  if DEBUG: print("get_measurement_xrays(%s)"%(period))
  if period == "6h": url = "https://services.swpc.noaa.gov/json/goes/primary/xrays-6-hour.json"
  if period == "1d": url = "https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json"
  if period == "3d": url = "https://services.swpc.noaa.gov/json/goes/primary/xrays-3-day.json"
  if period == "7d": url = "https://services.swpc.noaa.gov/json/goes/primary/xrays-7-day.json"

  with urllib.request.urlopen(url) as thisurl:
    data = json.loads(thisurl.read().decode())
  
  if DEBUG: print("Example satellite    : %s"%(data[0]["satellite"]))
  if DEBUG: print("Example flux         : %s"%(data[0]["flux"]))
  if DEBUG: print("Example energy       : %s"%(data[0]["energy"]))
  if DEBUG: print("Example time_tag[0]  : %s"%(data[0]["time_tag"]))
  if DEBUG: print("Example time_tag[-1] : %s"%(data[-1]["time_tag"]))
  if DEBUG: print("\n")
  
  return data # This is an array of dictionaries

###############################################################################
# The Sun Itself
###############################################################################
def get_solar_regions():
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
  if DEBUG: print("get_solar_regions()")
  url = "https://services.swpc.noaa.gov/json/solar_regions.json"
  
  with urllib.request.urlopen(url) as thisurl:
    data = json.loads(thisurl.read().decode())
  if DEBUG: print("Example region                  : %s"%(data[0]["region"]))
  if DEBUG: print("Example latitude                : %s"%(data[0]["latitude"]))
  if DEBUG: print("Example longitude               : %s"%(data[0]["longitude"]))
  if DEBUG: print("Example location                : %s"%(data[0]["location"]))
  if DEBUG: print("Example carrington_longitude    : %s"%(data[0]["carrington_longitude"]))
  if DEBUG: print("Example old_carrington_longitude: %s"%(data[0]["old_carrington_longitude"]))
  if DEBUG: print("Example area                    : %s"%(data[0]["area"]))
  if DEBUG: print("Example spot_class              : %s"%(data[0]["spot_class"]))
  if DEBUG: print("Example extent                  : %s"%(data[0]["extent"]))
  if DEBUG: print("Example number_spots            : %s"%(data[0]["number_spots"]))
  if DEBUG: print("Example mag_class               : %s"%(data[0]["mag_class"]))
  if DEBUG: print("Example mag_string              : %s"%(data[0]["mag_string"]))
  if DEBUG: print("Example status                  : %s"%(data[0]["status"]))
  if DEBUG: print("Example c_xray_events           : %s"%(data[0]["c_xray_events"]))
  if DEBUG: print("Example m_xray_events           : %s"%(data[0]["m_xray_events"]))
  if DEBUG: print("Example x_xray_events           : %s"%(data[0]["x_xray_events"]))
  if DEBUG: print("Example proton_events           : %s"%(data[0]["proton_events"]))
  if DEBUG: print("Example s_flares                : %s"%(data[0]["s_flares"]))
  if DEBUG: print("Example impulse_flares_1        : %s"%(data[0]["impulse_flares_1"]))
  if DEBUG: print("Example impulse_flares_2        : %s"%(data[0]["impulse_flares_2"]))
  if DEBUG: print("Example impulse_flares_3        : %s"%(data[0]["impulse_flares_3"]))
  if DEBUG: print("Example impulse_flares_4        : %s"%(data[0]["impulse_flares_4"]))
  if DEBUG: print("Example protons                 : %s"%(data[0]["protons"]))
  if DEBUG: print("Example c_flare_probability     : %s"%(data[0]["c_flare_probability"]))
  if DEBUG: print("Example m_flare_probability     : %s"%(data[0]["m_flare_probability"]))
  if DEBUG: print("Example x_flare_probability     : %s"%(data[0]["x_flare_probability"]))
  if DEBUG: print("Example proton_probability      : %s"%(data[0]["proton_probability"]))
  if DEBUG: print("Example first_date              : %s"%(data[0]["first_date"]))
  if DEBUG: print("Example observed_date[0]        : %s"%(data[0]["observed_date"]))
  if DEBUG: print("Example observed_date[-1]       : %s"%(data[-1]["observed_date"]))
  if DEBUG: print("\n")
  
  return data

def get_sunspot_report():
  # Get the Sunspot Report
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
  if DEBUG: print("get_sunspot_report()")
  url = "https://services.swpc.noaa.gov/json/sunspot_report.json"
  
  with urllib.request.urlopen(url) as thisurl:
    data = json.loads(thisurl.read().decode())
  
  if DEBUG: print("Example Obsdate:          %s"%(data[0]["Obsdate"]))
  if DEBUG: print("Example Obstime:          %s"%(data[0]["Obstime"]))
  if DEBUG: print("Example Station:          %s"%(data[0]["Station"]))
  if DEBUG: print("Example Observatory:      %s"%(data[0]["Observatory"]))
  if DEBUG: print("Example Type:             %s"%(data[0]["Type"]))
  if DEBUG: print("Example Quality:          %s"%(data[0]["Quality"]))
  if DEBUG: print("Example Region:           %s"%(data[0]["Region"]))
  if DEBUG: print("Example Latitude:         %s"%(data[0]["Latitude"]))
  if DEBUG: print("Example Report_Longitude: %s"%(data[0]["Report_Longitude"]))
  if DEBUG: print("Example Longitude:        %s"%(data[0]["Longitude"]))
  if DEBUG: print("Example Report_Location:  %s"%(data[0]["Report_Location"]))
  if DEBUG: print("Example Location:         %s"%(data[0]["Location"]))
  if DEBUG: print("Example Carlon:           %s"%(data[0]["Carlon"]))
  if DEBUG: print("Example Extent:           %s"%(data[0]["Extent"]))
  if DEBUG: print("Example Area:             %s"%(data[0]["Area"]))
  if DEBUG: print("Example Numspot:          %s"%(data[0]["Numspot"]))
  if DEBUG: print("Example Zurich:           %s"%(data[0]["Zurich"]))
  if DEBUG: print("Example Penumbra:         %s"%(data[0]["Penumbra"]))
  if DEBUG: print("Example Compact:          %s"%(data[0]["Compact"]))
  if DEBUG: print("Example Spotclass:        %s"%(data[0]["Spotclass"]))
  if DEBUG: print("Example Magcode:          %s"%(data[0]["Magcode"]))
  if DEBUG: print("Example Magclass:         %s"%(data[0]["Magclass"]))
  if DEBUG: print("Example Obsid:            %s"%(data[0]["Obsid"]))
  if DEBUG: print("Example Report_Status:    %s"%(data[0]["Report_Status"]))
  if DEBUG: print("Example ValidSpotClass:   %s"%(data[0]["ValidSpotClass"]))
  if DEBUG: print("Example time_tag[0]:      %s"%(data[0]["time_tag"]))
  if DEBUG: print("Example time_tag[-1]:     %s"%(data[-1]["time_tag"]))
  if DEBUG: print("Total data points: %d"%(len(data)))
  if DEBUG: print("\n")
  
  return data

###############################################################################
# Support Functions
###############################################################################
def listOfDicts_to_dictOfLists(dataI):
  # The purpose of this function is directly tied to the returned data from the NOAA servers
  # The data from NOAA is a list of dictionaries, where one element in the list is a specific
  # sample point, and the list is the set of samples. This is somewhat annoyingly formatted
  # as it would make more sense to return a dictionary of lists instead which is why it is
  # being reformatted here.
  if DEBUG: print("listOfDicts_to_dictOfLists()")
  dataO = dict()
  for sample in dataI:
    for key, value in sample.items():
      if key not in dataO:
        dataO[key] = list()
      dataO[key].append(value)

  if DEBUG:
    for key, value in dataO.items():
      print("Example dictionary list of key [%s]: %s"%(key,dataO[key]))

  return dataO

###############################################################################
# File Accesses
###############################################################################
def fetch_archive(file_to_read):
  try:
    with open(file_to_read, 'r') as fh:
      data = json.load(fh)
  except:
    if DEBUG: print("No file %s detected, returning empty dictionary"%(file_to_read))
    data = dict()
  return data

def store_archive(file_to_write, data):
  with open(file_to_write, 'w') as fh:
    if DEBUG: print("Storing to file %s"%(file_to_write))
    json.dump(data, fh)

###############################################################################
# MAIN
###############################################################################
if __name__ == "__main__":
  # Get the current sample datestamp for errors
  now = str(datetime.datetime.now())

  DEBUG                = True
  ENFILEWRITES         = True
  RECORDERRORS         = True

  #data = dict()

  # Determine what data to collect
  ENINDICESkp          = False
  ENINDICESk           = False
  ENWEATHERMEASURESd6e = False
  ENWEATHERMEASURESd1e = False
  ENWEATHERMEASURESd3e = False
  ENWEATHERMEASURESd7e = False
  ENWEATHERMEASURESd6p = False
  ENWEATHERMEASURESd1p = False
  ENWEATHERMEASURESd3p = False
  ENWEATHERMEASURESd7p = False
  ENWEATHERMEASURESi6e = False
  ENWEATHERMEASURESi1e = False
  ENWEATHERMEASURESi3e = False
  ENWEATHERMEASURESi7e = True
  ENWEATHERMEASURESi6p = False
  ENWEATHERMEASURESi1p = False
  ENWEATHERMEASURESi3p = False
  ENWEATHERMEASURESi7p = False
  ENWEATHERMEASURES6m  = False
  ENWEATHERMEASURES1m  = False
  ENWEATHERMEASURES3m  = False
  ENWEATHERMEASURES7m  = False
  ENWEATHERMEASURES6x  = False
  ENWEATHERMEASURES1x  = False
  ENWEATHERMEASURES3x  = False
  ENWEATHERMEASURES7x  = False
  ENSUNMEASURES        = False

  # Fetch the current data and error log
  if ENFILEWRITES:         data = fetch_archive('data.json')
  if RECORDERRORS:         error_log = fetch_archive('errors.json')

  # New Data and Error Collection Framework
  # Collect the Data and Errors, if the previous run was logging a type of data and the current run does not contain
  # that type of data, remove it from the error log as it has persistence
  if ENINDICESkp:          # Catch the data and the error log
                           all_info                                           = get_kp_index_1m(error_log, data, now)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif RECORDERRORS:       # Strip the data and error log if this data type is no longer being sampled
                           data.pop("get_kp_index_1m()", None)
                           error_log.pop("get_kp_index_1m()", None)

  if ENINDICESk:           # Catch the data and the error log
                           all_info                                           = get_k_index_1m(error_log, data, now)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif RECORDERRORS:       # Strip the data and error log if this data type is no longer being sampled
                           data.pop("get_k_index_1m()", None)
                           error_log.pop("get_k_index_1m()", None)

  if ENWEATHERMEASURESd6e: # Catch the data and the error log
                           all_info                                           = get_measurement_differential_electrons("6h", error_log, data, now)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif ENWEATHERMEASURESd1e: # Catch the data and the error log
                           all_info                                           = get_measurement_differential_electrons("1d", error_log, data, now)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif ENWEATHERMEASURESd3e: # Catch the data and the error log
                           all_info                                           = get_measurement_differential_electrons("3d", error_log, data, now)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif ENWEATHERMEASURESd7e: # Catch the data and the error log
                           all_info                                           = get_measurement_differential_electrons("7d", error_log, data, now)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif RECORDERRORS:       # Strip the data and error log if this data type is no longer being sampled
                           data.pop("get_measurement_differential_electrons()", None)
                           error_log.pop("get_measurement_differential_electrons()", None)

  if ENWEATHERMEASURESd6p: # Catch the data and the error log
                           all_info                                           = get_measurement_differential_protons("6h", error_log, data, now)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif ENWEATHERMEASURESd1p: # Catch the data and the error log
                           all_info                                           = get_measurement_differential_protons("1d", error_log, data, now)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif ENWEATHERMEASURESd3p: # Catch the data and the error log
                           all_info                                           = get_measurement_differential_protons("3d", error_log, data, now)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif ENWEATHERMEASURESd7p: # Catch the data and the error log
                           all_info                                           = get_measurement_differential_protons("7d", error_log, data, now)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif RECORDERRORS:       # Strip the data and error log if this data type is no longer being sampled
                           data.pop("get_measurement_differential_protons()", None)
                           error_log.pop("get_measurement_differential_protons()", None)

  if ENWEATHERMEASURESi6e: # Catch the data and the error log
                           all_info                                           = get_measurement_integral_electrons("6h", error_log, data, now)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif ENWEATHERMEASURESi1e: # Catch the data and the error log
                           all_info                                           = get_measurement_integral_electrons("1d", error_log, data, now)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif ENWEATHERMEASURESi3e: # Catch the data and the error log
                           all_info                                           = get_measurement_integral_electrons("3d", error_log, data, now)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif ENWEATHERMEASURESi7e: # Catch the data and the error log
                           all_info                                           = get_measurement_integral_electrons("7d", error_log, data, now)
                           error_log                                          = all_info[0]
                           data                                               = all_info[1]
  elif RECORDERRORS:       # Strip the data and error log if this data type is no longer being sampled
                           data.pop("get_measurement_integral_electrons()", None)
                           error_log.pop("get_measurement_integral_electrons()", None)

  # Old Data and Error Collection Framework
  if ENWEATHERMEASURESi6p: data["get_measurement_integral_protons(6h)"]       = listOfDicts_to_dictOfLists(get_measurement_integral_protons("6h"))
  if ENWEATHERMEASURESi1p: data["get_measurement_integral_protons(1d)"]       = listOfDicts_to_dictOfLists(get_measurement_integral_protons("1d"))
  if ENWEATHERMEASURESi3p: data["get_measurement_integral_protons(3d)"]       = listOfDicts_to_dictOfLists(get_measurement_integral_protons("3d"))
  if ENWEATHERMEASURESi7p: data["get_measurement_integral_protons(7d)"]       = listOfDicts_to_dictOfLists(get_measurement_integral_protons("7d"))
  if ENWEATHERMEASURES6m:  data["get_measurement_magnetometers(6h)"]          = listOfDicts_to_dictOfLists(get_measurement_magnetometers("6h"))
  if ENWEATHERMEASURES1m:  data["get_measurement_magnetometers(1d)"]          = listOfDicts_to_dictOfLists(get_measurement_magnetometers("1d"))
  if ENWEATHERMEASURES3m:  data["get_measurement_magnetometers(3d)"]          = listOfDicts_to_dictOfLists(get_measurement_magnetometers("3d"))
  if ENWEATHERMEASURES7m:  data["get_measurement_magnetometers(7d)"]          = listOfDicts_to_dictOfLists(get_measurement_magnetometers("7d"))
  if ENWEATHERMEASURES6x:  data["get_measurement_xrays(6h)"]                  = listOfDicts_to_dictOfLists(get_measurement_xrays("6h"))
  if ENWEATHERMEASURES1x:  data["get_measurement_xrays(1d)"]                  = listOfDicts_to_dictOfLists(get_measurement_xrays("1d"))
  if ENWEATHERMEASURES3x:  data["get_measurement_xrays(3d)"]                  = listOfDicts_to_dictOfLists(get_measurement_xrays("3d"))
  if ENWEATHERMEASURES7x:  data["get_measurement_xrays(7d)"]                  = listOfDicts_to_dictOfLists(get_measurement_xrays("7d"))
  if ENSUNMEASURES:        data["get_solar_regions()"]                        = listOfDicts_to_dictOfLists(get_solar_regions())
  if ENSUNMEASURES:        data["get_sunspot_report()"]                       = listOfDicts_to_dictOfLists(get_sunspot_report())

  # Store the updated data and error_log
  if ENFILEWRITES:         store_archive('data.json', data)
  if RECORDERRORS:         store_archive('errors.json', error_log)
