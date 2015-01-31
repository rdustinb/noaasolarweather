#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

import urllib.request
import urllib.error

"""
  Locations of data that I want to capture and eventually graph. This data
  is provided from the GOES and ACE satellites.

  = GOES =
  Energetic Proton Flux
    http://services.swpc.noaa.gov/text/goes-energetic-proton-flux-primary.txt
    http://services.swpc.noaa.gov/text/goes-energetic-proton-flux-secondary.txt
  Geomagnetic Components and Total Field
    http://services.swpc.noaa.gov/text/goes-magnetometer-primary.txt
    http://services.swpc.noaa.gov/text/goes-magnetometer-secondary.txt
  Energetic Particle Flux
    http://services.swpc.noaa.gov/text/goes-magnetospheric-particle-flux-ts1-primary.txt
    http://services.swpc.noaa.gov/text/goes-magnetospheric-particle-flux-ts1-secondary.txt
  Solar Particle and Electron Flux
    http://services.swpc.noaa.gov/text/goes-particle-flux-primary.txt
    http://services.swpc.noaa.gov/text/goes-particle-flux-secondary.txt
  xRay Flux
    http://services.swpc.noaa.gov/text/goes-xray-flux-primary.txt
    http://services.swpc.noaa.gov/text/goes-xray-flux-secondary.txt

  = ACE =
  Differential Electron / Proton Flux
    http://services.swpc.noaa.gov/text/ace-epam.txt
  Solar Isotope Spectrometer
    http://services.swpc.noaa.gov/text/ace-sis.txt
  Interplanetary Magnetic Field
    http://services.swpc.noaa.gov/text/ace-magnetometer.txt
  Solar Wind Plasma
    http://services.swpc.noaa.gov/text/ace-swepam.txt

  xRay Imager:
    http://sxi.ngdc.noaa.gov
  Coronograph Imager:
    http://lasco-www.nrl.navy.mil/index.php?p=content/realtime

  Exhaustive list of text files is located here:
    http://services.swpc.noaa.gov/text/

  Loads more data to look at here:
    http://www.swpc.noaa.gov/Data/index.html#measurements
"""

#################################################
#               GOES Data                       #
#################################################
def getProtonFlux():
  """
    Apparently the NOAA Data Site was restructured which could explain
    why I was having issues accessing data when I first started writing
    this script/application.

    This particular URL happens to be from GOES-13, the primary source of
    Proton Flux, however GOES-15 also provides Proton Flux measurements as
    a secondary source.
  """
  URL = 'http://services.swpc.noaa.gov/text/goes-energetic-proton-flux-primary.txt'
  URLs = 'http://services.swpc.noaa.gov/text/goes-energetic-proton-flux-secondary.txt'
  try:
    fh = urllib.request.urlopen(URL)
  except:
    print("NoaaApi.getProtonFlux > Error opening File Handle, retrying...")
    fh = ""
    fh = urllib.request.urlopen(URL)
  # Create the empty data structure
  data_ret = {
    "source":"",
    "data":{
      "P1" :[],
      "P2" :[],
      "P3" :[],
      "P4" :[],
      "P5" :[],
      "P6" :[],
      "P7" :[],
      "P8" :[],
      "P9" :[],
      "P10":[],
      "P11":[]
    },
    "units":{
      "P1" : "0.7-4 MeV",
      "P2" : "4-9 MeV",
      "P3" : "9-15 MeV",
      "P4" : "15-40 MeV",
      "P5" : "38-82 MeV",
      "P6" : "84-200 MeV",
      "P7" : "110-900 MeV",
      "P8" : "350-420 MeV",
      "P9" : "420-510 MeV",
      "P10": "510-700 MeV",
      "P11": ">700 MeV"
    },
    "datestamp":[],
    "rawlines":[]
  }
  # Loop through the remote data file
  for read_line in fh.readlines():
    read_line = read_line.decode('utf-8').split()
    if(len(read_line) > 1):
      # Get the data samples
      if((read_line[0][0] != '#') and (read_line[0][0] != ':')):
        data_ret["rawlines"   ].append(read_line)
        data_ret["datestamp"  ].append("%s/%s/%s:%s"%(read_line[0],read_line[1],read_line[2],read_line[3]))
        data_ret["data"]["P1" ].append(read_line[6])
        data_ret["data"]["P2" ].append(read_line[7])
        data_ret["data"]["P3" ].append(read_line[8])
        data_ret["data"]["P4" ].append(read_line[9])
        data_ret["data"]["P5" ].append(read_line[10])
        data_ret["data"]["P6" ].append(read_line[11])
        data_ret["data"]["P7" ].append(read_line[12])
        data_ret["data"]["P8" ].append(read_line[13])
        data_ret["data"]["P9" ].append(read_line[14])
        data_ret["data"]["P10"].append(read_line[15])
        data_ret["data"]["P11"].append(read_line[16])
      # Get some header info
      elif(read_line[1] == 'Source:'):
        data_ret["source"] = str(read_line[2])
  # Convert the data points from strings to numbers
  return data_ret

