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
progversion = "2.0.5"
progbuild = "1"
progdate = "20150402"

###########################################################################
# Application Globals
###########################################################################
font = {'size' : 7}
init_posx = 150
init_posy = 0
init_app_width = 1000
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

# GOES Differential Proton Flux
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

# GOES Geomagnetic Field
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

# GOES Discrete Particle Flux
if(colorMode == "Light"):
  GOESDiscreteParticleFluxColors = {
    'P1': '#9f0000',
    'P2': '#7f3f00',
    'P3': '#5f5f00',
    'P4': '#3f7f00',
    'P5': '#009f00',
    'E1': '#007f3f',
    'E2': '#005f5f',
    'E3': '#003f7f',
    'E4': '#00009f',
    'E5': '#3f009f'
  }
elif(colorMode == "Dark"):
  GOESDiscreteParticleFluxColors = {
    'P1': '#ff0000',
    'P2': '#bf4f00',
    'P3': '#8f8f00',
    'P4': '#4fbf00',
    'P5': '#00ff00',
    'E1': '#00bf4f',
    'E2': '#008f8f',
    'E3': '#00bf4f',
    'E4': '#0000ff',
    'E5': '#5f00ff'
  }

# GOES Integral Particle Flux
if(colorMode == "Light"):
  GOESIntegralParticleFluxColors = {
    'P>1'   : '#9f0000',
    'P>5'   : '#6f3f00',
    'P>10'  : '#3f6f00',
    'P>30'  : '#009f00',
    'P>50'  : '#006f3f',
    'P>100' : '#003f6f',
    'E>0.8' : '#00009f',
    'E>2.0' : '#3f006f',
    'E>4.0' : '#6f003f'
  }
elif(colorMode == "Dark"):
  GOESIntegralParticleFluxColors = {
    'P>1'   : '#ff0000',
    'P>5'   : '#af5f00',
    'P>10'  : '#5faf00',
    'P>30'  : '#00ff00',
    'P>50'  : '#00af5f',
    'P>100' : '#005faf',
    'E>0.8' : '#0000ff',
    'E>2.0' : '#5f00af',
    'E>4.0' : '#af005f'
  }

# GOES Xray Flux, Flares
if(colorMode == "Light"):
  GOESXrayFluxColors = {
    'Short' : '#9f0000',
    'Long'  : '#00009f'
  }
  GOESXrayFlare = {
    'R1' : '#fff700',
    'R2' : '#ffc900',
    'R3' : '#ff9a00',
    'R4' : '#ff0000',
    'R5' : '#7f0000'
  }
elif(colorMode == "Dark"):
  GOESXrayFluxColors = {
    'Short' : '#ff0000',
    'Long'  : '#0000ff'
  }
  GOESXrayFlare = {
    'R1' : '#fff700',
    'R2' : '#ffc900',
    'R3' : '#ff9a00',
    'R4' : '#ff0000',
    'R5' : '#7f0000'
  }

# ACE Differential Particle Flux
if(colorMode == "Light"):
  ACEDiffElecProtFluxColors = {
    '38-53'     : '#9f0000',
    '175-315'   : '#7f3f00',
    '47-68'     : '#5f5f00',
    '115-195'   : '#3f7f00',
    '310-580'   : '#009f00',
    '795-1193'  : '#007f3f',
    '1060-1900' : '#005f5f'
  }
elif(colorMode == "Dark"):
  ACEDiffElecProtFluxColors = {
    '38-53'     : '#ff0000',
    '175-315'   : '#bf4f00',
    '47-68'     : '#8f8f00',
    '115-195'   : '#4fbf00',
    '310-580'   : '#00ff00',
    '795-1193'  : '#00bf4f',
    '1060-1900' : '#008f8f'
  }

# ACE Integral Proton Flux
if(colorMode == "Light"):
  ACEIntegralProtonFluxColors = {
    '>10' : '#7f7f00',
    '>30' : '#007f7f'
  }
elif(colorMode == "Dark"):
  ACEIntegralProtonFluxColors = {
    '>10' : '#bf3f00',
    '>30' : '#003fbf'
  }

# ACE Solar Wind Plasma
if(colorMode == "Light"):
  ACESolarWindPlasmaColors = {
    'density' : '#9f0000',
    'speed'   : '#009f00',
    'temp'    : '#00009f'
  }
elif(colorMode == "Dark"):
  ACESolarWindPlasmaColors = {
    'density' : '#ff0000',
    'speed'   : '#00ff00',
    'temp'    : '#0000ff'
  }