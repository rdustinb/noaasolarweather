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
from matplotlib.legend_handler import HandlerPatch
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
    MyMplCanvas.__init__(self, left_edge=0.17, right_edge=0.82, top_edge=0.9,
        bottom_edge=0.18, *args, **kwargs)
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
    # Get the start date
    start_date = self.data["datestamp"][0].split(sep=":")[0]
    # Get the start date
    end_date = self.data["datestamp"][-1].split(sep=":")[0]
    # Strip only the timestamp out of the array of date/time stamps, keep only a few
    self.data["datestamp"] = [x.split(sep=":")[1] for x in self.data["datestamp"]]
    # Set the Plot Limits
    self.axes.autoscale(False)
    self.axes.set_xlim(0,360)
    # print(help(self.axes.set_xlim))
    self.axes.set_ylim(-90,90)
    # Remove data that is missing
    self.data["data"]["Bt"],self.data["data"]["Latitude"],  \
    self.data["data"]["Longitude"],self.data["datestamp"] = \
    zip(*[i for i in zip(                                   \
        self.data["data"]["Bt"],                            \
        self.data["data"]["Latitude"],                      \
        self.data["data"]["Longitude"],                     \
        self.data["datestamp"]                              \
      )                                                     \
      if i[0] != -999.9])
    # Calculate the smallest/largest mag field value to provide proper scaling
    smallest = min(self.data["data"]["Bt"])
    largest = max(self.data["data"]["Bt"])
    # Normalize values
    self.data["data"]["Bt"] = \
      [7*(3.14159*(t - smallest)**2) for t in self.data["data"]["Bt"]]
    # Create a color array
    pt_colors = [[1,0,0,i]                          \
      for i in [(1/len(self.data["data"]["Bt"]))*x  \
      for x in range(len(self.data["data"]["Bt"]))]]
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # Loop Through the individual plot values
    self.axes.scatter(
      self.data["data"]["Longitude"],
      self.data["data"]["Latitude"],
      s=self.data["data"]["Bt"],
      c=pt_colors, label=self.data["data"]["Bt"]
    )
    # Format the Graph
    self.axes.set_ylabel("Latitude (GSM)",
      fontsize=colors_and_globals.plotLabelSize)
    self.axes.set_xlabel("Longitude (GSM)",
      fontsize=colors_and_globals.plotLabelSize)
    # Show all plot grids
    self.axes.grid(True, which="both", color=colors_and_globals.grid_color)
    # Set the graph background color
    self.axes.set_axis_bgcolor(colors_and_globals.graph_bgcolor)
    # Set the Plot Title
    self.axes.set_title("Interplanetary Magnetic Field",
      fontsize=colors_and_globals.plotTitleSize)
    # Add Legend (time)
    newest = patches.Patch(color=(1,0,0), alpha=pt_colors[-1][3],
      ec='black', label=self.data["datestamp"][-1])
    oldest = patches.Patch(color=(1,0,0), alpha=pt_colors[1][3],
      ec='black', label=self.data["datestamp"][0])
    legend1 = self.axes.legend(
      handles=[newest,oldest],
      framealpha=0.1,
      loc=1, fontsize=colors_and_globals.legendSize,
      bbox_to_anchor=(1.27,1.12), title="Time")
    # Add Legend (size correlates to nT value)
    leg_small = patches.Circle(xy=(smallest,smallest), facecolor='none', edgecolor='none', label=str(smallest)+" nT")
    leg_large = patches.Circle(xy=(largest,largest), facecolor='none', edgecolor='none', label=str(largest)+" nT")
    legend2 = self.axes.legend(
      handles=[leg_small,leg_large],
      framealpha=0.1,
      loc=1, fontsize=colors_and_globals.legendSize,
      bbox_to_anchor=(1.27,0.81), title="Strength")
    self.axes.add_artist(legend1)
    self.axes.add_artist(legend2)
