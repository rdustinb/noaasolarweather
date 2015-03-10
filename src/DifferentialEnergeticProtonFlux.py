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
    # Get the new data
    self.data = NoaaApi.getGOESRangeProtonFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    p1, = self.axes.plot(data_points, self.data["data"]["0.7-4 MeV Protons"],
      colors_and_globals.DifferentialEnergeticProtonFluxColors[colors_and_globals.colorMode][0],
      label="0.7-4")
    # Now just overlay remaining datasets
    self.axes.hold(True)
    p2, = self.axes.plot(data_points, self.data["data"]["4-9 MeV Protons"],
      colors_and_globals.DifferentialEnergeticProtonFluxColors[colors_and_globals.colorMode][1],
      label="4-9")
    p3, = self.axes.plot(data_points, self.data["data"]["9-15 MeV Protons"],
      colors_and_globals.DifferentialEnergeticProtonFluxColors[colors_and_globals.colorMode][2],
      label="9-15")
    p4, = self.axes.plot(data_points, self.data["data"]["15-40 MeV Protons"],
      colors_and_globals.DifferentialEnergeticProtonFluxColors[colors_and_globals.colorMode][3],
      label="15-40")
    p5, = self.axes.plot(data_points, self.data["data"]["38-82 MeV Protons"],
      colors_and_globals.DifferentialEnergeticProtonFluxColors[colors_and_globals.colorMode][4],
      label="38-82")
    p6, = self.axes.plot(data_points, self.data["data"]["84-200 MeV Protons"],
      colors_and_globals.DifferentialEnergeticProtonFluxColors[colors_and_globals.colorMode][5],
      label="84-200")
    p7, = self.axes.plot(data_points, self.data["data"]["110-900 MeV Protons"],
      colors_and_globals.DifferentialEnergeticProtonFluxColors[colors_and_globals.colorMode][6],
      label="110-900")
    p8, = self.axes.plot(data_points, self.data["data"]["350-420 MeV Protons"],
      colors_and_globals.DifferentialEnergeticProtonFluxColors[colors_and_globals.colorMode][7],
      label="350-420")
    p9, = self.axes.plot(data_points, self.data["data"]["420-510 MeV Protons"],
      colors_and_globals.DifferentialEnergeticProtonFluxColors[colors_and_globals.colorMode][8],
      label="420-510")
    p10, = self.axes.plot(data_points, self.data["data"]["510-700 MeV Protons"],
      colors_and_globals.DifferentialEnergeticProtonFluxColors[colors_and_globals.colorMode][9],
      label="510-700")
    p11, = self.axes.plot(data_points, self.data["data"][">700 MeV Protons"],
      colors_and_globals.DifferentialEnergeticProtonFluxColors[colors_and_globals.colorMode][10],
      label=">700")
    # Format the Graph
    self.formatGraph(plotTitle="Differential Energetic Proton Flux",
      labelThinner=colors_and_globals.DifferentialEnergeticProtonFluxLabel,
      dataDict=self.data,
      legend1=[p1, p2, p3, p4, p5, p6, p7, p8, p9, p10, p11],
      legend1title='MeV', legend1xoffset='1.22', legend1yoffset='1.13')
