from MyMplCanvas import MyMplCanvas
from NoaaApi import storeInterplanetMagField
from NoaaApi import getInterplanetMagField
import colors_and_globals
"""
  As of MatPlotLib 1.5 qt4_compat will be deprecated for the more general
  qt_compat. Pulling that in instead.
"""
from matplotlib.backends.qt_compat import QT_API
from matplotlib.backends.qt_compat import QT_API_PYSIDE
"""
  Branch using PyQt or PySide based on MatPlotLib values.
"""
if(QT_API == QT_API_PYSIDE):
  from PySide.QtCore import QTimer
else:
  from PyQt4.QtCore import QTimer

###########################################################################
# Specific Plot Canvas Objects
###########################################################################
class MyInterplanetaryMagField(MyMplCanvas):
  datas = {}
  label_list = []
  stamp = []
  """
    Initialize the updating object.
  """
  def __init__(self, *args, **kwargs):
    MyMplCanvas.__init__(self, left_edge=0.17, right_edge=0.78, top_edge=0.9,
        bottom_edge=0.18, *args, **kwargs)
    timer = QTimer(self)
    # Tie the "update_figure" function to the timer
    timer.timeout.connect(self.update_figure)
    # Millisecond Timer, Assign the update time based on the value returned by
    # the API call, store the API call data in an object-global data variable
    # to reduce the number of API calls required to initialize the plot
    timer.start(60000)

  def update_figure(self):
    """
      This is the actual timer updating method.
    """
    # Update the graph data
    storeInterplanetMagField()
    # Call the compute initial function, only difference is the .draw() method below
    self.compute_initial_figure()
    # Redraw plots
    self.draw()

  def compute_initial_figure(self):
    """
      Initial data plot.
    """
    # Get the new data
    (self.label_list,self.datas,self.stamp) = \
      getInterplanetMagField()
    # Next plot overwrites all previous plots
    self.axes.hold(False)
    self.axes.plot(0)
    self.axes.hold(True)
    # Remove data that is missing
    self.datas["Total"],self.datas["Latitude"],   \
    self.datas["Longitude"],self.stamp =          \
    zip(*[i for i in zip(                         \
        self.datas["Total"],                      \
        self.datas["Latitude"],                   \
        self.datas["Longitude"],                  \
        self.stamp                                \
      )                                           \
      if i[0] != -999.9])
    # Calculate the smallest/largest mag field value to provide proper scaling
    smallest = min(self.datas["Total"])
    largest = max(self.datas["Total"])
    # Calculate the Sizing Multiplier
    area_m = 7/(largest - smallest)
    # Normalize values
    self.datas["Total"] = \
      [(3.14159*(area_m*(t - smallest))**2) for t in self.datas["Total"]]
    pt_colors = [x*(256/len(self.datas["Total"])) for x in range(len(self.datas["Total"]))]
    # Scatter Plot by Latitude/Longitude
    self.axes.scatter(
      self.datas["Longitude"],
      self.datas["Latitude"],
      s=self.datas["Total"],
      c=pt_colors, label=self.datas["Total"], alpha=0.4
    )
    # Draw False Values for size legend
    leg_smallest = (3.14159*(area_m*(smallest))**2)
    leg_largest = (3.14159*(area_m*(largest))**2)
    small = self.axes.scatter([], [], s=leg_smallest, facecolors='none', edgecolors='k')
    large = self.axes.scatter([], [], s=leg_largest, facecolors='none', edgecolors='k')
    # Create the size legend labels
    leg_labels = [str(smallest), str(largest)]
    # Legend
    leg = self.axes.legend(
      [small, large], leg_labels,
      framealpha=0.1,
      loc=1, fontsize=colors_and_globals.legendSize,
      bbox_to_anchor=(1.35, 1.12),
      title="nT",
      borderpad=1,
      scatterpoints=1)
    # Format the Graph
    self.format_graph(pt_colors,smallest,largest)

  def format_graph(self,pt_colors,smallest,largest):
    self.axes.set_ylabel("Latitude (GSM)",
      fontsize=colors_and_globals.plotLabelSize)
    self.axes.set_xlabel("Longitude (GSM)",
      fontsize=colors_and_globals.plotLabelSize)
    # Show all plot grids
    self.axes.grid(True, which="both", color=colors_and_globals.grid_color)
    # Set the graph background color
    self.axes.set_axis_bgcolor(colors_and_globals.graph_bgcolor)
    # Set the Plot Title
    self.axes.set_title("Interplanetary Magnetic Field",
      fontsize=colors_and_globals.plotTitleSize)
