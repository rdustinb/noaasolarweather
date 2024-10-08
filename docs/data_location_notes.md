# Science
NOAA determines three different kinds of Space Weather metrics which are a combination of multiple
satellite sensor measurements, not just one kind.
  * Geomagnetic Storms
    * Occur when the Kp level is 5, 6, 7, 8 or 9
  * Solar Radiation Storms
    * Occur when >= 10MeV particles with Flux levels above 10, 10^2, 10^3, 10^4 and 10^5
    * This ties directly to the Solar Wind summary(TODO what is this Flux)
      * https://services.swpc.noaa.gov/products/summary/solar-wind-mag-field.json
  * Radio Blackouts
    * Occur when the power(TODO what is this value?) is >10^-5, >5*10^-5, >10^-4, >10^-3 or >2*10^-3

# Hierarchy
The NOAA site is structure with the following base URL, everything is contained underneath this URL.

https://services.swpc.noaa.gov/

## Tri-Sensor Measurements Summary, 5 min
These do not directly correlate to the three kinds of Space Weather metrics mentioned above.

There are three summaries which appear to be where the nice little green/yellow/read graphic comes
from.

 * https://services.swpc.noaa.gov/products/summary/10cm-flux.json
 * https://services.swpc.noaa.gov/products/summary/solar-wind-mag-field.json
 * https://services.swpc.noaa.gov/products/summary/solar-wind-speed.json

# Extended Data
## Raw Sensor Data
These are split up based on spacecraft which adds another layer of complexity as the coder needs to
know where these satellites are when the measurements were taken.

### ACE
This satellite delivers 5m and 32s interval Low Enery Electrons and Protons data under the EPAM data
name.
This satellite delivers 5m and 32s interval High Energy Protons data under the SIS data name.
This satellite delivers 1h Magnetic Field data under the MAG data name.
This satellite delivers 1h Plasma data under the SWEPAM data name.
All the data is located under this FTP folder and subfolders.
  * https://services.swpc.noaa.gov/json/ace/

### Discover
This satellite collects 1s intervals of magnetometer data only.

### GOES 16
Considered the primary source of GOES data it goestation orbits at longitude 75.2. Sources of data
include electrons, protons, magnetometers and xrays. Multiple JSON archives of data located in this
FTP folder.
  * https://services.swpc.noaa.gov/json/goes/primary/

## Region Information
There is a list of E-Field data sources stored as a JSON object here that appear to only be based on
geographical location on the Earth itself and are only data points for the last 24 hours.

https://services.swpc.noaa.gov/products/lists/rgeojson.json

Here is an example of the data found at just one of those listed JSON locations.

{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": 
        {
          "type": "Point",
          "coordinates": [-81.0, 24.0]
        },
      "properties":
        {
          "Ex": 0.47,
          "Ey": -0.18,
          "quality_flag": 5,
          "distance_nearest_station": 1107.47
        }
    }, 
    {
      ...
    }
  ]
}

## All Sources

https://services.swpc.noaa.gov/json/goes/primary/differential-protons-1-day.json
https://services.swpc.noaa.gov/json/goes/primary/differential-electrons-1-day.json
https://services.swpc.noaa.gov/json/goes/primary/integral-protons-1-day.json
https://services.swpc.noaa.gov/json/goes/primary/integral-electrons-1-day.json
https://services.swpc.noaa.gov/json/goes/primary/magnetometers-1-day.json
https://services.swpc.noaa.gov/json/goes/primary/xrays-1-day.json
