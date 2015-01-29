#!/Library/Frameworks/Python.framework/Versions/3.4/bin/python3

import urllib.request
import urllib.error

"""
    Locations of data that I want to capture and eventually graph. This data
    is provided from the GOES satellites. These satellites also have

    GOES Particle Flux
        http://services.swpc.noaa.gov/text/goes-particle-flux-primary.txt
    GOES Magnetometer
        http://services.swpc.noaa.gov/text/goes-magnetometer-primary.txt
    Proton Flux
        http://services.swpc.noaa.gov/text/goes-energetic-proton-flux-primary.txt
    xRay Imager:
        http://sxi.ngdc.noaa.gov
    xRay Flux
        http://services.swpc.noaa.gov/text/goes-xray-flux-primary.txt
    Coronograph Imager:
        http://lasco-www.nrl.navy.mil/index.php?p=content/realtime



    Lots of information about cross-contamination of Electron and Proton
    data as well as calculating the direction angle of the satellite that
    is taking the reqpective measurements here:
        http://www.swpc.noaa.gov/ftpdir/lists/magnetospheric/README.txt

    Loads more data to look at here:
        http://www.swpc.noaa.gov/Data/index.html#measurements
"""

def getXrayFlux():
    """
        Apparently the NOAA Data Site was restructured which could explain
        why I was having issues accessing data when I first started writing
        this script/application.
    """
    URL = 'http://services.swpc.noaa.gov/text/goes-xray-flux-primary.txt'
    fh = urllib.request.urlopen(URL)
    data_info = {}
    data_units = {}
    data_measurements = []
    data_long = []
    data_short = []
    data_timestamp = []
    data_ret = [data_info, data_units, data_short, data_long, data_timestamp, data_measurements]
    # Loop through the remote data file
    for read_line in fh.readlines():
        read_line = read_line.decode('utf-8').split()
        if(len(read_line) > 1):
            # Get the data samples
            if((read_line[0][0] != '#') and (read_line[0][0] != ':')):
                data_measurements.append(read_line)
                data_timestamp.append("%s/%s/%s:%s"%(read_line[0],read_line[1],read_line[2],read_line[3]))
                data_long.append(read_line[7])
                data_short.append(read_line[6])
            # Get some header info
            elif(read_line[1] == 'Label:'):
                data_info[str(read_line[2])] = ' '.join(map(str, read_line[read_line.index('=')+1:]))
            # Get some header info
            elif(read_line[1] == 'Units:'):
                data_units[str(read_line[2])] = ' '.join(map(str, read_line[read_line.index('=')+1:]))
    # Convert the data points from strings to numbers
    data_short = [float(i) for i in data_short]
    data_long = [float(i) for i in data_long]
    return data_ret


if __name__ == '__main__':
    alldata = getXrayFlux()
    # Dump final values
    # print("data_info dictionary is:")
    # print(alldata[0])
    # print("data_units dictionary is:")
    # print(alldata[1])
    print("data_short data is:")
    print(alldata[2])
    print("data_long data is:")
    print(alldata[3])
    print("data_timestamp data is:")
    print(alldata[4])
    # print("all_data data is:")
    # print(alldata[5])


