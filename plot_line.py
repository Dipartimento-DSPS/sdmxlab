import plotly.offline as pyo
import plotly.graph_objs as go
from db import engine
import plotly.io as pio
pio.templates


class Plot(object):
    def __init__(self, dataset):
        self.dataset = dataset
        
    
    
    def line(self):
        data =[]
        df = self.dataset
        for geo in df.GEO.unique():
            dataset_filtered = df["GEO"] == geo
            trace = go.Scatter(
                x=dataset_filtered["TIME_PERIOD"],
                y=dataset_filtered["value"],
                mode="lines",
                name=geo,
                
                )
                
            data.append(trace)

        layout = go.Layout(title = "Grafico valori assoluti")

        self.fig = go.Figure(data=data, layout= layout) 
        
        return self

    
    def line_time_index_base_100(self):
        def index_base_100(dataset_filtered):
            temporary_data = dataset_filtered.dropna()
            first_series_time = temporary_data["TIME_PERIOD"].min()
            first_series_value = temporary_data[temporary_data["TIME_PERIOD"] == first_series_time]["value"].values[0]
            temporary_data["value"] = temporary_data["value"].apply(lambda x: x / first_series_value * 100)
            return temporary_data
        
        data =[]
        df = self.dataset
        for geo in df.GEO.unique():
            try:
                dataset_filtered = df[df["GEO"] == geo]
                dataset_filtered = index_base_100(dataset_filtered)
                #print(dataset_filtered)
                trace = go.Scatter(
                    x=dataset_filtered["TIME_PERIOD"],
                    y=dataset_filtered["value"],
                    mode="lines",
                    name=geo,
                    ) # line_shape='spline'
                    
                data.append(trace)
            except Exception as e:
                print(f""""
                ---{geo}---
                ---{e}---
                """)
        layout = go.Layout(title = "Grafico base 100")

        self.fig = go.Figure(data=data, layout= layout) 
        
        return self
        

    def generate_div_plot(self):
        return pyo.plot(self.fig, output_type='div', include_plotlyjs=False)
    
    def generate_html_plot(self):
        return pyo.plot(self.fig)
          


if __name__ == "__main__":
    import pandas as pd
    data_filter = '["tps00046", {"FACILITY": ["HBEDT"], "UNIT": ["P_HTHAB"]}]'
    df = pd.read_sql_table(data_filter, engine)
    print(df)
    #plot = Plot(df).line_time_index_base_100().generate_html_plot()
    Plot(df).line_time_index_base_100().generate_html_plot()
    #print(Plot(df).line_time_index_base_100().generate_div_plot())
    

