from sys import version

"""
  Full Space Weather Application. This is the top-level module that will
  pull in all low level API Libraries, Graphing Libraries and Application
  support Libraries.

  This application is heavily modelled after the examples provided by the
  good people at MatPlotLib. Thank you Florent Rougon and Darren Dale for
  your development of the embedding in Qt4 example.

  http://matplotlib.org/examples/index.html

  !!!!CURRENTLY ONLY WORKS WITH PYTHON 3.X!!!!
"""

###########################################################################
# Run the Application
###########################################################################
if int(version[0]) == 3:
  ###########################################################################
  # Imports
  ###########################################################################
  # Pull in the global values
  import colors_and_globals
  ###########################################################################
  # Plotting Objects, Calls the Backend API
  ###########################################################################
  from DifferentialEnergeticProtonFlux import MyGOESRangeProtonFluxCanvas
  from GeomagneticField import MyGOESGoemagFieldFluxCanvas
  # from DiscreteParticleFlux import MyGOESDiscreteParticleFlux
  from SolarParticleFlux import MyGOESIntegralParticleFlux
  from DualXRayFlux import MyGOESXrayFlux
  # from ACEDiffElectronProtonFlux import MyDiffElecProtFlux
  # from ACEIntegralProtonFlux import MyIntegralProtonFlux
  from ACEInterplanetaryMagField import MyInterplanetaryMagField
  from ACESolarWindPlasma import MySolarWindPlasma
  """
    As of MatPlotLib 1.5 qt4_compat will be deprecated for the more general
    qt_compat. Pulling that in instead.
  """
  from matplotlib import rc
  from matplotlib.backends import qt_compat
  # Libraries to create the GUI
  from sys import exit
  from sys import argv
  import os
  """
    Branch using PyQt or PySide based on MatPlotLib values.
  """
  if(qt_compat.QT_API == qt_compat.QT_API_PYSIDE):
    from PySide.QtGui import QMainWindow
    from PySide.QtGui import QMenu
    from PySide.QtGui import QWidget
    from PySide.QtGui import QVBoxLayout
    from PySide.QtGui import QHBoxLayout
    from PySide.QtGui import QMessageBox
    from PySide.QtGui import QApplication
    from PySide import QtCore
    from PySide.QtCore import QTimer
  else:
    from PyQt5.QtWidgets import (QMessageBox,QHBoxLayout,QMenu,QApplication,
      QMainWindow,QVBoxLayout,QWidget)
    from PyQt5 import QtCore
    from PyQt5.QtCore import QTimer

  ###########################################################################
  # Main Application Object
  ###########################################################################
  class ApplicationWindow(QMainWindow):
    def __init__(self):
      # Verify the existance of the data directory
      if(not(os.path.exists("../data"))):
        print("../data dir doesn't exist! Creating data directory...")
        os.makedirs("../data")

      # Create the Main Window
      QMainWindow.__init__(self)
      self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
      self.setWindowTitle("Space Weather")

      # Create the Menu Bar
      self.file_menu = QMenu('&File', self)
      self.file_menu.addAction('&Quit', self.fileQuit,
                   QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
      self.file_menu.addAction('&Close', self.fileQuit,
                   QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
      self.file_menu.addAction('&About', self.about)
      self.file_menu.addAction('&Version', self.version)
      self.menuBar().addMenu(self.file_menu)

      self.main_widget = QWidget(self)
      # Single Vertical Layout object
      l = QVBoxLayout(self.main_widget)
      # Four Horizontal Layout objects
      h1 = QHBoxLayout()
      h2 = QHBoxLayout()
      h3 = QHBoxLayout()
      # Added as sublayouts to the top level vertical layout
      l.addLayout(h1)
      l.addLayout(h2)
      l.addLayout(h3)

      self.main_widget.setFocus()
      self.setCentralWidget(self.main_widget)

      self.setWindowTitle("Space Weather Grapher - Fetching initial plot data...")
      self.show()

      # Set the Application BG Color
      self.setStyleSheet(colors_and_globals.ColorModeDef)

      # Position
      self.move(colors_and_globals.init_posx,colors_and_globals.init_posy)

      # Resize
      self.resize(colors_and_globals.init_app_width,colors_and_globals.init_app_height)

      # Add each individual Plot Widget to the horizontal layout objects in a
      # circular fashion will result in a nicely laid out set of plots
      self.GOESXrayFlux = MyGOESXrayFlux(self.main_widget, width=5, height=4, dpi=100)
      h1.addWidget(self.GOESXrayFlux)
      self.ACESolarWindPlasma = MySolarWindPlasma(self.main_widget, width=5, height=4, dpi=100)
      h1.addWidget(self.ACESolarWindPlasma)

      self.GOESRangeProtonFlux = MyGOESRangeProtonFluxCanvas(self.main_widget, width=5, height=4, dpi=100)
      h2.addWidget(self.GOESRangeProtonFlux)
      self.GOESRangeParticleFlux = MyGOESIntegralParticleFlux(self.main_widget, width=5, height=4, dpi=100)
      h2.addWidget(self.GOESRangeParticleFlux)

      self.GOESGoemagFieldFlux = MyGOESGoemagFieldFluxCanvas(self.main_widget, width=5, height=4, dpi=100)
      h3.addWidget(self.GOESGoemagFieldFlux)
      self.ACEInterplanetaryMagField = MyInterplanetaryMagField(self.main_widget, width=5, height=4, dpi=100)
      h3.addWidget(self.ACEInterplanetaryMagField)

      # ACEIntegralProtonFlux = MyIntegralProtonFlux(self.main_widget, width=5, height=4, dpi=100)
      # h3.addWidget(ACEIntegralProtonFlux)
      # GOESDiscreteParticleFlux = MyGOESDiscreteParticleFlux(self.main_widget, width=5, height=4, dpi=100)
      # h3.addWidget(GOESDiscreteParticleFlux)
      # ACEDiffElecProtFlux = MyDiffElecProtFlux(self.main_widget, width=5, height=4, dpi=100)
      # h3.addWidget(ACEDiffElecProtFlux)

      # Setup the Notification Bar Updater
      self.update_pos = 0
      timer = QTimer(self)
      timer.timeout.connect(self.update_notifier)
      timer.start(5000)

    def update_notifier(self):
      if(self.update_pos == 0):
        last_time = self.GOESXrayFlux.get_stamp()
        last_string = self.GOESXrayFlux.get_name_string()
        self.statusBar().showMessage("%s last data available: %s"%(last_string, last_time[-1][1]))
        self.update_pos = 1
      elif(self.update_pos == 1):
        last_time = self.ACESolarWindPlasma.get_stamp()
        last_string = self.ACESolarWindPlasma.get_name_string()
        self.statusBar().showMessage("%s last data available: %s"%(last_string, last_time[-1][1]))
        self.update_pos = 2
      elif(self.update_pos == 2):
        last_time = self.GOESRangeProtonFlux.get_stamp()
        last_string = self.GOESRangeProtonFlux.get_name_string()
        self.statusBar().showMessage("%s last data available: %s"%(last_string, last_time[-1][1]))
        self.update_pos = 3
      elif(self.update_pos == 3):
        last_time = self.GOESRangeParticleFlux.get_stamp()
        last_string = self.GOESRangeParticleFlux.get_name_string()
        self.statusBar().showMessage("%s last data available: %s"%(last_string, last_time[-1][1]))
        self.update_pos = 4
      elif(self.update_pos == 4):
        last_time = self.GOESGoemagFieldFlux.get_stamp()
        last_string = self.GOESGoemagFieldFlux.get_name_string()
        self.statusBar().showMessage("%s last data available: %s"%(last_string, last_time[-1][1]))
        self.update_pos = 5
      elif(self.update_pos == 5):
        last_time = self.ACEInterplanetaryMagField.get_stamp()
        last_string = self.ACEInterplanetaryMagField.get_name_string()
        self.statusBar().showMessage("%s last data available: %s"%(last_string, last_time[-1][1]))
        self.update_pos = 0

    def fileQuit(self):
      self.close()

    def closeEvent(self, ce):
      self.fileQuit()

    def about(self):
      QMessageBox.about(self, "About", ("Space Weather Application \nVersion: %s\n2015, RDustinB"%(colors_and_globals.progversion)))

    def version(self):
      QMessageBox.about(self, "Version", ("Version: %s\nBuild: %s\nDate: %s"%(colors_and_globals.progversion,colors_and_globals.progbuild,colors_and_globals.progdate)))

  rc('font', **colors_and_globals.font)
  qApp = QApplication(argv)
  aw = ApplicationWindow()
  # Notify user that initial data has been populater
  aw.setWindowTitle("Space Weather Grapher")
  exit(qApp.exec_())
  #qApp.exec_()
else:
  print("This application only works with Python Version 3.x.")
