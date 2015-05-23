import pandas as pd

pd.set_option('display.mpl_style', 'default')

fixed_data = pd.read_table(
  'http://legacy-www.swpc.noaa.gov/ftpdir/lists/xray/20150310_Gp_xr_1m.txt',
  sep=' ',
  skipinitialspace=True,
  parse_dates={'Time':[0,1,2,3]},
  names=['YY','MM','DD','HHMM','Short','Long'],
  usecols=[0,1,2,3,6,7],
  skiprows=19,
  na_values="-1.00e+05",
  index_col='Time')

fixed_data = fixed_data.append(
  pd.read_table(
    'http://legacy-www.swpc.noaa.gov/ftpdir/lists/xray/20150311_Gp_xr_1m.txt',
    sep=' ',
    skipinitialspace=True,
    parse_dates={'Time':[0,1,2,3]},
    names=['YY','MM','DD','HHMM','Short','Long'],
    usecols=[0,1,2,3,6,7],
    skiprows=19,
    na_values="-1.00e+05",
    index_col='Time')
  )

fixed_data = fixed_data.append(
  pd.read_table(
    'http://legacy-www.swpc.noaa.gov/ftpdir/lists/xray/20150312_Gp_xr_1m.txt',
    sep=' ',
    skipinitialspace=True,
    parse_dates={'Time':[0,1,2,3]},
    names=['YY','MM','DD','HHMM','Short','Long'],
    usecols=[0,1,2,3,6,7],
    skiprows=19,
    na_values="-1.00e+05",
    index_col='Time')
  )

fixed_data.plot(figsize=(15, 10), legend=True, logy=True, stacked=True, title="xRay Flux", rot=45).yaxis.grid(True, which='Minor')
