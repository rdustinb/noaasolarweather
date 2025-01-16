# This is the master view agent, it will display the local data files as graphs.
from support import filehandling
import configparser

from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

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

# Iris bar figure
def drawFigure(thisTitle: str, thisYAxis: str, thisLegendTitle: str):
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

dataType = "Differential Electrons"
dataFilename = '-'.join(dataType.lower().split(" "))+'-'+dataSpan+'.json'
dataDict = filehandling.getLocalData(localDataFolder=localFolder, localDataFilename=dataFilename)
plotDataDict = dataDict["plot_data"]
metaDataDict = dataDict["meta_data"]

# Dash Mode
app = Dash(external_stylesheets=[dbc.themes.SLATE])

app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    drawFigure(thisTitle=dataType, thisYAxis='Flux', thisLegendTitle='Particle Energy')
                ], width=12),
            ], align='center'),
            html.Br(),
        ]), color = 'dark'
    )
])

app.run_server(debug=True)
