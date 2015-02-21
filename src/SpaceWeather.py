"""
  Full Space Weather Application. This is the top-level module that will
  pull in all low level API Libraries, Graphing Libraries and Application
  support Libraries.

  This application is heavily modelled after the examples provided by the
  good people at MatPlotLib. Thank you Florent Rougon and Darren Dale for
  your development of the embedding in Qt4 example.

  http://matplotlib.org/examples/index.html
"""
###########################################################################
# Version of the application
###########################################################################
progversion = "0.1"
progbuild = "3"
progdate = "20150221"

###########################################################################
# Colors
###########################################################################
# Need 11
GOESRangeProtonFluxColors = ['#5789b0', '#366e9a', '#175e95',
  '#ffdc75', '#efc549', '#e8b316',
  '#ff9c75', '#ef7849', '#e85216',
  '#0f4773', '#b2890c']

###########################################################################
# Fonts, Default Font Size
###########################################################################
font = {'size'   : 8}

###########################################################################
# Imports
###########################################################################
# Custom backend Libraries
import NoaaApi
# Plotting Libraries
import numpy
import matplotlib
"""
  As of MatPlotLib 1.5 qt4_compat will be deprecated for the more general
  qt_compat. Pulling that in instead.
"""
from matplotlib.backends import qt_compat
# Libraries to create the GUI
import sys
import os
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
"""
  Branch using PyQt or PySide based on MatPlotLib values.
"""
if(qt_compat.QT_API == qt_compat.QT_API_PYSIDE):
  from PySide import QtGui, QtCore
else:
  from PyQt4 import QtGui, QtCore

