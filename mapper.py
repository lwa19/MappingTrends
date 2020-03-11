import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import geopy

import numpy as np
import shapefile as shp

import seaborn as sns

print("yeet")
#plot1()
state_code = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
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
# def get_coor(string_city):

#     '''
#     Attempt to use geocode tool to return coordinate
#     '''
#     print("string_city: " + string_city
#     return geopandas.tools.geocode(starting_city)

def plotter(test_dict = None, file_name = "noname"):
    #print("mk")

    shp_path = "./states_21basic/states.shp"
    sf = shp.Reader(shp_path)

    if test_dict == None:
        ##dictionary used for testing, missing Alaska and Alabama on purpose
        test_dict = { 'AR': 9, 'AZ': 7, 'CA': 5, 'CO': 0, 
        'CT': 8, 'DC': 4, 'DE': 4, 'FL': 8, 'GA': 6, 'HI': 7, 'IA': 0,
        'ID': 1, 'IL': 8, 'IN': 2, 'KS': 7, 'KY': 8, 'LA': 0, 'MA': 8, 
        'MD': 3, 'ME': 3, 'MI': 6, 'MN': 9, 'MO': 6, 'MS': 4, 'MT': 3,
        'NC': 0, 'ND': 7, 'NE': 9, 'NH': 8, 'NJ': 6, 'NM': 2, 'NV': 1,
        'NY': 2, 'OH': 2, 'OK': 9, 'OR': 5, 'PA': 2, 'RI': 5, 'SC': 6,
        'SD': 5, 'TN': 5, 'TX': 6, 'UT': 2, 'VA': 7, 'VT': 7, 'WA': 3,
        'WI': 0, 'WV': 8, 'WY': 8}
    for key in test_dict.keys():
        assert key in state_code





    alt_plot(shp_path, test_dict, file_name)

    #print(len(sf.shapes()))
    # print(sf.records()[i])
    # print("test commit")


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

###THIS CODE IS THE OLD IMPLEMENTATION

# def plot_shape(id,  s=None, path1 = "./states_21basic/states.shp",):
#     sf = shp.Reader(path1)
#     """ PLOTS A SINGLE SHAPE """
#     plt.figure()
#     ax = plt.axes()
#     ax.set_aspect('equal')

#     shape_ex = sf.shape(id)
#     x_lon = np.zeros((len(shape_ex.points),1))
#     y_lat = np.zeros((len(shape_ex.points),1))
#     for ip in range(len(shape_ex.points)):
#         x_lon[ip] = shape_ex.points[ip][0]
#         y_lat[ip] = shape_ex.points[ip][1]

#     x0 = np.mean(x_lon)
#     y0 = np.mean(y_lat)
#     plt.fill(x0, y0)
#     plt.plot(x_lon,y_lat)
#     plt.text(x0, y0, s, fontsize=10)

#     # use bbox (bounding box) to set plot limits
#     plt.xlim(shape_ex.bbox[0],shape_ex.bbox[2])
    
#     plt.savefig('./Plot_pngs/' + sf.record(id)['STATE_ABBR'] + '.png')
#     plt.show()
#     return x0, y0

# #def plot_map(x_lim = None, y_lim = None, figsize = (11,9), path1 = "./states_21basic/states.shp"):
# def plot_map(path1 = "./states_21basic/states.shp", x_lim = None, y_lim = None, figsize = (11,9)):
# #def plot_map(path1 = "./tl_2017_us_state/tl_2017_us_state.shp", x_lim = None, y_lim = None, figsize = (11,9)):
#     '''
#     Plot map with lim coordinates
#     '''
#     #print(path1, x_lim, y_lim, figsize)
#     sf = shp.Reader(path1)
#     plt.figure(figsize = figsize)
#     id=0
#     count = 0
#     for shape in sf.shapeRecords():
#         #print(count); count +=1
#         x = [i[0] for i in shape.shape.points[:]]
#         y = [i[1] for i in shape.shape.points[:]]
#         plt.plot(x, y, 'k') #plot outlines
#         plt.fill('red')
        
