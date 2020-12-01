import plotly.offline as pyo
import plotly.graph_objs as go
from db import engine



class Plot(object):
    def __init__(self):
        pass



if __name__ == "__main__":
    import pandas as pd
    data_filter = '["lfsa_egan22d", {"AGE": ["Y15-24"], "NACE_R2": ["TOTAL"], "SEX": ["T"], "UNIT": ["THS"]}]'
    df = pd.read_sql_table(data_filter, engine)
    
    data =[]
    for geo in df.GEO.unique():
        trace = go.Scatter(
            x=df[df["GEO"] == geo]["TIME_PERIOD"],
            y=df[df["GEO"] == geo]["value"],
            mode="lines",
            name=geo)
            
        data.append(trace)

    layout = go.Layout(title = data_filter)

    fig = go.Figure(data=data, layout= layout) 

    pyo.plot(fig)


