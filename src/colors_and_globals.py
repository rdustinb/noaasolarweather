###########################################################################
# This is the master color mode controlling variable. The architecture
# currently supports only "Dark" or "Light". I may branch this to colorize
# the interface, but that would require creating a type of HEX calculating
# algorithm for each plot trace, etc
###########################################################################
colorMode = "Light"

###########################################################################
# Version of the application
###########################################################################
progversion = "0.2"
progbuild = "5"
progdate = "20150310"

###########################################################################
# Application Globals
###########################################################################
font = {'size' : 7}
init_posx = 150
init_posy = 0
init_app_width = 1024
init_app_height = 850
plotTitleSize = 8
plotLabelSize = 6
legendSize = 6
if(colorMode == "Dark"):
  ColorModeDef = "background-color: #494949;"
  ColorWidgetDef = "#494949"
  canvas_alpha = 0.2
  graph_bgcolor = "#696969"
  grid_color = '#555555'
else:
  ColorModeDef = "background-color: #d9d9d9;"
  ColorWidgetDef = "#d9d9d9"
  canvas_alpha = 0.2
  graph_bgcolor = "#e9e9e9"
  grid_color = '#aaaaaa'

###########################################################################
# Graphing Widget Values
###########################################################################
plot_angle = "-45"

DifferentialEnergeticProtonFluxLabel = 1
DiscreteParticleFluxLabelThinner = 5
DualXrayFluxLabelThinner = 7
GeomagneticFieldLabelThinner = 7
SolarParticleFluxLabelThinner = 1
ACEDiffElectronProtonFluxLabelThinner = 1
ACEIntegralProtonFluxLabelThinner = 2
ACEInterplanetaryMagFieldLabelThinner = 1
ACESolarWindPlasmaLabelThinner = 7

DifferentialEnergeticProtonFluxColors = {
  "Light": [
    '#9f0000',
    '#7f3f00',
    '#5f5f00',
    '#3f7f00',
    '#009f00',
    '#007f3f',
    '#005f5f',
    '#003f7f',
    '#00009f',
    '#3f009f',
    '#6f009f'
  ],
  "Dark": [
    '#ff0000',
    '#bf4f00',
    '#8f8f00',
    '#4fbf00',
    '#00ff00',
    '#00bf4f',
    '#008f8f',
    '#00bf4f',
    '#0000ff',
    '#5f00ff',
    '#af00ff'
  ]
}

GOESGeomagFieldFluxColors = {
  "Light": [
    "#9f0000",
    "#009f00",
    "#00009f",
    "#5f005f"
  ],
  "Dark": [
    "#ff0000",
    "#00ff00",
    "#0000ff",
    "#7f007f"
  ]
}

GOESDiscreteParticleFluxColors = {
  "Light": [
    '#9f0000',
    '#7f3f00',
    '#5f5f00',
    '#3f7f00',
    '#009f00',
    '#007f3f',
    '#005f5f',
    '#003f7f',
    '#00009f',
    '#3f009f'
  ],
  "Dark": [
    '#ff0000',
    '#bf4f00',
    '#8f8f00',
    '#4fbf00',
    '#00ff00',
    '#00bf4f',
    '#008f8f',
    '#00bf4f',
    '#0000ff',
    '#5f00ff'
  ]
}

GOESRangeParticleFluxColors = {
  "Light": [
    "#9f0000",
    "#6f3f00",
    "#3f6f00",
    "#009f00",
    "#006f3f",
    "#003f6f",
    "#00009f",
    "#3f006f",
    "#6f003f"
  ],
  "Dark": [
    "#ff0000",
    "#af5f00",
    "#5faf00",
    "#00ff00",
    "#00af5f",
    "#005faf",
    "#0000ff",
    "#5f00af",
    "#af005f"
  ]
}

GOESXrayFluxColors = {
  "Light": [
    "#9f0000",
    "#00009f"
  ],
  "Dark": [
    "#ff0000",
    "#0000ff"
  ]
}

ACEDiffElecProtFluxColors = {
  "Light": [
    '#9f0000',
    '#5f5f00',
    '#009f00',
    '#005f5f',
    '#00009f',
    '#3f007f',
    '#7f003f'
  ],
  "Dark": [
    '#ff0000',
    '#7f7f00',
    '#00ff00',
    '#007f7f',
    '#0000ff',
    '#4f00bf',
    '#bf004f'
  ]
}

ACEIntegralProtonFluxColors = {
  "Light": [
    '#7f7f00',
    '#007f7f'
  ],
  "Dark": [
    '#bf3f00',
    '#003fbf'
  ]
}

ACESolarWindPlasmaColors = {
  "Light": [
    '#9f0000',
    '#009f00',
    '#00009f'
  ],
  "Dark": [
    '#ff0000',
    '#00ff00',
    '#0000ff'
  ]
}
