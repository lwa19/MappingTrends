import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import geopy

import numpy as np
import shapefile as shp

import seaborn as sns

print("yeet")
#plot1()

def plot1():

    ##this is the previous coordinate method
    print("hello world")

    df = pd.DataFrame(
        {'City': ["New York", "Los Angeles", "Chicago", "Miami", "Dallas", "Philadelphia", "Houston", "Washington", "Atlanta", "Boston"],
        'Latitude': [40.6943, 34.1139, 41.8373, 25.7839, 32.7936, 40.0077, 29.7869, 38.9047, 33.7627, 42.3188],
        'Longitude': [-73.9249, -118.4068, -87.6862, -80.2102, -96.7662, -75.1339, -95.3905, -77.0163, -84.4225, -71.0846]})

#cols = ["city", "city_ascii", "state_id", "state_name", "county_fips", "county_name", "county_fips_all", "county_name_all", "lat", "lng", "population", "density", "source", "military", "incorporated", "timezone", "ranking", "zips"]
    #print(df['Longitude'])
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

    mk = gdf.plot(ax = usa.plot(), color='red')
    plt.show()
    mk.savefig('./Plot_pngs/test.png')
    #plt.close()


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
    print("test commit")

def get_reader(path):
    '''
    Input: path (string)
    Output shapefile object
    '''

    return shp.Reader(path)

def read_shapefile(path1 = "./states_21basic/states.shp"):
    '''
    Read a shapefile object a Pandas dataframe with a 'coords' 
    column holding the geometry information. This uses the pyshp
    package
    '''
    sf = shp.Reader(path1)
    fields = [x[0] for x in sf.fields][1:]
    field_attributes = sf.fields
    records = sf.records()
    shapes_objs = sf.shapes()

    shps = [s.points for s in sf.shapes()]
    df = pd.DataFrame(columns=fields, data=records)
    df = df.assign(coords=shps)
    return df

def plot_shape(id,  s=None, path1 = "./states_21basic/states.shp",):
    sf = shp.Reader(path1)
    """ PLOTS A SINGLE SHAPE """
    plt.figure()
    ax = plt.axes()
    ax.set_aspect('equal')

    shape_ex = sf.shape(id)
    x_lon = np.zeros((len(shape_ex.points),1))
    y_lat = np.zeros((len(shape_ex.points),1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]

    x0 = np.mean(x_lon)
    y0 = np.mean(y_lat)
    plt.fill(x0, y0)
    plt.plot(x_lon,y_lat)
    plt.text(x0, y0, s, fontsize=10)

    # use bbox (bounding box) to set plot limits
    plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])
    
    plt.savefig('./Plot_pngs/' + sf.record(id)['STATE_ABBR'] + '.png')
    plt.show()
    return x0, y0

#def plot_map(x_lim = None, y_lim = None, figsize = (11,9), path1 = "./states_21basic/states.shp"):
def plot_map(path1 = "./states_21basic/states.shp", x_lim = None, y_lim = None, figsize = (11,9)):
#def plot_map(path1 = "./tl_2017_us_state/tl_2017_us_state.shp", x_lim = None, y_lim = None, figsize = (11,9)):
    '''
    Plot map with lim coordinates
    '''
    #print(path1, x_lim, y_lim, figsize)
    sf = shp.Reader(path1)
    plt.figure(figsize = figsize)
    id=0
    count = 0
    for shape in sf.shapeRecords():
        #print(count); count +=1
        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]
        plt.plot(x, y, 'k') #plot outlines
        plt.fill('red')
        
        if (x_lim == None) & (y_lim == None):
            x0 = np.mean(x)
            y0 = np.mean(y)
            plt.text(x0, y0, sf.record(id)['STATE_ABBR'], fontsize=10) #textlabel
            ax = plt.axes()
            ax.fill(x0, y0, 'r')

            #plt.text(x0, y0, sf.record(id)['STUSPS'], fontsize=10)

            ##plt.text(x0, y0, id, fontsize=10)
        id = id+1
    
    if (x_lim != None) & (y_lim != None):     
        plt.xlim(x_lim)
        plt.ylim(y_lim)

    plt.savefig('./Plot_pngs/map1.png')
    plt.show()

def alt_plot(shp_path):
    # new = geopandas.read_file(shp_path+".shp")
    # return new.plot()

    from geopandas import GeoDataFrame
    test = GeoDataFrame.from_file(shp_path)
    #test.set_index('id', inplace=True)
    #test.sort()
    test['geometry']

    import matplotlib.pyplot as plt 
    from descartes import PolygonPatch
    import random
    
    BLUE = '#6699cc'
    fig = plt.figure() 
    for i in range(51):
        poly= test['geometry'][i]
        
        ax = fig.gca() 
        #ax.add_patch(PolygonPatch(poly, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2 ))
        ax.add_patch(PolygonPatch(poly, fc = random.choice(['r','g','b']), zorder=2 ))
        ax.axis('scaled')
    plt.show()


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