def getGeomagField():
  """
  """
  pass

def getEnergeticParticleFlux():
  """
  """
  pass

def getSolarParticleFlux():
  """
  """
  pass

def getXrayFlux():
  """
    Apparently the NOAA Data Site was restructured which could explain
    why I was having issues accessing data when I first started writing
    this script/application.
  """
  URL = 'http://services.swpc.noaa.gov/text/goes-xray-flux-primary.txt'
  try:
    fh = urllib.request.urlopen(URL)
  except:
    print("NoaaApi.getXrayFlux > Error opening File Handle, retrying...")
    fh = urllib.request.urlopen(URL)
  # Create the empty data structure
  data_ret = {
    "source":"",
    "data":{
      "long" :[],
      "short":[],
    },
    "units":"W/m2",
    "datestamp":[],
    "rawlines":[]
  }
  # Loop through the remote data file
  for read_line in fh.readlines():
    read_line = read_line.decode('utf-8').split()
    if(len(read_line) > 1):
      # Get the data samples
      if((read_line[0][0] != '#') and (read_line[0][0] != ':')):
        data_ret["rawlines"].append(read_line)
        data_ret["datestamp"].append("%s/%s/%s:%s"%(read_line[0],read_line[1],read_line[2],read_line[3]))
        data_ret["data"]["long"].append(read_line[7])
        data_ret["data"]["short"].append(read_line[6])
      # Get some header info
      elif(read_line[1] == 'Source:'):
        data_ret["source"] = str(read_line[2])
  # Convert the data points from strings to numbers
  data_ret["data"]["short"] = [float(i) for i in data_ret["data"]["short"]]
  data_ret["data"]["long"] = [float(i) for i in data_ret["data"]["long"]]
  return data_ret

#################################################
#                  ACE Data                     #
#################################################
def getDiffElecProtFlux():
  """
  """
  pass

def getSolarIsotopeSpectrometer():
  """
  """
  pass

def getInterplanetMagField():
  """
  """
  pass

def getSolarPlasma():
  """
  """
  pass

if __name__ == '__main__':
  # Get XRay Flux Data
  alldata = getXrayFlux()
  print("data source is:")
  print(alldata["source"])
  print("data_short data is:")
  print(alldata["data"]["short"])
  print("data_long data is:")
  print(alldata["data"]["long"])
  print("data units are:")
  print(alldata["units"])
  print("timestamps are:")
  print(alldata["datestamp"])

  # Get Proton Flux Data
  alldata = getProtonFlux()
  print("data source is:")
  print(alldata["source"])
  for key,value in alldata["data"].items():
    print("%s data is:" % (key))
    print(value)
  print("data units are:")
  print(alldata["units"])
  print("timestamps are:")
  print(alldata["datestamp"])
