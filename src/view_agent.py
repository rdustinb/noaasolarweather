# This is the master view agent, it will display the local data files as graphs.
from support import filehandling, dataformat, timestamp, colors
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
localFolder     = config.get('general', 'local_formatted')
showGui         = config.getboolean('view', 'show_gui')
guiStyle        = config.get('view', 'gui_style')
dataTypes       = config.get('view', 'data_types').split()
dataFilters     = config.get('view', 'data_filters').split()
dataSpan        = config.get('view', 'data_span')
colorMode       = config.get('view', 'color_mode')
localTimeData   = config.getboolean('view', 'local_time_data')
cleanDataMethod = config.get('view', 'clean_data_method')

templates = ("plotly", "plotly_white", "plotly_dark", "ggplot2", "seaborn", "simple_white", "none")

# Generate the full URLs
allSourceFiles  = [thisType+"-"+dataSpan+".json" for thisType in dataTypes]

################################
# Using Graph Objects
if guiStyle == "Go":
    # Generate all the Subplots from all the Data
    fig = make_subplots(
        rows=3,
        cols=2,
        specs=[
            [{}, {}],
            #[{"colspan": 2}, None],
            [{}, {}],
            [{}, {}],
            ]#,
        #subplot_titles=[thisSourceFile.replace(dataSpan, " ").split(".")[0].replace("-"," ").title() for thisSourceFile in allSourceFiles]
        )
    
    row_index = 1
    col_index = 1

    for (thisSourceFilter,thisSourceFile) in zip(dataFilters,allSourceFiles):
        print("Data key filter is set to: %s"%(thisSourceFilter))
        ################
        # Store the Formatted Data
        dataDict = filehandling.getLocalData(localDataFolder=localFolder, localDataFilename=thisSourceFile)
        ################
        # Convert the time_tag array to the local time
        if(localTimeData):
            dataDict["time_tag"] = timestamp.convertTimestamps(theseTimestamps=dataDict["time_tag"])
        ################
        # Get the color family (only request colors for the keys which have data in them)
        thisColorSet = colors.getColorSet(len(dataDict["data_keys"]))
        ################
        # Generate the Figure
        for thisKey in dataDict:
            # Skip the Time Tag array and the Last Update information
            if (thisSourceFilter == "all" or thisSourceFilter in thisKey) and thisKey in dataDict["data_keys"]:
                print("Plotting data key %s"%(thisKey))
                ################
                # Clean the data arrays if they contain 0s
                dataDict[thisKey] = dataformat.cleanupData(thisDataArray=dataDict[thisKey], thisDetectionMethod=cleanDataMethod)
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
                thisColorSet = thisColorSet[1:]
        # Create the Title and Subtitle
        thisTitle = thisSourceFile.replace(dataSpan, " ").split(".")[0].replace("-"," ").title()
        thisSubTitle = "<br><sup>Last Updated: %s</sup>"%(dataDict["last_update"])
        fig.add_annotation(
            xref="x domain",
            yref="y domain",
            x=0.5, 
            y=1.2, 
            showarrow=False,
            text="%s %s"%(thisTitle,thisSubTitle), 
            row=row_index, 
            col=col_index
        )
        ################
        # Change this subplot to logarithmic
        fig.update_yaxes(type="log", row=row_index, col=col_index)
        ################
        # Update the Indices
        col_index += 1
        # first row is different...
        if col_index == 3: # or row_index == 1:
            col_index = 1
            row_index += 1
            if row_index == 4:
                row_index = 1

    # Disable the Legend as it is too cluttered being a single legend for all subplots
    fig.update(layout_showlegend=False)

    # Make the hover annotations legible
    fig.update_layout(hovermode="x") # This one adds "thought bubbles" at each data point where the cursor is
    #fig.update_layout(hovermode="x unified") # This one adds a "floating legend" at the x position where the cursor is
    
    # Show the figure...
    if showGui:
        fig.layout.template = colorMode
        fig.show()

# Other View GUIs are not currently supported
else:
    print("Other GUI modes are not currently supported, please change config.ini to use Go")

# Using Dash Server
#if guiStyle == "Dash":
#    fig1 = px.line(
#        x=["a","b","c"], y=[1,3,2], # replace with your own data source
#        title="sample 1 figure", height=325,
#        template="plotly_dark"
#    )
#    fig2 = px.line(
#        x=["d","e","f"], y=[4,1,2], # replace with your own data source
#        title="sample 2 figure", height=325,
#        template="plotly_dark"
#    )
#    fig3 = px.line(
#        x=["a","b","c"], y=[3,1,1], # replace with your own data source
#        title="sample 3 figure", height=325,
#        template="plotly_dark"
#    )
#    
#    app = Dash(__name__)
#    
#    app.layout = html.Div([
#        html.H4('Displaying figure structure as JSON'),
#        dcc.Graph(id="graph1", figure=fig1),
#        dcc.Graph(id="graph2", figure=fig2),
#        dcc.Graph(id="graph3", figure=fig3),
#        dcc.Clipboard(target_id="structure"),
#        html.Pre(
#            id='structure',
#            style={
#                'border': 'thin lightgrey solid', 
#                'overflowY': 'scroll',
#                'height': '275px'
#            }
#        ),
#    ])
#
#    @app.callback(
#        Output("structure", "children"), 
#        Input("graph1", "figure"),
#        Input("graph2", "figure"),
#        Input("graph3", "figure"),
#        )
#    
#    # This is required though not called directly here...
#    def display_structure(fig_json):
#        return json.dumps(fig_json, indent=2)
#
#    app.run_server(debug=True)
