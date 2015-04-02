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

#################################################
#        GOES Energetic Proton Flux             #
#################################################
def storeGOESRangeProtonFlux():
  """
    This particular URL happens to be from GOES-13, the primary source of
    Proton Flux, however GOES-15 also provides Proton Flux measurements as
    a secondary source.
  """
  # Store the data locally
  URL = 'http://services.swpc.noaa.gov/text/goes-energetic-proton-flux-primary.txt'
  with openUrl(URL) as urlfh , open("../data/Gp_pchan_5m.txt", "w") as locfh:
    for line in urlfh:
      line = line.decode('utf-8')
      locfh.write(line)

def getGOESRangeProtonFlux():
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
      if(line.startswith('#') and not(line.startswith('#-'))):
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
          # Remove all whitespace from energy labels
          energy = re.sub(" ", "", energy)
          energy = energy.strip(" MeV")
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
      # Map out each data line to yr, mo, dy, hhmm, skip, skip, d0, d1, ... , dn
      # Zipping up the original sequence of labels with the remainder data
      # lines allows the for loop to then iterate through the new list
      (yr,mo,dy,time,blah1,blah2,*datarow) = line.split()
      stamp.append((str.join("",(yr,mo,dy)), time))
      for (key, value) in zip(label_list, datarow):
        datas[key].append(float(value))
  # Now return the data
  return(label_list,datas,stamp,units,particles)

#################################################
#          GOES Geomagnetic Field               #
#################################################
def storeGOESGeomagFieldFlux():
  """
    This function call will return the three dimensions of geomagnetic Flux
    density around the earth. The three dimensions and the total field have
    units of nanotesla.
  """
  URL = 'http://services.swpc.noaa.gov/text/goes-magnetometer-primary.txt'
  with openUrl(URL) as urlfh , open("../data/Gp_mag_1m.txt", "w") as locfh:
    for line in urlfh:
      line = line.decode('utf-8')
      locfh.write(line)

def getGOESGeomagFieldFlux():
  # Parse local data
  with open("../data/Gp_mag_1m.txt", "r") as fh:
    datas = {}
    units = "nT"
    label_list = ["Hp","He","Hn","Total"]
    stamp = []
    # Create the datas
    for label in label_list:
      datas[label] = []
    # Skip the first two lines, just boiler plate stuff
    next(fh)
    next(fh)
    # Iterator of Header
    for line in fh:
      if(line.startswith('#') and not(line.startswith('#-'))):
        next(fh)
      else:
        # Stop decoding header
        break
    # Iterator of Data
    for line in fh:
      # Map out each data line to yr, mo, dy, hhmm, skip, skip, d0, d1, ... , dn
      # Zipping up the original sequence of labels with the remainder data
      # lines allows the for loop to then iterate through the new list
      (yr,mo,dy,time,blah1,blah2,*datarow) = line.split()
      stamp.append((str.join("",(yr,mo,dy)), time))
      for (key, value) in zip(label_list, datarow):
        datas[key].append(float(value))
  # Now return the data
  return(label_list,datas,stamp,units)

#################################################
#         GOES Discrete Particle Flux           #
#################################################
def storeGOESDiscreteParticleFlux():
  """
    This call will collect the data from the energetic Proton/Electron Flux. This
    API returns a list of 10 data lists of as many distinct proton and electron
    energies.
  """
  URL = 'http://services.swpc.noaa.gov/text/goes-magnetospheric-particle-flux-ts1-primary.txt'
  with openUrl(URL) as urlfh , open("../data/Gp_magnetospheric_particles_ts1.txt", "w") as locfh:
    for line in urlfh:
      line = line.decode('utf-8')
      locfh.write(line)

def getGOESDiscreteParticleFlux():
  # Parse local data
  with open("../data/Gp_magnetospheric_particles_ts1.txt", "r") as fh:
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
      if(line.startswith('#') and not(line.startswith('#-'))):
        if(line.find('Label') != -1):
          (blah,label) = line.split('Label:')
          (label,energy) = label.split('=')
          (blah,energy) = energy.split('from')
          (energy,particle) = energy.split(' keV ')
          (particle,unit) = particle.split('units #/')
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
          # Append either 'p' or 'e'
          if(particle == "Protons"):
            energy = " ".join(['p',energy])
          elif(particle == "Electrons"):
            energy = " ".join(['e',energy])
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
      # Map out each data line to yr, mo, dy, hhmm, skip, skip, d0, d1, ... , dn
      # Zipping up the original sequence of labels with the remainder data
      # lines allows the for loop to then iterate through the new list
      (yr,mo,dy,time,blah1,blah2,*datarow) = line.split()
      stamp.append((str.join("",(yr,mo,dy)), time))
      for (key, value) in zip(label_list, datarow):
        datas[key].append(float(value))
  # Now return the data
  return(label_list,datas,stamp,units,particles)

