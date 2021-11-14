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
import numpy as np

app = dash.Dash(__name__)
# für Heroku-Server ist die untenstehende Zeile notwendig
server = app.server

df = pd.read_csv("Erdbebendaten_1965-2015_Ereignisse.csv")
df['time'] = pd.to_datetime(df['time'])
df['Jahr'] = df['time'].dt.year
df['number'] = 1 #add a new colum with the value 1 for each earthquake
df['id'] = df.index
df['store_num'] = [(num+1) for num in range(len(df))]



app.layout = html.Div(children=[

    html.H1("Erdbeben Dashboard USA & Umgebung mit Dash and Plotly Express"),

    html.H2(children=["Zahlen und Fakten zu den Erdbeben bzw. erdbebenähnlichen Ereignissen von ", str(df['Jahr'].min()),  " bis " , str(df['Jahr'].max()) ]),


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
                         value=[2012, df['Jahr'].max()],
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
                dcc.RangeSlider(id='mag-slider', min=df['mag'].min(), max=df['mag'].max(), step=0.1, value=[3.8, 5],
               tooltip={"placement": "bottom", 'always_visible': True},
               marks={2.0:'2.0m',2.5:'2.5m', 3.0:'3.0m', 3.5:'3.5m', 4.0:'4.0m', 4.5:'4.5m', 5.0: "5.0m", 5.5: '5.5m', 6.0: '6.0m', 6.5: '6.5m', 7.0: '7.0m', 7.5: '7.5m', 8.0: '8.0m'}, )]),

    ]),




    html.Div(id='content_div',children=[
        dcc.Graph(id='scatter_geo', figure={}),
        dcc.Graph(id='barchart', figure={}),
        dcc.Graph(id='small_multiples', figure={}, style={'overflowY': 'scroll', 'height': 400}),
        dash_table.DataTable(
        id="table_chart",
        data=df.to_dict('records'),
        sort_action='native',
        filter_action="native",
        columns=[
            {'name': 'Ort', 'id': 'place', 'type': 'text', 'editable': False},
            {'name': 'Tiefe (km)', 'id': 'depth', 'type': 'numeric'},
            {'name': 'Magnitude', 'id': 'mag', 'type': 'numeric'},
            {'name': 'Jahr', 'id': 'Jahr', 'type': 'datetime'},
        ],
        page_size=9,
        editable=True,
        ),
        ]),

    html.Div(id='footer',
       children=[html.P('ADV HS21 Gruppe 4 | © D. Hubatka, S. Haug und F. Schnellmann')])
])



@app.callback(
    [Output(component_id='scatter_geo', component_property='figure'),
     Output(component_id='barchart', component_property='figure'),
     Output(component_id='small_multiples', component_property='figure')],

    dash.dependencies.Output('table_chart','data'),

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

    # Barchart Earthquake per Year
    fig2 = px.bar(dff, x="Jahr",
                  y="number",
                  color='mag',
                  hover_name="type",
                  hover_data={'Jahr': True, 'mag': True, "place": True, 'number': False},
                  template='plotly_dark',
                  color_continuous_scale="solar",
                  # plasma, Bluered_r, aggrnyl, brwnyl, deep, thermal, orrd, redor, gray, temps, reds, ylorrd
                  labels={
                      "number": "Anzahl",
                      "mag": "Magnitude",
                      "Jahr": "Jahr"}, )

    fig2.update_layout(
        title='Anzahl der ' + '"' + str(option_slctd).capitalize() + 's"' + ' pro Jahr von ' + str(
            years_slctd[0]) + ' bis ' + str(years_slctd[1]),
        font=dict(size=9)

    )

    # Earthquake-Map
    fig1 = px.scatter_geo(dff, lat='latitude', lon='longitude',
                          scope='usa',
                          hover_data=['Jahr', 'place'],
                          opacity=0.5, projection='albers usa',
                          template='plotly_dark',
                          color_continuous_scale="solar",
                          # plasma, Bluered_r, aggrnyl, brwnyl, deep, thermal, orrd, redor, gray, temps, reds, ylorrd
                          color='mag',
                          size="mag",
                          labels={"mag": "Magnitude"})

    fig1.update_layout(
        title='"' + str(option_slctd).capitalize() + 's"' + ' in den USA (Karte) von ' + str(years_slctd[0]) + ' bis ' + str(years_slctd[1]),
        geo_scope='usa',
        font=dict(size=9)
    )

    data1 = []

    years = dff['Jahr'].unique()
    if len(years) < 4:
        set_height = 400
    else:
        if len(years) % 4 == 0:
            set_height = len(years) * 100
        else:
            set_height = (len(years) + (4 - (len(years) % 4))) * 100


    layout = dict(
        title='"' + str(option_slctd).capitalize() + 's"' + ' in der Jahresentwicklung auf der Karte der USA von ' + str(years_slctd[0]) + ' bis ' + str(years_slctd[1]),
        # showlegend = False,
        autosize=False,
        height=set_height,
        hovermode=False,
        template='plotly_dark',
        font=dict(size=9),
        legend=dict(
            x=0.7,
            y=-0.1,
            bgcolor="rgba(255, 255, 255, 0)",
            font=dict(size=10),
        )
    )


    for i in range(len(years)):
        geo_key = 'geo' + str(i + 1) if i != 0 else 'geo'
        lons = list(dff[dff['Jahr'] == years[i]]['longitude'])
        lats = list(dff[dff['Jahr'] == years[i]]['latitude'])
        data1.append(
            dict(
                type='scattergeo',
                showlegend=False,
                lon=lons,
                lat=lats,
                geo=geo_key,
                name=int(years[i]),
                marker=dict(
                    color="#BB2020",
                    opacity=0.5
                )
            )
        )
        # Year markers
        data1.append(
            dict(
                type='scattergeo',
                showlegend=False,
                lon=[-78],
                lat=[47],
                geo=geo_key,
                text=[years[i]],
                mode='text',
            )
        )
        layout[geo_key] = dict(
            scope='usa',
            showland=True,
            #landcolor='rgb(229, 229, 229)',
            showcountries=False,
            domain=dict(x=[], y=[]),
            #subunitcolor="rgb(255, 255, 255)",

        )

    z = 0
    COLS = 4
    ROWS = int(np.ceil(len(years) / COLS))
    for y in reversed(range(ROWS)):
        for x in range(COLS):
            geo_key = 'geo' + str(z + 1) if z != 0 else 'geo'
            layout[geo_key]['domain']['x'] = [float(x) / float(COLS), float(x + 1) / float(COLS)]
            layout[geo_key]['domain']['y'] = [float(y) / float(ROWS), float(y + 1) / float(ROWS)]
            z = z + 1
            if z > len(years)-1:
                break

    fig5 = go.Figure(data=data1, layout=layout)
    #fig5.update_layout(height = 2000)

    return fig1, fig2, fig5, data


if __name__ == '__main__':
    app.title = "Erdbeben Dashboard USA"
    app.run_server(debug=True)
