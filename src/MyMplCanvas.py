from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
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

# Generic Canvas Object
class MyMplCanvas(FigureCanvas):
  def __init__(self, parent=None, width=5, height=4, dpi=100, subplot=111):
    """
      class matplotlib.figure.Figure(figsize=None, dpi=None, facecolor=None,
        edgecolor=None, linewidth=0.0, frameon=None, subplotpars=None,
        tight_layout=None)
    """
    fig = Figure(figsize=(width, height), dpi=dpi)
    # Adjust the layout
    fig.subplots_adjust(left=0.11,right=0.85,top=0.92,bottom=0.18)
    # Make Figure Canvas transparent
    fig.patch.set_alpha(colors_and_globals.canvas_alpha)
    # This may need to be parameterized to control layout
    self.axes = fig.add_subplot(subplot)
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