#################################################
#         GOES Integral Particle Flux           #
#################################################
def storeGOESIntegralParticleFlux():
  """
    Similar to the getGOESDiscreteParticleFlux function, however this dataset returns
    particle counts for only 6 proton ranges and 3 electron ranges. The ranges of
    particle energies are low-barrier energies and greater.
    For instance the first set of data is of protons >1MeV, while the second is
    of protons >5MeV.
  """
  URL = 'http://services.swpc.noaa.gov/text/goes-particle-flux-primary.txt'
  with openUrl(URL) as urlfh , open("../data/Gp_part_5m.txt", "w") as locfh:
    for line in urlfh:
      line = line.decode('utf-8')
      locfh.write(line)

def getGOESIntegralParticleFlux():
  # Parse local data
  with open("../data/Gp_part_5m.txt", "r") as fh:
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
      if(line.startswith('#') and not(line.startswith('#-'))):
        if(line.find('Label') != -1):
          (blah,label) = line.split('Label:')
          (label,particle) = label.split('=')
          (particle,energy) = particle.split('at')
          # Remove leading and trailing whitespace
          label = label.strip()
          particle = particle.strip()
          energy = energy.strip()
          # Now remove excess whitespace
          label = re.sub(" ", "", label)
          particle = re.sub(" {2,}", " ", particle)
          energy = re.sub(" {2,}", " ", energy)
          energy = energy.strip(" Mev")
          # Append either 'p' or 'e'
          if(particle == "Particles"):
            energy = " ".join(['p',energy])
          elif(particle == "Electrons"):
            energy = " ".join(['e',energy])
          # Add the label to the data structure
          datas[label] = []
          units[label] = "cm2-s-sr"
          particles[label] = (particle, energy)
          label_list.append(label)
      else:
        # Stop decoding header
        break
    # Iterator of Data
    for line in fh:
      # Map out each data line to yr, mo, dy, hhmm, skip, skip, d0, d1, ... , dn
      # Zipping up the original sequence of labels with the remainder data
      # lines allows the for loop to then iterate through the new list
      (yr,mo,dy,time,blah1,blah2,*datarow) = line.split()
      stamp.append((str.join("",(yr,mo,dy)), time))
      for (key, value) in zip(label_list, datarow):
        datas[key].append(float(value))
  # Now return the data
  return(label_list,datas,stamp,units,particles)

#################################################
#                 GOES XRay Flux                #
#################################################
def storeGOESXrayFlux():
  """
    Apparently the NOAA Data Site was restructured which could explain
    why I was having issues accessing data when I first started writing
    this script/application.
  """
  URL = 'http://services.swpc.noaa.gov/text/goes-xray-flux-primary.txt'
  with openUrl(URL) as urlfh , open("../data/Gp_xr_1m.txt", "w") as locfh:
    for line in urlfh:
      line = line.decode('utf-8')
      locfh.write(line)

def getGOESXrayFlux():
  # Parse local data
  with open("../data/Gp_xr_1m.txt", "r") as fh:
    datas = {}
    units = "W/m2"
    particles = {}
    label_list = []
    stamp = []
    # Create the datas
    for label in label_list:
      datas[label] = []
    # Skip the first two lines, just boiler plate stuff
    next(fh)
    next(fh)
    # Iterator of Header
    for line in fh:
      if(line.startswith('#') and not(line.startswith('#-'))):
        if(line.find('Label') != -1):
          (blah,label) = line.split('Label:')
          (label,particle) = label.split('=')
          (particle,blah) = particle.split('nanometer')
          # Remove leading and trailing whitespace
          label = label.strip()
          particle = particle.strip()
          # Now remove excess whitespace
          label = re.sub(" ", "", label)
          particle = re.sub(" ", "", particle)
          # Add the label to the data structure
          datas[label] = []
          particles[label] = ("nm", particle)
          label_list.append(label)
      else:
        # Stop decoding header
        break
    # Iterator of Data
    for line in fh:
      # Map out each data line to yr, mo, dy, hhmm, skip, skip, d0, d1, ... , dn
      # Zipping up the original sequence of labels with the remainder data
      # lines allows the for loop to then iterate through the new list
      (yr,mo,dy,time,blah1,blah2,*datarow) = line.split()
      stamp.append((str.join("",(yr,mo,dy)), time))
      for (key, value) in zip(label_list, datarow):
        datas[key].append(float(value))
  # Now return the data
  return(label_list,datas,stamp,units,particles)

