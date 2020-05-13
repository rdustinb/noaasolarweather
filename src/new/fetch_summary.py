import urllib.request, json

global DEBUG

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
# Solar Weather Indices
###############################################################################
def get_kp_index_1m():
  # Get the Kp Index
  if DEBUG: print("get_kp_index_1m()")
  url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
  
  with urllib.request.urlopen(url) as thisurl:
    data = json.loads(thisurl.read().decode())
  
  if DEBUG: print("Example kp_index:         %s"%(data[0]["kp_index"]))
  if DEBUG: print("Example time_tag[0]:      %s"%(data[0]["time_tag"]))
  if DEBUG: print("Example time_tag[-1]:     %s"%(data[-1]["time_tag"]))
  if DEBUG: print("Total data points: %d"%(len(data)))
  if DEBUG: print("\n")
  
  return data # This is an array of dictionaries

def get_k_index_1m():
  # Get the Boulder K Index
  if DEBUG: print("get_k_index_1m()")
  url = "https://services.swpc.noaa.gov/json/boulder_k_index_1m.json"

  with urllib.request.urlopen(url) as thisurl:
    data = json.loads(thisurl.read().decode())
  
  if DEBUG: print("Example k_index:          %s"%(data[0]["k_index"]))
  if DEBUG: print("Example time_tag[0]:      %s"%(data[0]["time_tag"]))
  if DEBUG: print("Example time_tag[-1]:     %s"%(data[-1]["time_tag"]))
  if DEBUG: print("Total data points: %d"%(len(data)))
  if DEBUG: print("\n")
  
  return data # This is an array of dictionaries

###############################################################################
# Solar Weather Measurements
###############################################################################
def get_measurement_differential_electrons(period):
  # "time_tag"
  # "satellite"
  # "flux"
  # "energy"
  if DEBUG: print("get_measurement_differential_electrons(%s)"%(period))
  if period == "6h": url = "https://services.swpc.noaa.gov/json/goes/primary/differential-electrons-6-hour.json"
  if period == "1d": url = "https://services.swpc.noaa.gov/json/goes/primary/differential-electrons-1-day.json"
  if period == "3d": url = "https://services.swpc.noaa.gov/json/goes/primary/differential-electrons-3-day.json"
  if period == "7d": url = "https://services.swpc.noaa.gov/json/goes/primary/differential-electrons-7-day.json"

  with urllib.request.urlopen(url) as thisurl:
    data = json.loads(thisurl.read().decode())
  
  if DEBUG: print("Example satellite    : %s"%(data[0]["satellite"]))
  if DEBUG: print("Example flux         : %s"%(data[0]["flux"]))
  if DEBUG: print("Example energy       : %s"%(data[0]["energy"]))
  if DEBUG: print("Example time_tag[0]  : %s"%(data[0]["time_tag"]))
  if DEBUG: print("Example time_tag[-1] : %s"%(data[-1]["time_tag"]))
  if DEBUG: print("\n")
  
  return data # This is an array of dictionaries

def get_measurement_differential_protons(period):
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

  with urllib.request.urlopen(url) as thisurl:
    data = json.loads(thisurl.read().decode())
  
  if DEBUG: print("Example satellite    : %s"%(data[0]["satellite"]))
  if DEBUG: print("Example flux         : %s"%(data[0]["flux"]))
  if DEBUG: print("Example energy       : %s"%(data[0]["energy"]))
  if DEBUG: print("Example yaw_flip     : %s"%(data[0]["yaw_flip"]))
  if DEBUG: print("Example channel      : %s"%(data[0]["channel"]))
  if DEBUG: print("Example time_tag[0]  : %s"%(data[0]["time_tag"]))
  if DEBUG: print("Example time_tag[-1] : %s"%(data[-1]["time_tag"]))
  if DEBUG: print("\n")
  
  return data # This is an array of dictionaries

def get_measurement_integral_electrons(period):
  # "time_tag"
  # "satellite"
  # "flux"
  # "energy"
  if DEBUG: print("get_measurement_integral_electrons(%s)"%(period))
  if period == "6h": url = "https://services.swpc.noaa.gov/json/goes/primary/integral-electrons-6-hour.json"
  if period == "1d": url = "https://services.swpc.noaa.gov/json/goes/primary/integral-electrons-1-day.json"
  if period == "3d": url = "https://services.swpc.noaa.gov/json/goes/primary/integral-electrons-3-day.json"
  if period == "7d": url = "https://services.swpc.noaa.gov/json/goes/primary/integral-electrons-7-day.json"

  with urllib.request.urlopen(url) as thisurl:
    data = json.loads(thisurl.read().decode())
  
  if DEBUG: print("Example satellite    : %s"%(data[0]["satellite"]))
  if DEBUG: print("Example flux         : %s"%(data[0]["flux"]))
  if DEBUG: print("Example energy       : %s"%(data[0]["energy"]))
  if DEBUG: print("Example time_tag[0]  : %s"%(data[0]["time_tag"]))
  if DEBUG: print("Example time_tag[-1] : %s"%(data[-1]["time_tag"]))
  if DEBUG: print("\n")
  
  return data # This is an array of dictionaries

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

