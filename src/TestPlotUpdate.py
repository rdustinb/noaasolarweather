"""
    Now use PyQtGraph

    http://www.pyqtgraph.org/documentation/introduction.html
"""

from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg
import NoaaApi

app = QtGui.QApplication([])

win = pg.GraphicsWindow(title="Basic plotting examples")
win.resize(400,200)
win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

# def update():
#     global curve, data, ptr, p6
#     curve.setData(data[ptr%10])
#     if ptr == 0:
#         p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
#     ptr += 1

# Timer Function
def xray_flux_short():
    global xrayFlux, xrayFlux_curve, xrayFlux_data
    xrayFlux_curve.setData(xrayFlux_data[2])
    xrayFlux_data = NoaaApi.getXrayFlux()

# Create the XRay Flux Graph Instance
xrayFlux = win.addPlot(title="XRay Flux")
xrayFlux_curve = xrayFlux.plot(pen='y')
xrayFlux_data = NoaaApi.getXrayFlux()

xrayFluxtimer = QtCore.QTimer()
xrayFluxtimer.timeout.connect(xray_flux_short)
xrayFluxtimer.start(60000)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()