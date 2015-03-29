###########################################################################
# This is the master color mode controlling variable. The architecture
# currently supports only "Dark" or "Light". I may branch this to colorize
# the interface, but that would require creating a type of HEX calculating
# algorithm for each plot trace, etc
###########################################################################
colorMode = "Dark"

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

DiscreteParticleFluxLabelThinner = 5
DualXrayFluxLabelThinner = 7
SolarParticleFluxLabelThinner = 1
ACEDiffElectronProtonFluxLabelThinner = 1
ACEIntegralProtonFluxLabelThinner = 2
ACEInterplanetaryMagFieldLabelThinner = 1
ACESolarWindPlasmaLabelThinner = 7

if(colorMode == "Light"):
  DifferentialEnergeticProtonFluxColors = {
    'P1' :'#9f0000',
    'P2' :'#7f3f00',
    'P3' :'#5f5f00',
    'P4' :'#3f7f00',
    'P5' :'#009f00',
    'P6' :'#007f3f',
    'P7' :'#005f5f',
    'P8' :'#003f7f',
    'P9' :'#00009f',
    'P10':'#3f009f',
    'P11':'#6f009f'
  }
elif(colorMode == "Dark"):
  DifferentialEnergeticProtonFluxColors = {
    'P1' :'#ff0000',
    'P2' :'#bf4f00',
    'P3' :'#8f8f00',
    'P4' :'#4fbf00',
    'P5' :'#00ff00',
    'P6' :'#00bf4f',
    'P7' :'#008f8f',
    'P8' :'#00bf4f',
    'P9' :'#0000ff',
    'P10':'#5f00ff',
    'P11':'#af00ff'
  }

if(colorMode == "Light"):
  GOESGeomagFieldFluxColors = {
    'Hp'    : '#9f0000',
    'He'    : '#009f00',
    'Hn'    : '#00009f',
    'Total' : '#5f005f'
  }
elif(colorMode == "Dark"):
  GOESGeomagFieldFluxColors = {
    'Hp'    : '#ff0000',
    'He'    : '#00ff00',
    'Hn'    : '#0000ff',
    'Total' : '#7f007f'
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
