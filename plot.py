import plotly.offline as pyo
import plotly.graph_objs as go
from db import engine



class Plot(object):
    

    def __init__(self):
        pass
    
    @staticmethod
    def line(dataset):
        data =[]
        for geo in df.GEO.unique():
            dataset_filtered = df["GEO"] == geo
            trace = go.Scatter(
                x=dataset_filtered["TIME_PERIOD"],
                y=dataset_filtered["value"],
                mode="lines",
                name=geo)
                
            data.append(trace)

        layout = go.Layout(title = data_filter)

        fig = go.Figure(data=data, layout= layout) 

        pyo.plot(fig)
    
    

    @staticmethod
    def line_time_index_base_100(dataset):
        def index_base_100(dataset_filtered):
            temporary_data = dataset_filtered.dropna()
            first_series_time = temporary_data["TIME_PERIOD"].min()
            first_series_value = temporary_data[temporary_data["TIME_PERIOD"] == first_series_time]["value"].values[0]
            temporary_data["value"] = temporary_data["value"].apply(lambda x: x / first_series_value * 100)
            return temporary_data
        
        data =[]
        for geo in df.GEO.unique():
            dataset_filtered = df[df["GEO"] == geo]
            dataset_filtered = index_base_100(dataset_filtered)
            print(dataset_filtered)
            trace = go.Scatter(
                x=dataset_filtered["TIME_PERIOD"],
                y=dataset_filtered["value"],
                mode="lines",
                name=geo)
                
            data.append(trace)

        layout = go.Layout(title = data_filter)

        fig = go.Figure(data=data, layout= layout) 

        pyo.plot(fig) 


if __name__ == "__main__":
    import pandas as pd
    data_filter = '["lfsa_egan22d", {"AGE": ["Y15-24"], "NACE_R2": ["TOTAL"], "SEX": ["T"], "UNIT": ["THS"]}]'
    df = pd.read_sql_table(data_filter, engine)
    
    Plot.line_time_index_base_100(df)


