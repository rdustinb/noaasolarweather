# This is the master view agent, it will display the local data files as graphs.
from support import filehandling, dataformat, timestamp
import configparser

#from dash import Dash, dcc, html, Input, Output, callback
import dash
import dash_bootstrap_components as dbc
from flask import Flask
import plotly.express as px

################################
# Draw a line graph inside an HTML Div
def drawFigure(plotDataDict: dict, thisTitle: str, thisYAxis: str, thisLegendTitle: str):
    return  dash.html.Div([
        dbc.Card(
            dbc.CardBody([
                dash.dcc.Graph(
                    figure=px.line(
                        plotDataDict, x="time_tag", y=[thisY for thisY in plotDataDict.keys() if thisY != "time_tag"]
                    ).update_layout(
                        title=thisTitle,
                        yaxis_title=thisYAxis,
                        xaxis_title=None,
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
    dbc.Card(
        dbc.CardBody(
            # This ID name calls to the callback below with the same name, every time the interval is reached
            id='live-update-text'
        ), color = 'dark'
    ),
    dash.dcc.Interval(
        id='interval-component',
        interval=60*1000, # in milliseconds
        n_intervals=0
    )
])

# Multiple components can update everytime interval gets fired.
@dash.callback(dash.Output('live-update-text', 'children'),
              dash.Input('interval-component', 'n_intervals'))
def update_graph_settings(n):
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
            drawFigure(plotDataDict=plotDataDict, thisTitle=thisDataTypeName, thisYAxis=metaDataDict['yAxisUnit'], thisLegendTitle='Particle Energy')
        ], align='center'))
        dbc_Row_array.append(dash.html.Br())

    # Create the Card Body
    return dbc_Row_array

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port='8080', debug=True)
