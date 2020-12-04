import pandasdmx as sdmx
import pandas as pd
import time
from db import engine
import json
#geopandas (join right with geojson)

class Sdmx_connector(object):
    def __init__(self, agency_id, dataset_id):
        self.agency_id = agency_id
        self.dataset_id = dataset_id.lower()
        self.dsd_id = f"DSD_{dataset_id.lower()}"
        self.__connect_to_agency(agency_id)
        self.__get_dsd(self.dsd_id)
        self.__get_codelist()
        self.__get_variable()
        self.get_variable_code_label()

    def __connect_to_agency(self, agency_id):
        self.__connection = sdmx.Request(agency_id)
        return self.__connection

    def __get_dsd(self, dsd_id):
        self.metadata = self.__connection.datastructure(dsd_id)
        return self.metadata

    def __get_codelist(self):
        self.codelist = self.metadata.to_pandas()["codelist"]
        return self.codelist

    def __get_variable(self):
        return self.codelist.keys()

    def get_variable_code_label(self):
        self.variable_code_label_cl = dict()
        self.variable_code_label = dict()
        codelist = self.codelist
        variables = self.codelist.keys()
        for variable in variables:
            self.variable_code_label_cl[variable] = codelist[variable].to_dict()
            self.variable_code_label[variable.split("CL_")[1]] = codelist[variable].to_dict()

        metavariables = ["FREQ", "OBS_FLAG", "OBS_STATUS", "GEO"]
        for variable in self.variable_code_label.keys():
            if variable in metavariables:
                self.variable_code_label[variable].update({"auto": "auto"})
            else:
                pass
        
        return self.variable_code_label
    
    def get_variable_code_test(self, geo=True):
        # useful for testing monodimensional data 
        self.variable_code_test = dict()
        for variable in self.variable_code_label.keys():
            self.variable_code_test[variable] = [list(self.variable_code_label[variable].keys())[0]]
  
        metavariables = ["FREQ", "OBS_FLAG", "OBS_STATUS"]
        if geo:
            metavariables = ["FREQ", "OBS_FLAG", "OBS_STATUS", "GEO"]
        for item in metavariables:
            self.variable_code_test.pop(item, None)
        return self.variable_code_test


    def get_all_data(self):
        start = time.time()
        self.dataset = self.__connection.data(self.dataset_id)
        finish = time.time()
        exec_time = finish - start
        print(f"Query execution time is: {exec_time}")
        return self.dataset.to_pandas()

    def get_all_data_and_put_in_wide_datasets_all_time_one_variabile(self):
        #one variable for all time
        return self.__get_data_and_put_in_wide_datasets_all_time_one_variabile(self.get_all_data())

    def get_all_data_and_put_in_wide_datasets_one_time_all_variable(self):
        #all variable for one time
        return self.__get_data_and_put_in_wide_datasets_all_time_one_variabile(self.get_all_data())

    def __get_data_and_put_in_wide_datasets_all_time_one_variabile(self, dataflow):
        try:
            datasets = {}
            dataflow = dataflow
            dataflow_wide = dataflow.unstack("TIME_PERIOD")
            columns = list(dataflow.index.names)
            columns.remove('GEO') 
            columns.remove('FREQ')
            columns.remove('TIME_PERIOD')
            print(columns)
            dataflow_wide = dataflow_wide.reset_index()
            for column in columns:
                for variable in list(dataflow_wide[column].unique()):
                    datasets[f"{column}:{variable}"] = dataflow_wide[dataflow_wide[column] == variable]
            self.datasets_all_time_one_variabile = datasets
            return self.datasets_all_time_one_variabile
        except:
            return {"Error": "Error during download, please reduce the number of variables by using the filter function."}

    def __get_data_and_put_in_wide_datasets_one_time_all_variable(self, dataflow):
        #all variable for one time
        try:
            datasets = {}
            dataflow = dataflow
            columns = list(dataflow.index.names)
            columns.remove('GEO') 
            columns.remove('FREQ')
            columns.remove('TIME_PERIOD')
            dataflow = dataflow.unstack(columns[0])
            dataflow.reset_index(inplace= True)
            time_segment = list(dataflow['TIME_PERIOD'].unique())
            for variable in time_segment:
                datasets[f"time: {variable}"] = dataflow[dataflow['TIME_PERIOD'] == variable]
            self.datasets_one_time_all_variable = datasets
            return self.datasets_one_time_all_variable
        except UnboundLocalError:
            return {"Error": "Error during download, please reduce the number of variables by using the filter function."}

    def get_filtered_data(self, key, params = {'startPeriod': '1970'}):
        #key: {'GEO': ['EL', 'IT'], "SEX": ["M"]}
        #params: {'startPeriod': '2016', "endPeriod": "2016"}
        self.key = key
        self.params = params
        start = time.time()
        self.filtered_data = self.__connection.data(
                        self.dataset_id,
                        key=key,
                        params=params).to_pandas()
        finish = time.time()
        exec_time = finish - start
        self.filtered_data = self.filtered_data.reset_index()
        print(f"Query execution time is: {exec_time}")
        return self.filtered_data

    def get_filtered_data_and_put_in_wide_datasets_one_time_all_variable(self, filtered_data):
        return self.__get_data_and_put_in_wide_datasets_all_time_one_variabile(filtered_data)

    def get_filtered_data_and_put_in_wide_datasets_all_time_one_variabile(self, filtered_data):
        return self.__get_data_and_put_in_wide_datasets_all_time_one_variabile(filtered_data)
    
    def save_filtered_data(self):
        self.table_name = json.dumps([self.dataset_id, self.key])
        self.filtered_data.to_sql(self.table_name, engine, if_exists="replace")



    @staticmethod
    def dataset_stats(dataset):
        dimension = {}
        for column in dataset.columns:
            dimension[column] = len(dataset[column].unique())
        return dimension


if __name__ == "__main__":
    #do stuff
    #sdmxlab = SdmxConnector
    #("ESTAT", 'lfst_r_lfe2en2')
    sdmxlab = Sdmx_connector("ESTAT",'une_rt_m')
    #print(sdmxlab.codelist.keys())
    #print(sdmxlab.variable_code_label_cl)
    #print(sdmxlab.get_filtered_data(key={'GEO': ['EL', 'IT'], "SEX": ["M"]}, params={'startPeriod': '2016', "endPeriod": "2016"}))
    
    #print(sdmxlab.variable_code_label)
    #print(sdmxlab.get_filtered_data(key={'GEO': ['IT'], "AGE": ['Y15-24'], "SEX": ['T']}))
    
    print("---------")
    #print(sdmxlab.get_all_data_and_put_in_wide_datasets_all_time_one_variabile())
    print(sdmxlab.get_variable_code_test())
    print("---------")
    
    
    print(sdmxlab.get_filtered_data(key=sdmxlab.get_variable_code_test()))
    sdmxlab.save_filtered_data()
    print(sdmxlab.table_name)
    #one_time_all_variable = sdmxlab.get_all_data_and_put_in_wide_datasets_one_time_all_variable()
    #print(one_time_all_variable)
    
    #filtered = sdmxlab.get_filtered_data(key={'GEO': ['IT'], "AGE": ['Y15-24']}, params={'startPeriod': '2016', "endPeriod": "2016"})
    #print(sdmxlab.dataset_stats(filtered))
    #print(filtered)

