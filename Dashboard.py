import pandas as pd
import plotly.express as px
import requests
import io
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import datetime

app = dash.Dash(__name__)


df = pd.read_csv("Erdbebendaten_USA_1965-2016.csv")
df['time'] = pd.to_datetime(df['time'])
df['Jahr'] = df['time'].dt.year

lats=df['latitude'].to_list()
lons=df['longitude'].to_list()
coords=list(zip(lats,lons))



app.layout = html.Div(children=[

    html.H1("Erdbeben Dashboard USA mit Dash and Plotly Express", style={'text-align': 'center'}),

    html.H3("Zahlen und Fakten zu den Erdbeben von 1965-2016", style={'text-align': 'left'}),
    html.Div([html.P(),
              html.H5('Ereignis-Typ'),
                dcc.Dropdown(id='type',
                 options=[
                     {"label": "earthquake", "value": 'earthquake'}],
                 multi=False,
                 value='earthquake',
                 style={"width": "40%"})]),

    html.Div([html.P(),
              html.H5('Magnitude-Slider'),
                dcc.Slider(id='mag-slider', min=0, max=9, step=0.1, value=5.5,
               tooltip={'always_visible': False},
               marks={5.5: '5.5m', 6.0: '6.0m', 6.6: '6.5m', 7.0: '7.0m', 7.5: '7.5m', 8.0: '8.0m'}, )]),

    html.Div(children=[
        dcc.Graph(id='earthquakeplot', figure={}),
        dcc.Graph(id='earthquakeplot2', figure={})],
        style={'display': 'inline-block',
               'vertical-align': 'top',
               'margin-left': '3vw', 'margin-top': '3vw',
               'width': '40vw', 'height': '40vh'}),

    html.Div(children=[
        dcc.Graph(id='earthquakeplot3', figure={}),
        dcc.Graph(id='earthquakeplot4', figure={})],
        style={'display': 'inline-block',
               'vertical-align': 'top',
               'margin-left': '3vw', 'margin-top': '3vw',
               'width': '40vw', 'height': '40vh'}),

])


@app.callback(

    [Output(component_id='earthquakeplot', component_property='figure'),
     Output(component_id='earthquakeplot2', component_property='figure'),
     Output(component_id='earthquakeplot3', component_property='figure'),],

    [Input(component_id='type', component_property='value'),
     Input(component_id='mag-slider', component_property='value')]

)


def update_graph(option_slctd, option_slctd2):
    dff = df.copy()
    dff = dff[dff["type"] == option_slctd]
    dff = dff[dff["mag"] > option_slctd2]

    # Plotly Express
    fig = px.scatter_matrix(dff, title="Scatter-Matrix Earthquakes in the USA",
                dimensions=["depth", "mag", "latitude", "longitude"], hover_data=['place'],
                 color="mag", labels=dict(depth="Depth", mag="Magnitude", latitude="Latitude", longitude="Longitude"))
    fig.update_layout(title_font_size=20)

    fig2 = px.scatter(dff, title="Magnitude & Depth Earthquakes in the USA", x="depth", y="mag", color="mag",
                 size='mag', hover_data=['place'], labels=dict(depth="Depth", mag="Magnitude"))
    fig2.update_layout(title_font_size=20)


    fig3 = px.scatter_geo(dff, lat='latitude', lon='longitude',
                  scope='usa', text='place',
                  hover_data=['Jahr'], size='mag',
                  opacity=0.4, animation_frame='Jahr', projection='albers usa')

    return fig, fig2, fig3


if __name__ == '__main__':
    app.run_server(debug=True)


