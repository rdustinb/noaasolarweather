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
class MyGOESDiscreteParticleFlux(MyMplCanvas):
  data = ""
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
    timer.start(self.data["update"])

  def compute_initial_figure(self):
    """
      Initial data plot.
    """
    # Get the new data
    self.data = NoaaApi.getGOESDiscreteParticleFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    Protons_95_keV, = self.axes.plot(data_points,
      self.data["data"]["95 keV Protons"],
      colors_and_globals.GOESDiscreteParticleFluxColors[colors_and_globals.colorMode][0],
      label="95")
    # Now just overlay remaining datasets
    self.axes.hold(True)
    Protons_140_keV, = self.axes.plot(data_points,
      self.data["data"]["140 keV Protons"],
      colors_and_globals.GOESDiscreteParticleFluxColors[colors_and_globals.colorMode][1],
      label="140")
    Protons_210_keV, = self.axes.plot(data_points,
      self.data["data"]["210 keV Protons"],
      colors_and_globals.GOESDiscreteParticleFluxColors[colors_and_globals.colorMode][2],
      label="210")
    Protons_300_keV, = self.axes.plot(data_points,
      self.data["data"]["300 keV Protons"],
      colors_and_globals.GOESDiscreteParticleFluxColors[colors_and_globals.colorMode][3],
      label="300")
    Protons_475_keV, = self.axes.plot(data_points,
      self.data["data"]["475 keV Protons"],
      colors_and_globals.GOESDiscreteParticleFluxColors[colors_and_globals.colorMode][4],
      label="475")
    Electrons_40_keV, = self.axes.plot(data_points,
      self.data["data"]["40 keV Electrons"],
      colors_and_globals.GOESDiscreteParticleFluxColors[colors_and_globals.colorMode][5],
      label="40")
    Electrons_75_keV, = self.axes.plot(data_points,
      self.data["data"]["75 keV Electrons"],
      colors_and_globals.GOESDiscreteParticleFluxColors[colors_and_globals.colorMode][6],
      label="75")
    Electrons_150_keV, = self.axes.plot(data_points,
      self.data["data"]["150 keV Electrons"],
      colors_and_globals.GOESDiscreteParticleFluxColors[colors_and_globals.colorMode][7],
      label="150")
    Electrons_275_keV, = self.axes.plot(data_points,
      self.data["data"]["275 keV Electrons"],
      colors_and_globals.GOESDiscreteParticleFluxColors[colors_and_globals.colorMode][8],
      label="275")
    Electrons_475_keV, = self.axes.plot(data_points,
      self.data["data"]["475 keV Electrons"],
      colors_and_globals.GOESDiscreteParticleFluxColors[colors_and_globals.colorMode][9],
      label="475")
    # Format the Graph
    self.formatGraph(plotTitle="Discrete Particle Flux",
      labelThinner=colors_and_globals.DiscreteParticleFluxLabelThinner,
      dataDict=self.data,
      legend1=[Protons_95_keV,Protons_140_keV,Protons_210_keV,Protons_300_keV,Protons_475_keV],
      legend1title='p (keV)', legend1xoffset='1.2', legend1yoffset='1.12',
      legend2=[Electrons_40_keV,Electrons_75_keV,Electrons_150_keV,Electrons_275_keV,Electrons_475_keV],
      legend2title='e (keV)', legend2xoffset='1.2', legend2yoffset='0.45')
