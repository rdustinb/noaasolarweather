# This is the master view agent, it will display the local data files as graphs.
from support import filehandling, dataformat, timestamp
import configparser

#from dash import Dash, dcc, html, Input, Output, callback
import dash
import dash_bootstrap_components as dbc
from flask import Flask
import plotly.express as px

import subprocess

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
    
# Initially run the data agent, block until the initial fetch is complete...
data_process = subprocess.Popen(["python", "data_agent_master.py"])
output, error = data_process.communicate()

################################
# Draw a line graph inside an HTML Div
def drawFigure(plotDataDict: dict, thisTitle: str, thisYAxisTitle: str, thisXAxisTitle: str, thisLegendTitle: str):
    return  dash.html.Div([
        dbc.Card(
            dbc.CardBody([
                dash.dcc.Graph(
                    figure=px.line(
                        plotDataDict, x="time_tag", y=[thisY for thisY in plotDataDict.keys() if thisY != "time_tag"]
                    ).update_layout(
                        title=thisTitle,
                        yaxis_title=thisYAxisTitle,
                        xaxis_title=thisXAxisTitle,
                        legend_title=thisLegendTitle,
                        template='plotly_dark',
                        plot_bgcolor= 'rgba(0, 0, 0, 0)',
                        paper_bgcolor= 'rgba(0, 0, 0, 0)',
                    ).update_yaxes(
                        type="log"
                    ),
                    config={
                        'displayModeBar': False
                    }
                ),
            ])
        ),  
    ])

################################
# Create the Flask Server
server = Flask(__name__)

################################
# Create the Dash Application
app = dash.Dash(name="NOAA View Agent",
           server=server,
           external_stylesheets=[dbc.themes.SLATE, dbc.icons.FONT_AWESOME]
           )

# Define the layout of the webpage
app.layout = dash.html.Div([
    # Handle the view agent updates here...
    dbc.Card(
        dbc.CardBody(
            # This ID name calls to the callback below with the same name, every time the interval is reached
            id='view-live-update'
        ), color = 'dark'
    ),
    dash.dcc.Interval(
        id='view-interval',
        interval=1*60*1000, # in milliseconds
        n_intervals=0
    ),
    # Handle the data agent updates here...
    dbc.Card(
        dbc.CardBody(
            # This ID name calls to the callback below with the same name, every time the interval is reached
            id='data-live-update'
        ), color = 'dark'
    ),
    dash.dcc.Interval(
        id='data-interval',
        interval=15*60*1000, # in milliseconds
        n_intervals=0
    )
])

@dash.callback(dash.Output('data-live-update', 'children'),
              dash.Input('data-interval', 'n_intervals'))
def update_data(n):
    ################################
    # Update the data, fork to the background
    subprocess.Popen(["python", "data_agent_master.py"])

    dbc_Row_array = list()

    ################################
    # Get the configuration
    # Read the configuration file
    config          = configparser.ConfigParser()
    config.read('config.ini')
    
    # Access values from the configuration file
    localFolder     = config.get('general', 'local_formatted')
    dataTypes       = config.get('data', 'data_types').split()
    dataSpan        = config.get('view', 'data_span')

    for thisDataType in dataTypes:
        # Setup
        thisDataTypeName = ' '.join(thisDataType.split('-')).title()
        dataFilename = thisDataType+'-'+dataSpan+'.json'

        # Fetch the JSON archive for this data type
        dataDict = filehandling.getLocalData(localDataFolder=localFolder, localDataFilename=dataFilename)
        metaDataDict = dataDict["meta_data"]

        dbc_Row_array.append("%s last updated: %s"%(thisDataTypeName, metaDataDict["last_update"]))
        dbc_Row_array.append(dash.html.Br())

    # Create the Card Body
    return dbc_Row_array

@dash.callback(dash.Output('view-live-update', 'children'),
              dash.Input('view-interval', 'n_intervals'))
def update_view(n):
    ################################
    # Get the configuration
    # Read the configuration file
    config          = configparser.ConfigParser()
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

    ################################
    # Generate the plot data
    dbc_Row_array = list()

    print("Updating Dash application at "+timestamp.getTimestamp())
    
    for thisDataType in dataTypes:
        thisDataTypeName = ' '.join(thisDataType.split('-')).title()
        dataFilename = thisDataType+'-'+dataSpan+'.json'
        dataDict = filehandling.getLocalData(localDataFolder=localFolder, localDataFilename=dataFilename)
        plotDataDict = dataDict["plot_data"]
        metaDataDict = dataDict["meta_data"]
        ################
        # Clean the data arrays if they contain 0s
        for thisKey in [thisY for thisY in plotDataDict.keys() if thisY != "time_tag"]:
            plotDataDict[thisKey] = dataformat.cleanupData(thisDataArray=plotDataDict[thisKey], thisDetectionMethod=cleanDataMethod)
        ################
        # Convert the time_tag array to the local time
        if(localTimeData):
            plotDataDict["time_tag"] = timestamp.convertTimestamps(theseTimestamps=plotDataDict["time_tag"])
        # Append the plot to the layout array
        dbc_Row_array.append(dbc.Row([
            drawFigure(
                plotDataDict=plotDataDict,
                thisTitle=thisDataTypeName,
                thisYAxisTitle=metaDataDict['yAxisUnit'],
                thisXAxisTitle=None,
                thisLegendTitle=None
            )
        ], align='center'))
        dbc_Row_array.append(dash.html.Br())

    # Create the Card Body
    return dbc_Row_array

# This is only used when the view agent is run directly, rather than through gunicorn
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8080', debug=True)
