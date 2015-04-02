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
class MyGOESXrayFlux(MyMplCanvas):
  datas = {}
  units = ""
  particles = {}
  label_list = []
  stamp = []
  def __init__(self, *args, **kwargs):
    """
      Initialize the updating object.
    """
    MyMplCanvas.__init__(self, *args, **kwargs)
    timer = QtCore.QTimer(self)
    # Tie the "update_figure" function to the timer
    timer.timeout.connect(self.update_figure)
    # Millisecond Timer, Assign the update time based on the value returned by
    # the API call, store the API call data in an object-global data variable
    # to reduce the number of API calls required to initialize the plot
    timer.start(60000)
    self.compute_initial_figure()

  def update_figure(self):
    """
      This is the actual timer updating method.
    """
    # Update the graph data
    NoaaApi.storeGOESXrayFlux()
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
      NoaaApi.getGOESXrayFlux()
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    self.axes.plot(0)
    self.axes.hold(True)
    # Plot all data sets
    plot1 = [self.axes.plot(numpy.linspace(0,1,len(self.stamp)), self.datas[key],
      colors_and_globals.GOESXrayFluxColors[key],
      label=self.particles[key][1]
      ) for key in self.label_list]
    # Add Highlighting for flares
    R1 = numpy.repeat(numpy.array(10e-6), len(self.stamp))
    R2 = numpy.repeat(numpy.array(50e-6), len(self.stamp))
    R3 = numpy.repeat(numpy.array(10e-5), len(self.stamp))
    R4 = numpy.repeat(numpy.array(10e-4), len(self.stamp))
    R5 = numpy.repeat(numpy.array(20e-4), len(self.stamp))
    # Test Data
    # R1 = numpy.repeat(numpy.array(10e-10), len(self.stamp))
    # R2 = numpy.repeat(numpy.array(50e-10), len(self.stamp))
    # R3 = numpy.repeat(numpy.array(10e-9), len(self.stamp))
    # R4 = numpy.repeat(numpy.array(50e-9), len(self.stamp))
    # R5 = numpy.repeat(numpy.array(10e-8), len(self.stamp))
    # Fill Flares if present
    self.axes.fill_between(numpy.linspace(0,1,len(self.stamp)), R1, \
      self.datas["Short"], where=self.datas["Short"]>R1, \
      color=colors_and_globals.GOESXrayFlare['R1'])
    self.axes.fill_between(numpy.linspace(0,1,len(self.stamp)), R2, \
      self.datas["Short"], where=self.datas["Short"]>R2, \
      color=colors_and_globals.GOESXrayFlare['R2'])
    self.axes.fill_between(numpy.linspace(0,1,len(self.stamp)), R3, \
      self.datas["Short"], where=self.datas["Short"]>R3, \
      color=colors_and_globals.GOESXrayFlare['R3'])
    self.axes.fill_between(numpy.linspace(0,1,len(self.stamp)), R4, \
      self.datas["Short"], where=self.datas["Short"]>R4, \
      color=colors_and_globals.GOESXrayFlare['R4'])
    self.axes.fill_between(numpy.linspace(0,1,len(self.stamp)), R5, \
      self.datas["Short"], where=self.datas["Short"]>R5, \
      color=colors_and_globals.GOESXrayFlare['R5'])
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
    self.stamp = [x \
      for x in self.stamp[0::7]
    ]
    # Set number of X-Axis ticks
    self.axes.set_xticks(numpy.linspace(0,1,len(self.stamp)))
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
    self.axes.set_ylabel(self.units, rotation='vertical',
      fontsize=colors_and_globals.plotLabelSize)
    # Show Units of x-axis
    if(dates[0] != dates[-1]):
      self.axes.set_xlabel(("UTC Time (%s - %s)"%(dates[0],dates[-1])),
        fontsize=colors_and_globals.plotLabelSize)
    else:
      self.axes.set_xlabel(("UTC Time (%s)"%(dates[-1])),
        fontsize=colors_and_globals.plotLabelSize)
    # Set the Plot Title
    self.axes.set_title("XRay Flux", fontsize=colors_and_globals.plotTitleSize)
    # class matplotlib.legend.Legend(parent, handles, labels, loc=None,
    # numpoints=None, markerscale=None, scatterpoints=None, scatteryoffsets=None,
    # prop=None, fontsize=None, borderpad=None, labelspacing=None, handlelength=None,
    # handleheight=None, handletextpad=None, borderaxespad=None, columnspacing=None,
    # ncol=1, mode=None, fancybox=None, shadow=None, title=None, framealpha=None,
    # bbox_to_anchor=None, bbox_transform=None, frameon=None, handler_map=None)
    # Create the legends
    legend1 = self.axes.legend(
      framealpha=0.1,
      loc=1, fontsize=colors_and_globals.legendSize,
      bbox_to_anchor=(1.24, 1.12),
      title="Nanometer")
    self.axes.add_artist(legend1)


