import pandas as pd
import plotly.express as px
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import datetime
from datetime import date
from dash import dash_table
import plotly.graph_objects as go

app = dash.Dash(__name__)
# für Heroku-Server ist die untenstehende Zeile notwendig
server = app.server

df = pd.read_csv("Erdbebendaten_1965-2015_Ereignisse.csv")
df['time'] = pd.to_datetime(df['time'])
df['Jahr'] = df['time'].dt.year
df['number'] = 1 #add a new colum with the value 1 for each earthquake
df['id'] = df.index

app.layout = html.Div(children=[

    html.H1("Erdbeben Dashboard USA & Umgebung mit Dash and Plotly Express"),

    html.H2(children=["Zahlen und Fakten zu den Erdbeben bzw. erdbebenähnlichen Ereignissen von ", str(df['Jahr'].min()),  " - " , str(df['Jahr'].max()) ]),


    html.Div(id='header_div',

        children=[
    html.Div([html.H3('Ereignis-Typ'),
                dcc.Dropdown(id='type',
                 options=[
                     # die Labels könnte man auch über eine Funktion als Liste automatisch generieren
                     {"label": "Erdbeben", "value": 'earthquake'},
                     {"label": "Minen-Explosionen", "value": 'mining explosion'},
                     {"label": "Explosionen", "value": 'explosion'},
                     {"label": "Nukleare Explosionen", "value": 'nuclear explosion'},
                     {"label": "Steinbruch-Sprengungen", "value": 'quarry blast'},
                 ],
                 multi=False,
                 value='earthquake')]),


    html.Div([html.H3('Jahresfilter von/bis'),
              dcc.RangeSlider(id='Years',
                         min=df['Jahr'].min(),
                         max=df['Jahr'].max(),
                         value=[2011, df['Jahr'].max()],
                         dots=True,
                         marks={1965: '1965',
                                1975: '1975',
                                1985: '1985',
                                1995: '1995',
                                2005: '2005',
                                2015: '2015'},
                         allowCross=False,
                         tooltip={"placement": "bottom", 'always_visible': True},
                         disabled=False,
                         step=1, )]),


    html.Div([html.H3('Erdbebenstärke-Slider'),
                dcc.RangeSlider(id='mag-slider', min=df['mag'].min(), max=df['mag'].max(), step=0.1, value=[6.5, df['mag'].max()],
               tooltip={"placement": "bottom", 'always_visible': True},
               marks={2.0:'2.0m',2.5:'2.5m', 3.0:'3.0m', 3.5:'3.5m', 4.0:'4.0m', 4.5:'4.5m', 5.0: "5.0m", 5.5: '5.5m', 6.0: '6.0m', 6.5: '6.5m', 7.0: '7.0m', 7.5: '7.5m', 8.0: '8.0m'}, )]),

    ]),




    html.Div(id='content_div',children=[
        html.Div(children=[
            dcc.Graph(id='earthquakeplot1', figure={})]),
        html.Div(children=[
            dcc.Graph(id='earthquakeplot3', figure={})]),
        html.Div(children=[
            dcc.Graph(id='earthquakeplot2', figure={})]),
        html.Div(dash_table.DataTable(
        id="earthquakeplot4",
        data=df.to_dict('records'),
        sort_action='native',
        filter_action="native",
        columns=[
            {'name': 'Ort', 'id': 'place', 'type': 'text', 'editable': False},
            {'name': 'Tiefe', 'id': 'depth', 'type': 'numeric'},
            {'name': 'Magnitude', 'id': 'mag', 'type': 'numeric'},
            {'name': 'Jahr', 'id': 'Jahr', 'type': 'datetime'},
        ],
        page_size=12,
        editable=True,
        )),
        ]),

    html.Div(id='footer',
       children=[html.P('ADV HS21 Gruppe 4 | © D. Hubatka, S. Haug und F. Schnellmann')])
])



@app.callback(
    [Output(component_id='earthquakeplot1', component_property='figure'),
     Output(component_id='earthquakeplot3', component_property='figure'),
     Output(component_id='earthquakeplot2', component_property='figure')],

    dash.dependencies.Output('earthquakeplot4','data'),

    [Input(component_id='type', component_property='value'),
     Input(component_id='mag-slider', component_property='value'),
     Input(component_id='Years', component_property='value')]
)


def update_graph(option_slctd, option_slctd2, years_slctd):
    dff = df.copy()
    dff = dff[dff["type"] == option_slctd]
    dff = dff[(dff["mag"] >= option_slctd2[0]) & (dff["mag"] <= option_slctd2[1])]
    dff = dff[(dff['Jahr'] >= years_slctd[0]) & (dff['Jahr'] <= years_slctd[1])]
    data = dff.to_dict('records')


    # Plotly Express

    # Earthquake-Map 1 (with year slider)
    fig3 = px.scatter_geo(dff, lat='latitude', lon='longitude',
                          scope='usa', text=None,
                          hover_data=['Jahr'],
                          opacity=0.2, animation_frame='Jahr', projection='albers usa',
                          color='mag',
                          template='plotly_dark',
                          color_continuous_scale="solar",
                          # plasma, Bluered_r, aggrnyl, brwnyl, deep, thermal, orrd, redor, gray, temps, reds, ylorrd
                          size="mag",
                          labels={"mag": "Magnitude"})
    fig3.update_layout(
        title='"' + str(option_slctd).capitalize() + 's"' + ' in den USA (mit Zeitschieberegler) von ' + str(years_slctd[0]) + '-' + str(years_slctd[1]),
        geo_scope='usa')

    # Earthquake-Map 2
    fig1 = px.scatter_geo(dff, lat='latitude', lon='longitude',
                          scope='usa',
                          hover_data=['Jahr', 'place'],
                          opacity=0.2, projection='albers usa',
                          template='plotly_dark',
                          color_continuous_scale="solar",
                          # plasma, Bluered_r, aggrnyl, brwnyl, deep, thermal, orrd, redor, gray, temps, reds, ylorrd
                          color='mag',
                          size="mag",
                          labels={"mag": "Magnitude"})

    fig1.update_layout(
        title='"' + str(option_slctd).capitalize() + 's"' + ' in den USA (Karte) von ' + str(years_slctd[0]) + '-' + str(years_slctd[1]),
        geo_scope='usa',
    )


    #Barchart Earthquake per Year
    fig2 = px.bar(dff, x="Jahr",
             y="number",
             color='mag',
             hover_name="type",
             hover_data={'Jahr':True, 'mag':True, "place":True,'number':False},
             template='plotly_dark',
             color_continuous_scale="solar", #plasma, Bluered_r, aggrnyl, brwnyl, deep, thermal, orrd, redor, gray, temps, reds, ylorrd
             labels={
                     "number": "Anzahl",
                     "mag": "Magnitude",
                     "Jahr": "Jahr"},)

    fig2.update_layout(
        title='Anzahl der ' + '"' + str(option_slctd).capitalize() + 's"' + ' pro Jahr von ' + str(years_slctd[0]) + '-' + str(years_slctd[1]),

    )

    return fig1, fig2, fig3, data


if __name__ == '__main__':
    app.run_server(debug=True)
