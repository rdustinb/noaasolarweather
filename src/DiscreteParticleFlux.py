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
class MyGOESDiscreteParticleFlux(MyMplCanvas):
  data = ""
  def __init__(self, *args, **kwargs):
    """
      Initialize the updating object.
    """
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
    # Set the graph background color
    self.axes.set_axis_bgcolor(colors_and_globals.graph_bgcolor)
    # Get the new data
    self.data = NoaaApi.getGOESDiscreteParticleFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Get the start date
    start_date = self.data["datestamp"][0].split(sep=":")[0]
    # Get the start date
    end_date = self.data["datestamp"][-1].split(sep=":")[0]
    # Strip only the timestamp out of the array of date/time stamps, keep only a few
    loop = 0
    for stamp in self.data["datestamp"]:
      if(loop % colors_and_globals.label_thinner_2 == 0):
        self.data["datestamp"][loop] = stamp.split(sep=":")[1]
      else:
        self.data["datestamp"][loop] = ""
      loop += 1
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    Protons_95_keV,     = self.axes.plot(data_points, self.data["data"]["95 keV Protons"]   , colors_and_globals.GOESDiscreteParticleFluxColors[0], label="95")
    # Now just overlay remaining datasets
    self.axes.hold(True)
    Protons_140_keV,    = self.axes.plot(data_points, self.data["data"]["140 keV Protons"]  , colors_and_globals.GOESDiscreteParticleFluxColors[1], label="140")
    Protons_210_keV,    = self.axes.plot(data_points, self.data["data"]["210 keV Protons"]  , colors_and_globals.GOESDiscreteParticleFluxColors[2], label="210")
    Protons_300_keV,    = self.axes.plot(data_points, self.data["data"]["300 keV Protons"]  , colors_and_globals.GOESDiscreteParticleFluxColors[3], label="300")
    Protons_475_keV,    = self.axes.plot(data_points, self.data["data"]["475 keV Protons"]  , colors_and_globals.GOESDiscreteParticleFluxColors[4], label="475")
    Electrons_40_keV,   = self.axes.plot(data_points, self.data["data"]["40 keV Electrons"] , colors_and_globals.GOESDiscreteParticleFluxColors[5], label="40")
    Electrons_75_keV,   = self.axes.plot(data_points, self.data["data"]["75 keV Electrons"] , colors_and_globals.GOESDiscreteParticleFluxColors[6], label="75")
    Electrons_150_keV,  = self.axes.plot(data_points, self.data["data"]["150 keV Electrons"], colors_and_globals.GOESDiscreteParticleFluxColors[7], label="150")
    Electrons_275_keV,  = self.axes.plot(data_points, self.data["data"]["275 keV Electrons"], colors_and_globals.GOESDiscreteParticleFluxColors[8], label="275")
    Electrons_475_keV,  = self.axes.plot(data_points, self.data["data"]["475 keV Electrons"], colors_and_globals.GOESDiscreteParticleFluxColors[9], label="475")
    # Set number of X-Axis ticks
    self.axes.set_xticks(data_points)
    # Change the plot tick labels
    if(colors_and_globals.plot_angle[0] == "-"):
      self.axes.set_xticklabels(self.data["datestamp"], rotation=colors_and_globals.plot_angle, rotation_mode='anchor',
        horizontalalignment='left', fontsize=7)
    else:
      self.axes.set_xticklabels(self.data["datestamp"], rotation=colors_and_globals.plot_angle, rotation_mode='anchor',
        horizontalalignment='right', fontsize=7)
    # Change Plot to logarithmic
    self.axes.set_yscale("log")
    # Show all plot grids
    self.axes.grid(True, which="both", color=colors_and_globals.grid_color)
    # Show Units of y-axis
    self.axes.set_ylabel(self.data["units"], rotation='vertical', fontsize=8)
    # Show Units of x-axis
    if(start_date != end_date):
      self.axes.set_xlabel(("UTC Time (%s - %s)"%(start_date,end_date)), fontsize=7)
    else:
      self.axes.set_xlabel(("UTC Time (%s)"%(end_date)), fontsize=7)
    # Set the Plot Title
    self.axes.set_title("Discrete Particle Flux", fontsize=10)
    # Create the Legend
    proton_legend = self.axes.legend(
      handles=[Protons_95_keV,Protons_140_keV,Protons_210_keV,Protons_300_keV,Protons_475_keV],
      framealpha=0,
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 1.1), title='p (keV)')
    electron_legend = self.axes.legend(
      handles=[Electrons_40_keV,Electrons_75_keV,Electrons_150_keV,Electrons_275_keV,Electrons_475_keV],
      framealpha=0,
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 0.65), title='e (keV)')
    # Add Legends to plot
    self.axes.add_artist(proton_legend)
    self.axes.add_artist(electron_legend)

  def update_figure(self):
    """
      This is the actual timer updating method.
    """
    # Set the graph background color
    self.axes.set_axis_bgcolor(colors_and_globals.graph_bgcolor)
    # Get the new data
    self.data = NoaaApi.getGOESDiscreteParticleFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Get the start date
    start_date = self.data["datestamp"][0].split(sep=":")[0]
    # Get the start date
    end_date = self.data["datestamp"][-1].split(sep=":")[0]
    # Strip only the timestamp out of the array of date/time stamps, keep only a few
    loop = 0
    for stamp in self.data["datestamp"]:
      if(loop % colors_and_globals.label_thinner_2 == 0):
        self.data["datestamp"][loop] = stamp.split(sep=":")[1]
      else:
        self.data["datestamp"][loop] = ""
      loop += 1
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    Protons_95_keV,     = self.axes.plot(data_points, self.data["data"]["95 keV Protons"]   , colors_and_globals.GOESDiscreteParticleFluxColors[0], label="95")
    # Now just overlay remaining datasets
    self.axes.hold(True)
    Protons_140_keV,    = self.axes.plot(data_points, self.data["data"]["140 keV Protons"]  , colors_and_globals.GOESDiscreteParticleFluxColors[1], label="140")
    Protons_210_keV,    = self.axes.plot(data_points, self.data["data"]["210 keV Protons"]  , colors_and_globals.GOESDiscreteParticleFluxColors[2], label="210")
    Protons_300_keV,    = self.axes.plot(data_points, self.data["data"]["300 keV Protons"]  , colors_and_globals.GOESDiscreteParticleFluxColors[3], label="300")
    Protons_475_keV,    = self.axes.plot(data_points, self.data["data"]["475 keV Protons"]  , colors_and_globals.GOESDiscreteParticleFluxColors[4], label="475")
    Electrons_40_keV,   = self.axes.plot(data_points, self.data["data"]["40 keV Electrons"] , colors_and_globals.GOESDiscreteParticleFluxColors[5], label="40")
    Electrons_75_keV,   = self.axes.plot(data_points, self.data["data"]["75 keV Electrons"] , colors_and_globals.GOESDiscreteParticleFluxColors[6], label="75")
    Electrons_150_keV,  = self.axes.plot(data_points, self.data["data"]["150 keV Electrons"], colors_and_globals.GOESDiscreteParticleFluxColors[7], label="150")
    Electrons_275_keV,  = self.axes.plot(data_points, self.data["data"]["275 keV Electrons"], colors_and_globals.GOESDiscreteParticleFluxColors[8], label="275")
    Electrons_475_keV,  = self.axes.plot(data_points, self.data["data"]["475 keV Electrons"], colors_and_globals.GOESDiscreteParticleFluxColors[9], label="475")
    # Set number of X-Axis ticks
    self.axes.set_xticks(data_points)
    # Change the plot tick labels
    if(colors_and_globals.plot_angle[0] == "-"):
      self.axes.set_xticklabels(self.data["datestamp"], rotation=colors_and_globals.plot_angle, rotation_mode='anchor',
        horizontalalignment='left', fontsize=7)
    else:
      self.axes.set_xticklabels(self.data["datestamp"], rotation=colors_and_globals.plot_angle, rotation_mode='anchor',
        horizontalalignment='right', fontsize=7)
    # Change Plot to logarithmic
    self.axes.set_yscale("log")
    # Show all plot grids
    self.axes.grid(True, which="both", color=colors_and_globals.grid_color)
    # Show Units of y-axis
    self.axes.set_ylabel(self.data["units"], rotation='vertical', fontsize=8)
    # Show Units of x-axis
    if(start_date != end_date):
      self.axes.set_xlabel(("UTC Time (%s - %s)"%(start_date,end_date)), fontsize=7)
    else:
      self.axes.set_xlabel(("UTC Time (%s)"%(end_date)), fontsize=7)
    # Set the Plot Title
    self.axes.set_title("Discrete Particle Flux", fontsize=10)
    # Create the Legend
    proton_legend = self.axes.legend(
      handles=[Protons_95_keV,Protons_140_keV,Protons_210_keV,Protons_300_keV,Protons_475_keV],
      framealpha=0,
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 1.1), title='p (keV)')
    electron_legend = self.axes.legend(
      handles=[Electrons_40_keV,Electrons_75_keV,Electrons_150_keV,Electrons_275_keV,Electrons_475_keV],
      framealpha=0,
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 0.65), title='e (keV)')
    # Add Legends to plot
    self.axes.add_artist(proton_legend)
    self.axes.add_artist(electron_legend)
    # Redraw plots
    self.draw()
