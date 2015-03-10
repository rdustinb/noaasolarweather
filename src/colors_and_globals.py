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
init_app_height = 900
plotTitleSize = 8
plotLabelSize = 6
legendSize = 6
if(colorMode == "Dark"):
  ColorModeDef = "background-color: #494949;"
  ColorWidgetDef = "#494949"
  canvas_alpha = 0.2
  graph_bgcolor = "#696969"
  grid_color = '#aaaaaa'
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

DifferentialEnergeticProtonFluxLabelThinner = 1
DiscreteParticleFluxLabelThinner = 5
DualXrayFluxLabelThinner = 7
GeomagneticFieldLabelThinner = 7
SolarParticleFluxLabelThinner = 1
ACEDiffElectronProtonFluxLabelThinner = 1
ACEIntegralProtonFluxLabelThinner = 2
ACEInterplanetaryMagFieldLabelThinner = 1
ACESolarWindPlasmaLabelThinner = 7

GOESRangeProtonFluxColors = [
  '#ffd3aa',
  '#aa7039',
  '#552900',
  '#cfd369',
  '#a4a938',
  '#515400',
  '#6a959d',
  '#255e69',
  '#012c34',
  '#9974aa',
  '#5b2971']

GOESGoemagFieldFluxColors = [
  '#aa7039',
  '#a4a938',
  '#255e69',
  '#5b2971']

GOESDiscreteParticleFluxColors = [
  '#ffd3aa',
  '#aa7039',
  '#552900',
  '#cfd369',
  '#a4a938',
  '#515400',
  '#6a959d',
  '#255e69',
  '#012c34',
  '#9974aa']

GOESRangeParticleFluxColors = [
  '#ffd3aa',
  '#aa7039',
  '#552900',
  '#cfd369',
  '#a4a938',
  '#515400',
  '#6a959d',
  '#255e69',
  '#012c34']

GOESXrayFluxColors = [
  '#aa7039',
  '#255e69']

ACEDiffElecProtFluxColors = [
  '#ffd3aa',
  '#aa7039',
  '#552900',
  '#cfd369',
  '#a4a938',
  '#515400',
  '#6a959d']

ACEIntegralProtonFluxColors = [
  '#aa7039',
  '#255e69']

ACESolarWindPlasmaColors = [
  '#aa7039',
  '#a4a938',
  '#255e69']