# Support Functions
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

if __name__ == "__main__":
  data = dict()

  DEBUG                = False
  ENFILEWRITES         = True

  # Determine what data to collect
  ENINDICES            = True
  ENWEATHERMEASURESd6e = True
  ENWEATHERMEASURESd1e = False
  ENWEATHERMEASURESd3e = False
  ENWEATHERMEASURESd7e = False
  ENWEATHERMEASURESd6p = True
  ENWEATHERMEASURESd1p = False
  ENWEATHERMEASURESd3p = False
  ENWEATHERMEASURESd7p = False
  ENWEATHERMEASURESi6e = True
  ENWEATHERMEASURESi1e = False
  ENWEATHERMEASURESi3e = False
  ENWEATHERMEASURESi7e = False
  ENWEATHERMEASURESi6p = True
  ENWEATHERMEASURESi1p = False
  ENWEATHERMEASURESi3p = False
  ENWEATHERMEASURESi7p = False
  ENWEATHERMEASURES6m  = True
  ENWEATHERMEASURES1m  = False
  ENWEATHERMEASURES3m  = False
  ENWEATHERMEASURES7m  = False
  ENWEATHERMEASURES6x  = True
  ENWEATHERMEASURES1x  = False
  ENWEATHERMEASURES3x  = False
  ENWEATHERMEASURES7x  = False
  ENSUNMEASURES        = True

  # Collect the Data
  if ENINDICES:            data["get_kp_index_1m()"]                          = listOfDicts_to_dictOfLists(get_kp_index_1m())
  if ENINDICES:            data["get_k_index_1m()"]                           = listOfDicts_to_dictOfLists(get_k_index_1m())
  if ENWEATHERMEASURESd6e: data["get_measurement_differential_electrons(6h)"] = listOfDicts_to_dictOfLists(get_measurement_differential_electrons("6h"))
  if ENWEATHERMEASURESd1e: data["get_measurement_differential_electrons(1d)"] = listOfDicts_to_dictOfLists(get_measurement_differential_electrons("1d"))
  if ENWEATHERMEASURESd3e: data["get_measurement_differential_electrons(3d)"] = listOfDicts_to_dictOfLists(get_measurement_differential_electrons("3d"))
  if ENWEATHERMEASURESd7e: data["get_measurement_differential_electrons(7d)"] = listOfDicts_to_dictOfLists(get_measurement_differential_electrons("7d"))
  if ENWEATHERMEASURESd6p: data["get_measurement_differential_protons(6h)"]   = listOfDicts_to_dictOfLists(get_measurement_differential_protons("6h"))
  if ENWEATHERMEASURESd1p: data["get_measurement_differential_protons(1d)"]   = listOfDicts_to_dictOfLists(get_measurement_differential_protons("1d"))
  if ENWEATHERMEASURESd3p: data["get_measurement_differential_protons(3d)"]   = listOfDicts_to_dictOfLists(get_measurement_differential_protons("3d"))
  if ENWEATHERMEASURESd7p: data["get_measurement_differential_protons(7d)"]   = listOfDicts_to_dictOfLists(get_measurement_differential_protons("7d"))
  if ENWEATHERMEASURESi6e: data["get_measurement_integral_electrons(6h)"]     = listOfDicts_to_dictOfLists(get_measurement_integral_electrons("6h"))
  if ENWEATHERMEASURESi1e: data["get_measurement_integral_electrons(1d)"]     = listOfDicts_to_dictOfLists(get_measurement_integral_electrons("1d"))
  if ENWEATHERMEASURESi3e: data["get_measurement_integral_electrons(3d)"]     = listOfDicts_to_dictOfLists(get_measurement_integral_electrons("3d"))
  if ENWEATHERMEASURESi7e: data["get_measurement_integral_electrons(7d)"]     = listOfDicts_to_dictOfLists(get_measurement_integral_electrons("7d"))
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

  # Write to the file, overwrite what is there
  if ENFILEWRITES:
    with open('data.json', 'w') as fh:
      json.dump(data, fh)
