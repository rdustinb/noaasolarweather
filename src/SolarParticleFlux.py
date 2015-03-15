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
class MyGOESRangeParticleFlux(MyMplCanvas):
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
    # Get the new data
    self.data = NoaaApi.getGOESRangeParticleFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    Protons_gt1_MeV, = self.axes.plot(data_points,
      self.data["data"][">1 Mev Protons"],
      colors_and_globals.GOESRangeParticleFluxColors[colors_and_globals.colorMode][0],
      label=">1")
    # Now just overlay remaining datasets
    self.axes.hold(True)
    Protons_gt5_MeV, = self.axes.plot(data_points,
      self.data["data"][">5 Mev Protons"],
      colors_and_globals.GOESRangeParticleFluxColors[colors_and_globals.colorMode][1],
      label=">5")
    Protons_gt10_MeV, = self.axes.plot(data_points,
      self.data["data"][">10 Mev Protons"],
      colors_and_globals.GOESRangeParticleFluxColors[colors_and_globals.colorMode][2],
      label=">10")
    Protons_gt30_MeV, = self.axes.plot(data_points,
      self.data["data"][">30 Mev Protons"],
      colors_and_globals.GOESRangeParticleFluxColors[colors_and_globals.colorMode][3],
      label=">30")
    Protons_gt50_MeV, = self.axes.plot(data_points,
      self.data["data"][">50 Mev Protons"],
      colors_and_globals.GOESRangeParticleFluxColors[colors_and_globals.colorMode][4],
      label=">50")
    Protons_gt100_MeV, = self.axes.plot(data_points,
      self.data["data"][">100 Mev Protons"],
      colors_and_globals.GOESRangeParticleFluxColors[colors_and_globals.colorMode][5],
      label=">100")
    Electrons_gt0_8_MeV, = self.axes.plot(data_points,
      self.data["data"][">0.8 Mev Electrons"],
      colors_and_globals.GOESRangeParticleFluxColors[colors_and_globals.colorMode][6],
      label=">0.8")
    Electrons_gt2_0_MeV, = self.axes.plot(data_points,
      self.data["data"][">2.0 Mev Electrons"],
      colors_and_globals.GOESRangeParticleFluxColors[colors_and_globals.colorMode][7],
      label=">2.0")
    Electrons_gt4_0_MeV, = self.axes.plot(data_points,
      self.data["data"][">4.0 Mev Electrons"],
      colors_and_globals.GOESRangeParticleFluxColors[colors_and_globals.colorMode][8],
      label=">4.0")
    # Format the Graph
    self.formatGraph(plotTitle="Integral Particle Flux", labelThinner=colors_and_globals.SolarParticleFluxLabelThinner, dataDict=self.data,
      legend1=[Protons_gt1_MeV,Protons_gt5_MeV,Protons_gt10_MeV,Protons_gt30_MeV,Protons_gt50_MeV,Protons_gt100_MeV], legend1title='p (MeV)', legend1xoffset='1.22', legend1yoffset='1.12',
      legend2=[Electrons_gt0_8_MeV,Electrons_gt2_0_MeV,Electrons_gt4_0_MeV], legend2title='e (MeV)', legend2xoffset='1.215', legend2yoffset='0.35')

