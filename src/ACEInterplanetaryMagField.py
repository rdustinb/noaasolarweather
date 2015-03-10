from MyMplCanvas import MyMplCanvas
import NoaaApi
import numpy
import colors_and_globals
"""
  As of MatPlotLib 1.5 qt4_compat will be deprecated for the more general
  qt_compat. Pulling that in instead.
"""
from matplotlib.backends import qt_compat
"""
  Branch using PyQt or PySide based on MatPlotLib values.
"""
if(qt_compat.QT_API == qt_compat.QT_API_PYSIDE):
  from PySide import QtGui, QtCore
else:
  from PyQt4 import QtGui, QtCore

###########################################################################
# Specific Plot Canvas Objects
###########################################################################
class MyInterplanetaryMagField(MyMplCanvas):
  data = ""
  """
    Initialize the updating object.
  """
  def __init__(self, *args, **kwargs):
    MyMplCanvas.__init__(self, left_edge=0.15, right_edge=0.82, top_edge=0.9, bottom_edge=0.18, *args, **kwargs)
    timer = QtCore.QTimer(self)
    # Tie the "update_figure" function to the timer
    timer.timeout.connect(self.update_figure)
    # Millisecond Timer, Assign the update time based on the value returned by
    # the API call, store the API call data in an object-global data variable
    # to reduce the number of API calls required to initialize the plot
    timer.start(self.data["update"])

  def compute_initial_figure(self):
    """
      Initial data plot.
    """
    # Get the new data
    self.data = NoaaApi.getInterplanetMagField()
    # Set the Plot Limits
    self.axes.autoscale(False)
    self.axes.set_xlim(0,360)
    # print(help(self.axes.set_xlim))
    self.axes.set_ylim(-90,90)
    # Remove data that is missing
    self.data["data"]["Bt"]         = [t for t in self.data["data"]["Bt"]         if(t) != -999.9]
    self.data["data"]["Latitude"]   = [l for l in self.data["data"]["Latitude"]   if(l) != -999.9]
    self.data["data"]["Longitude"]  = [l for l in self.data["data"]["Longitude"]  if(l) != -999.9]
    # Calculate the smallest mag field value to provide proper scaling
    smallest = abs(min(self.data["data"]["Bt"])) + 0.1
    # Normalize values
    self.data["data"]["Bt"] = [2*(t + smallest) for t in self.data["data"]["Bt"]]
    # Create an alpha array
    pt_colors = [(1/len(self.data["data"]["Bt"]))*x for x in range(len(self.data["data"]["Bt"]))]
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # Loop Through the individual plot values
    self.axes.scatter(self.data["data"]["Longitude"],self.data["data"]["Latitude"],s=self.data["data"]["Bt"],alpha=0.5,c=pt_colors)
    # Format the Graph
    self.axes.set_ylabel("Latitude", fontsize=colors_and_globals.plotLabelSize)
    self.axes.set_xlabel("Longitude", fontsize=colors_and_globals.plotLabelSize)
    # Show all plot grids
    self.axes.grid(True, which="both", color=colors_and_globals.grid_color)
    # Set the graph background color
    self.axes.set_axis_bgcolor(colors_and_globals.graph_bgcolor)
    # Set the Plot Title
    self.axes.set_title("Interplanetary Magnetic Field", fontsize=colors_and_globals.plotTitleSize)

