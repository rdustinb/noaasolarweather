"""
  This script pulls from the archived 30-day list of text files for as many
  sources as is desired. This script parses all available data files, only
  concatenating the actual data into a single text file.

  The date format for the files is:
    YYYYMMDD_<Gp/Gs/ace>_<xr/pchan/part/swepam/sis/mag/epam>_<5m/1m>.txt

    Where Gp is for GOES-13 at location 75 West.
    Where Gs is for GOES-15 at location 134 West.
    Where ace is for ACE which has a variable location.

    Where xr is for the X-Ray Flux data.
    Where pchan is for the Differential Proton Flux data.
    Where part is for the Integral Electron/Proton Flux data.
    Where swepam is for the Solar Wind Plasma data.
    Where sis is for the High Energy Solar Proton Flux data.
    Where mag is for the Interplanetary Megnetic Field data.
    Where epam is for the Differential Electron/Proton Flux data.

    Where 5m is for 5-minute updated data files.
    Where 1m is for 1-minute updated data files.

  The currently known 30-day archived GOES data is located in the following
  URL locations:

    http://legacy-www.swpc.noaa.gov/ftpmenu/lists/xray.html
    http://legacy-www.swpc.noaa.gov/ftpmenu/lists/pchan.html
    http://legacy-www.swpc.noaa.gov/ftpmenu/lists/particle.html

  To find a specific date of data, remove the <foo>.html file and utilize the
  file format mentioned above for that particular folder. For instance:

    http://legacy-www.swpc.noaa.gov/ftpmenu/lists/xray/20150105_Gp_xr_5m.txt

  Will access the GOES-15 X-Ray Flux satellite data from 2015/01/05.
"""