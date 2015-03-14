from MyMplCanvas import MyMplCanvas
import NoaaApi
import numpy
import colors_and_globals
"""
  As of MatPlotLib 1.5 qt4_compat will be deprecated for the more general
  qt_compat. Pulling that in instead.
"""
from matplotlib.backends import qt_compat
from matplotlib import patches
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
    self.data["data"]["Bt"],self.data["data"]["Latitude"],self.data["data"]["Longitude"],self.data["datestamp"] = zip(*[i for i in zip(self.data["data"]["Bt"],self.data["data"]["Latitude"],self.data["data"]["Longitude"],self.data["datestamp"]) if i[0] != -999.9])
    # Calculate the smallest mag field value to provide proper scaling
    smallest = abs(min(self.data["data"]["Bt"])) + 0.1
    # Normalize values
    self.data["data"]["Bt"] = [2*(t + smallest) for t in self.data["data"]["Bt"]]
    # Create a color array
    pt_colors = [[1,0,0,i] for i in [(1/len(self.data["data"]["Bt"]))*x for x in range(len(self.data["data"]["Bt"]))]]
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # Loop Through the individual plot values
    self.axes.scatter(self.data["data"]["Longitude"],self.data["data"]["Latitude"],s=self.data["data"]["Bt"],c=pt_colors)
    # Format the Graph
    self.axes.set_ylabel("Latitude", fontsize=colors_and_globals.plotLabelSize)
    self.axes.set_xlabel("Longitude", fontsize=colors_and_globals.plotLabelSize)
    # Show all plot grids
    self.axes.grid(True, which="both", color=colors_and_globals.grid_color)
    # Set the graph background color
    self.axes.set_axis_bgcolor(colors_and_globals.graph_bgcolor)
    # Set the Plot Title
    self.axes.set_title("Interplanetary Magnetic Field", fontsize=colors_and_globals.plotTitleSize)
    # Add Legend
    # print(pt_colors[-1])
    # print(pt_colors[0])
    # newest = patches.Patch(color=str(pt_colors[-1]), label=self.data["datestamp"][-1])
    # oldest = patches.Patch(color=str(pt_colors[0]), label=self.data["datestamp"][0])
    # legend1 = self.axes.legend(
    #   handles=[newest,oldest],
    #   framealpha=0.1,
    #   loc=1, fontsize=colors_and_globals.legendSize, bbox_to_anchor=(1.22,1.12), title="Colors")
    # self.axes.add_artist(legend1)


