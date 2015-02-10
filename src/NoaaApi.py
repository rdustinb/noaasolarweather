#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

import urllib.request
import urllib.error

"""
  Locations of data that I want to capture and eventually graph. This data
  is provided from the GOES and ACE satellites.

  = GOES =
  Energetic Proton Flux - getGOESRangeProtonFlux()
    http://services.swpc.noaa.gov/text/goes-energetic-proton-flux-primary.txt
    http://services.swpc.noaa.gov/text/goes-energetic-proton-flux-secondary.txt

  Geomagnetic Components and Total Field - getGOESGoemagFieldFlux()
    http://services.swpc.noaa.gov/text/goes-magnetometer-primary.txt
    http://services.swpc.noaa.gov/text/goes-magnetometer-secondary.txt

  Energetic Particle Flux - getGOESDiscreteParticleFlux()
    http://services.swpc.noaa.gov/text/goes-magnetospheric-particle-flux-ts1-primary.txt
    http://services.swpc.noaa.gov/text/goes-magnetospheric-particle-flux-ts1-secondary.txt

  Solar Particle and Electron Flux - getGOESRangeParticleFlux()
    http://services.swpc.noaa.gov/text/goes-particle-flux-primary.txt
    http://services.swpc.noaa.gov/text/goes-particle-flux-secondary.txt

  xRay Flux - getGOESXrayFlux()
    http://services.swpc.noaa.gov/text/goes-xray-flux-primary.txt
    http://services.swpc.noaa.gov/text/goes-xray-flux-secondary.txt


  = ACE =
  Differential Electron / Proton Flux - getDiffElecProtFlux()
    http://services.swpc.noaa.gov/text/ace-epam.txt

  Solar Isotope Spectrometer - getSolarIsotopeSpectrometer()
    http://services.swpc.noaa.gov/text/ace-sis.txt

  Interplanetary Magnetic Field - getInterplanetMagField()
    http://services.swpc.noaa.gov/text/ace-magnetometer.txt

  Solar Wind Plasma - getSolarPlasma()
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
def getGOESRangeProtonFlux():
  """
    Apparently the NOAA Data Site was restructured which could explain
    why I was having issues accessing data when I first started writing
    this script/application.

    This particular URL happens to be from GOES-13, the primary source of
    Proton Flux, however GOES-15 also provides Proton Flux measurements as
    a secondary source.
  """
  URL = 'http://services.swpc.noaa.gov/text/goes-energetic-proton-flux-primary.txt'
  try:
    fh = urllib.request.urlopen(URL)
  except:
    print("NoaaApi.getGOESRangeProtonFlux > Error opening File Handle, retrying...")
    fh = ""
    fh = urllib.request.urlopen(URL)
  # Create the empty data structure
  data_ret = {
    "source":"",
    "data":{
      "0.7-4 MeV Protons"  :[],
      "4-9 MeV Protons"    :[],
      "9-15 MeV Protons"   :[],
      "15-40 MeV Protons"  :[],
      "38-82 MeV Protons"  :[],
      "84-200 MeV Protons" :[],
      "110-900 MeV Protons":[],
      "350-420 MeV Protons":[],
      "420-510 MeV Protons":[],
      "510-700 MeV Protons":[],
      ">700 MeV Protons"   :[]
    },
    "units":"p/cm2 * s * sr * MeV",
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
        data_ret["datestamp"  ].append("%s/%s/%s:%s"%(read_line[0],read_line[1],
          read_line[2],read_line[3]))
        data_ret["data"]["0.7-4 MeV Protons"  ].append(read_line[6])
        data_ret["data"]["4-9 MeV Protons"    ].append(read_line[7])
        data_ret["data"]["9-15 MeV Protons"   ].append(read_line[8])
        data_ret["data"]["15-40 MeV Protons"  ].append(read_line[9])
        data_ret["data"]["38-82 MeV Protons"  ].append(read_line[10])
        data_ret["data"]["84-200 MeV Protons" ].append(read_line[11])
        data_ret["data"]["110-900 MeV Protons"].append(read_line[12])
        data_ret["data"]["350-420 MeV Protons"].append(read_line[13])
        data_ret["data"]["420-510 MeV Protons"].append(read_line[14])
        data_ret["data"]["510-700 MeV Protons"].append(read_line[15])
        data_ret["data"][">700 MeV Protons"   ].append(read_line[16])
      # Get some header info
      elif(read_line[1] == 'Source:'):
        data_ret["source"] = str(read_line[2])
  # Convert the data points from strings to numbers
  for key in data_ret["data"].keys():
    data_ret["data"][key] = [float(i) for i in data_ret["data"][key]]
  return data_ret

def getGOESGoemagFieldFlux():
  """
    This function call will return the three dimensions of geomagnetic Flux
    density around the earth. The three dimensions and the total field have
    units of nanotesla.
  """
  URL = 'http://services.swpc.noaa.gov/text/goes-magnetometer-primary.txt'
  try:
    fh = urllib.request.urlopen(URL)
  except:
    print("NoaaApi.getGOESGoemagFieldFlux > Error opening File Handle, retrying...")
    fh = urllib.request.urlopen(URL)
  # Create the empty data structure
  data_ret = {
    "source":"",
    "data":{
      "Hp"   :[],
      "He"   :[],
      "Hn"   :[],
      "Total":[]
    },
    "units":"nT",
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
        data_ret["datestamp"].append("%s/%s/%s:%s"%(read_line[0],read_line[1],
          read_line[2],read_line[3]))
        data_ret["data"]["Hp"].append(read_line[6])
        data_ret["data"]["He"].append(read_line[7])
        data_ret["data"]["Hn"].append(read_line[8])
        data_ret["data"]["Total"].append(read_line[9])
      # Get some header info
      elif(read_line[1] == 'Source:'):
        data_ret["source"] = str(read_line[2])
  # Convert the data points from strings to numbers
  for key in data_ret["data"].keys():
    data_ret["data"][key] = [float(i) for i in data_ret["data"][key]]
  return data_ret

def getGOESDiscreteParticleFlux():
  """
    This call will collect the data from the energetic Proton/Electron Flux. This
    API returns a list of 10 data lists of as many distinct proton and electron
    energies.
  """
  URL = 'http://services.swpc.noaa.gov/text/goes-magnetospheric-particle-flux-ts1-primary.txt'
  try:
    fh = urllib.request.urlopen(URL)
  except:
    print("NoaaApi.getGOESDiscreteParticleFlux > Error opening File Handle, retrying...")
    fh = urllib.request.urlopen(URL)
  # Create the empty data structure
  data_ret = {
    "source":"",
    "data":{
      "95 keV Protons"   :[],
      "140 keV Protons"  :[],
      "210 keV Protons"  :[],
      "300 keV Protons"  :[],
      "475 keV Protons"  :[],
      "40 keV Electrons" :[],
      "75 keV Electrons" :[],
      "150 keV Electrons":[],
      "275 keV Electrons":[],
      "475 keV Electrons":[]
    },
    "units":"p/cm2 * s * sr * MeV",
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
        data_ret["datestamp"].append("%s/%s/%s:%s"%(read_line[0],read_line[1],
          read_line[2],read_line[3]))
        data_ret["data"]["95 keV Protons"   ].append(read_line[6])
        data_ret["data"]["140 keV Protons"  ].append(read_line[7])
        data_ret["data"]["210 keV Protons"  ].append(read_line[8])
        data_ret["data"]["300 keV Protons"  ].append(read_line[9])
        data_ret["data"]["475 keV Protons"  ].append(read_line[10])
        data_ret["data"]["40 keV Electrons" ].append(read_line[11])
        data_ret["data"]["75 keV Electrons" ].append(read_line[12])
        data_ret["data"]["150 keV Electrons"].append(read_line[13])
        data_ret["data"]["275 keV Electrons"].append(read_line[14])
        data_ret["data"]["475 keV Electrons"].append(read_line[15])
      # Get some header info
      elif(read_line[1] == 'Source:'):
        data_ret["source"] = str(read_line[2])
  # Convert the data points from strings to numbers
  for key in data_ret["data"].keys():
    data_ret["data"][key] = [float(i) for i in data_ret["data"][key]]
  return data_ret

def getGOESRangeParticleFlux():
  """
    Similar to the getGOESDiscreteParticleFlux function, however this dataset returns
    particle counts for only 6 proton ranges and 3 electron ranges. The ranges of
    particle energies are low-barrier energies and greater.
    For instance the first set of data is of protons >1MeV, while the second is
    of protons >5MeV.
  """
  URL = 'http://services.swpc.noaa.gov/text/goes-particle-flux-primary.txt'
  try:
    fh = urllib.request.urlopen(URL)
  except:
    print("NoaaApi.getGOESRangeParticleFlux > Error opening File Handle, retrying...")
    fh = urllib.request.urlopen(URL)
  # Create the empty data structure
  data_ret = {
    "source":"",
    "data":{
      ">1 Mev Protons"    :[],
      ">5 Mev Protons"    :[],
      ">10 Mev Protons"   :[],
      ">30 Mev Protons"   :[],
      ">50 Mev Protons"   :[],
      ">100 Mev Protons"  :[],
      ">0.8 Mev Electrons":[],
      ">2.0 Mev Electrons":[],
      ">4.0 Mev Electrons":[]
    },
    "units":"p/cm2 * s * sr * MeV",
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
        data_ret["datestamp"].append("%s/%s/%s:%s"%(read_line[0],read_line[1],
          read_line[2],read_line[3]))
        data_ret["data"][">1 Mev Protons"    ].append(read_line[6])
        data_ret["data"][">5 Mev Protons"    ].append(read_line[7])
        data_ret["data"][">10 Mev Protons"   ].append(read_line[8])
        data_ret["data"][">30 Mev Protons"   ].append(read_line[9])
        data_ret["data"][">50 Mev Protons"   ].append(read_line[10])
        data_ret["data"][">100 Mev Protons"  ].append(read_line[11])
        data_ret["data"][">0.8 Mev Electrons"].append(read_line[12])
        data_ret["data"][">2.0 Mev Electrons"].append(read_line[13])
        data_ret["data"][">4.0 Mev Electrons"].append(read_line[14])
      # Get some header info
      elif(read_line[1] == 'Source:'):
        data_ret["source"] = str(read_line[2])
  # Convert the data points from strings to numbers
  for key in data_ret["data"].keys():
    data_ret["data"][key] = [float(i) for i in data_ret["data"][key]]
  return data_ret

def getGOESXrayFlux():
  """
    Apparently the NOAA Data Site was restructured which could explain
    why I was having issues accessing data when I first started writing
    this script/application.
  """
  URL = 'http://services.swpc.noaa.gov/text/goes-xray-flux-primary.txt'
  try:
    fh = urllib.request.urlopen(URL)
  except:
    print("NoaaApi.getGOESXrayFlux > Error opening File Handle, retrying...")
    fh = urllib.request.urlopen(URL)
  # Create the empty data structure
  data_ret = {
    "source":"",
    "data":{
      "0.05-0.4 nm":[],
      "0.1-0.8 nm" :[]
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
        data_ret["data"]["0.05-0.4 nm"].append(read_line[6])
        data_ret["data"]["0.1-0.8 nm"].append(read_line[7])
      # Get some header info
      elif(read_line[1] == 'Source:'):
        data_ret["source"] = str(read_line[2])
  # Convert the data points from strings to numbers
  for key in data_ret["data"].keys():
    data_ret["data"][key] = [float(i) for i in data_ret["data"][key]]
  return data_ret

#################################################
#                  ACE Data                     #
#################################################
def getDiffElecProtFlux():
  """
    This API call will pull data from the ACE Satellite for real-time averaged
    electron and proton flux. The units of measure are for differential flux
    particles.

    Differential Flux as defined by JEDEC:
      'The particle flux density per unit energy incident on a surface; i.e.,
      the number of radiant-energy particles incident on a surface during a given
      period of time divided by the product of the area of that surface, the
      characteristic energy of the incident particles, and the given period of
      time.'

    The units provided by NOAA are 'particles/cm2-s-ster-MeV' where:
      cm2 - area, centimeters squared
      s - unit of time, seconds
      ster - measurement of incidental angle, steradians
      MeV - unit of energy, Mega Electrov-Volt
  """
  URL = 'http://services.swpc.noaa.gov/text/ace-epam.txt'
  try:
    fh = urllib.request.urlopen(URL)
  except:
    print("NoaaApi.getDiffElecProtFlux > Error opening File Handle, retrying...")
    fh = ""
    fh = urllib.request.urlopen(URL)
  # Create the empty data structure
  data_ret = {
    "source":"",
    "data":{
      "38-53 eV Electron"   :[],
      "175-315 eV Electron" :[],
      "47-68 keV Proton"    :[],
      "115-195 keV Proton"  :[],
      "310-580 keV Proton"  :[],
      "795-1193 keV Proton" :[],
      "1060-1900 keV Proton":[]
    },
    "units":"p/cm2 * s * sr * MeV",
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
        data_ret["datestamp"  ].append("%s/%s/%s:%s"%(read_line[0],read_line[1],
          read_line[2],read_line[3]))
        # Electron Flux
        data_ret["data"]["38-53 eV Electron"   ].append(read_line[7])
        data_ret["data"]["175-315 eV Electron" ].append(read_line[8])
        # Proton Flux
        data_ret["data"]["47-68 keV Proton"    ].append(read_line[10])
        data_ret["data"]["115-195 keV Proton"  ].append(read_line[11])
        data_ret["data"]["310-580 keV Proton"  ].append(read_line[12])
        data_ret["data"]["795-1193 keV Proton" ].append(read_line[13])
        data_ret["data"]["1060-1900 keV Proton"].append(read_line[14])
      # Get some header info
      elif(read_line[1] == 'Source:'):
        data_ret["source"] = str(read_line[2])
  # Convert the data points from strings to numbers
  for key in data_ret["data"].keys():
    data_ret["data"][key] = [float(i) for i in data_ret["data"][key]]
  return data_ret

def getSolarIsotopeSpectrometer():
  """
    This API call only measures the integral of high energy protons above two
    specific energy levels: 10MeV and 30MeV.
  """
  URL = 'http://services.swpc.noaa.gov/text/ace-sis.txt'
  try:
    fh = urllib.request.urlopen(URL)
  except:
    print("NoaaApi.getSolarIsotopeSpectrometer > Error opening File Handle, retrying...")
    fh = ""
    fh = urllib.request.urlopen(URL)
  # Create the empty data structure
  data_ret = {
    "source":"",
    "data":{
      ">10 MeV Proton":[],
      ">30 MeV Proton":[]
    },
    "units":"p/cm2 * s * sr",
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
        data_ret["datestamp"  ].append("%s/%s/%s:%s"%(read_line[0],read_line[1],
          read_line[2],read_line[3]))
        # High Energy Solar Proton Flux
        data_ret["data"][">10 MeV Proton"].append(read_line[7])
        data_ret["data"][">30 MeV Proton"].append(read_line[9])
      # Get some header info
      elif(read_line[1] == 'Source:'):
        data_ret["source"] = str(read_line[2])
  # Convert the data points from strings to numbers
  for key in data_ret["data"].keys():
    data_ret["data"][key] = [float(i) for i in data_ret["data"][key]]
  return data_ret

def getInterplanetMagField():
  """
  """
  pass

def getSolarPlasma():
  """
  """
  pass

if __name__ == '__main__':
  # Get Proton Flux Data
  print("")
  print("------------------------------------")
  print("           Range Proton Flux")
  print("------------------------------------")
  alldata = getGOESRangeProtonFlux()
  print("data source is:")
  print(alldata["source"])
  for key,value in alldata["data"].items():
    print("%s data is:" % (key))
    print(value)
  print("data units are:")
  print(alldata["units"])
  print("timestamps are:")
  print(alldata["datestamp"])

  # Get Geomagnetic Flux Data
  print("")
  print("------------------------------------")
  print("          Geomagnetic Flux")
  print("------------------------------------")
  alldata = getGOESGoemagFieldFlux()
  print("data source is:")
  print(alldata["source"])
  for key,value in alldata["data"].items():
    print("%s data is:" % (key))
    print(value)
  print("data units are:")
  print(alldata["units"])
  print("timestamps are:")
  print(alldata["datestamp"])

  # Get Discrete Energetic Particle Flux Data
  print("")
  print("------------------------------------")
  print("  Discrete Energetic Particle Flux")
  print("------------------------------------")
  alldata = getGOESDiscreteParticleFlux()
  print("data source is:")
  print(alldata["source"])
  for key,value in alldata["data"].items():
    print("%s data is:" % (key))
    print(value)
  print("data units are:")
  print(alldata["units"])
  print("timestamps are:")
  print(alldata["datestamp"])

  # Get Range Energetic Particle Flux Data
  print("")
  print("------------------------------------")
  print("   Range Energetic Particle Flux")
  print("------------------------------------")
  alldata = getGOESRangeParticleFlux()
  print("data source is:")
  print(alldata["source"])
  for key,value in alldata["data"].items():
    print("%s data is:" % (key))
    print(value)
  print("data units are:")
  print(alldata["units"])
  print("timestamps are:")
  print(alldata["datestamp"])

  # Get XRay Flux Data
  print("")
  print("------------------------------------")
  print("           XRay Flux")
  print("------------------------------------")
  alldata = getGOESXrayFlux()
  print("data source is:")
  print(alldata["source"])
  for key,value in alldata["data"].items():
    print("%s data is:" % (key))
    print(value)
  print("data units are:")
  print(alldata["units"])
  print("timestamps are:")
  print(alldata["datestamp"])

  # Get Differential Flux Data
  print("")
  print("------------------------------------")
  print("          Differential Flux")
  print("------------------------------------")
  alldata = getDiffElecProtFlux()
  print("data source is:")
  print(alldata["source"])
  for key,value in alldata["data"].items():
    print("%s data is:" % (key))
    print(value)
  print("data units are:")
  print(alldata["units"])
  print("timestamps are:")
  print(alldata["datestamp"])

  # Get Differential Flux Data
  print("")
  print("------------------------------------")
  print("  Integral High Energy Proton Flux")
  print("------------------------------------")
  alldata = getSolarIsotopeSpectrometer()
  print("data source is:")
  print(alldata["source"])
  for key,value in alldata["data"].items():
    print("%s data is:" % (key))
    print(value)
  print("data units are:")
  print(alldata["units"])
  print("timestamps are:")
  print(alldata["datestamp"])
