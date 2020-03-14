import pandas as pd
import geopandas
import matplotlib.pyplot as plt

import numpy as np
import shapefile as shp

from descartes import PolygonPatch
import random

#print("yeet")
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
    ##run init,then add_data, then plot_data

    def __init__(self, shp_path = "./states_21basic/states.shp"):
        '''
        Read in a shapefile using its path
        By default uses a shapefile of the 50 US States + DC
        '''
        #print("a")
        self.gdf = geopandas.GeoDataFrame.from_file(shp_path)
        #print(self.gdf)

    
        self.sf = shp.Reader(shp_path)
        self.fields = [x[0] for x in self.sf.fields][1:]
        self.field_attributes = self.sf.fields
        self.records = self.sf.records()
        self.shapes_objs = self.sf.shapes()

        self.shps = [s.points for s in self.sf.shapes()]
        self.df = pd.DataFrame(columns=self.fields, data=self.records)
        self.df = self.df.assign(coords=self.shps)
        
        self.test_dict = test_dict


    def add_data(self, dict_data = [test_dict], col_names = ["column"]):
        '''
        Adds data to geodataframe
        Inputs: 
            dict_data (list of dicts)
            col_names (list of strings)
        '''
        self.cols = col_names
        self.gdf = join_dict_data(dict_data, self.gdf, col_names)



    def plot_data(self, file_name = "test_file", show_plot = True):
        plot_list = []
        output_path =[]
        for col in self.cols:
            plot_list.append(build_plot(self, file_name, col, show_plot))

        if len(plot_list) == 1:
            assert type(file_name) == str
            plot_list[0].savefig('./static/Plot_pngs/' + file_name + '.png')
            output_path.append('./Plot_pngs/' + file_name + '.png')
        else:
            assert (type(file_name) == list and type(file_name[0]) == str) or type(file_name) == str
            names_list = []
            if type(file_name) == str:
                for i in range(len(plot_list)):
                    names_list.append(file_name + "("+str(i) + ")")
            elif type(file_name) == list:
                names_list = file_name[:]
                #print(names_list)

            #print(names_list)
            for i, plot in enumerate(plot_list):
                # plot.savefig('./Plot_pngs/' + file_name + "("+str(i)+").png")
                # output_path.append('./Plot_pngs/' + file_name + "("+str(i)+").png")
                plot.savefig('./static/Plot_pngs/' + names_list[i]+".png")
                output_path.append('./Plot_pngs/' + names_list[i]+".png")
        return output_path





def map_data(dict_data, col_names, file_name, show_plot = True):
    '''
    All-in-one function that creates new Shapefile object, adds data to
        geodataframe and plots data.
    Inputs: 
            dict_data (list of dicts) key STATE ABBR to integer/count values
            col_names (list of strings)
            file_name: Determines names of written .png files, some flexibility on datatype
                (string): basefilename, if multiple images are to be made it appends an integer
                (list): custom filenames
            show_plot (bool): Choice on whether or not to display plot
                              (the file(s) are still saved regardless of show_plot)
    Output:
        paths (list of strings): representing filepaths that images are written to

    '''
    # print(dict_data)
    # print(col_names)
    # print(file_name)
    map1 = Shapefile()
    map1.add_data(dict_data,col_names)
    paths =  map1.plot_data(file_name, show_plot)
    return paths


def build_plot(shapefile_object, file_name, col = 'count', show_plot = True):
    '''
    Main function to build plot in matplotlib
    Inputs:
        Shapefile_object (object of Shapefile class)
        file_name: Determines names of written .png files, some flexibility
            (string): basefilename, if multiple images are to be made it appends an integer
            (list): custom filenames
        col (string): Name of the column data to plot
        show_plot (bool): Choice on whether or not to display plot
                          (the file(s) are still saved regardless of show_plot)
    Outputs:
        fig (matplotlib figure)
        UI display of figure if show_plot = True                      
    '''


    test = shapefile_object.gdf

    color_map = get_color_bins(test, col)
    ##return color_map
    ##??onlytest
    color_sq =['#ffffff00', '#b3cde0','#6497b1','#005b96','#03396c']
    
    BLUE = '#6699cc'
    fig = plt.figure() 

    for i in range(51):
        poly= test['geometry'][i]
        
        ax = fig.gca() 

        #ax.add_patch(PolygonPatch(poly, fc=BLUE, ec=BLUE, alpha=0.5, zorder=2 ))
        #color_sq =['#b3cde0','#6497b1','#005b96','#03396c','#011f4b']
        ##print(test['STATE_ABBR'][i])
        ##print("color_map: " + str(color_map[test['STATE_ABBR'][i]]))
        # print(color_map[test['STATE_ABBR'][i]])
        ax.add_patch(PolygonPatch(poly, fc = color_sq[color_map[test['STATE_ABBR'][i]]], zorder=2 ))
        ax.axis('scaled')
    if show_plot:
        plt.show()
    else:
        plt.close() #prevents pop ups next time

    return fig

def get_color_bins(geoframe, col = 'count', unified_scale = True):
    temp_map  = {}
    #temp_list = []    unused variable
    list_key = []
    list_val = []
    list_none = []
    for row in geoframe.iterrows():
        ##print(row[1][col], type(row[1][col]))
        if pd.notna(row[1][col]): ##??check for null
            #temp_list.append((row[1]['STATE_ABBR'],row[1]['count']))
            list_key.append(row[1]['STATE_ABBR'])
            list_val.append(row[1][col])

        else:
            ##print("appended none")
            list_none.append(row[1]['STATE_ABBR'])

    assert len(list_key) == len(list_val)
    ##print(list_val)

    # print(geoframe)
    # print(list_val)
    if len(list_val) >= 1:
        if len(set(list_val)) == 1:
            list_val, bins = pd.qcut(list_val, q = 1, duplicates = 'drop', retbins = True)
        else:
            list_val, bins = pd.qcut(list_val, q = 4, duplicates = 'drop', retbins = True)
        names = bins.size
        list1 = list(range(1,names))
        # print('list:' + str(list1))
        # print('bins: ' + str(bins))
        # print('bins size: ' + str(bins.size))
        # print(list_val)
        list_val = pd.Series(list_val)
        list_val = list_val.cat.rename_categories(list1)
    # print(list_val)
    ##print(list_key)

    for i, state in enumerate(list_key):
        temp_map[state] = list_val[i]

    for state in state_code:
        if state not in temp_map:
            temp_map[state] = 0
    print("reached return")
    # print(temp_map)
    return temp_map

    

def join_dict_data(state_dicts, geoframe, cols = ['count']):

    #assert type(state_dict) == dict or (type(state_dict)== list and type(state_dict[0])==dict)
    #list_of_lists = [[]] * len(cols)
    list_of_lists = [[] for _ in range(len(cols))]
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
                list_of_lists[i].append(np.nan)
                counter = counter + 1
        # print("counter: " + str(counter) + " , i: " + str(i))
        # print(list_of_lists[i])
        other_count += 1
    # print("other: " + str(other_count))
    # print(len(list_of_lists[0]))
    # print(list_of_lists)
    # return list_of_lists
    for i, col in enumerate(cols):
        #print(i, col)
        #print(len(geoframe[col]))
        #print(len(list_of_lists[i]))
        #print(list_of_lists)
        geoframe[col] = list_of_lists[i]

    return geoframe



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
