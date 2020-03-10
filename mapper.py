import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import geopy

import numpy as np
import shapefile as shp

import seaborn as sns

def plot():
    print("hello world")

    df = pd.DataFrame(
        {'City': ["New York", "Los Angeles", "Chicago", "Miami", "Dallas", "Philadelphia", "Houston", "Washington", "Atlanta", "Boston"],
        'Latitude': [40.6943, 34.1139, 41.8373, 25.7839, 32.7936, 40.0077, 29.7869, 38.9047, 33.7627, 42.3188],
     '  Longitude': [-73.9249, -118.4068, -87.6862, -80.2102, -96.7662, -75.1339, -95.3905, -77.0163, -84.4225, -71.0846]})

#cols = ["city", "city_ascii", "state_id", "state_name", "county_fips", "county_name", "county_fips_all", "county_name_all", "lat", "lng", "population", "density", "source", "military", "incorporated", "timezone", "ranking", "zips"]

    gdf = geopandas.GeoDataFrame(df, geometry=geopandas.points_from_xy(df.Longitude, df.Latitude))
    geopandas.tools
    print(gdf.head())

#world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
#print(world.head())
# We restrict to South America.
#ax = world[world.continent == 'North America'].plot(
 #   color='white', edgecolor='black')

# We can now plot our ``GeoDataFrame``.




#path1 = 'home/kunalmahajan/cmsc12200-win-20-kunalmahajan/states_21basic/states.shp'
    path1 = "states_21basic/states.shp"
    usa = geopandas.read_file(path1)

    gdf.plot(ax = usa.plot(), color='red')
    plt.show()


def get_coor(string_city):
	print("string_city: " + string_city)
	return geopandas.tools.geocode(starting_city)

def test_plot(i):
    #print("mk")
    shp_path = "./states_21basic/states.shp"
    sf = shp.Reader(shp_path)
    #print(len(sf.shapes()))
    print(sf.records()[i])

def get_reader(path):

    return shp.Reader(path)
