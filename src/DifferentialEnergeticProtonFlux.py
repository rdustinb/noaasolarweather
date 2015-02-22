from MyMplCanvas import MyMplCanvas
import NoaaApi
import numpy
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
# Globals
###########################################################################
# Plot Colors
GOESRangeProtonFluxColors = ['#5789b0', '#366e9a', '#175e95',
  '#ffdc75', '#efc549', '#e8b316',
  '#ff9c75', '#ef7849', '#e85216',
  '#0f4773', '#b2890c']

grid_color = '#999999'

# Plot x-axis Angle
plot_angle = "-45"

# Specific Plot Canvas Objects
class MyGOESRangeProtonFluxCanvas(MyMplCanvas):
  data = ""
  """
    Initialize the updating object.
  """
  def __init__(self, *args, **kwargs):
    MyMplCanvas.__init__(self, *args, **kwargs)
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
    self.data = NoaaApi.getGOESRangeProtonFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Strip only the timestamp out of the array of date/time stamps
    loop = 0
    for stamp in self.data["datestamp"]:
      self.data["datestamp"][loop] = stamp.split(sep=":")[1]
      loop += 1
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    p1 = self.axes.plot(data_points, self.data["data"]["0.7-4 MeV Protons"]  , GOESRangeProtonFluxColors[0])
    # Now just overlay remaining datasets
    self.axes.hold(True)
    p2 = self.axes.plot(data_points, self.data["data"]["4-9 MeV Protons"]    , GOESRangeProtonFluxColors[1])
    p3 = self.axes.plot(data_points, self.data["data"]["9-15 MeV Protons"]   , GOESRangeProtonFluxColors[2])
    p4 = self.axes.plot(data_points, self.data["data"]["15-40 MeV Protons"]  , GOESRangeProtonFluxColors[3])
    p5 = self.axes.plot(data_points, self.data["data"]["38-82 MeV Protons"]  , GOESRangeProtonFluxColors[4])
    p6 = self.axes.plot(data_points, self.data["data"]["84-200 MeV Protons"] , GOESRangeProtonFluxColors[5])
    p7 = self.axes.plot(data_points, self.data["data"]["110-900 MeV Protons"], GOESRangeProtonFluxColors[6])
    p8 = self.axes.plot(data_points, self.data["data"]["350-420 MeV Protons"], GOESRangeProtonFluxColors[7])
    p9 = self.axes.plot(data_points, self.data["data"]["420-510 MeV Protons"], GOESRangeProtonFluxColors[8])
    p10 = self.axes.plot(data_points, self.data["data"]["510-700 MeV Protons"], GOESRangeProtonFluxColors[9])
    p11 = self.axes.plot(data_points, self.data["data"][">700 MeV Protons"]   , GOESRangeProtonFluxColors[10])
    # Set number of X-Axis ticks
    self.axes.set_xticks(data_points)
    # Change the plot tick labels
    if(plot_angle[0] == "-"):
      self.axes.set_xticklabels(self.data["datestamp"], rotation=plot_angle, rotation_mode='anchor',
        horizontalalignment='left', fontsize=7)
    else:
      self.axes.set_xticklabels(self.data["datestamp"], rotation=plot_angle, rotation_mode='anchor',
        horizontalalignment='right', fontsize=7)
    # Change Plot to logarithmic
    self.axes.set_yscale("log")
    # Show all plot grids
    self.axes.grid(True, which="both", color=grid_color)
    # Show Units of y-axis
    self.axes.set_ylabel(self.data["units"], rotation='vertical', fontsize=7)
    # Show Units of x-axis
    self.axes.set_xlabel("UTC Time", fontsize=7)
    # Set the Plot Title
    self.axes.set_title("Differential Energetic Proton Flux", fontsize=10)
    # Create the Legend
    self.axes.legend(
      ('0.7-4','4-9','9-15','15-40','38-82','84-200',
        '110-900','350-420','420-510','510-700','>700'),
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 1.1), title='MeV')

  def update_figure(self):
    """
      This is the actual timer updating method.
    """
    self.data = NoaaApi.getGOESRangeProtonFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Strip only the timestamp out of the array of date/time stamps
    loop = 0
    for stamp in self.data["datestamp"]:
      self.data["datestamp"][loop] = stamp.split(sep=":")[1]
      loop += 1
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    self.axes.plot(data_points, self.data["data"]["0.7-4 MeV Protons"]  , GOESRangeProtonFluxColors[0])
    # Now just overlay remaining datasets
    self.axes.hold(True)
    self.axes.plot(data_points, self.data["data"]["4-9 MeV Protons"]    , GOESRangeProtonFluxColors[1])
    self.axes.plot(data_points, self.data["data"]["9-15 MeV Protons"]   , GOESRangeProtonFluxColors[2])
    self.axes.plot(data_points, self.data["data"]["15-40 MeV Protons"]  , GOESRangeProtonFluxColors[3])
    self.axes.plot(data_points, self.data["data"]["38-82 MeV Protons"]  , GOESRangeProtonFluxColors[4])
    self.axes.plot(data_points, self.data["data"]["84-200 MeV Protons"] , GOESRangeProtonFluxColors[5])
    self.axes.plot(data_points, self.data["data"]["110-900 MeV Protons"], GOESRangeProtonFluxColors[6])
    self.axes.plot(data_points, self.data["data"]["350-420 MeV Protons"], GOESRangeProtonFluxColors[7])
    self.axes.plot(data_points, self.data["data"]["420-510 MeV Protons"], GOESRangeProtonFluxColors[8])
    self.axes.plot(data_points, self.data["data"]["510-700 MeV Protons"], GOESRangeProtonFluxColors[9])
    self.axes.plot(data_points, self.data["data"][">700 MeV Protons"]   , GOESRangeProtonFluxColors[10])
    # Set number of X-Axis ticks
    self.axes.set_xticks(data_points)
    # Change the plot tick labels
    if(plot_angle[0] == "-"):
      self.axes.set_xticklabels(self.data["datestamp"], rotation=plot_angle, rotation_mode='anchor',
        horizontalalignment='left', fontsize=7)
    else:
      self.axes.set_xticklabels(self.data["datestamp"], rotation=plot_angle, rotation_mode='anchor',
        horizontalalignment='right', fontsize=7)
    # Change Plot to logarithmic
    self.axes.set_yscale("log")
    # Show all plot grids
    self.axes.grid(True, which="both", color=grid_color)
    # Show Units of y-axis
    self.axes.set_ylabel(self.data["units"], rotation='vertical', fontsize=7)
    # Show Units of x-axis
    self.axes.set_xlabel("UTC Time", fontsize=7)
    # Set the Plot Title
    self.axes.set_title("Differential Energetic Proton Flux", fontsize=10)
    # Create the Legend
    self.axes.legend(
      ('0.7-4','4-9','9-15','15-40','38-82','84-200',
        '110-900','350-420','420-510','510-700','>700'),
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 1.1), title='MeV')
    # Redraw plots
    self.draw()
