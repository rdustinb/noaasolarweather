# This is the master view agent, it will display the local data files as graphs.
from support import filehandling, colors
import configparser
from dash import Dash, dcc, html, Input, Output
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
pullAndUseLocalData         = config.getboolean('general', 'use_local')
localRawDataFolder          = config.get('general', 'local_raw')
localFormattedDataFolder    = config.get('general', 'local_formatted')
guiStyle                    = config.get('general', 'gui_style')
allDataSourceURLs           = config.get('sources', 'urls').split()
showGui                     = config.getboolean('debug', 'show_gui')

################################
# Using Graph Objects
if guiStyle == "Go":
    # Generate all the Subplots from all the Data
    fig = make_subplots(
        rows=3,
        cols=2,
        specs=[
            [{"colspan": 2}, None],
            [{}, {}],
            [{}, {}],
            ],
        subplot_titles=[thisDataFilename.split("/")[-1].split(".")[0].replace("-"," ").split("1")[0].title() for thisDataFilename in allDataSourceURLs]
        )
    
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
        # Get the color family
        thisColorSet = colors.getColorSet(len(dataDict)-1)
        ################
        # Generate the Figure
        for thisKey in dataDict:
            if thisKey == "time_tag":
                next
            else:
                # Each energy for this data dictionary is added to the same plot row/col offset
                fig.add_trace(
                    go.Scatter(
                        x=dataDict["time_tag"],
                        y=dataDict[thisKey],
                        name=thisKey,
                        mode='lines',
                        line=dict(
                            color=thisColorSet[0],
                            width=2
                        )
                    ),
                    row=row_index,
                    col=col_index
                )
                # Shift off the color at index 0
                thisColorSet = thisColorSet[1:]
        ################
        # Change this subplot to logarithmic
        fig.update_yaxes(type="log", row=row_index, col=col_index)
        ################
        # Update the Indices
        col_index += 1
        # first row is different...
        if col_index == 3 or row_index == 1:
            col_index = 1
            row_index += 1
            if row_index == 4:
                row_index = 1
    
    # Show the figure...
    if showGui:
        fig.show()

# Using Graph Objects
if guiStyle == "Dash":
    fig1 = px.line(
        x=["a","b","c"], y=[1,3,2], # replace with your own data source
        title="sample 1 figure", height=325
    )
    fig2 = px.line(
        x=["d","e","f"], y=[4,1,2], # replace with your own data source
        title="sample 2 figure", height=325
    )
    fig3 = px.line(
        x=["a","b","c"], y=[3,1,1], # replace with your own data source
        title="sample 3 figure", height=325
    )
    
    app = Dash(__name__)
    
    app.layout = html.Div([
        html.H4('Displaying figure structure as JSON'),
        dcc.Graph(id="graph", figure=fig1),
        dcc.Graph(id="graph", figure=fig2),
        dcc.Graph(id="graph", figure=fig3),
        dcc.Clipboard(target_id="structure"),
        html.Pre(
            id='structure',
            style={
                'border': 'thin lightgrey solid', 
                'overflowY': 'scroll',
                'height': '275px'
            }
        ),
    ])

    @app.callback(
        Output("structure", "children"), 
        Input("graph", "figure"))
    
    # This is required though not called directly here...
    def display_structure(fig_json):
        return json.dumps(fig_json, indent=2)

    app.run_server(debug=True)