#################################################
#         ACE Differential Particle Flux        #
#################################################
def storeDiffElecProtFlux():
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
  with openUrl(URL) as urlfh , open("../data/ace_epam_5m.txt", "w") as locfh:
    for line in urlfh:
      line = line.decode('utf-8')
      locfh.write(line)

def getDiffElecProtFlux():
  # Parse local data
  with open("../data/ace_epam_5m.txt", "r") as fh:
    datas = {}
    units = "Particles/cm2*s*sr*MeV"
    particles = {}
    label_list = ['38-53','175-315','47-68','115-195','310-580','795-1193','1060-1900']
    stamp = []
    # Skip the first two lines, just boiler plate stuff
    next(fh)
    next(fh)
    # Iterator of Header
    for line in fh:
      if(line.startswith('#') and not(line.startswith('#-'))):
        pass
      else:
        # Stop decoding header
        break
    # Iterator of Data
    for line in fh:
      # Map out each data line to yr, mo, dy, hhmm, skip, skip, d0, d1, ... , dn
      # Zipping up the original sequence of labels with the remainder data
      # lines allows the for loop to then iterate through the new list
      (yr,mo,dy,time,blah1,blah2,blah3,datarow1,datarow2,blah4,*datarow) = line.split()
      stamp.append((str.join("",(yr,mo,dy)), time))
      for (key, value) in zip(label_list[0:2], [datarow1,datarow2]):
        if(key in datas):
          datas[key].append(float(value))
        else:
          datas[key] = [float(value)]
      for (key, value) in zip(label_list[2:], datarow):
        if(key in datas):
          datas[key].append(float(value))
        else:
          datas[key] = [float(value)]
  # Format the Particles
  particle_tuple = zip(['Electron','Electron','Proton','Proton','Proton','Proton','Proton'], label_list)
  for (particle, key) in particle_tuple:
    if(particle == 'Electron'):
      particles[key] = (particle, " ".join(['e',key]))
    elif(particle == 'Proton'):
      particles[key] = (particle, " ".join(['p',key]))
  # Now return the data
  return(label_list,datas,stamp,units,particles)

#################################################
#           ACE Integral Proton Flux            #
#################################################
def storeIntegralProtonFlux():
  """
    This API call only measures the integral of high energy protons above two
    specific energy levels: 10MeV and 30MeV.

    Measurements are taken every 5 minutes.
  """
  URL = 'http://services.swpc.noaa.gov/text/ace-sis.txt'
  with openUrl(URL) as urlfh , open("../data/ace_sis_5m.txt", "w") as locfh:
    for line in urlfh:
      line = line.decode('utf-8')
      locfh.write(line)

def getIntegralProtonFlux():
  # Parse local data
  with open("../data/ace_sis_5m.txt", "r") as fh:
    datas = {}
    units = "Protons/cm2*s*sr*MeV"
    particles = {}
    label_list = ['>10','>30']
    stamp = []
    # Skip the first two lines, just boiler plate stuff
    next(fh)
    next(fh)
    # Iterator of Header
    for line in fh:
      if(line.startswith('#') and not(line.startswith('#-'))):
        pass
      else:
        # Stop decoding header
        break
    # Iterator of Data
    for line in fh:
      # Map out each data line to yr, mo, dy, hhmm, skip, skip, d0, d1, ... , dn
      # Zipping up the original sequence of labels with the remainder data
      # lines allows the for loop to then iterate through the new list
      (yr,mo,dy,time,blah1,blah2,blah3,datarow1,blah4,datarow2) = line.split()
      stamp.append((str.join("",(yr,mo,dy)), time))
      for (key, value) in zip(label_list, [datarow1,datarow2]):
        if(key in datas):
          datas[key].append(float(value))
        else:
          datas[key] = [float(value)]
  # Format the Particles
  particle_tuple = zip(['Proton','Proton'], label_list)
  for (particle, key) in particle_tuple:
    particles[key] = (particle, key)
  # Now return the data
  return(label_list,datas,stamp,units,particles)

#################################################
#       ACE Interplanetary Magnetic Field       #
#################################################
def storeInterplanetMagField():
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
  with openUrl(URL) as urlfh , open("../data/ace_mag_1m.txt", "w") as locfh:
    for line in urlfh:
      line = line.decode('utf-8')
      locfh.write(line)

def getInterplanetMagField():
  # Parse local data
  with open("../data/ace_mag_1m.txt", "r") as fh:
    datas = {}
    label_list = ['Total','Latitude','Longitude']
    stamp = []
    # Skip the first two lines, just boiler plate stuff
    next(fh)
    next(fh)
    # Iterator of Header
    for line in fh:
      if(line.startswith('#') and not(line.startswith('#-'))):
        pass
      else:
        # Stop decoding header
        break
    # Iterator of Data
    for line in fh:
      # Map out each data line to yr, mo, dy, hhmm, skip, skip, d0, d1, ... , dn
      # Zipping up the original sequence of labels with the remainder data
      # lines allows the for loop to then iterate through the new list
      (yr,mo,dy,time,blah1,blah2,blah3,blah4,blah5,blah6,*datarow) = line.split()
      stamp.append((str.join("",(yr,mo,dy)), time))
      for (key, value) in zip(label_list, datarow):
        if key in datas:
          datas[key].append(float(value))
        else:
          datas[key] = [float(value)]
  # Now return the data
  return(label_list,datas,stamp)

