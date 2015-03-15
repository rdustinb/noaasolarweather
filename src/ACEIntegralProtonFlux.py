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
class MyIntegralProtonFlux(MyMplCanvas):
  data = ""
  """
    Initialize the updating object.
  """
  def __init__(self, *args, **kwargs):
    MyMplCanvas.__init__(self, left_edge=0.16, right_edge=0.82, top_edge=0.9,
      bottom_edge=0.22, *args, **kwargs)
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
    self.data = NoaaApi.getSolarIsotopeSpectrometer()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    proton_gt10mev,  = self.axes.plot(data_points, self.data["data"][">10 MeV Proton"],
      colors_and_globals.ACEIntegralProtonFluxColors[colors_and_globals.colorMode][0],
      label=">10")
    # Now just overlay remaining datasets
    self.axes.hold(True)
    proton_gt30mev,  = self.axes.plot(data_points, self.data["data"][">30 MeV Proton"],
      colors_and_globals.ACEIntegralProtonFluxColors[colors_and_globals.colorMode][1],
      label=">30")
    # Format the Graph
    self.formatGraph(plotTitle="Integral Proton Flux",
      labelThinner=colors_and_globals.ACEIntegralProtonFluxLabelThinner,
      dataDict=self.data, legend1=[proton_gt10mev,proton_gt30mev],
      legend1title='p (MeV)', legend1xoffset='1.27', legend1yoffset='1.12')
