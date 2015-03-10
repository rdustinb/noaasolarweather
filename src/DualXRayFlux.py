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
class MyGOESXrayFlux(MyMplCanvas):
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
    self.data = NoaaApi.getGOESXrayFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    short_xray, = self.axes.plot(data_points, self.data["data"]["0.05-0.4 nm"], colors_and_globals.GOESXrayFluxColors[0], label="0.05-0.4")
    # Now just overlay remaining datasets
    self.axes.hold(True)
    long_xray,  = self.axes.plot(data_points, self.data["data"]["0.1-0.8 nm"] , colors_and_globals.GOESXrayFluxColors[1], label="0.1-0.8")
    # Format the Graph
    self.formatGraph(plotTitle="Differential xRay Flux", labelThinner=colors_and_globals.DualXrayFluxLabelThinner, dataDict=self.data,
      legend1=[short_xray,long_xray], legend1title='nm', legend1xoffset='1.22', legend1yoffset='1.12')
