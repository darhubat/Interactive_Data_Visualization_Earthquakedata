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
from dash import dash_table
import plotly.graph_objects as go

app = dash.Dash(__name__)


df = pd.read_csv("Erdbebendaten_USA_1965-2016.csv")
df['time'] = pd.to_datetime(df['time'])
df['Jahr'] = df['time'].dt.year
df['number'] = 1 #add a new colum with the value 1 for each earthquake

app.layout = html.Div(children=[

    html.H1("Erdbeben Dashboard USA mit Dash and Plotly Express", style={'text-align': 'center'}),

    html.H2("Zahlen und Fakten zu den Erdbeben von 1965-2016", style={'text-align': 'center'}),

    html.Div(id='header_div',

        children=[
    html.Div([html.H3('Ereignis-Typ'),
                dcc.Dropdown(id='type',
                 options=[
                     {"label": "earthquake", "value": 'earthquake'}],
                 multi=False,
                 value='earthquake')]),


    html.Div([html.H3('Jahresfilter von/bis'),
              dcc.RangeSlider(id='Years',
                         min=1965,
                         max=2014,
                         value=[2000, 2014],
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


    html.Div([html.H3('Erdbebenstärke-Slider'),
                dcc.Slider(id='mag-slider', min=5, max=8, step=0.1, value=df['mag'].max(),
               tooltip={'always_visible': True},
               marks={5.5: '5.5m', 6.0: '6.0m', 6.6: '6.5m', 7.0: '7.0m', 7.5: '7.5m', 8.0: '8.0m'}, )]),

    ]),
    html.Div(children=[
        dcc.Graph(id='earthquakeplot3', figure={}),
        dcc.Graph(id='earthquakeplot4', figure={})],
        style={'display': 'inline-block',
               'vertical-align': 'top',
               'margin-left': '3vw', 'margin-top': '3vw',
               'width': '40vw', 'height': '40vh'}),

    html.Div(children=[
        dcc.Graph(id='earthquakeplot5', figure={}),
        dcc.Graph(id='earthquakeplot6', figure={})],
        style={'display': 'inline-block',
               'vertical-align': 'top',
               'margin-left': '3vw', 'margin-top': '3vw',
               'width': '40vw', 'height': '40vh'}),


    #html.Div(id='footer',
    #         children=[html.P('copyright simons und co')])
])



@app.callback(
    [Output(component_id='earthquakeplot3', component_property='figure'),
     Output(component_id='earthquakeplot4', component_property='figure'),
     Output(component_id='earthquakeplot5', component_property='figure'),
     Output(component_id='earthquakeplot6', component_property='figure')],

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

    # Earthquake-Map 1 (with year slider)
    fig4 = px.scatter_geo(dff, lat='latitude', lon='longitude',
                          scope='usa', text='place',
                          hover_data=['Jahr'],
                          opacity=0.4, animation_frame='Jahr', projection='albers usa',
                          color='mag',
                          size="mag",
                          labels={"mag": "Magnitude"})
    fig4.update_layout(
        title='Earthquakes in the United States (Timeline',
        geo_scope='usa')


    # Earthquake-Map 2
    fig3 = px.scatter_geo(dff, lat='latitude', lon='longitude',
                          scope='usa',
                          hover_data=['Jahr', 'place'],
                          opacity=0.4, projection='albers usa',
                          color='mag',
                          size="mag",
                          labels={"mag": "Magnitude"})

    fig3.update_layout(
        title='Earthquakes in the United States',
        geo_scope='usa')


    #Barchart Earthquake per Year
    fig5 = px.bar(dff, x="Jahr",
             y="number",
             color='mag',
             hover_name="type",
             hover_data={'Jahr':True, 'mag':True, "place":True,'number':False},
             title="Number of earthquakes per year",
             color_continuous_scale='plasma', #plasma, Bluered_r, aggrnyl, brwnyl, deep
             labels={
                     "number": "Number",
                     "mag": "Magnitude",
                     "Jahr": "Year"},)


    # Table with detail for each Earthquake
    fig6 = go.Figure(data=[go.Table(
        header=dict(
            values=["Jahr", "Magnitude", "Depth (in Miles?)", "Place"],
            font=dict(size=13),
            line_color='silver',
            font_color='black',
            fill_color='#e5ecf6',
            align="left"),
        cells=dict(
            values=[dff["Jahr"].tolist(), dff["mag"].tolist(), dff["depth"].tolist(), dff["place"].tolist()],
            line_color='silver',
            font_color='black',
            fill_color='#e5ecf6',
            align="left"))

    ])

    return fig3, fig4, fig5, fig6


if __name__ == '__main__':
    app.run_server(debug=True)
