"""
    Proton Flux Example plotting, the plot comes up in log mode
    as the highest power proton flux is about 3 orders of magnitude
    smaller than the lowest energy level.

    PyQtGraph
    http://www.pyqtgraph.org/documentation/introduction.html
"""

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import NoaaApi

app = QtGui.QApplication([])

win = pg.GraphicsWindow()
win.resize(800,400)
win.setWindowTitle('Flux : Proton Range Plot')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

# Timer Function
def timer_getGOESRangeProtonFlux():
    global protonFlux_curve_0_7_4MeV,protonFlux_curve_4_9MeV
    global protonFlux_curve_9_15MeV,protonFlux_curve_15_40MeV
    global protonFlux_curve_38_82MeV,protonFlux_curve_84_200MeV
    global protonFlux_curve_110_900MeV,protonFlux_curve_350_420MeV
    global protonFlux_curve_420_510MeV,protonFlux_curve_510_700MeV
    global protonFlux_curve_gt700MeV
    global protonFlux_data
    protonFlux_curve_0_7_4MeV.setData(protonFlux_data  ["data"]["0.7-4 MeV Protons"  ])
    protonFlux_curve_4_9MeV.setData(protonFlux_data    ["data"]["4-9 MeV Protons"    ])
    protonFlux_curve_9_15MeV.setData(protonFlux_data   ["data"]["9-15 MeV Protons"   ])
    protonFlux_curve_15_40MeV.setData(protonFlux_data  ["data"]["15-40 MeV Protons"  ])
    protonFlux_curve_38_82MeV.setData(protonFlux_data  ["data"]["38-82 MeV Protons"  ])
    protonFlux_curve_84_200MeV.setData(protonFlux_data ["data"]["84-200 MeV Protons" ])
    protonFlux_curve_110_900MeV.setData(protonFlux_data["data"]["110-900 MeV Protons"])
    protonFlux_curve_350_420MeV.setData(protonFlux_data["data"]["350-420 MeV Protons"])
    protonFlux_curve_420_510MeV.setData(protonFlux_data["data"]["420-510 MeV Protons"])
    protonFlux_curve_510_700MeV.setData(protonFlux_data["data"]["510-700 MeV Protons"])
    protonFlux_curve_gt700MeV.setData(protonFlux_data  ["data"][">700 MeV Protons"   ])
    protonFlux_data = NoaaApi.getGOESRangeProtonFlux()

# Create the Proton Flux Graph Instance
protonFlux = win.addPlot(title="Proton Flux")
protonFlux.setLogMode(y=True)
protonFlux.showGrid(x=True,y=True,alpha=0.3)

# Grab initial plot data, contains all Proton Flux Energies
protonFlux_data = NoaaApi.getGOESRangeProtonFlux()

# One "plot" for each energy of protons
protonFlux_curve_0_7_4MeV   = protonFlux.plot(pen="4e98b0")
protonFlux_curve_4_9MeV     = protonFlux.plot(pen="2d809b")
protonFlux_curve_9_15MeV    = protonFlux.plot(pen="0e7495")
protonFlux_curve_15_40MeV   = protonFlux.plot(pen="075975")
protonFlux_curve_38_82MeV   = protonFlux.plot(pen="03455b")
protonFlux_curve_84_200MeV  = protonFlux.plot(pen="5680b7")
protonFlux_curve_110_900MeV = protonFlux.plot(pen="3565a3")
protonFlux_curve_350_420MeV = protonFlux.plot(pen="16519d")
protonFlux_curve_420_510MeV = protonFlux.plot(pen="0d3d7a")
protonFlux_curve_510_700MeV = protonFlux.plot(pen="072e60")
protonFlux_curve_gt700MeV   = protonFlux.plot(pen="4DB59B")

# Create the legend
protonLegend = pg.LegendItem()
protonLegend.setParentItem(protonFlux)
protonLegend.addItem(protonFlux_curve_0_7_4MeV,   "0.7-4 MeV Protons")
protonLegend.addItem(protonFlux_curve_4_9MeV,     "4-9 MeV Protons")
protonLegend.addItem(protonFlux_curve_9_15MeV,    "9-15 MeV Protons")
protonLegend.addItem(protonFlux_curve_15_40MeV,   "15-40 MeV Protons")
protonLegend.addItem(protonFlux_curve_38_82MeV,   "38-82 MeV Protons")
protonLegend.addItem(protonFlux_curve_84_200MeV,  "84-200 MeV Protons")
protonLegend.addItem(protonFlux_curve_110_900MeV, "110-900 MeV Protons")
protonLegend.addItem(protonFlux_curve_350_420MeV, "350-420 MeV Protons")
protonLegend.addItem(protonFlux_curve_420_510MeV, "420-510 MeV Protons")
protonLegend.addItem(protonFlux_curve_510_700MeV, "510-700 MeV Protons")
protonLegend.addItem(protonFlux_curve_gt700MeV,   ">700 MeV Protons")

# Plot initial
protonFlux_curve_0_7_4MeV.setData(protonFlux_data  ["data"]["0.7-4 MeV Protons"  ])
protonFlux_curve_4_9MeV.setData(protonFlux_data    ["data"]["4-9 MeV Protons"    ])
protonFlux_curve_9_15MeV.setData(protonFlux_data   ["data"]["9-15 MeV Protons"   ])
protonFlux_curve_15_40MeV.setData(protonFlux_data  ["data"]["15-40 MeV Protons"  ])
protonFlux_curve_38_82MeV.setData(protonFlux_data  ["data"]["38-82 MeV Protons"  ])
protonFlux_curve_84_200MeV.setData(protonFlux_data ["data"]["84-200 MeV Protons" ])
protonFlux_curve_110_900MeV.setData(protonFlux_data["data"]["110-900 MeV Protons"])
protonFlux_curve_350_420MeV.setData(protonFlux_data["data"]["350-420 MeV Protons"])
protonFlux_curve_420_510MeV.setData(protonFlux_data["data"]["420-510 MeV Protons"])
protonFlux_curve_510_700MeV.setData(protonFlux_data["data"]["510-700 MeV Protons"])
protonFlux_curve_gt700MeV.setData(protonFlux_data  ["data"][">700 MeV Protons"   ])
protonFlux_data = NoaaApi.getGOESRangeProtonFlux()

protonFluxtimer = QtCore.QTimer()
protonFluxtimer.timeout.connect(timer_getGOESRangeProtonFlux)
protonFluxtimer.start(int(protonFlux_data["update"]))

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()