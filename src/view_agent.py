# This is the master view agent, it will display the local data files as graphs.
from support import filehandling
import configparser
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go


################################
# Get the configuration
# Create a config parser object
config = configparser.ConfigParser()

# Read the configuration file
config.read('config.ini')

# Access values from the configuration file
pullAndUseLocalData         = config.getboolean('general', 'use_local')
localRawDataFolder          = config.get('general', 'local_raw')
localFormattedDataFolder    = config.get('general', 'local_formatted')
allDataSourceURLs           = config.get('sources', 'urls').split()

# Renders directly into a browser window
# Dependencies: pip3 install plotly pandas

fig = make_subplots(rows=3, cols=2)
row_index = 1
col_index = 1

for thisDataSourceURL in allDataSourceURLs:
    ################
    # Generate the local filename based off the URL... (is this a good idea?)
    thisDataFilename = thisDataSourceURL.split("/")[-1]
    ################
    # Store the Formatted Data
    dataDict = filehandling.getLocalData(localDataFolder=localFormattedDataFolder, localDataFilename=thisDataFilename)
    ################
    # Generate the Figure
    for thisKey in dataDict:
        if thisKey == "time_tag":
            next
        else:
            # Each energy for this data dictionary is added to the same plot row/col offset
            fig.add_trace(go.Scatter(x=dataDict["time_tag"], y=dataDict[thisKey], name=thisKey), row=row_index, col=col_index)
    ################
    # Update the Indices
    col_index += 1
    if col_index == 3:
        col_index = 1
        row_index += 1
        if row_index == 4:
            row_index = 1

fig.show()

# Runs as a Flash server webpage
# Dependencies: pip3 install plotly pandas dash
#from dash import Dash, dcc, html, Input, Output
#import json
#
#fig = px.line(
#    x=["a","b","c"], y=[1,3,2], # replace with your own data source
#    title="sample figure", height=325
#)
#
#app = Dash(__name__)
#
#app.layout = html.Div([
#    html.H4('Displaying figure structure as JSON'),
#    dcc.Graph(id="graph", figure=fig),
#    dcc.Clipboard(target_id="structure"),
#    html.Pre(
#        id='structure',
#        style={
#            'border': 'thin lightgrey solid', 
#            'overflowY': 'scroll',
#            'height': '275px'
#        }
#    ),
#])
#
#@app.callback(
#    Output("structure", "children"), 
#    Input("graph", "figure"))
#
#def display_structure(fig_json):
#    return json.dumps(fig_json, indent=2)
#
#app.run_server(debug=True)