###########################################################################
# Main Application Object
###########################################################################
class ApplicationWindow(QtGui.QMainWindow):
  def __init__(self):
    # Create the Main Window
    QtGui.QMainWindow.__init__(self)
    self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    self.setWindowTitle("application main window")

    # Create the Menu Bar
    self.file_menu = QtGui.QMenu('&File', self)
    self.file_menu.addAction('&Quit', self.fileQuit,
                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
    self.file_menu.addAction('&Close', self.fileQuit,
                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
    self.file_menu.addAction('&About', self.about)
    self.file_menu.addAction('&Version', self.version)
    self.menuBar().addMenu(self.file_menu)

    self.main_widget = QtGui.QWidget(self)
    l = QtGui.QVBoxLayout(self.main_widget)
    # Embed All Plotting Objects Here, giving them each a unique variable name
    GOESRangeProtonFlux = MyGOESRangeProtonFluxCanvas(self.main_widget, width=5, height=4, dpi=100)
    l.addWidget(GOESRangeProtonFlux)

    self.main_widget.setFocus()
    self.setCentralWidget(self.main_widget)

    # Print initial plot data status message
    self.statusBar().showMessage("Fetching initial plot data...", 5000)

  def fileQuit(self):
    self.close()

  def closeEvent(self, ce):
    self.fileQuit()

  def about(self):
    QtGui.QMessageBox.about(self, "About",
      (
"""Space Weather Application
ver %s
2015 RDustinB"""%progversion)
    )
  def version(self):
    QtGui.QMessageBox.about(self, "Version",
      (
"""Version: %s
Build: %s
Date: %s"""%(progversion,progbuild,progdate))
    )

###########################################################################
# Plotting Objects, Calls the Backend API
###########################################################################
# Generic Canvas Object
class MyMplCanvas(FigureCanvas):
  def __init__(self, parent=None, width=5, height=4, dpi=100):
    """
      class matplotlib.figure.Figure(figsize=None, dpi=None, facecolor=None,
        edgecolor=None, linewidth=0.0, frameon=None, subplotpars=None,
        tight_layout=None)
    """
    fig = Figure(figsize=(width, height), dpi=dpi)
    # Adjust the layout
    fig.subplots_adjust(left=0.11,right=0.85,top=0.92,bottom=0.20)
    # This may need to be parameterized to control layout
    self.axes = fig.add_subplot(111)
    self.compute_initial_figure()
    # Call Parent canvas init
    FigureCanvas.__init__(self, fig)
    self.setParent(parent)
    # Plot size adjusts with window adjustment
    FigureCanvas.setSizePolicy(self,
                              QtGui.QSizePolicy.Expanding,
                              QtGui.QSizePolicy.Expanding)
    FigureCanvas.updateGeometry(self)

  """
    This method must be overwritten in the child.
  """
  def compute_initial_figure(self):
      pass

# Specific Plot Canvas Objects
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

  """
    Initial data plot.
  """
  def compute_initial_figure(self):
    self.data = NoaaApi.getGOESRangeProtonFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    p1 = self.axes.plot(data_points, self.data["data"]["0.7-4 MeV Protons"]  , GOESRangeProtonFluxColors[0])
    # Now just overlay remaining datasets
    self.axes.hold(True)
    p2 = self.axes.plot(data_points, self.data["data"]["4-9 MeV Protons"]    , GOESRangeProtonFluxColors[1])
    p3 = self.axes.plot(data_points, self.data["data"]["9-15 MeV Protons"]   , GOESRangeProtonFluxColors[2])
    p4 = self.axes.plot(data_points, self.data["data"]["15-40 MeV Protons"]  , GOESRangeProtonFluxColors[3])
    p5 = self.axes.plot(data_points, self.data["data"]["38-82 MeV Protons"]  , GOESRangeProtonFluxColors[4])
    p6 = self.axes.plot(data_points, self.data["data"]["84-200 MeV Protons"] , GOESRangeProtonFluxColors[5])
    p7 = self.axes.plot(data_points, self.data["data"]["110-900 MeV Protons"], GOESRangeProtonFluxColors[6])
    p8 = self.axes.plot(data_points, self.data["data"]["350-420 MeV Protons"], GOESRangeProtonFluxColors[7])
    p9 = self.axes.plot(data_points, self.data["data"]["420-510 MeV Protons"], GOESRangeProtonFluxColors[8])
    p10 = self.axes.plot(data_points, self.data["data"]["510-700 MeV Protons"], GOESRangeProtonFluxColors[9])
    p11 = self.axes.plot(data_points, self.data["data"][">700 MeV Protons"]   , GOESRangeProtonFluxColors[10])
    # Set number of X-Axis ticks
    self.axes.set_xticks(data_points)
    # Change the plot tick labels
    self.axes.set_xticklabels(self.data["datestamp"], rotation=-45, rotation_mode='anchor',
      horizontalalignment='left', fontsize=7)
    # Change Plot to logarithmic
    self.axes.set_yscale("log")
    # Show all plot grids
    self.axes.grid(True, which="both")
    # Show Units of x-axis
    self.axes.set_ylabel(self.data["units"], rotation='vertical', fontsize=8)
    # Set the Plot Title
    self.axes.set_title("Differential Energetic Proton Flux", fontsize=10)
    # Create the Legend
    self.axes.legend(
      ('0.7-4','4-9','9-15','15-40','38-82','84-200',
        '110-900','350-420','420-510','510-700','>700'),
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 1.12), title='MeV')

  """
    This is the actual timer updating method.
  """
  def update_figure(self):
    self.data = NoaaApi.getGOESRangeProtonFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    self.axes.plot(data_points, self.data["data"]["0.7-4 MeV Protons"]  , GOESRangeProtonFluxColors[0])
    # Now just overlay remaining datasets
    self.axes.hold(True)
    self.axes.plot(data_points, self.data["data"]["4-9 MeV Protons"]    , GOESRangeProtonFluxColors[1])
    self.axes.plot(data_points, self.data["data"]["9-15 MeV Protons"]   , GOESRangeProtonFluxColors[2])
    self.axes.plot(data_points, self.data["data"]["15-40 MeV Protons"]  , GOESRangeProtonFluxColors[3])
    self.axes.plot(data_points, self.data["data"]["38-82 MeV Protons"]  , GOESRangeProtonFluxColors[4])
    self.axes.plot(data_points, self.data["data"]["84-200 MeV Protons"] , GOESRangeProtonFluxColors[5])
    self.axes.plot(data_points, self.data["data"]["110-900 MeV Protons"], GOESRangeProtonFluxColors[6])
    self.axes.plot(data_points, self.data["data"]["350-420 MeV Protons"], GOESRangeProtonFluxColors[7])
    self.axes.plot(data_points, self.data["data"]["420-510 MeV Protons"], GOESRangeProtonFluxColors[8])
    self.axes.plot(data_points, self.data["data"]["510-700 MeV Protons"], GOESRangeProtonFluxColors[9])
    self.axes.plot(data_points, self.data["data"][">700 MeV Protons"]   , GOESRangeProtonFluxColors[10])
    # Set number of X-Axis ticks
    self.axes.set_xticks(data_points)
    # Change the plot tick labels
    self.axes.set_xticklabels(self.data["datestamp"], rotation=-45, rotation_mode='anchor',
      horizontalalignment='left', fontsize=7)
    # Change Plot to logarithmic
    self.axes.set_yscale("log")
    # Show all plot grids
    self.axes.grid(True, which="both")
    # Show Units of x-axis
    self.axes.set_ylabel(self.data["units"], rotation='vertical', fontsize=8)
    # Set the Plot Title
    self.axes.set_title("Differential Energetic Proton Flux", fontsize=10)
    # Create the Legend
    self.axes.legend(
      ('0.7-4','4-9','9-15','15-40','38-82','84-200',
        '110-900','350-420','420-510','510-700','>700'),
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 1.12), title='MeV')
    # Redraw plots
    self.draw()


###########################################################################
# Run the Application
###########################################################################
matplotlib.rc('font', **font)
qApp = QtGui.QApplication(sys.argv)
aw = ApplicationWindow()
aw.setWindowTitle("Space Weather Grapher")
aw.show()
sys.exit(qApp.exec_())
#qApp.exec_()