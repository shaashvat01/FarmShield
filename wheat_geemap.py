import ee 
from ee_plugin import Map

map = ui.Map()
map.setCenter(-98.5795, 39.8283, 4); # Center on the United States
ui.root.clear(); # Clear the default panels
ui.root.add(map); # Add the map to the UI

# Custom base map style (optional)
basemapStyle = [
  {'elementType': 'geometry', 'stylers': '[{color': '#f5f5f5'}]},
  {'elementType': 'labels.icon', 'stylers': '[{visibility': 'off'}]},
  {'elementType': 'labels.text.fill', 'stylers': '[{color': '#616161'}]},
  {'elementType': 'labels.text.stroke', 'stylers': '[{color': '#f5f5f5'}]},
  {
    'featureType': 'administrative.land_parcel',
    'elementType': 'labels.text.fill',
    'stylers': '[{color': '#bdbdbd'}]
  },
  {
    'featureType': 'poi',
    'elementType': 'geometry',
    'stylers': '[{color': '#eeeeee'}]
  },
  {
    'featureType': 'poi',
    'elementType': 'labels.text.fill',
    'stylers': '[{color': '#757575'}]
  },
  {
    'featureType': 'poi.park',
    'elementType': 'geometry',
    'stylers': '[{color': '#e5e5e5'}]
  },
  {
    'featureType': 'poi.park',
    'elementType': 'labels.text.fill',
    'stylers': '[{color': '#9e9e9e'}]
  },
  {
    'featureType': 'road',
    'elementType': 'geometry',
    'stylers': '[{color': '#ffffff'}]
  },
  {
    'featureType': 'road.arterial',
    'elementType': 'labels.text.fill',
    'stylers': '[{color': '#757575'}]
  },
  {
    'featureType': 'road.highway',
    'elementType': 'geometry',
    'stylers': '[{color': '#dadada'}]
  },
  {
    'featureType': 'road.highway',
    'elementType': 'labels.text.fill',
    'stylers': '[{color': '#616161'}]
  },
  {
    'featureType': 'road.local',
    'elementType': 'labels.text.fill',
    'stylers': '[{color': '#9e9e9e'}]
  },
  {
    'featureType': 'transit.line',
    'elementType': 'geometry',
    'stylers': '[{color': '#e5e5e5'}]
  },
  {
    'featureType': 'transit.station',
    'elementType': 'geometry',
    'stylers': '[{color': '#eeeeee'}]
  },
  {
    'featureType': 'water',
    'elementType': 'geometry',
    'stylers': '[{color': '#c9c9c9'}]
  },
  {
    'featureType': 'water',
    'elementType': 'labels.text.fill',
    'stylers': '[{color': '#9e9e9e'}]
  }
]

map.setOptions('Custom Style', { 'Custom Style': basemapStyle })

panel = ui.Panel({'style': '{width': '300px'}})
ui.root.add(panel); # Add the panel to the UI



# Define a region of interest as a point
point = ee.Geometry.Point(-105.077209, 39.766098)

# Adjust the filter date for specific wheat farming seasons over 2-4 years, considering winter wheat
startYear = 2018; # Example start year
endYear = 2021; # Example end year, adjust according to your needs

# Load CDL dataset for wheat (class 24 and 26 for winter wheat and double crop)
cdl = ee.ImageCollection("USDA/NASS/CDL") \
             .filter(ee.Filter.calendarRange(startYear, endYear, 'year')) \
             .select(['cropland'])

def func_uji(image):
               return image.eq(24).Or(image.eq(26)).selfMask() \
             .map(func_uji)




# Visualize the CDL data on the map to identify wheat farming areas
m.addLayer(cdl.sum(), {'min': 0, 'max': endYear-startYear, 'palette': ['yellow', 'green']}, 'Wheat Farming Areas')

# For water availability, consider integrating a precipitation dataset, like CHIRPS
precipitation = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY") \
                      .filterDate(ee.Date.fromYMD(startYear, 4, 1), ee.Date.fromYMD(endYear, 7, 31))

# Calculate and visualize total precipitation during the wheat seasons
totalPrecipitation = precipitation.sum()
m.addLayer(totalPrecipitation, {'min': 0, 'max': 2000, 'palette': ['blue', 'limegreen', 'yellow']}, 'Total Precipitation')

# Generate a graph for precipitation over time
precipChart = ui.Chart.image.series({
  'imageCollection': precipitation,
  'region': point,
  'reducer': ee.Reducer.sum(),
  'scale': 5000,
  'xProperty': 'system:time_start'
}).setOptions({
  'title': 'Precipitation over Wheat Season',
  'vAxis': '{title': 'Precipitation (mm)'},
  'hAxis': '{title': 'Time'},
  'lineWidth': 1,
  'pointSize': 3
})

# Display the precipitation chart
print(precipChart)

# Define a region of interest as a point
point = ee.Geometry.Point(-105.077209, 39.766098)

