#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3
import sys
import re

if int(sys.version[0]) == 3:
  # print("Version 3.x!")
  import urllib.request
  import urllib.error

  def openUrl(URL):
    fh = urllib.request.urlopen(URL)
    return fh
if int(sys.version[0]) == 2:
  # print("Version 2.x!")
  import urllib

  def openUrl(URL):
    fh = urllib.urlopen(URL)
    return fh

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

def getData(url: str = "http://services.swpc.noaa.gov/text/goes-energetic-proton-flux-primary.txt"):
  """
    Generic data fetching function.
  """
  datas = {}
  units = {}
  particles = {}
  label_list = []
  stamp = []
  source = ""
  # Preliminary Check of the URL
  if(not(isinstance(url,str))):
    return TypeError
  elif((url.find('http') == -1) or (url.find('.txt') == -1)):
    return LookupError
  else:
    fh = urllib.request.urlopen(url)
    # Print the Header
    for line in fh:
      line = line.decode('utf-8')
      if(line.startswith('#')):
        if(line.find('Label') != -1):
          (blah,label) = line.split('Label:')
          if(label.find('from') != -1):
            (label,particle) = label.split('=')
            (particle,energy) = particle.split('from')
            (energy,unit) = energy.split('units #/')
            # Remove leading and trailing whitespace
            label = label.strip()
            particle = particle.strip()
            energy = energy.strip()
            unit = unit.strip()
            # Now remove excess whitespace
            label = re.sub(" ", "", label)
            particle = re.sub(" {2,}", " ", particle)
            energy = re.sub(" {2,}", " ", energy)
            unit = re.sub(" {2,}", " ", unit)
            # Add the label to the data structure
            datas[label] = []
            units[label] = unit
            particles[label] = (particle, energy)
          elif(label.find('component') != -1):
            (label,blah) = label.split('component =')
            # Remove leading and trailing whitespace
            label = label.strip()
            # Now remove excess whitespace
            label = re.sub(" {2,}", " ", label)
            # Add the label to the data structure
            datas[label] = []
          else:
            (label,blah) = label.split('=')
            # Remove leading and trailing whitespace
            # label = label.strip()
            # Now remove all whitespace
            label = re.sub(" ", "", label)
            # Add the label to the data structure
            datas[label] = []
          label_list.append(label)
        elif(line.find('Units') != -1):
          # Dynamically change units to a string object
          units = ""
          (blah,units) = line.split('Units:')
          # Split again if formatted this way
          if(units.find('/') != -1):
            (blah,units) = units.split('/')
          units = units.strip()
          units = re.sub(" {2,}", " ", units)
        elif(line.find('Source') != -1):
          (blah,source) = line.split('Source:')
          source = source.strip()
          source = re.sub(" {2,}", " ", source)
        else:
          pass
      elif(line.startswith(':')):
        pass
      elif(len(line) == 0):
        pass
      else:
        # Map out each data line to yr, mo, dy, hhmm, skip, skip, d0, d1, ... , dn
        # Zipping up the original sequence of labels with the remainder data
        # lines allows the for loop to then iterate through the new list
        (yr,mo,dy,time,blah1,blah2,*datarow) = line.split()
        stamp.append((str.join("",(yr,mo,dy)), time))
        for (key, value) in zip(label_list, datarow):
          datas[key].append(value)
    return (datas, units, particles, stamp, source)

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
  # Store the data locally
  URL = 'http://services.swpc.noaa.gov/text/goes-energetic-proton-flux-primary.txt'
  with urllib.request.urlopen(URL) as urlfh , open("../data/Gp_pchan_5m.txt", "w") as locfh:
    for line in urlfh:
      line = line.decode('utf-8')
      locfh.write(line)
  # Parse local data
  with open("../data/Gp_pchan_5m.txt", "r") as fh:
    datas = {}
    units = {}
    particles = {}
    label_list = []
    stamp = []
    # Skip the first two lines, just boiler plate stuff
    next(fh)
    next(fh)
    # Iterator of Header
    for line in fh:
      # line = line.decode('utf-8')
      if(line.startswith('#')):
        if(line.find('Label') != -1):
          (blah,label) = line.split('Label:')
          (label,particle) = label.split('=')
          (particle,energy) = particle.split('from')
          (energy,unit) = energy.split('units #/')
          # Remove leading and trailing whitespace
          label = label.strip()
          particle = particle.strip()
          energy = energy.strip()
          unit = unit.strip()
          # Now remove excess whitespace
          label = re.sub(" ", "", label)
          particle = re.sub(" {2,}", " ", particle)
          energy = re.sub(" {2,}", " ", energy)
          unit = re.sub(" {2,}", " ", unit)
          # Add the label to the data structure
          datas[label] = []
          units[label] = unit
          particles[label] = (particle, energy)
          label_list.append(label)
      else:
        # Stop decoding header
        break
    # Iterator of Data
    for line in fh:
      # line = line.decode('utf-8')
      # Map out each data line to yr, mo, dy, hhmm, skip, skip, d0, d1, ... , dn
      # Zipping up the original sequence of labels with the remainder data
      # lines allows the for loop to then iterate through the new list
      (yr,mo,dy,time,blah1,blah2,*datarow) = line.split()
      stamp.append((str.join("",(yr,mo,dy)), time))
      for (key, value) in zip(label_list, datarow):
        datas[key].append(value)
  # Now return the data
  return(label_list,datas,stamp,units,particles)

