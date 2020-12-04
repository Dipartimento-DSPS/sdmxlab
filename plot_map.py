import geopandas
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go
from db import engine
import plotly.express as px

class Choroplete():
    def __init__(self, dataset, geojson_url):
        self.df = dataset
        self.geojson = geojson_url
    
    def load_shape(self):
        self.df_shape = geopandas.read_file(self.geojson)
    
    def apply_eurostat(self):
        self.df.rename(columns = {"GEO": "NUTS_ID"}, inplace = True)
        self.df_geo = self.df_shape.merge(self.df, on='NUTS_ID')
        self.df_geo.set_index("NUTS_NAME", inplace = True)
        self.min = self.df_geo["value"].min()
        self.max = self.df_geo["value"].max()


    def generate_fig(self):
        self.fig = px.choropleth_mapbox(self.df_geo,
                   geojson=self.df_geo.geometry,
                   locations=self.df_geo.index,
                   hover_name="NUTS_ID",
                   color="value",
                   color_continuous_scale=px.colors.diverging.PuOr,
                   animation_frame="TIME_PERIOD",
                   range_color=[self.min, self.max],
                   mapbox_style='open-street-map',
                   center={"lat": 43, "lon": 11},
                   zoom=3,
                   opacity=0.85
                   )
        self.fig.update_geos(fitbounds="locations", visible=False)
    
    
    def generate_div_map(self):
        #for flask
        return pyo.plot(self.fig, output_type='div', include_plotlyjs=False)
    
    def generate_html_map(self):
        #for testingS 
        pyo.plot(self.fig) 
        



if __name__ == "__main__":
    geojson_url = "static_map/NUTS_RG_20M_2021_4326.geojson"
    query = '["lfsa_egan22d", {"AGE": ["Y15-24"], "NACE_R2": ["TOTAL"], "SEX": ["T"], "UNIT": ["THS"]}]'

    map = Choroplete(pd.read_sql(query, engine), geojson_url)
    map.load_shape()
    map.apply_eurostat()
    map.generate_fig() 
    map.generate_html_map()




