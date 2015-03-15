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
class MyGOESGoemagFieldFluxCanvas(MyMplCanvas):
  data = ""
  def __init__(self, *args, **kwargs):
    """
      Initialize the updating object.
    """
    MyMplCanvas.__init__(self, left_edge=0.15, right_edge=0.82, top_edge=0.9,
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
    self.data = NoaaApi.getGOESGoemagFieldFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    hp, = self.axes.plot(data_points, self.data["data"]["Hp"],
      colors_and_globals.GOESGeomagFieldFluxColors[colors_and_globals.colorMode][0],
      label="East")
    # Now just overlay remaining datasets
    self.axes.hold(True)
    he, = self.axes.plot(data_points, self.data["data"]["He"],
      colors_and_globals.GOESGeomagFieldFluxColors[colors_and_globals.colorMode][1],
      label="Down")
    hn, = self.axes.plot(data_points, self.data["data"]["Hn"],
      colors_and_globals.GOESGeomagFieldFluxColors[colors_and_globals.colorMode][2],
      label="Axis")
    total, = self.axes.plot(data_points, self.data["data"]["Total"],
      colors_and_globals.GOESGeomagFieldFluxColors[colors_and_globals.colorMode][3],
      label="Total")
    # Format the Graph
    self.formatGraph(plotTitle="Geomagnetic Vector Field Flux",
      labelThinner=colors_and_globals.GeomagneticFieldLabelThinner,
      dataDict=self.data, legend1=[hp, he, hn, total], legend1title='H Vector',
      legend1xoffset='1.27', legend1yoffset='1.12')
