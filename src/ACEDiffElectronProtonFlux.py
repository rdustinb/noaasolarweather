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
class MyDiffElecProtFlux(MyMplCanvas):
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
    self.data = NoaaApi.getDiffElecProtFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    p1,  = self.axes.plot(data_points, self.data["data"]["47-68 keV Proton"],
      colors_and_globals.ACEDiffElecProtFluxColors[colors_and_globals.colorMode][0],
      label="47-68")
    p2,  = self.axes.plot(data_points, self.data["data"]["115-195 keV Proton"],
      colors_and_globals.ACEDiffElecProtFluxColors[colors_and_globals.colorMode][1],
      label="115-195")
    p3,  = self.axes.plot(data_points, self.data["data"]["310-580 keV Proton"],
      colors_and_globals.ACEDiffElecProtFluxColors[colors_and_globals.colorMode][2],
      label="310-580")
    p4,  = self.axes.plot(data_points, self.data["data"]["795-1193 keV Proton"],
      colors_and_globals.ACEDiffElecProtFluxColors[colors_and_globals.colorMode][3],
      label="795-1193")
    p5,  = self.axes.plot(data_points, self.data["data"]["1060-1900 keV Proton"],
      colors_and_globals.ACEDiffElecProtFluxColors[colors_and_globals.colorMode][4],
      label="1060-1900")
    # Now just overlay remaining datasets
    self.axes.hold(True)
    e1,  = self.axes.plot(data_points, self.data["data"]["38-53 eV Electron"],
      colors_and_globals.ACEDiffElecProtFluxColors[colors_and_globals.colorMode][5],
      label="38-53")
    e2,  = self.axes.plot(data_points, self.data["data"]["175-315 eV Electron"],
      colors_and_globals.ACEDiffElecProtFluxColors[colors_and_globals.colorMode][6],
      label="175-315")
    # Format the Graph
    self.formatGraph(plotTitle="Differential Particle Flux",
      labelThinner=colors_and_globals.ACEDiffElectronProtonFluxLabelThinner,
      dataDict=self.data, legend1=[p1,p2,p3,p4,p5], legend1title='p (keV)',
      legend1xoffset='1.245', legend1yoffset='1.12', legend2=[e1,e2],
      legend2title='e (eV)', legend2xoffset='1.215', legend2yoffset='0.45')