# Adjust the filter date for specific wheat farming seasons over 2-4 years, considering winter wheat
startYear = 2018; # Example start year
endYear = 2021; # Example end year, adjust according to your needs

# Load CDL dataset for wheat (class 24 and 26 for winter wheat and double crop)
cdl = ee.ImageCollection("USDA/NASS/CDL") \
             .filter(ee.Filter.calendarRange(startYear, endYear, 'year')) \
             .select(['cropland'])

def func_unp(image):
               return image.eq(24).Or(image.eq(26)).selfMask() \
             .map(func_unp)




# Visualize the CDL data on the map to identify wheat farming areas
m.addLayer(cdl.sum(), {'min': 0, 'max': endYear-startYear, 'palette': ['yellow', 'green']}, 'Wheat Farming Areas')

# For water availability, consider integrating a precipitation dataset, like CHIRPS
precipitation = ee.ImageCollection("UCSB-CHG/CHIRPS/DAILY") \
                      .filterDate(ee.Date.fromYMD(startYear, 4, 1), ee.Date.fromYMD(endYear, 7, 31))

# Calculate and visualize total precipitation during the wheat seasons
totalPrecipitation = precipitation.sum()
m.addLayer(totalPrecipitation, {'min': 0, 'max': 2000, 'palette': ['blue', 'limegreen', 'yellow']}, 'Total Precipitation')

# No change needed in the graph generation part as it correctly shows total precipitation over time.

# Define the spring wheat growing season
springStart = '04-01'
springEnd = '07-31'

# Define the winter wheat growing season
winterStart = '09-01'
winterEnd = '06-30'

# Calculate total precipitation for the spring wheat season
springPrecipitation = precipitation.filter(ee.Filter.date(ee.Date.fromYMD(startYear, 4, 1), ee.Date.fromYMD(endYear, 7, 31)))
totalSpringPrecipitation = springPrecipitation.sum()

# Calculate total precipitation for the winter wheat season spanning years
winterPrecipitation = precipitation.filter(ee.Filter.date(ee.Date.fromYMD(startYear - 1, 9, 1), ee.Date.fromYMD(endYear, 6, 30)))
totalWinterPrecipitation = winterPrecipitation.sum()

# Function to calculate and print total precipitation for spring and winter wheat
def printTotalPrecipitation(image, label):
  totalPrecipitation = image.reduceRegion({
    'reducer': ee.Reducer.sum(),
    'geometry': point,
    'scale': 5000,
    'maxPixels': 1e9
  }).values().get(0)

  totalPrecipitation.evaluate(function(result) {
    print(label + ': ' + (result || 0).toFixed(2) + ' mm')
  })


# Print total precipitation for Spring and Winter Wheat
printTotalPrecipitation(totalSpringPrecipitation, 'Total Spring Wheat Precipitation')
printTotalPrecipitation(totalWinterPrecipitation, 'Total Winter Wheat Precipitation')

bufferedRegion = point.buffer(10000); # Buffer by 10 km to capture surrounding fields

# Define the time range for your analysis
startYear = 2018
endYear = 2021

# Load the CDL dataset
cdl = ee.ImageCollection("USDA/NASS/CDL") \
             .filter(ee.Filter.calendarRange(startYear, endYear, 'year')) \
             .select(['cropland'])

# Function to calculate the area for a given crop class (band value)
def calculateCropArea(cropClass, colorHex, label):

def func_bnc(image):
    return image.eq(cropClass).selfMask()

  cropArea = cdl.map(func_bnc
).sum().multiply(ee.Image.pixelArea()).divide(1e4); # Area in hectares

).sum().multiply(ee.Image.pixelArea()).divide(1e4); # Area in hectares

  totalCropArea = cropArea.reduceRegion({
    'reducer': ee.Reducer.sum(),
    'geometry': bufferedRegion,
    'scale': 30,
    'maxPixels': 1e9
  }).get('cropland')

  totalCropArea.evaluate(function(result) {
    print(label + ' Area (hectares) - ' + colorHex + ':', result)
  })


# Calculate areas for Spring Wheat (class 23), Winter Wheat (class 24), and Durum Wheat
calculateCropArea(23, '#d8b56b', 'Spring Wheat')
calculateCropArea(24, '#a57000', 'Winter Wheat')
calculateCropArea(22, '#896054', 'Durum Wheat'); # Assuming the class value for Durum Wheat is 22


# Load a temperature dataset such as MODIS Land Surface Temperature
temperature = ee.ImageCollection('MODIS/061/MOD11A2') \
                   .filter(ee.Filter.date(ee.Date.fromYMD(startYear, 1, 1), ee.Date.fromYMD(endYear, 12, 31))) \
                   .select('LST_Day_1km')

