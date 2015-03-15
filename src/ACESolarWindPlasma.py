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
class MySolarWindPlasma(MyMplCanvas):
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
    self.data = NoaaApi.getSolarPlasma()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    density,      = self.axes.plot(data_points, self.data["data"]["Density"],
      colors_and_globals.ACESolarWindPlasmaColors[colors_and_globals.colorMode][0],
      label=self.data["units"]["Density"])
    # Now just overlay remaining datasets
    self.axes.hold(True)
    speed,        = self.axes.plot(data_points, self.data["data"]["Speed"],
      colors_and_globals.ACESolarWindPlasmaColors[colors_and_globals.colorMode][1],
      label=self.data["units"]["Speed"])
    temperature,  = self.axes.plot(data_points, self.data["data"]["Temperature"],
      colors_and_globals.ACESolarWindPlasmaColors[colors_and_globals.colorMode][2],
      label=self.data["units"]["Temperature"])
    # Format the Graph
    self.formatGraph(plotTitle="Solar Plasma", dataDict=self.data,
      labelThinner=colors_and_globals.ACESolarWindPlasmaLabelThinner,
      disableYLabel=True, legend1=[density,speed,temperature],
      legend1title='Params', legend1xoffset='1.21', legend1yoffset='1.12')
