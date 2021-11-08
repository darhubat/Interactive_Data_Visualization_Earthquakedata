import plotly.express as px
import pandas as pd
import datetime

df = pd.read_csv("Erdbebendaten_USA_1965-2016.csv")
df['time'] = pd.to_datetime(df['time'])
df['Jahr'] = df['time'].dt.year

fig = px.scatter_geo(df, lat='latitude', lon='longitude',
                  scope='usa', text='place',
                  hover_data=['Jahr'], size='mag',
                  opacity=0.4, animation_frame='Jahr', projection='albers usa')
fig.show()