#/ Convert temperature from Kelvin to Celsius, and calculate average temperature during the spring and winter seasons
def tempToCelsius(image):
  # MODIS LST data are in Kelvin and scaled by 0.02; thus, we divide by 50, then subtract 273.15 to convert to Celsius.
  return image.multiply(0.02).subtract(273.15).set('system:time_start', image.get('system:time_start'))


# Modify the band name for solar radiation
radiation = ee.ImageCollection("NASA/GLDAS/V021/NOAH/G025/T3H") \
                 .filter(ee.Filter.date(ee.Date.fromYMD(startYear, 1, 1), ee.Date.fromYMD(endYear, 12, 31))) \
                 .select('SWdown_f_tavg'); 
                 #Shortwave radiation downwards

def tempToCelsius(image):
  # MODIS LST data are in Kelvin and scaled by 0.02; thus, we divide by 50, then subtract 273.15 to convert to Celsius.
  return image.multiply(0.02).subtract(273.15).set('system:time_start', image.get('system:time_start'))


# Calculate average daily solar radiation during the spring and winter seasons
avgSpringRadiation = radiation.filter(ee.Filter.dayOfYear(91, 182)).mean()
avgWinterRadiation = radiation.filter(ee.Filter.dayOfYear(274, 365)).mean()

# Reduce the region to get average radiation values
def getRadiationStats(image, label):
  stats = image.reduceRegion({
    'reducer': ee.Reducer.mean(),
    'geometry': point,
    'scale': 30,
    'maxPixels': 1e9
  })
  print(label, stats.get('SWdown_f_tavg'))

# ... (other code)

# Convert the temperature collection to Celsius
temperatureCelsius = temperature.map(tempToCelsius)

# Function to create a time series chart of temperature
def createTempChart(tempCollection, seasonName):
  tempChart = ui.Chart.image.series({
    'imageCollection': tempCollection,
    'region': bufferedRegion,
    'reducer': ee.Reducer.mean(),
    'scale': 1000
  }).setOptions({
    'title': seasonName + ' Temperature Over Time',
    'vAxis': '{title': 'Temperature (Celsius)'},
    'hAxis': '{title': 'Time'},
    'lineWidth': 1,
    'pointSize': 3,
    'series': '{0': '{color': 'FF0000'}} # Color the line red for visibility
  })

  print(tempChart)


# Create temperature charts for the spring and winter seasons
'tempDuringSpring = temperatureCelsius.filter(ee.Filter.dayOfYear(91, 182)); # Spring': April to June
createTempChart(tempDuringSpring, 'Spring')

'tempDuringWinter = temperatureCelsius.filter(ee.Filter.dayOfYear(274, 365)); # Winter': October to December
createTempChart(tempDuringWinter, 'Winter')

# ... (other code)


# Print average solar radiation for spring and winter
getRadiationStats(avgSpringRadiation, 'Average Intensity of Sunlight (b/w 200-600) (W/m^2)')
getRadiationStats(avgWinterRadiation, 'Average Intensity of Sunlight (b/w 200-600) (W/m^2)')


# Define your point of interest with longitude and latitude
pointOfInterest = ee.Geometry.Point(-98.484246, 39.011902)

# Import the SMAP soil moisture data
dataset = ee.ImageCollection('NASA/SMAP/SPL4SMGP/007') \
                .filter(ee.Filter.date('2020-01-01', '2020-01-10'))

# Select the surface and root zone soil moisture data
surfaceSoilMoisture = dataset.select('sm_surface')
rootZoneSoilMoisture = dataset.select('sm_rootzone')

# Get the mean soil moisture over the specified period for both layers
meanSurfaceSoilMoisture = surfaceSoilMoisture.mean()
meanRootZoneSoilMoisture = rootZoneSoilMoisture.mean()

# Add the soil moisture layers to the map with different color palettes for visualization
m.addLayer(meanSurfaceSoilMoisture, {'min': 0, 'max': 0.5, 'palette': ['blue', 'green', 'yellow', 'red']}, 'Mean Surface Soil Moisture')
m.addLayer(meanRootZoneSoilMoisture, {'min': 0, 'max': 0.5, 'palette': ['lightblue', 'lightgreen', 'lightyellow', 'pink']}, 'Mean Root Zone Soil Moisture')
m.centerObject(pointOfInterest, 10)

surfaceSoilMoistureValue = meanSurfaceSoilMoisture.reduceRegion({
  'reducer': ee.Reducer.mean(),
  'geometry': pointOfInterest,
  'scale': 10000
}).get('sm_surface').getInfo()

rootZoneSoilMoistureValue = meanRootZoneSoilMoisture.reduceRegion({
  'reducer': ee.Reducer.mean(),
  'geometry': pointOfInterest,
  'scale': 10000
}).get('sm_rootzone').getInfo()

print('Surface Soil Moisture Value (b/w 0.2-0.3:', surfaceSoilMoistureValue)
print('Root Zone Soil Moisture Value (b/w 0.2-0.3:', rootZoneSoilMoistureValue)

# Mannan A - Fear the Fork
m