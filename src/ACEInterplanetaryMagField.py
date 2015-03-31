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
  datas = {}
  label_list = []
  stamp = []
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
    timer.start(60000)

  def compute_initial_figure(self):
    """
      Initial data plot.
    """
    # Get the new data
    (self.label_list,self.datas,self.stamp) = \
      NoaaApi.getInterplanetMagField()
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    self.axes.plot(0)
    self.axes.hold(True)
    # Set the Plot Limits
    # self.axes.autoscale(False)
    # self.axes.set_xlim(0,360)
    # self.axes.set_ylim(-90,90)
    # Remove data that is missing
    self.datas["Total"],self.datas["Latitude"],  \
    self.datas["Longitude"],self.stamp = \
    zip(*[i for i in zip(                                   \
        self.datas["Total"],                            \
        self.datas["Latitude"],                      \
        self.datas["Longitude"],                     \
        self.stamp                              \
      )                                                     \
      if i[0] != -999.9])
    # Calculate the smallest/largest mag field value to provide proper scaling
    smallest = min(self.datas["Total"])
    largest = max(self.datas["Total"])
    # Normalize values
    self.datas["Total"] = \
      [7*(3.14159*(t - smallest)**2) for t in self.datas["Total"]]
    # Create a color array
    pt_colors = [[1,0,0,i]                          \
      for i in [(1/len(self.datas["Total"]))*x  \
      for x in range(len(self.datas["Total"]))]]
    # Loop Through the individual plot values
    self.axes.scatter(
      self.datas["Longitude"],
      self.datas["Latitude"],
      s=self.datas["Total"],
      c=pt_colors, label=self.datas["Total"]
    )
    # Format the Graph
    self.format_graph(pt_colors,smallest,largest)

  def format_graph(self,pt_colors,smallest,largest):
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
      ec='black', label=self.stamp[-1][1])
    oldest = patches.Patch(color=(1,0,0), alpha=pt_colors[1][3],
      ec='black', label=self.stamp[0][1])
    legend1 = self.axes.legend(
      handles=[newest,oldest],
      framealpha=0.1,
      loc=1, fontsize=colors_and_globals.legendSize,
      bbox_to_anchor=(1.27,1.12), title="Time")
    # Add Legend (size correlates to nT value)
    # leg_small = patches.Circle(xy=(smallest,smallest), facecolor='none', edgecolor='none', label=str(smallest)+" nT")
    # leg_large = patches.Circle(xy=(largest,largest), facecolor='none', edgecolor='none', label=str(largest)+" nT")
    # legend2 = self.axes.legend(
    #   handles=[leg_small,leg_large],
    #   framealpha=0.1,
    #   loc=1, fontsize=colors_and_globals.legendSize,
    #   bbox_to_anchor=(1.27,0.81), title="Strength")
    self.axes.add_artist(legend1)
    # self.axes.add_artist(legend2)
