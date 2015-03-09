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
    # Set the graph background color
    self.axes.set_axis_bgcolor(colors_and_globals.graph_bgcolor)
    # Get the new data
    self.data = NoaaApi.getGOESRangeProtonFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Get the start date
    start_date = self.data["datestamp"][0].split(sep=":")[0]
    # Get the start date
    end_date = self.data["datestamp"][-1].split(sep=":")[0]
    # Strip only the timestamp out of the array of date/time stamps, keep only a few
    loop = 0
    for stamp in self.data["datestamp"]:
      if(loop % colors_and_globals.label_thinner_1 == 0):
        self.data["datestamp"][loop] = stamp.split(sep=":")[1]
      else:
        self.data["datestamp"][loop] = ""
      loop += 1
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    p1, = self.axes.plot(data_points, self.data["data"]["0.7-4 MeV Protons"]    , colors_and_globals.GOESRangeProtonFluxColors[0] , label="0.7-4")
    # Now just overlay remaining datasets
    self.axes.hold(True)
    p2, = self.axes.plot(data_points, self.data["data"]["4-9 MeV Protons"]      , colors_and_globals.GOESRangeProtonFluxColors[1] , label="4-9")
    p3, = self.axes.plot(data_points, self.data["data"]["9-15 MeV Protons"]     , colors_and_globals.GOESRangeProtonFluxColors[2] , label="9-15")
    p4, = self.axes.plot(data_points, self.data["data"]["15-40 MeV Protons"]    , colors_and_globals.GOESRangeProtonFluxColors[3] , label="15-40")
    p5, = self.axes.plot(data_points, self.data["data"]["38-82 MeV Protons"]    , colors_and_globals.GOESRangeProtonFluxColors[4] , label="38-82")
    p6, = self.axes.plot(data_points, self.data["data"]["84-200 MeV Protons"]   , colors_and_globals.GOESRangeProtonFluxColors[5] , label="84-200")
    p7, = self.axes.plot(data_points, self.data["data"]["110-900 MeV Protons"]  , colors_and_globals.GOESRangeProtonFluxColors[6] , label="110-900")
    p8, = self.axes.plot(data_points, self.data["data"]["350-420 MeV Protons"]  , colors_and_globals.GOESRangeProtonFluxColors[7] , label="350-420")
    p9, = self.axes.plot(data_points, self.data["data"]["420-510 MeV Protons"]  , colors_and_globals.GOESRangeProtonFluxColors[8] , label="420-510")
    p10, = self.axes.plot(data_points, self.data["data"]["510-700 MeV Protons"] , colors_and_globals.GOESRangeProtonFluxColors[9] , label="510-700")
    p11, = self.axes.plot(data_points, self.data["data"][">700 MeV Protons"]    , colors_and_globals.GOESRangeProtonFluxColors[10], label=">700")
    # Set number of X-Axis ticks
    self.axes.set_xticks(data_points)
    # Change the plot tick labels
    if(colors_and_globals.plot_angle[0] == "-"):
      self.axes.set_xticklabels(self.data["datestamp"], rotation=colors_and_globals.plot_angle, rotation_mode='anchor',
        horizontalalignment='left', fontsize=7)
    else:
      self.axes.set_xticklabels(self.data["datestamp"], rotation=colors_and_globals.plot_angle, rotation_mode='anchor',
        horizontalalignment='right', fontsize=7)
    # Change Plot to logarithmic
    self.axes.set_yscale("log")
    # Show all plot grids
    self.axes.grid(True, which="both", color=colors_and_globals.grid_color)
    # Show Units of y-axis
    self.axes.set_ylabel(self.data["units"], rotation='vertical', fontsize=7)
    # Show Units of x-axis
    if(start_date != end_date):
      self.axes.set_xlabel(("UTC Time (%s - %s)"%(start_date,end_date)), fontsize=7)
    else:
      self.axes.set_xlabel(("UTC Time (%s)"%(end_date)), fontsize=7)
    # Set the Plot Title
    self.axes.set_title("Differential Energetic Proton Flux", fontsize=10)
    # Create the Legend
    self.axes.legend(
      handles=[p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11],
      framealpha=0,
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 1.1), title='MeV')

  def update_figure(self):
    """
      This is the actual timer updating method.
    """
    # Set the graph background color
    self.axes.set_axis_bgcolor(colors_and_globals.graph_bgcolor)
    # Get the new data
    self.data = NoaaApi.getGOESRangeProtonFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Get the start date
    start_date = self.data["datestamp"][0].split(sep=":")[0]
    # Get the start date
    end_date = self.data["datestamp"][-1].split(sep=":")[0]
    # Strip only the timestamp out of the array of date/time stamps, keep only a few
    loop = 0
    for stamp in self.data["datestamp"]:
      if(loop % colors_and_globals.label_thinner_1 == 0):
        self.data["datestamp"][loop] = stamp.split(sep=":")[1]
      else:
        self.data["datestamp"][loop] = ""
      loop += 1
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    p1, = self.axes.plot(data_points, self.data["data"]["0.7-4 MeV Protons"]    , colors_and_globals.GOESRangeProtonFluxColors[0] , label="0.7-4")
    # Now just overlay remaining datasets
    self.axes.hold(True)
    p2, = self.axes.plot(data_points, self.data["data"]["4-9 MeV Protons"]      , colors_and_globals.GOESRangeProtonFluxColors[1] , label="4-9")
    p3, = self.axes.plot(data_points, self.data["data"]["9-15 MeV Protons"]     , colors_and_globals.GOESRangeProtonFluxColors[2] , label="9-15")
    p4, = self.axes.plot(data_points, self.data["data"]["15-40 MeV Protons"]    , colors_and_globals.GOESRangeProtonFluxColors[3] , label="15-40")
    p5, = self.axes.plot(data_points, self.data["data"]["38-82 MeV Protons"]    , colors_and_globals.GOESRangeProtonFluxColors[4] , label="38-82")
    p6, = self.axes.plot(data_points, self.data["data"]["84-200 MeV Protons"]   , colors_and_globals.GOESRangeProtonFluxColors[5] , label="84-200")
    p7, = self.axes.plot(data_points, self.data["data"]["110-900 MeV Protons"]  , colors_and_globals.GOESRangeProtonFluxColors[6] , label="110-900")
    p8, = self.axes.plot(data_points, self.data["data"]["350-420 MeV Protons"]  , colors_and_globals.GOESRangeProtonFluxColors[7] , label="350-420")
    p9, = self.axes.plot(data_points, self.data["data"]["420-510 MeV Protons"]  , colors_and_globals.GOESRangeProtonFluxColors[8] , label="420-510")
    p10, = self.axes.plot(data_points, self.data["data"]["510-700 MeV Protons"] , colors_and_globals.GOESRangeProtonFluxColors[9] , label="510-700")
    p11, = self.axes.plot(data_points, self.data["data"][">700 MeV Protons"]    , colors_and_globals.GOESRangeProtonFluxColors[10], label=">700")
    # Set number of X-Axis ticks
    self.axes.set_xticks(data_points)
    # Change the plot tick labels
    if(colors_and_globals.plot_angle[0] == "-"):
      self.axes.set_xticklabels(self.data["datestamp"], rotation=colors_and_globals.plot_angle, rotation_mode='anchor',
        horizontalalignment='left', fontsize=7)
    else:
      self.axes.set_xticklabels(self.data["datestamp"], rotation=colors_and_globals.plot_angle, rotation_mode='anchor',
        horizontalalignment='right', fontsize=7)
    # Change Plot to logarithmic
    self.axes.set_yscale("log")
    # Show all plot grids
    self.axes.grid(True, which="both", color=colors_and_globals.grid_color)
    # Show Units of y-axis
    self.axes.set_ylabel(self.data["units"], rotation='vertical', fontsize=7)
    # Show Units of x-axis
    if(start_date != end_date):
      self.axes.set_xlabel(("UTC Time (%s - %s)"%(start_date,end_date)), fontsize=7)
    else:
      self.axes.set_xlabel(("UTC Time (%s)"%(end_date)), fontsize=7)
    # Set the Plot Title
    self.axes.set_title("Differential Energetic Proton Flux", fontsize=10)
    # Create the Legend
    self.axes.legend(
      handles=[p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11],
      framealpha=0,
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 1.1), title='MeV')
    # Redraw plots
    self.draw()