#         if (x_lim == None) & (y_lim == None):
#             x0 = np.mean(x)
#             y0 = np.mean(y)
#             plt.text(x0, y0, sf.record(id)['STATE_ABBR'], fontsize=10) #textlabel
#             ax = plt.axes()
#             ax.fill(x0, y0, 'r')

#             #plt.text(x0, y0, sf.record(id)['STUSPS'], fontsize=10)

#             ##plt.text(x0, y0, id, fontsize=10)
#         id = id+1
    
#     if (x_lim != None) & (y_lim != None):     
#         plt.xlim(x_lim)
#         plt.ylim(y_lim)

#     plt.savefig('./Plot_pngs/map1.png')
#     plt.show()

def alt_plot(shp_path, test_dict, file_name):
    # new = geopandas.read_file(shp_path+".shp")
    # return new.plot()
    print("mkay")

    from geopandas import GeoDataFrame
    test = GeoDataFrame.from_file(shp_path)
    

    #test_dict = {'AK': 7, 'AL': 6, 'AR': 9}

    test = join_dict_data(test_dict, test)

    #print(test)
    #test['color_bin_code'] = pd.qcut(test['count'], q =4, labels = [1,2,3,4])
    #print(test['color_bin_code'])
    color_map = get_color_bins(test)
    ##return color_map
    ##??onlytest
    color_sq =['#ffffff00', '#b3cde0','#6497b1','#005b96','#03396c']
    #rint(color_sq[test['color_bin_code'][0]])
    #test.set_index('id', inplace=True)
    #test.sort()
    #test['geometry']
    #print(test.columns())

    import matplotlib.pyplot as plt 
    from descartes import PolygonPatch
    import random
    
    BLUE = '#6699cc'
    fig = plt.figure() 
    for i in range(51):
        poly= test['geometry'][i]
        
        ax = fig.gca() 

        #ax.add_patch(PolygonPatch(poly, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2 ))
        #color_sq =['#b3cde0','#6497b1','#005b96','#03396c','#011f4b']
        print(test['STATE_ABBR'][i])
        print("color_map: " + str(color_map[test['STATE_ABBR'][i]]))
        ax.add_patch(PolygonPatch(poly, fc = color_sq[color_map[test['STATE_ABBR'][i]]], zorder=2 ))
        ax.axis('scaled')
    plt.show()

    #folder "Plot_pngs" needs to exist for this to work
    fig.savefig('./Plot_pngs/' + file_name + '.png')
    #mk.savefig('./Plot_pngs/test.png')
    return test

def get_color_bins(geoframe):
    temp_map  = {}
    temp_list = []
    list_key = []
    list_val = []
    list_none = []
    for row in geoframe.iterrows():
        print(row[1]['count'], type(row[1]['count']))
        if pd.notna(row[1]['count']): ##??check for null
            #temp_list.append((row[1]['STATE_ABBR'],row[1]['count']))
            list_key.append(row[1]['STATE_ABBR'])
            list_val.append(row[1]['count'])
        else:
            print("appended none")
            list_none.append(row[1]['STATE_ABBR'])

    assert len(list_key) == len(list_val)
    list_val = pd.qcut(list_val, q = 4, labels = [1,2,3,4])

    print(list_key)

    for i, state in enumerate(list_key):
        temp_map[state] = list_val[i]

    for state in state_code:
        if state not in temp_map:
            temp_map[state] = 0

    return temp_map

    


def join_dict_data(state_dict, geoframe):
    lst1 = []
    for row in geoframe.iterrows(): ##??cchange iterrows so no index
        is_found = False
        for key, value in state_dict.items():
            if row[1]['STATE_ABBR'] == key:
                lst1.append(value)
                is_found = True
        if is_found == False:
            #print("added none")
            lst1.append(None)

    geoframe['count'] = lst1
    #print("*****************")
    #print(geoframe['count'])
    #print(geoframe['count'])
    return geoframe

# def get_color(state_dict, bin_num):
#     for key,value in state_dict:
#         if 




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
