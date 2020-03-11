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
test_dict = { 'AR': 9, 'AZ': 7, 'CA': 5, 'CO': 0, 
        'CT': 8, 'DC': 4, 'DE': 4, 'FL': 8, 'GA': 6, 'HI': 7, 'IA': 0,
        'ID': 1, 'IL': 8, 'IN': 2, 'KS': 7, 'KY': 8, 'LA': 0, 'MA': 8, 
        'MD': 3, 'ME': 3, 'MI': 6, 'MN': 9, 'MO': 6, 'MS': 4, 'MT': 3,
        'NC': 0, 'ND': 7, 'NE': 9, 'NH': 8, 'NJ': 6, 'NM': 2, 'NV': 1,
        'NY': 2, 'OH': 2, 'OK': 9, 'OR': 5, 'PA': 2, 'RI': 5, 'SC': 6,
        'SD': 5, 'TN': 5, 'TX': 6, 'UT': 2, 'VA': 7, 'VT': 7, 'WA': 3,
        'WI': 0, 'WV': 8, 'WY': 8}

class Shapefile:

    def __init__(self, shp_path = "./states_21basic/states.shp"):
        '''
        Read a shapefile object a Pandas dataframe with a 'coords' 
        column holding the geometry information. This uses the pyshp
        package
        '''
        print("a")
        self.gdf = geopandas.GeoDataFrame.from_file(shp_path)
        print(self.gdf)

    
        self.sf = shp.Reader(shp_path)
        self.fields = [x[0] for x in self.sf.fields][1:]
        self.field_attributes = self.sf.fields
        self.records = self.sf.records()
        self.shapes_objs = self.sf.shapes()

        self.shps = [s.points for s in self.sf.shapes()]
        self.df = pd.DataFrame(columns=self.fields, data=self.records)
        self.df = self.df.assign(coords=self.shps)
        
        self.test_dict = test_dict


    def add_data(self, dict_data = [test_dict], col_name = ["column"]):
        self.cols = col_name
        return join_dict_data(dict_data, self.gdf, col_name)
        self.gdf = join_dict_data(dict_data, self.gdf, col_name)





    def plot_data(self, file_name = "test_file", show_plot = True):
        for col in self.cols:
            alt_plot(self, file_name, col, show_plot)






def alt_plot(shapefile_object, file_name, col = 'count', show_plot = True):
    # new = geopandas.read_file(shp_path+".shp")
    # return new.plot()
    # print("mkay")

    # from geopandas import GeoDataFrame
    # test = GeoDataFrame.from_file(shp_path)
    
    test = shapefile_object.gdf

    #test_dict = {'AK': 7, 'AL': 6, 'AR': 9}

    ###test = join_dict_data(test_dict, test)

    #print(test)
    #test['color_bin_code'] = pd.qcut(test['count'], q =4, labels = [1,2,3,4])
    #print(test['color_bin_code'])
    color_map = get_color_bins(test, col)
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
    if show_plot:
        plt.show()
    else:
        plt.close() #prevents pop ups next time

    #folder "Plot_pngs" needs to exist for this to work
    fig.savefig('./Plot_pngs/' + file_name + '.png')
    #mk.savefig('./Plot_pngs/test.png')
    return test

def get_color_bins(geoframe, col = 'count'):
    temp_map  = {}
    temp_list = []
    list_key = []
    list_val = []
    list_none = []
    for row in geoframe.iterrows():
        print(row[1][col], type(row[1][col]))
        if pd.notna(row[1][col]): ##??check for null
            #temp_list.append((row[1]['STATE_ABBR'],row[1]['count']))
            list_key.append(row[1]['STATE_ABBR'])
            list_val.append(row[1][col])
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

    


def join_dict_data(state_dicts, geoframe, cols = ['count']):

    #assert type(state_dict) == dict or (type(state_dict)== list and type(state_dict[0])==dict)
    list_of_lists = [[]] * len(cols)
    other_count = 0
    for i, state_dict in enumerate(state_dicts):
        counter = 0
        for row in geoframe.iterrows(): ##??cchange iterrows so no index
            lst1 = []
            is_found = False
            for key, value in state_dict.items():
                if row[1]['STATE_ABBR'] == key:
                    list_of_lists[i].append(value)
                    is_found = True
                    counter = counter + 1
            if is_found == False:
                #print("added none")
                list_of_lists[i].append(None)
                counter = counter + 1
        print("counter: " + str(counter))
        other_count += 1
    print("other: " + str(other_count))

    print(list_of_lists)
    return list_of_lists
    for i, col in enumerate(cols):
        print(i, col)
        #print(len(geoframe[col]))
        print(len(list_of_lists[i]))
        print(list_of_lists)
        geoframe[col] = list_of_lists[i]

    #print("*****************")
    #print(geoframe['count'])
    #print(geoframe['count'])
    return geoframe

# def join_dict_data(state_dict, geoframe, col = 'count'):

#     #assert type(state_dict) == dict or (type(state_dict)== list and type(state_dict[0])==dict)
#     lst1 = []
#     for row in geoframe.iterrows(): ##??cchange iterrows so no index
#         is_found = False
#         for key, value in state_dict.items():
#             if row[1]['STATE_ABBR'] == key:
#                 lst1.append(value)
#                 is_found = True
#         if is_found == False:
#             #print("added none")
#             lst1.append(None)

#     geoframe[col] = lst1
#     #print("*****************")
#     #print(geoframe['count'])
#     #print(geoframe['count'])
#     return geoframe


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
