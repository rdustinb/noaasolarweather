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
GOESGoemagFieldFluxColors = ['#5789b0', '#366e9a', '#175e95', '#e85216']

grid_color = '#aaaaaa'

# Plot x-axis Angle
plot_angle = "-45"

# Specific Plot Canvas Objects
class MyGOESGoemagFieldFluxCanvas(MyMplCanvas):
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
    self.data = NoaaApi.getGOESGoemagFieldFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Get the start date
    start_date = self.data["datestamp"][0].split(sep=":")[0]
    # Get the start date
    end_date = self.data["datestamp"][-1].split(sep=":")[0]
    # Strip only the timestamp out of the array of date/time stamps, keep only a few
    loop = 0
    for stamp in self.data["datestamp"]:
      if(loop % 7 == 0):
        self.data["datestamp"][loop] = stamp.split(sep=":")[1]
      else:
        self.data["datestamp"][loop] = ""
      loop += 1
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    hp    = self.axes.plot(data_points, self.data["data"]["Hp"]   , GOESGoemagFieldFluxColors[0])
    # Now just overlay remaining datasets
    self.axes.hold(True)
    he    = self.axes.plot(data_points, self.data["data"]["He"]   , GOESGoemagFieldFluxColors[1])
    hn    = self.axes.plot(data_points, self.data["data"]["Hn"]   , GOESGoemagFieldFluxColors[2])
    total = self.axes.plot(data_points, self.data["data"]["Total"], GOESGoemagFieldFluxColors[3])
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
    self.axes.set_ylabel(self.data["units"], rotation='vertical', fontsize=8)
    # Show Units of x-axis
    if(start_date != end_date):
      self.axes.set_xlabel(("UTC Time (%s - %s)"%(start_date,end_date)), fontsize=7)
    else:
      self.axes.set_xlabel(("UTC Time (%s)"%(end_date)), fontsize=7)
    # Set the Plot Title
    self.axes.set_title("Three Dimensions of Geomagnetic Field Flux", fontsize=10)
    # Create the Legend
    self.axes.legend(
      ('East','Down','Axis', 'Total'),
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 1.1), title='nT')

  def update_figure(self):
    """
      This is the actual timer updating method.
    """
    self.data = NoaaApi.getGOESGoemagFieldFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Get the start date
    start_date = self.data["datestamp"][0].split(sep=":")[0]
    # Get the start date
    end_date = self.data["datestamp"][-1].split(sep=":")[0]
    # Strip only the timestamp out of the array of date/time stamps, keep only a few
    loop = 0
    for stamp in self.data["datestamp"]:
      if(loop % 7 == 0):
        self.data["datestamp"][loop] = stamp.split(sep=":")[1]
      else:
        self.data["datestamp"][loop] = ""
      loop += 1
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    hp    = self.axes.plot(data_points, self.data["data"]["Hp"]   , GOESGoemagFieldFluxColors[0])
    # Now just overlay remaining datasets
    self.axes.hold(True)
    he    = self.axes.plot(data_points, self.data["data"]["He"]   , GOESGoemagFieldFluxColors[1])
    hn    = self.axes.plot(data_points, self.data["data"]["Hn"]   , GOESGoemagFieldFluxColors[2])
    total = self.axes.plot(data_points, self.data["data"]["Total"], GOESGoemagFieldFluxColors[3])
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
    if(start_date != end_date):
      self.axes.set_xlabel(("UTC Time (%s - %s)"%(start_date,end_date)), fontsize=7)
    else:
      self.axes.set_xlabel(("UTC Time (%s)"%(end_date)), fontsize=7)
    # Set the Plot Title
    self.axes.set_title("Three Dimensions of Geomagnetic Field Flux", fontsize=10)
    # Create the Legend
    self.axes.legend(
      ('East','Down','Axis', 'Total'),
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 1.1), title='nT')
    # Redraw plots
    self.draw()
