import pandasdmx as sdmx
import pandas as pd
import time

class Sdmxlab(object):
    def __init__(self, agency_id, dataset_id):
        self.agency_id = agency_id
        self.dataset_id = dataset_id
        self.dsd_id = f"DSD_{dataset_id}"
        self.__connect_to_agency(agency_id)
        self.__get_dsd(self.dsd_id)
        self.__get_codelist()
        self.__get_variable()
        self.get_variable_code_label()

    def __connect_to_agency(self, agency_id):
        self.connection = sdmx.Request(agency_id)
        return self.connection

    def __get_dsd(self, dsd_id):
        self.metadata = self.connection.datastructure(dsd_id)
        return self.metadata

    def __get_codelist(self):
        self.codelist = self.metadata.to_pandas()["codelist"]
        return self.codelist

    def __get_variable(self):
        return self.codelist.keys()

    def get_variable_code_label(self):
        self.variable_code_label = dict()
        codelist = self.codelist
        variables = self.codelist.keys()
        for variable in variables:
            self.variable_code_label[variable] = codelist[variable].to_dict()
        return self.variable_code_label

    def get_all_data(self):
        start = time.time()
        self.dataset = self.connection.data(self.dataset_id)
        finish = time.time()
        exec_time = finish - start
        print(f"Query execution time is: {exec_time}")
        return self.dataset.to_pandas()

    def get_all_data_and_put_in_wide_datasets_all_time_one_variabile(self):
        #one variable for all time
        datasets = {}
        dataflow = self.get_all_data()
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
        return datasets

    def get_all_data_and_put_in_wide_datasets_one_time_all_variable(self):
        #all variable for one time
        datasets = {}
        dataflow = self.get_all_data()
        columns = list(dataflow.index.names)
        columns.remove('GEO') 
        columns.remove('FREQ')
        columns.remove('TIME_PERIOD')
        dataflow = dataflow.unstack(columns[0])
        dataflow.reset_index(inplace= True)
        time_segment = list(dataflow['TIME_PERIOD'].unique())
        for variable in time_segment:
            datasets[f"time: {variable}"] = dataflow[dataflow['TIME_PERIOD'] == variable]
        return datasets


    def get_filtered_data(self, key, params):
        pass


if __name__ == "__main__":
    #do stuff
    sdmxlab = Sdmxlab("ESTAT", "aact_ali01")
    print(sdmxlab.variable_code_label)
    print(sdmxlab.get_all_data_and_put_in_wide_datasets_all_time_one_variabile())