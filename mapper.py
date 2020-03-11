import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import geopy

import numpy as np
import shapefile as shp

import seaborn as sns

def plot():

    ##this is the previous coordinate method
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
    '''

    Attempt to use geocode tool to return coordinate
    '''
	print("string_city: " + string_city)
	return geopandas.tools.geocode(starting_city)

def test_plot(i):
    #print("mk")
    shp_path = "./states_21basic/states.shp"
    sf = shp.Reader(shp_path)
    #print(len(sf.shapes()))
    print(sf.records()[i])

def get_reader(path):
    '''
    Input: path (string)
    Output shapefile object
    '''

    return shp.Reader(path)

def read_shapefile(sf):
    '''
    Read a shapefile object a Pandas dataframe with a 'coords' 
    column holding the geometry information. This uses the pyshp
    package
    '''
    fields = [x[0] for x in sf.fields][1:]
    field_attributes = sf.fields
    records = sf.records()
    shapes_objs = sf.shapes()

    shps = [s.points for s in sf.shapes()]f
    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(coords=shps)
    1 + 1
    return df

def file_editor():
    '''
    Initializes new shapefile

    '''

    w = shapefile.Writer('./testfile')

def record_editor():
    '''
    Updates dbf file in shapefile folder
    '''

    db = dbf.Dbf("your_file.dbf")

    #Editing a value, assuming you want to edit the first field of the first record
    
    for rec in db:
        rec["Count"] = sf.records()


    rec.store()
    del rec
    db.close()  

def image_make(bins):
    '''
    Inputs: bins(list of matplotlib objects)
    Outputs: multiple png files
            ##directory not yet made for this

    '''
    for bin1 in bins:
        plt.savefig(bin1)
