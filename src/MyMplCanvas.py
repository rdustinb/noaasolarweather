from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import colors_and_globals
import numpy
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
  def __init__(self, parent=None, width=5, height=4, dpi=100, subplot=111,
    left_edge=0.10, right_edge=0.82, top_edge=0.9, bottom_edge=0.22):
    """
      class matplotlib.figure.Figure(figsize=None, dpi=None, facecolor=None,
        edgecolor=None, linewidth=0.0, frameon=None, subplotpars=None,
        tight_layout=None)
    """
    fig = Figure(figsize=(width, height), dpi=dpi)
    # Adjust the layout
    fig.subplots_adjust(left=left_edge,right=right_edge,top=top_edge,bottom=bottom_edge)
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

  def compute_initial_figure(self):
    """
      This method must be overwritten in the child.
    """
    pass

  def update_figure(self):
    """
      This is the actual timer updating method.
    """
    pass

  def formatGraph(self, scale="log", plotTitle='', labelThinner=1, dataDict={},
    disableYLabel=False, legend1=[], legend1title='', legend1xoffset=1.22,
    legend1yoffset=1.12, legend2=[], legend2title='', legend2xoffset=1.22,
    legend2yoffset=0.55):
    # Get the start date
    start_date = dataDict["datestamp"][0].split(sep=":")[0]
    # Get the start date
    end_date = dataDict["datestamp"][-1].split(sep=":")[0]
    # Strip only the timestamp out of the array of date/time stamps, keep only a few
    dataDict["datestamp"] = [x.split(sep=":")[1] for x in dataDict["datestamp"][0::labelThinner]]
    dataPts = numpy.linspace(0,1,len(dataDict["datestamp"]))
    # Set the graph background color
    self.axes.set_axis_bgcolor(colors_and_globals.graph_bgcolor)
    # Change Plot to logarithmic
    self.axes.set_yscale(scale)
    # Show all plot grids
    self.axes.grid(True, which="both", color=colors_and_globals.grid_color)
    # Set number of X-Axis ticks
    self.axes.set_xticks(dataPts)
    # Change the plot tick labels
    if(colors_and_globals.plot_angle[0] == "-"):
      self.axes.set_xticklabels(dataDict["datestamp"],
        rotation=colors_and_globals.plot_angle, rotation_mode='anchor',
        horizontalalignment='left', fontsize=colors_and_globals.plotLabelSize)
    else:
      self.axes.set_xticklabels(dataDict["datestamp"],
        rotation=colors_and_globals.plot_angle, rotation_mode='anchor',
        horizontalalignment='right', fontsize=colors_and_globals.plotLabelSize)
    # Show Units of y-axis if enabled
    if(disableYLabel == False):
      self.axes.set_ylabel(dataDict["units"], rotation='vertical',
        fontsize=colors_and_globals.plotLabelSize)
    # Show Units of x-axis
    if(start_date != end_date):
      self.axes.set_xlabel(("UTC Time (%s - %s)"%(start_date,end_date)),
        fontsize=colors_and_globals.plotLabelSize)
    else:
      self.axes.set_xlabel(("UTC Time (%s)"%(end_date)),
        fontsize=colors_and_globals.plotLabelSize)
    # Set the Plot Title
    self.axes.set_title(plotTitle, fontsize=colors_and_globals.plotTitleSize)
    # Create the Legends
    if((legend1 != []) and (legend1title != '')):
      legend1 = self.axes.legend(
        handles=legend1,
        framealpha=0.1,
        loc=1, fontsize=colors_and_globals.legendSize,
        bbox_to_anchor=(float(legend1xoffset), float(legend1yoffset)),
        title=legend1title)
      self.axes.add_artist(legend1)
    if((legend2 != []) and (legend2title != '')):
      legend2 = self.axes.legend(
        handles=legend2,
        framealpha=0.1,
        loc=1, fontsize=colors_and_globals.legendSize,
        bbox_to_anchor=(float(legend2xoffset), float(legend2yoffset)),
        title=legend2title)
      self.axes.add_artist(legend2)


