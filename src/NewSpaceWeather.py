import pandas as pd

pd.set_option('display.mpl_style', 'default')

# Determine Start Date
start_date_YYYY = 2015
start_date_MM = 3
start_date_DD = 7

# Determine Length of Time in Days
day_length = 10

# Loop Through Number of Days
for dates in range(0,day_length):
  # Calculate Date Stamp
  date_stamp = ("%4d%02d%02d"%(start_date_YYYY,start_date_MM,(start_date_DD+dates)))
  # Create the List
  if(dates == 0):
    plotData = pd.read_table(
      ("http://legacy-www.swpc.noaa.gov/ftpdir/lists/xray/%s_Gp_xr_1m.txt"%(date_stamp)),
      sep=' ',
      skipinitialspace=True,
      parse_dates={'Time':[0,1,2,3]},
      names=['YY','MM','DD','HHMM','Short','Long'],
      usecols=[0,1,2,3,6,7],
      skiprows=19,
      na_values="-1.00e+05",
      index_col='Time'
      )
  else:
    plotData = plotData.append(
      pd.read_table(
        ("http://legacy-www.swpc.noaa.gov/ftpdir/lists/xray/%s_Gp_xr_1m.txt"%(date_stamp)),
        sep=' ',
        skipinitialspace=True,
        parse_dates={'Time':[0,1,2,3]},
        names=['YY','MM','DD','HHMM','Short','Long'],
        usecols=[0,1,2,3,6,7],
        skiprows=19,
        na_values="-1.00e+05",
        index_col='Time'
        )
      )

plotData.plot(figsize=(15, 10), legend=True, logy=True, stacked=True, title="xRay Flux", rot=45).yaxis.grid(True, which='Minor')
