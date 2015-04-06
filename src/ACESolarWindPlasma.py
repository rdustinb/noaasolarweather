from MyMplCanvas import MyMplCanvas
from numpy import linspace
from NoaaApi import storeSolarPlasma
from NoaaApi import getSolarPlasma
import colors_and_globals
"""
  As of MatPlotLib 1.5 qt4_compat will be deprecated for the more general
  qt_compat. Pulling that in instead.
"""
from matplotlib.backends.qt_compat import QT_API
from matplotlib.backends.qt_compat import QT_API_PYSIDE
"""
  Branch using PyQt or PySide based on MatPlotLib values.
"""
if(QT_API == QT_API_PYSIDE):
  from PySide.QtCore import QTimer
else:
  from PyQt4.QtCore import QTimer

###########################################################################
# Specific Plot Canvas Objects
###########################################################################
class MySolarWindPlasma(MyMplCanvas):
  datas = {}
  units = ""
  particles = {}
  label_list = []
  stamp = []
  def __init__(self, *args, **kwargs):
    """
      Initialize the updating object.
    """
    MyMplCanvas.__init__(self, right_edge=0.84, *args, **kwargs)
    timer = QTimer(self)
    # Tie the "update_figure" function to the timer
    timer.timeout.connect(self.update_figure)
    # Millisecond Timer, Assign the update time based on the value returned by
    # the API call, store the API call data in an object-global data variable
    # to reduce the number of API calls required to initialize the plot
    timer.start(60000)
    storeSolarPlasma()
    self.compute_initial_figure()

  def update_figure(self):
    """
      This is the actual timer updating method.
    """
    # Update the graph data
    storeSolarPlasma()
    # Call the compute initial function, only difference is the .draw() method below
    self.compute_initial_figure()
    # Redraw plots
    self.draw()

  def compute_initial_figure(self):
    """
      Initial data plot.
    """
    # Get the new data
    (self.label_list,self.datas,self.stamp,self.units,self.particles) = \
      getSolarPlasma()
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    self.axes.plot(0)
    self.axes.hold(True)
    # Plot all data sets
    plot1 = [self.axes.plot(linspace(0,1,len(self.stamp)), self.datas[key],
      colors_and_globals.ACESolarWindPlasmaColors[key],
      label=self.particles[key][1]
      ) for key in self.label_list]
    # Format the Graph
    self.format_graph()

  def format_graph(self):
    # Set the graph background color
    self.axes.set_axis_bgcolor(colors_and_globals.graph_bgcolor)
    # Change Plot to logarithmic
    self.axes.set_yscale("log")
    # Show all plot grids
    self.axes.grid(True, which="both", color=colors_and_globals.grid_color)
    # Thin the number of x-axis labels and ticks, this works with the list of
    # tuples that are the date/time stamps
    thinner = int(len(self.stamp)/11)
    self.stamp = [x \
      for x in self.stamp[0::thinner]
    ]
    # Set number of X-Axis ticks
    self.axes.set_xticks(linspace(0,1,len(self.stamp)))
    # Separate dates and times
    (dates,times) = zip(*self.stamp)
    # Change the plot tick labels
    if(colors_and_globals.plot_angle.find("-") != -1):
      self.axes.set_xticklabels(times,
        rotation=colors_and_globals.plot_angle, rotation_mode='anchor',
        horizontalalignment='left', fontsize=colors_and_globals.plotLabelSize)
    else:
      self.axes.set_xticklabels(times,
        rotation=colors_and_globals.plot_angle, rotation_mode='anchor',
        horizontalalignment='right', fontsize=colors_and_globals.plotLabelSize)
    # Show Units of y-axis
    self.axes.set_ylabel("Density, Speed, Temperature", rotation='vertical',
      fontsize=colors_and_globals.plotLabelSize)
    # Show Units of x-axis
    if(dates[0] != dates[-1]):
      self.axes.set_xlabel(("UTC Time (%s - %s)"%(dates[0],dates[-1])),
        fontsize=colors_and_globals.plotLabelSize)
    else:
      self.axes.set_xlabel(("UTC Time (%s)"%(dates[-1])),
        fontsize=colors_and_globals.plotLabelSize)
    # Set the Plot Title
    self.axes.set_title("Solar Wind Plasma", fontsize=colors_and_globals.plotTitleSize)
    # class matplotlib.legend.Legend(parent, handles, labels, loc=None,
    # numpoints=None, markerscale=None, scatterpoints=None, scatteryoffsets=None,
    # prop=None, fontsize=None, borderpad=None, labelspacing=None, handlelength=None,
    # handleheight=None, handletextpad=None, borderaxespad=None, columnspacing=None,
    # ncol=1, mode=None, fancybox=None, shadow=None, title=None, framealpha=None,
    # bbox_to_anchor=None, bbox_transform=None, frameon=None, handler_map=None)
    # Create the legends
    legend1 = self.axes.legend(
      framealpha=0,
      loc=1, fontsize=colors_and_globals.legendSize,
      bbox_to_anchor=(1.25, 1.12),
      title="Params")
    self.axes.add_artist(legend1)
