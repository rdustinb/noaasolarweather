# This is the master view agent, it will display the local data files as graphs.
from support import filehandling, dataformat
import configparser

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

################################
# Draw a line graph inside an HTML Div
def drawFigure(thisTitle: str, thisYAxis: str, thisLegendTitle: str, thisColorTemplate: str):
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                dcc.Graph(
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
    # Append the plot to the layout array
    dbc_Row_array.append(dbc.Row([
        drawFigure(thisTitle=thisDataTypeName, thisYAxis='Flux', thisLegendTitle='Particle Energy', thisColorTemplate=colorMode)
    ], align='center'))
    dbc_Row_array.append(html.Br())

################################
# Create the Dash Application
app = Dash(external_stylesheets=[dbc.themes.SLATE])

# Define the layout of the webpage
app.layout = html.Div([
    html.Div(id="onload"),
    dbc.Card(
        dbc.CardBody(
            dbc_Row_array
        ), color = 'dark'
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
