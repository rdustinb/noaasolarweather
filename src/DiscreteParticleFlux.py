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
GOESDiscreteParticleFluxColors = ['#5789b0', '#366e9a', '#175e95',
  '#ffdc75', '#efc549', '#e8b316',
  '#ff9c75', '#ef7849', '#e85216',
  '#0f4773', '#b2890c']

grid_color = '#999999'

# Plot x-axis Angle
plot_angle = "-45"

# Specific Plot Canvas Objects
class MyGOESDiscreteParticleFlux(MyMplCanvas):
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
    self.data = NoaaApi.getGOESDiscreteParticleFlux()
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
    Protons_95_keV    = self.axes.plot(data_points, self.data["data"]["95 keV Protons"]   , GOESDiscreteParticleFluxColors[0])
    # Now just overlay remaining datasets
    self.axes.hold(True)
    Protons_140_keV   = self.axes.plot(data_points, self.data["data"]["140 keV Protons"]  , GOESDiscreteParticleFluxColors[1])
    Protons_210_keV   = self.axes.plot(data_points, self.data["data"]["210 keV Protons"]  , GOESDiscreteParticleFluxColors[2])
    Protons_300_keV   = self.axes.plot(data_points, self.data["data"]["300 keV Protons"]  , GOESDiscreteParticleFluxColors[3])
    Protons_475_keV   = self.axes.plot(data_points, self.data["data"]["475 keV Protons"]  , GOESDiscreteParticleFluxColors[4])
    Electrons_40_keV  = self.axes.plot(data_points, self.data["data"]["40 keV Electrons"] , GOESDiscreteParticleFluxColors[5])
    Electrons_75_keV  = self.axes.plot(data_points, self.data["data"]["75 keV Electrons"] , GOESDiscreteParticleFluxColors[6])
    Electrons_150_keV = self.axes.plot(data_points, self.data["data"]["150 keV Electrons"], GOESDiscreteParticleFluxColors[7])
    Electrons_275_keV = self.axes.plot(data_points, self.data["data"]["275 keV Electrons"], GOESDiscreteParticleFluxColors[8])
    Electrons_475_keV = self.axes.plot(data_points, self.data["data"]["475 keV Electrons"], GOESDiscreteParticleFluxColors[9])
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
    self.axes.set_title("Discrete Particle Flux", fontsize=10)
    # Create the Legend
    self.axes.legend(
      ('95 keV', '140 keV', '210 keV', '300 keV', '475 keV'),
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 1.1), title='Protons')
    self.axes.legend(
      ('40 keV', '75 keV', '150 keV', '275 keV', '475 keV'),
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 0.81), title='Electrons')

  def update_figure(self):
    """
      This is the actual timer updating method.
    """
    self.data = NoaaApi.getGOESDiscreteParticleFlux()
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
    Protons_95_keV    = self.axes.plot(data_points, self.data["data"]["95 keV Protons"]   , GOESDiscreteParticleFluxColors[0])
    # Now just overlay remaining datasets
    self.axes.hold(True)
    Protons_140_keV   = self.axes.plot(data_points, self.data["data"]["140 keV Protons"]  , GOESDiscreteParticleFluxColors[1])
    Protons_210_keV   = self.axes.plot(data_points, self.data["data"]["210 keV Protons"]  , GOESDiscreteParticleFluxColors[2])
    Protons_300_keV   = self.axes.plot(data_points, self.data["data"]["300 keV Protons"]  , GOESDiscreteParticleFluxColors[3])
    Protons_475_keV   = self.axes.plot(data_points, self.data["data"]["475 keV Protons"]  , GOESDiscreteParticleFluxColors[4])
    Electrons_40_keV  = self.axes.plot(data_points, self.data["data"]["40 keV Electrons"] , GOESDiscreteParticleFluxColors[5])
    Electrons_75_keV  = self.axes.plot(data_points, self.data["data"]["75 keV Electrons"] , GOESDiscreteParticleFluxColors[6])
    Electrons_150_keV = self.axes.plot(data_points, self.data["data"]["150 keV Electrons"], GOESDiscreteParticleFluxColors[7])
    Electrons_275_keV = self.axes.plot(data_points, self.data["data"]["275 keV Electrons"], GOESDiscreteParticleFluxColors[8])
    Electrons_475_keV = self.axes.plot(data_points, self.data["data"]["475 keV Electrons"], GOESDiscreteParticleFluxColors[9])
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
      ('95 keV', '140 keV', '210 keV', '300 keV', '475 keV'),
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 1.1), title='Protons')
    self.axes.legend(
      ('40 keV', '75 keV', '150 keV', '275 keV', '475 keV'),
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 0.81), title='Electrons')
    # Redraw plots
    self.draw()
