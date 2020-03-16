import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import numpy as np
import shapefile as shp
from descartes import PolygonPatch


state_code = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA", 
          "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", 
          "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", 
          "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", 
          "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

class Shapefile:

    def __init__(self, shp_path = "./states_21basic/states.shp"):
        '''
        Read in a shapefile using its path
        By default uses a shapefile of the 50 US States + DC
        '''
        self.gdf = geopandas.GeoDataFrame.from_file(shp_path)


    def add_data(self, dict_data, col_names = ["column"]):
        '''
        Adds data to geodataframe
        Inputs: 
            dict_data (list of dicts)
            col_names (list of strings)
        '''
        self.cols = col_names
        self.gdf = join_dict_data(dict_data, self.gdf, col_names)


    def plot_data(self, file_name = "test_file", show_plot = True):
        '''
        Builds necessary matplotlib figure objects using helper function
        Inputs:
            file_name (str): name for outputted file
            show_plot (bool)
        Output:
            output_path (list of str): file paths of created .png files
        '''
        plot_list = []
        output_path =[]
        for col in self.cols:
            plot_list.append(build_plot(self, file_name, col, show_plot))
        if len(plot_list) == 1:
            plot_list[0].savefig('./static/Plot_pngs/' + file_name + '.png')
            output_path.append('./Plot_pngs/' + file_name + '.png')
        else:
            names_list = []
            if type(file_name) == str:
                for i in range(len(plot_list)):
                    names_list.append(file_name + "("+str(i) + ")")
            elif type(file_name) == list:
                names_list = file_name[:]
            for i, plot in enumerate(plot_list):
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
            file_name: Determines names of written .png files, 2 datatypes
                (string): basefilename, if multiple images are to be made it
                    appends an integer
                (list): custom filenames
            show_plot (bool): Choice on whether or not to display plot
                              (the file(s) are still saved regardless of
                              show_plot)
    Output:
        paths (list of strings): filepaths that images are written to
    '''
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
            (string): basefilename, if multiple images are to be made it 
                appends an integer
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
    color_scale =['#ffffff00', '#b3cde0','#6497b1','#005b96','#03396c']
    fig = plt.figure() 

    for i in range(51):
        poly= test['geometry'][i]
        #fc = color_scale[color_map[test['STATE_ABBR'][i]]]
        ax = fig.gca()        
        fc1 = color_scale[color_map[test['STATE_ABBR'][i]]]
        ax.add_patch(PolygonPatch(poly, fc = fc1 , zorder=2))
        ax.axis('scaled')
    if show_plot:
        plt.show()
    else:
        plt.close() #prevents pop ups next time
    return fig

def get_color_bins(geoframe, col = 'count'):
    '''
    Returns a color map that keys for a specific color index
    Inputs:
        geoframe (geodataframe): very similar to standard pandas Dataframe
        col (str): column name for data to be mapped to a color index
    Return:
        color_map (dict): maps data values to a color index for color_scale
    '''
    color_map  = {}
    list_key = []
    list_val = []
    list_none = []
    for row in geoframe.iterrows():
        if pd.notna(row[1][col]): 
            list_key.append(row[1]['STATE_ABBR'])
            list_val.append(row[1][col])
        else:
            list_none.append(row[1]['STATE_ABBR'])
    if len(list_val) >= 1:
        if len(set(list_val)) == 1:
            list_val, bins = pd.qcut(list_val, q = 1, duplicates = 'drop',
                                     retbins = True)
        else:
            list_val, bins = pd.qcut(list_val, q = 4, duplicates = 'drop',
                                     retbins = True)
        names = bins.size
        list1 = list(range(1,names))
        list_val = pd.Series(list_val)
        list_val = list_val.cat.rename_categories(list1)

    for i, state in enumerate(list_key):
        color_map[state] = list_val[i]
    for state in state_code:
        if state not in color_map:
            color_map[state] = 0
    return color_map
    

def join_dict_data(state_dicts, geoframe, cols = ['count']):
    '''
    Adds data to geodataframe
    Inputs: 
        state_dicts (list of dicts)
        geoframe (geodataframe)
        cols (list of strings)
    Return:
        geoframe with updated columns
    '''
    list_of_lists = [[] for _ in range(len(cols))]
    for i, state_dict in enumerate(state_dicts):
        for row in geoframe.iterrows():
            is_found = False
            for key, value in state_dict.items():
                if row[1]['STATE_ABBR'] == key:
                    list_of_lists[i].append(value)
                    is_found = True
            if is_found == False:
                list_of_lists[i].append(np.nan)
    for i, col in enumerate(cols):
        geoframe[col] = list_of_lists[i]
    return geoframe