def getGOESGoemagFieldFlux():
  """
    This function call will return the three dimensions of geomagnetic Flux
    density around the earth. The three dimensions and the total field have
    units of nanotesla.
  """
  URL = 'http://services.swpc.noaa.gov/text/goes-magnetometer-primary.txt'
  try:
    fh = openUrl(URL)
  except:
    print("NoaaApi.getGOESGoemagFieldFlux > Timeout while pulling NOAA Data...")
    fh = ""
    fh = openUrl(URL)
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
    "update":"",
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
      # Get data source
      elif(read_line[1] == 'Source:'):
        data_ret["source"] = str(read_line[2])
      else:
        # Capture the update period
        try:
          if int(sys.version[0]) == 3:
            check_val = read_line[1].split(sep="-")
          if int(sys.version[0]) == 2:
            check_val = read_line[1].split("-")
          if(check_val[1] == "minute"):
            data_ret["update"] = int(check_val[0])*60*1000
        except IndexError:
          pass
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
    fh = openUrl(URL)
  except:
    print("NoaaApi.getGOESDiscreteParticleFlux > Timeout while pulling NOAA Data...")
    fh = ""
    fh = openUrl(URL)
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
    "update":"",
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
      # Get data source
      elif(read_line[1] == 'Source:'):
        data_ret["source"] = str(read_line[2])
      else:
        # Capture the update period
        try:
          if int(sys.version[0]) == 3:
            check_val = read_line[1].split(sep="-")
          if int(sys.version[0]) == 2:
            check_val = read_line[1].split("-")
          if(check_val[1] == "minute"):
            data_ret["update"] = int(check_val[0])*60*1000
        except IndexError:
          pass
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
    fh = openUrl(URL)
  except:
    print("NoaaApi.getGOESRangeParticleFlux > Timeout while pulling NOAA Data...")
    fh = ""
    fh = openUrl(URL)
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
    "update":"",
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
      # Get data source
      elif(read_line[1] == 'Source:'):
        data_ret["source"] = str(read_line[2])
      else:
        # Capture the update period
        try:
          if int(sys.version[0]) == 3:
            check_val = read_line[1].split(sep="-")
          if int(sys.version[0]) == 2:
            check_val = read_line[1].split("-")
          if(check_val[1] == "minute"):
            data_ret["update"] = int(check_val[0])*60*1000
        except IndexError:
          pass
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
    fh = openUrl(URL)
  except:
    print("NoaaApi.getGOESXrayFlux > Timeout while pulling NOAA Data...")
    fh = ""
    fh = openUrl(URL)
  # Create the empty data structure
  data_ret = {
    "source":"",
    "data":{
      "0.05-0.4 nm":[],
      "0.1-0.8 nm" :[]
    },
    "units":"W/m2",
    "update":"",
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
      # Get data source
      elif(read_line[1] == 'Source:'):
        data_ret["source"] = str(read_line[2])
      else:
        # Capture the update period
        try:
          if int(sys.version[0]) == 3:
            check_val = read_line[1].split(sep="-")
          if int(sys.version[0]) == 2:
            check_val = read_line[1].split("-")
          if(check_val[1] == "minute"):
            data_ret["update"] = int(check_val[0])*60*1000
        except IndexError:
          pass
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
    fh = openUrl(URL)
  except:
    print("NoaaApi.getDiffElecProtFlux > Timeout while pulling NOAA Data...")
    fh = ""
    fh = openUrl(URL)
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
    "update":"",
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
      # Get data source
      elif(read_line[1] == 'Source:'):
        data_ret["source"] = str(read_line[2])
      else:
        # Capture the update period
        try:
          if int(sys.version[0]) == 3:
            check_val = read_line[1].split(sep="-")
          if int(sys.version[0]) == 2:
            check_val = read_line[1].split("-")
          if(check_val[1] == "minute"):
            data_ret["update"] = int(check_val[0])*60*1000
        except IndexError:
          pass
  # Convert the data points from strings to numbers
  for key in data_ret["data"].keys():
    data_ret["data"][key] = [float(i) for i in data_ret["data"][key]]
  return data_ret

def getSolarIsotopeSpectrometer():
  """
    This API call only measures the integral of high energy protons above two
    specific energy levels: 10MeV and 30MeV.

    Measurements are taken every 5 minutes.
  """
  URL = 'http://services.swpc.noaa.gov/text/ace-sis.txt'
  try:
    fh = openUrl(URL)
  except:
    print("NoaaApi.getSolarIsotopeSpectrometer > Timeout while pulling NOAA Data...")
    fh = ""
    fh = openUrl(URL)
  # Create the empty data structure
  data_ret = {
    "source":"",
    "data":{
      ">10 MeV Proton":[],
      ">30 MeV Proton":[]
    },
    "units":"p/cm2 * s * sr",
    "update":"",
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
      # Get data source
      elif(read_line[1] == 'Source:'):
        data_ret["source"] = str(read_line[2])
      else:
        # Capture the update period
        try:
          if int(sys.version[0]) == 3:
            check_val = read_line[1].split(sep="-")
          if int(sys.version[0]) == 2:
            check_val = read_line[1].split("-")
          if(check_val[1] == "minute"):
            data_ret["update"] = int(check_val[0])*60*1000
        except IndexError:
          pass
  # Convert the data points from strings to numbers
  for key in data_ret["data"].keys():
    data_ret["data"][key] = [float(i) for i in data_ret["data"][key]]
  return data_ret

def getInterplanetMagField():
  """
    This API returns an interesting set of data, it provides a measurement of
    three dimensional axis of magnetic flux in nano-tesla, and a total 3D vector
    magnetic flux also in nano-tesla. Each measurement is taken by the satellite
    at a specific latitude and longitude which is also recorded which each
    measurement.

    Measurements are taken every minute.
  """
  # Open the file handle
  URL = 'http://services.swpc.noaa.gov/text/ace-magnetometer.txt'
  try:
    fh = openUrl(URL)
  except:
    print("NoaaApi.getInterplanetMagField > Timeout while pulling NOAA Data...")
    fh = ""
    fh = openUrl(URL)
  # Create the empty data structure
  data_ret = {
    "source":"",
    "data":{
      "Bx"       :[],
      "By"       :[],
      "Bz"       :[],
      "Bt"       :[],
      "Latitude" :[],
      "Longitude":[]
    },
    "units":"nT",
    "update":"",
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
        # Interplanetary Magnetic Field
        data_ret["data"]["Bx"       ].append(read_line[7])
        data_ret["data"]["By"       ].append(read_line[8])
        data_ret["data"]["Bz"       ].append(read_line[9])
        data_ret["data"]["Bt"       ].append(read_line[10])
        data_ret["data"]["Latitude" ].append(read_line[11])
        data_ret["data"]["Longitude"].append(read_line[12])
      # Get data source
      elif(read_line[1] == 'Source:'):
        data_ret["source"] = str(read_line[2])
      else:
        # Capture the update period
        try:
          if int(sys.version[0]) == 3:
            check_val = read_line[1].split(sep="-")
          if int(sys.version[0]) == 2:
            check_val = read_line[1].split("-")
          if(check_val[1] == "minute"):
            data_ret["update"] = int(check_val[0])*60*1000
        except IndexError:
          pass
  # Convert the data points from strings to numbers
  for key in data_ret["data"].keys():
    data_ret["data"][key] = [float(i) for i in data_ret["data"][key]]
  return data_ret

def getSolarPlasma():
  """
    This API returns the real time averaged data of the solar wind plasma as
    measured by one of the ACE satellites. It measures proton density, bulk
    particle speed and ION Temperatures.
    This is the only API call here thus far that has three data sets with three
    completely different units. Thus instead of the units key only having one
    value, it also has an embedded dictionary.

    Measurements are updated once a minute.
  """
  # Open the file handle
  URL = 'http://services.swpc.noaa.gov/text/ace-swepam.txt'
  try:
    fh = openUrl(URL)
  except:
    print("NoaaApi.getSolarPlasma > Timeout while pulling NOAA Data...")
    fh = ""
    fh = openUrl(URL)
  # Create the empty data structure
  data_ret = {
    "source":"",
    "data":{
      "Density"    :[],
      "Speed"      :[],
      "Temperature":[]
    },
    "units":{
      "Density"    :"p/cc",
      "Speed"      :"km/s",
      "Temperature":"Kelvin"
    },
    "update":"",
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
        # Solar Wind Plasma
        data_ret["data"]["Density"    ].append(read_line[7])
        data_ret["data"]["Speed"      ].append(read_line[8])
        data_ret["data"]["Temperature"].append(read_line[9])
      # Get data source
      elif(read_line[1] == 'Source:'):
        data_ret["source"] = str(read_line[2])
      else:
        # Capture the update period
        try:
          if int(sys.version[0]) == 3:
            check_val = read_line[1].split(sep="-")
          if int(sys.version[0]) == 2:
            check_val = read_line[1].split("-")
          if(check_val[1] == "minute"):
            data_ret["update"] = int(check_val[0])*60*1000
        except IndexError:
          pass
  # Convert the data points from strings to numbers
  for key in data_ret["data"].keys():
    data_ret["data"][key] = [float(i) for i in data_ret["data"][key]]
  return data_ret

if __name__ == '__main__':
  # Get Proton Flux Data
  print("")
  print("------------------------------------")
  print("           Range Proton Flux")
  print("------------------------------------")
  (label_list,datas,stamp,units,particles) = getGOESRangeProtonFlux()
  print(label_list)
  print(datas)
  print(stamp)
  print(units)
  print(particles)
  # print("data source is:")
  # print(alldata["source"])
  # for key,value in alldata["data"].items():
  #   print("%s data is:" % (key))
  #   print(value)
  # print("data units are:")
  # print(alldata["units"])
  # print("timestamps are:")
  # print(alldata["datestamp"])
  # print("update period in (ms) is:")
  # print(alldata["update"])

  # # Get Geomagnetic Flux Data
  # print("")
  # print("------------------------------------")
  # print("          Geomagnetic Flux")
  # print("------------------------------------")
  # alldata = getGOESGoemagFieldFlux()
  # print("data source is:")
  # print(alldata["source"])
  # for key,value in alldata["data"].items():
  #   print("%s data is:" % (key))
  #   print(value)
  # print("data units are:")
  # print(alldata["units"])
  # print("timestamps are:")
  # print(alldata["datestamp"])
  # print("update period in (ms) is:")
  # print(alldata["update"])

  # # Get Discrete Energetic Particle Flux Data
  # print("")
  # print("------------------------------------")
  # print("  Discrete Energetic Particle Flux")
  # print("------------------------------------")
  # alldata = getGOESDiscreteParticleFlux()
  # print("data source is:")
  # print(alldata["source"])
  # for key,value in alldata["data"].items():
  #   print("%s data is:" % (key))
  #   print(value)
  # print("data units are:")
  # print(alldata["units"])
  # print("timestamps are:")
  # print(alldata["datestamp"])
  # print("update period in (ms) is:")
  # print(alldata["update"])

  # # Get Range Energetic Particle Flux Data
  # print("")
  # print("------------------------------------")
  # print("   Range Energetic Particle Flux")
  # print("------------------------------------")
  # alldata = getGOESRangeParticleFlux()
  # print("data source is:")
  # print(alldata["source"])
  # for key,value in alldata["data"].items():
  #   print("%s data is:" % (key))
  #   print(value)
  # print("data units are:")
  # print(alldata["units"])
  # print("timestamps are:")
  # print(alldata["datestamp"])
  # print("update period in (ms) is:")
  # print(alldata["update"])

  # # Get XRay Flux Data
  # print("")
  # print("------------------------------------")
  # print("           XRay Flux")
  # print("------------------------------------")
  # alldata = getGOESXrayFlux()
  # print("data source is:")
  # print(alldata["source"])
  # for key,value in alldata["data"].items():
  #   print("%s data is:" % (key))
  #   print(value)
  # print("data units are:")
  # print(alldata["units"])
  # print("timestamps are:")
  # print(alldata["datestamp"])
  # print("update period in (ms) is:")
  # print(alldata["update"])

  # # Get Differential Flux Data
  # print("")
  # print("------------------------------------")
  # print("          Differential Flux")
  # print("------------------------------------")
  # alldata = getDiffElecProtFlux()
  # print("data source is:")
  # print(alldata["source"])
  # for key,value in alldata["data"].items():
  #   print("%s data is:" % (key))
  #   print(value)
  # print("data units are:")
  # print(alldata["units"])
  # print("timestamps are:")
  # print(alldata["datestamp"])
  # print("update period in (ms) is:")
  # print(alldata["update"])

  # # Get Differential Flux Data
  # print("")
  # print("------------------------------------")
  # print("  Integral High Energy Proton Flux")
  # print("------------------------------------")
  # alldata = getSolarIsotopeSpectrometer()
  # print("data source is:")
  # print(alldata["source"])
  # for key,value in alldata["data"].items():
  #   print("%s data is:" % (key))
  #   print(value)
  # print("data units are:")
  # print(alldata["units"])
  # print("timestamps are:")
  # print(alldata["datestamp"])
  # print("update period in (ms) is:")
  # print(alldata["update"])

  # # Get Interplanetary Magnetic Field Flux
  # print("")
  # print("------------------------------------")
  # print("   Interplanetary Magnetic Field")
  # print("------------------------------------")
  # alldata = getInterplanetMagField()
  # print("data source is:")
  # print(alldata["source"])
  # for key,value in alldata["data"].items():
  #   print("%s data is:" % (key))
  #   print(value)
  # print("data units are:")
  # print(alldata["units"])
  # print("timestamps are:")
  # print(alldata["datestamp"])
  # print("update period in (ms) is:")
  # print(alldata["update"])

  # # Get Solar Wind Plasma
  # print("")
  # print("------------------------------------")
  # print("         Solar Wind Plasma")
  # print("------------------------------------")
  # alldata = getSolarPlasma()
  # print("data source is:")
  # print(alldata["source"])
  # for key,value in alldata["data"].items():
  #   print("%s data is:" % (key))
  #   print(value)
  # for key,value in alldata["units"].items():
  #   print("%s units are:" % (key))
  #   print(value)
  # print("timestamps are:")
  # print(alldata["datestamp"])
  # print("update period in (ms) is:")
  # print(alldata["update"])
