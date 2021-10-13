import pandas as pd
import plotly.express as px
import requests
import io
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import datetime
from datetime import date

app = dash.Dash(__name__)


df = pd.read_csv("Erdbebendaten_USA_1965-2016.csv")
df['time'] = pd.to_datetime(df['time'])
df['Jahr'] = df['time'].dt.year


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
              html.H5('Jahresfilter von/bis'),
              dcc.RangeSlider(id='Years',
                         min=1965,
                         max=2015,
                         value=[1965, 2015],
                         dots=True,
                         marks={1965: '1965',
                                1975: '1975',
                                1985: '1985',
                                1995: '1995',
                                2005: '2005',
                                2015: '2015'},
                         allowCross=False,
                         tooltip={'always_visible': True},
                         disabled=False,
                         step=1, )]),


    html.Div([html.P(),
              html.H5('Erdbebenstärke-Slider'),
                dcc.Slider(id='mag-slider', min=4.5, max=8, step=0.1, value=df['mag'].max(),
               tooltip={'always_visible': True},
               marks={4.5: '4.5m', 5.0: '5.0m', 5.5: '5.5m', 6.0: '6.0m', 6.6: '6.5m', 7.0: '7.0m', 7.5: '7.5m', 8.0: '8.0m'}, )], style={'width': '25%'}),


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
     Output(component_id='earthquakeplot3', component_property='figure'),
     Output(component_id='earthquakeplot4', component_property='figure')],

    [Input(component_id='type', component_property='value'),
     Input(component_id='mag-slider', component_property='value'),
     Input(component_id='Years', component_property='value')]

)


def update_graph(option_slctd, option_slctd2, years_slctd):
    dff = df.copy()
    dff = dff[dff["type"] == option_slctd]
    dff = dff[dff["mag"] <= option_slctd2]
    dff = dff[(dff['Jahr'] >= years_slctd[0]) & (dff['Jahr'] <= years_slctd[1])]


    # Plotly Express
    fig = px.scatter_matrix(dff, title="Scatter-Matrix Earthquakes in the USA",
                dimensions=["depth", "mag", "latitude", "longitude"], hover_data=['place'],
                 color="mag", labels=dict(depth="Depth", mag="Magnitude", latitude="Latitude", longitude="Longitude"))
    fig.update_layout(title_font_size=20)


    fig2 = px.scatter(dff, title="Magnitude & Depth Earthquakes in the USA", x="depth", y="mag", color="mag",
                 size='mag', hover_data=['place'], labels=dict(depth="Depth", mag="Magnitude"))
    fig2.update_layout(title_font_size=20)


    fig4 = px.scatter_geo(dff, title='Erdbeben in den USA animiert jährlich von ' + str(years_slctd[0]) + ' bis ' + str(years_slctd[1]),
                          lat='latitude', lon='longitude',
                  scope='usa', text='place',
                  hover_data=['Jahr'], size='mag',
                  opacity=0.4, animation_frame='Jahr', projection='albers usa')
    fig4.update_layout(title_font_size=20)

    fig3 = px.scatter_geo(dff, title='Alle Erdbeben in den USA von ' + str(years_slctd[0]) + ' bis ' + str(years_slctd[1]),
                          lat='latitude', lon='longitude',
                  scope='usa',
                  hover_data=['Jahr', 'place'], size='mag',
                  opacity=0.4, projection='albers usa')
    fig3.update_layout(title_font_size=20)

    return fig, fig2, fig3, fig4


if __name__ == '__main__':
    app.run_server(debug=True)


