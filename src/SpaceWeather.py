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
progversion = "0.2"
progbuild = "2"
progdate = "20150303"

###########################################################################
# Fonts, Default Font Size
###########################################################################
font = {'size'   : 7}

###########################################################################
# Imports
###########################################################################
# Custom backend Libraries
import NoaaApi
# Plotting Libraries
import matplotlib
"""
  As of MatPlotLib 1.5 qt4_compat will be deprecated for the more general
  qt_compat. Pulling that in instead.
"""
from matplotlib.backends import qt_compat
# Libraries to create the GUI
import sys
import os
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
    # Single Vertical Layout object
    l = QtGui.QVBoxLayout(self.main_widget)
    # Three Horizontal Layout objects
    h1 = QtGui.QHBoxLayout()
    h2 = QtGui.QHBoxLayout()
    h3 = QtGui.QHBoxLayout()
    # Added as sublayouts to the top level vertical layout
    l.addLayout(h1)
    l.addLayout(h2)
    l.addLayout(h3)
    # Add each individual Plot Widget to the horizontal layout objects in a
    # circular fashion will result in a nicely laid out set of plots
    GOESRangeProtonFlux = MyGOESRangeProtonFluxCanvas(self.main_widget, width=5, height=4, dpi=100)
    h1.addWidget(GOESRangeProtonFlux)
    GOESGoemagFieldFlux = MyGOESGoemagFieldFluxCanvas(self.main_widget, width=5, height=4, dpi=100)
    h2.addWidget(GOESGoemagFieldFlux)
    GOESDiscreteParticleFlux = MyGOESDiscreteParticleFlux(self.main_widget, width=5, height=4, dpi=100)
    h3.addWidget(GOESDiscreteParticleFlux)

    GOESRangeParticleFlux = MyGOESRangeParticleFlux(self.main_widget, width=5, height=4, dpi=100)
    h1.addWidget(GOESRangeParticleFlux)
    GOESXrayFlux = MyGOESXrayFlux(self.main_widget, width=5, height=4, dpi=100)
    h2.addWidget(GOESXrayFlux)
    ACEDiffElecProtFlux = MyDiffElecProtFlux(self.main_widget, width=5, height=4, dpi=100)
    h3.addWidget(ACEDiffElecProtFlux)

    ACEIntegralProtonFlux = MyIntegralProtonFlux(self.main_widget, width=5, height=4, dpi=100)
    h1.addWidget(ACEIntegralProtonFlux)
    ACESolarWindPlasma = MySolarWindPlasma(self.main_widget, width=5, height=4, dpi=100)
    h2.addWidget(ACESolarWindPlasma)

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
from DifferentialEnergeticProtonFlux import MyGOESRangeProtonFluxCanvas
from GeomagneticField import MyGOESGoemagFieldFluxCanvas
from DiscreteParticleFlux import MyGOESDiscreteParticleFlux
from SolarParticleFlux import MyGOESRangeParticleFlux
from DualXRayFlux import MyGOESXrayFlux
from ACEDiffElectronProtonFlux import MyDiffElecProtFlux
from ACEIntegralProtonFlux import MyIntegralProtonFlux
from ACESolarWindPlasma import MySolarWindPlasma

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