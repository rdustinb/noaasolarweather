from MyMplCanvas import MyMplCanvas
from numpy import linspace
from NoaaApi import storeGOESIntegralParticleFlux
from NoaaApi import getGOESIntegralParticleFlux
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
class MyGOESIntegralParticleFlux(MyMplCanvas):
  def __init__(self, *args, **kwargs):
    """
      Initialize the updating object.
    """
    MyMplCanvas.__init__(self, *args, **kwargs)
    timer = QTimer(self)
    # Tie the "update_figure" function to the timer
    timer.timeout.connect(self.update_figure)
    # Millisecond Timer, Assign the update time based on the value returned by
    # the API call, store the API call data in an object-global data variable
    # to reduce the number of API calls required to initialize the plot
    timer.start(300000)
    storeGOESIntegralParticleFlux()
    self.compute_initial_figure()

  def update_figure(self):
    """
      This is the actual timer updating method.
    """
    # Update the graph data
    storeGOESIntegralParticleFlux()
    # Call the compute initial function, only difference is the .draw() method below
    self.compute_initial_figure()
    # Redraw plots
    self.draw()

  def compute_initial_figure(self):
    """
      Initial data plot.
    """
    # Get the new data
    (label_list,datas,stamp,units,particles) = getGOESIntegralParticleFlux()
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    self.axes.plot(0)
    self.axes.hold(True)
    # Plot all data sets
    plot1 = [self.axes.plot(linspace(0,1,len(stamp)), datas[key],
      colors_and_globals.GOESIntegralParticleFluxColors[key],
      label=particles[key][1]
      ) for key in label_list]
    # Format the Graph
    self.format_graph(stamp)

  def format_graph(self,stamp):
    # Set the graph background color
    self.axes.set_axis_bgcolor(colors_and_globals.graph_bgcolor)
    # Change Plot to logarithmic
    self.axes.set_yscale("log")
    # Show all plot grids
    self.axes.grid(True, which="both", color=colors_and_globals.grid_color)
    # Thin the number of x-axis labels and ticks, this works with the list of
    # tuples that are the date/time stamps
    if(len(stamp) > 11):
      thinner = int(len(stamp)/11)
    else:
      thinner = 1
    stamp = [x \
      for x in stamp[0::thinner]
    ]
    # Set number of X-Axis ticks
    self.axes.set_xticks(linspace(0,1,len(stamp)))
    # Separate dates and times
    (dates,times) = zip(*stamp)
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
    self.axes.set_ylabel("Particles / (cm2*s*sr*MeV)", rotation='vertical',
      fontsize=colors_and_globals.plotLabelSize)
    # Show Units of x-axis
    if(dates[0] != dates[-1]):
      self.axes.set_xlabel(("UTC Time (%s - %s)"%(dates[0],dates[-1])),
        fontsize=colors_and_globals.plotLabelSize)
    else:
      self.axes.set_xlabel(("UTC Time (%s)"%(dates[-1])),
        fontsize=colors_and_globals.plotLabelSize)
    # Set the Plot Title
    self.axes.set_title("Integral Particle Flux", fontsize=colors_and_globals.plotTitleSize)
    # class matplotlib.legend.Legend(parent, handles, labels, loc=None,
    # numpoints=None, markerscale=None, scatterpoints=None, scatteryoffsets=None,
    # prop=None, fontsize=None, borderpad=None, labelspacing=None, handlelength=None,
    # handleheight=None, handletextpad=None, borderaxespad=None, columnspacing=None,
    # ncol=1, mode=None, fancybox=None, shadow=None, title=None, framealpha=None,
    # bbox_to_anchor=None, bbox_transform=None, frameon=None, handler_map=None)
    # Create the legends
    self.axes.legend(
      framealpha=0, title="MeV",
      bbox_to_anchor=(1.24, 1.12), loc=1,
      fontsize=colors_and_globals.legendSize)
