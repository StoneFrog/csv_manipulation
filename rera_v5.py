import numpy as np
import scipy as sp
import os, time, datetime
import pandas as pd
                
class ImportFile(object):
#open csv file and creates an array with four columns - id, date, device name and efficiecny. Change usecols to choose other data
#dict - assign column number to the type of value needed

    def __init__(self):
        self.column_dict = {'id':0, 'code':1, 'suffix':2, 'time':3, 'description':4, 
        'size':5, 'beta':6, 'alpha':7, 'mismatchfactor':8, 'ismodule':9, 'cellnumber':10, 
        'voc':11, 'isc':12, 'impp':13, 'vmpp':14, 'fillfactor':15, 'eta':16, 'r_shunt':17, 
        'i01_fit':18, 'i02_fit':19, 'n1_fit':20, 'n2_fit':21, 'slope_voc':22, 'module_area':23,
        'activecell_area':24, 'strings':25, 'cells_per_string':26, 'module_eta':27, 
        'curve_type':28, 'rs_fit':29, 'isc_fit':30, 'voc_fit':31, 'fillfactor_fit':32, 
        'eta_fit':33, 'gsh_fit':34, 'diodemodel':35, 'irradiance':36, 'temperature_before':37, 
        'temperature_after':38, 'is_stc_corrected':39, 'rawcurve':40, 'curve':41, 
        'tracer_guid':42, 'user':43, 'impp_fit':44, 'vmpp_fit':45, 'pmpp':46
        }

    def export_dict(self):
        column_dict = self.column_dict
        return column_dict


    def open_csv_file(self, column_names_initial, filename):  

        column_numbers = []      
        
        for element in column_names_initial:
            column_numbers.append(self.column_dict[element])
        column_numbers = sorted(column_numbers)

        entry_data = pd.read_csv(filename, sep=',', skipinitialspace=True, dayfirst=True, 
                                            na_filter=False, usecols=(column_numbers))

        
        return entry_data, column_names_initial

        
class DataConversion(object):
#converts date to timestample, changes data type from string to float, from every timestample subtract initial date value 

    def __init__(self):
        pass
        
    def convert_date(self, entry_data):
        col_2 = entry_data['time']
        col_2 = pd.to_datetime(col_2)
        entry_data['time'] = col_2
        return entry_data
               
    def subtract_date(self, time_data):
        col_2 = time_data['time']
        col_2 = [element-col_2[0] for element in col_2[:]]
        col_2 = [element/np.timedelta64(1,'s') for element in col_2[:]]
        time_data['time'] = col_2
        return time_data


class ListDivision(object):
#searching when the module number is changing and adds this rownumber to the list, slice list 
#into as many parts as there are modules and assignes names in order as mentioned in FileName class
    
    def __init__(self):
        self.array_dict = {}
        
    def find_row_to_slice(self, time_data):
        col_3 = time_data['cellnumber']
        slice_number = [0]
        counter = 0
        for name_1, name_2 in zip(col_3, col_3[1:]):
            if name_1.split(':', 1)[0] == name_2.split(':', 1)[0]:
                counter += 1
            else:
                slice_number.append(counter+1)
                counter += 1                
        slice_number.append(len(time_data))
        return time_data, slice_number, col_3
        
        
    def create_new_arrays(self, time_data, slice_number, col_3): 
        for row_1, row_2 in zip(slice_number, slice_number[1:]):            
            self.array_dict[col_3[row_1].split(':', 1)[0]] = time_data[row_1:row_2]
        return self.array_dict

class Main(object):
#executes all commands, and saves files

    def __init__(self, data_pathname):
        self.data_pathname = data_pathname
        self.import_file = ImportFile()
        self.data_conversion = DataConversion()
        self.list_division = ListDivision()
        self.fmt_list = ['%d', '%f', '%s']
        
    def save_data(self, chose_column, save_file_path):
        import_file = ImportFile()
        data_conversion = DataConversion()
        list_division = ListDivision()
        
        entry_data, chose_column = import_file.open_csv_file(chose_column, self.data_pathname)
        entry_data = data_conversion.convert_date(entry_data)
        time_data = data_conversion.subtract_date(entry_data)
        time_data, slice_number, col_3 = list_division.find_row_to_slice(time_data)
        list_division.create_new_arrays(time_data, slice_number, col_3)        
        while len(self.fmt_list) != len(chose_column)+3:
            self.fmt_list.append('%f') 
        
        for key in list_division.array_dict:
            file_to_save = list_division.array_dict[key]
            #print (file_to_save)
            file_to_save.to_csv(index=False, path_or_buf= save_file_path + '/' +list(key)[0] + 'odule_' + 
              list(key)[1] + "_" + "_".join(chose_column) + '.csv') 
