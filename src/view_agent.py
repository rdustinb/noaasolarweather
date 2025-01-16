# This is the master view agent, it will display the local data files as graphs.
from support import filehandling, dataformat, timestamp, colors
import configparser
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import json

################################
# Get the configuration
# Create a config parser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Access values from the configuration file
localFolder     = config.get('general', 'local_formatted')
showGui         = config.getboolean('view', 'show_gui')
guiStyle        = config.get('view', 'gui_style')
dataTypes       = config.get('view', 'data_types').split()
dataFilters     = config.get('view', 'data_filters').split()
dataSpan        = config.get('view', 'data_span')
colorMode       = config.get('view', 'color_mode')
localTimeData   = config.getboolean('view', 'local_time_data')
cleanDataMethod = config.get('view', 'clean_data_method')

# Generate the full URLs
allSourceFiles  = [thisType+"-"+dataSpan+".json" for thisType in dataTypes]

# Iris bar figure
def drawFigure():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
                    figure=px.line(
                        df, x="time_tag", y="1000-1900 keV"
                    )
                ) 
            ])
        ),  
    ])

# Full Dictionary:
#   "last_update": string
#   "time_tag": list()
#   "data_keys": list()
#   "data_name": string
#   "<energy val 0>": list()
#   "<energy val 1>": list()
#       ...
#   "<energy val 2>": list()

# Data Dictionary:
#   "time_tag": list()
#   "<energy val 0>": list()
#   "<energy val 1>": list()
#       ...
#   "<energy val 2>": list()

df = filehandling.getLocalData(localDataFolder=localFolder, localDataFilename="differential-electrons-6-hour.json")
df.pop("last_update", None)
df.pop("data_keys", None)
df.pop("data_name", None)


#print(len(df["time_tag"]))
#print(len(df["1000-1900 keV"]))
#print(len(df["115-165 keV"]))
#print(len(df["165-235 keV"]))
#print(len(df["1900-3200 keV"]))
#print(len(df["235-340 keV"]))
#print(len(df["3200-6500 keV"]))
#print(len(df["340-500 keV"]))
#print(len(df["500-700 keV"]))
#print(len(df["700-1000 keV"]))
#print(len(df["80-115 keV"]))

# Dash Mode
app = Dash(external_stylesheets=[dbc.themes.SLATE])

app.layout = html.Div([
    dbc.Card(
        drawFigure()
    )
])

app.run_server(debug=True)