#################################################
#               ACE Solar Plasma                #
#################################################
def storeSolarPlasma():
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
  with openUrl(URL) as urlfh , open("../data/ace_swepam_1m.txt", "w") as locfh:
    for line in urlfh:
      line = line.decode('utf-8')
      locfh.write(line)

def getSolarPlasma():
  # Parse local data
  with open("../data/ace_swepam_1m.txt", "r") as fh:
    datas = {}
    units = {'density':'p/cc', 'speed':'km/s', 'temp':'K'}
    particles = {}
    label_list = ['density','speed','temp']
    stamp = []
    # Skip the first two lines, just boiler plate stuff
    next(fh)
    next(fh)
    # Iterator of Header
    for line in fh:
      if(line.startswith('#') and not(line.startswith('#-'))):
        pass
      else:
        # Stop decoding header
        break
    # Iterator of Data
    for line in fh:
      # Map out each data line to yr, mo, dy, hhmm, skip, skip, d0, d1, ... , dn
      # Zipping up the original sequence of labels with the remainder data
      # lines allows the for loop to then iterate through the new list
      (yr,mo,dy,time,blah1,blah2,blah3,*datarow) = line.split()
      stamp.append((str.join("",(yr,mo,dy)), time))
      for (key, value) in zip(label_list, datarow):
        if(key in datas):
          datas[key].append(float(value))
        else:
          datas[key] = [float(value)]
  # Format the Particles
  particle_tuple = zip(['Ion','Ion','Ion'], label_list)
  for (particle, key) in particle_tuple:
    particles[key] = (particle, units[key])
  # Now return the data
  return(label_list,datas,stamp,units,particles)

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

  # Get Geomagnetic Flux Data
  print("")
  print("------------------------------------")
  print("          Geomagnetic Flux")
  print("------------------------------------")
  (label_list,datas,stamp,units) = getGOESGeomagFieldFlux()
  print(label_list)
  print(datas)
  print(stamp)
  print(units)

  # Get Discrete Energetic Particle Flux Data
  print("")
  print("------------------------------------")
  print("  Discrete Energetic Particle Flux")
  print("------------------------------------")
  (label_list,datas,stamp,units,particles) = getGOESDiscreteParticleFlux()
  print(label_list)
  print(datas)
  print(stamp)
  print(units)
  print(particles)

  # # Get Integral Energetic Particle Flux Data
  print("")
  print("------------------------------------")
  print("   Integral Energetic Particle Flux")
  print("------------------------------------")
  (label_list,datas,stamp,units,particles) = getGOESIntegralParticleFlux()
  print(label_list)
  print(datas)
  print(stamp)
  print(units)
  print(particles)

  # Get XRay Flux Data
  print("")
  print("------------------------------------")
  print("           XRay Flux")
  print("------------------------------------")
  (label_list,datas,stamp,units,particles) = getGOESXrayFlux()
  print(label_list)
  print(datas)
  print(stamp)
  print(units)
  print(particles)

  # Get Differential Flux Data
  print("")
  print("------------------------------------")
  print("          Differential Flux")
  print("------------------------------------")
  (label_list,datas,stamp,units,particles) = getDiffElecProtFlux()
  print(label_list)
  print(datas)
  print(stamp)
  print(units)
  print(particles)

  # Get Integral Proton Flux Data
  print("")
  print("------------------------------------")
  print("  Integral High Energy Proton Flux")
  print("------------------------------------")
  (label_list,datas,stamp,units,particles) = getIntegralProtonFlux()
  print(label_list)
  print(datas)
  print(stamp)
  print(units)
  print(particles)

  # Get Interplanetary Magnetic Field Flux
  print("")
  print("------------------------------------")
  print("   Interplanetary Magnetic Field")
  print("------------------------------------")
  (label_list,datas,stamp) = getInterplanetMagField()
  print(label_list)
  print(datas)
  print(stamp)

  # Get Solar Wind Plasma
  print("")
  print("------------------------------------")
  print("         Solar Wind Plasma")
  print("------------------------------------")
  (label_list,datas,stamp,units,particles) = getSolarPlasma()
  print(label_list)
  print(datas)
  print(stamp)
  print(units)
  print(particles)
