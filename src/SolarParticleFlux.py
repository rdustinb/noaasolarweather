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
class MyGOESRangeParticleFlux(MyMplCanvas):
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
    self.data = NoaaApi.getGOESRangeParticleFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Get the start date
    start_date = self.data["datestamp"][0].split(sep=":")[0]
    # Get the start date
    end_date = self.data["datestamp"][-1].split(sep=":")[0]
    # Strip only the timestamp out of the array of date/time stamps, keep only a few
    loop = 0
    for stamp in self.data["datestamp"]:
      if(loop % colors_and_globals.label_thinner_1 == 0):
        self.data["datestamp"][loop] = stamp.split(sep=":")[1]
      else:
        self.data["datestamp"][loop] = ""
      loop += 1
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    Protons_gt1_MeV,      = self.axes.plot(data_points, self.data["data"][">1 Mev Protons"]     , colors_and_globals.GOESRangeParticleFluxColors[0], label=">1 Mev")
    # Now just overlay remaining datasets
    self.axes.hold(True)
    Protons_gt5_MeV,      = self.axes.plot(data_points, self.data["data"][">5 Mev Protons"]     , colors_and_globals.GOESRangeParticleFluxColors[1], label=">5 Mev")
    Protons_gt10_MeV,     = self.axes.plot(data_points, self.data["data"][">10 Mev Protons"]    , colors_and_globals.GOESRangeParticleFluxColors[2], label=">10 Mev")
    Protons_gt30_MeV,     = self.axes.plot(data_points, self.data["data"][">30 Mev Protons"]    , colors_and_globals.GOESRangeParticleFluxColors[3], label=">30 Mev")
    Protons_gt50_MeV,     = self.axes.plot(data_points, self.data["data"][">50 Mev Protons"]    , colors_and_globals.GOESRangeParticleFluxColors[4], label=">50 Mev")
    Protons_gt100_MeV,    = self.axes.plot(data_points, self.data["data"][">100 Mev Protons"]   , colors_and_globals.GOESRangeParticleFluxColors[5], label=">100 Mev")
    Electrons_gt0_8_MeV,  = self.axes.plot(data_points, self.data["data"][">0.8 Mev Electrons"] , colors_and_globals.GOESRangeParticleFluxColors[6], label=">0.8 Mev")
    Electrons_gt2_0_MeV,  = self.axes.plot(data_points, self.data["data"][">2.0 Mev Electrons"] , colors_and_globals.GOESRangeParticleFluxColors[7], label=">2.0 Mev")
    Electrons_gt4_0_MeV,  = self.axes.plot(data_points, self.data["data"][">4.0 Mev Electrons"] , colors_and_globals.GOESRangeParticleFluxColors[8], label=">4.0 Mev")
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
    self.axes.set_title("Integral Particle Flux", fontsize=10)
    # Create the Legend
    proton_legend = self.axes.legend(
      handles=[Protons_gt1_MeV,Protons_gt5_MeV,Protons_gt10_MeV,Protons_gt30_MeV,Protons_gt50_MeV,Protons_gt100_MeV],
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 1.1), title='Protons')
    electron_legend = self.axes.legend(
      handles=[Electrons_gt0_8_MeV,Electrons_gt2_0_MeV,Electrons_gt4_0_MeV],
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 0.51), title='Electrons')
    # Add Legends to plot
    self.axes.add_artist(proton_legend)
    self.axes.add_artist(electron_legend)

  def update_figure(self):
    """
      This is the actual timer updating method.
    """
    self.data = NoaaApi.getGOESRangeParticleFlux()
    # Get number of data points
    data_points = numpy.linspace(0,1,len(self.data["datestamp"]))
    # Get the start date
    start_date = self.data["datestamp"][0].split(sep=":")[0]
    # Get the start date
    end_date = self.data["datestamp"][-1].split(sep=":")[0]
    # Strip only the timestamp out of the array of date/time stamps, keep only a few
    loop = 0
    for stamp in self.data["datestamp"]:
      if(loop % label_thinner == 0):
        self.data["datestamp"][loop] = stamp.split(sep=":")[1]
      else:
        self.data["datestamp"][loop] = ""
      loop += 1
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    # x-axis, y-axis, color
    Protons_gt1_MeV,      = self.axes.plot(data_points, self.data["data"][">1 Mev Protons"]     , colors_and_globals.GOESRangeParticleFluxColors[0], label=">1 Mev")
    # Now just overlay remaining datasets
    self.axes.hold(True)
    Protons_gt5_MeV,      = self.axes.plot(data_points, self.data["data"][">5 Mev Protons"]     , colors_and_globals.OESRangeParticleFluxColors[1], label=">5 Mev")
    Protons_gt10_MeV,     = self.axes.plot(data_points, self.data["data"][">10 Mev Protons"]    , colors_and_globals.OESRangeParticleFluxColors[2], label=">10 Mev")
    Protons_gt30_MeV,     = self.axes.plot(data_points, self.data["data"][">30 Mev Protons"]    , colors_and_globals.OESRangeParticleFluxColors[3], label=">30 Mev")
    Protons_gt50_MeV,     = self.axes.plot(data_points, self.data["data"][">50 Mev Protons"]    , colors_and_globals.OESRangeParticleFluxColors[4], label=">50 Mev")
    Protons_gt100_MeV,    = self.axes.plot(data_points, self.data["data"][">100 Mev Protons"]   , colors_and_globals.OESRangeParticleFluxColors[5], label=">100 Mev")
    Electrons_gt0_8_MeV,  = self.axes.plot(data_points, self.data["data"][">0.8 Mev Electrons"] , colors_and_globals.OESRangeParticleFluxColors[6], label=">0.8 Mev")
    Electrons_gt2_0_MeV,  = self.axes.plot(data_points, self.data["data"][">2.0 Mev Electrons"] , colors_and_globals.OESRangeParticleFluxColors[7], label=">2.0 Mev")
    Electrons_gt4_0_MeV,  = self.axes.plot(data_points, self.data["data"][">4.0 Mev Electrons"] , colors_and_globals.OESRangeParticleFluxColors[8], label=">4.0 Mev")
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
    self.axes.set_ylabel(self.data["units"], rotation='vertical', fontsize=7)
    # Show Units of x-axis
    if(start_date != end_date):
      self.axes.set_xlabel(("UTC Time (%s - %s)"%(start_date,end_date)), fontsize=7)
    else:
      self.axes.set_xlabel(("UTC Time (%s)"%(end_date)), fontsize=7)
    # Set the Plot Title
    self.axes.set_title("Integral Particle Flux", fontsize=10)
    # Create the Legend
    proton_legend = self.axes.legend(
      handles=[Protons_gt1_MeV,Protons_gt5_MeV,Protons_gt10_MeV,Protons_gt30_MeV,Protons_gt50_MeV,Protons_gt100_MeV],
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 1.1), title='Protons')
    electron_legend = self.axes.legend(
      handles=[Electrons_gt0_8_MeV,Electrons_gt2_0_MeV,Electrons_gt4_0_MeV],
      loc=1, fontsize=6, bbox_to_anchor=(1.2, 0.61), title='Electrons')
    # Add Legends to plot
    self.axes.add_artist(proton_legend)
    self.axes.add_artist(electron_legend)
    # Redraw plots
    self.draw()
