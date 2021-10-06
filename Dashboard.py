import pandas as pd
import plotly.express as px
import requests
import io
import dash
import dash_core_components as dcc
from dash import dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import datetime

app = dash.Dash(__name__)

# CSV_URL = 'https://covid.ourworldindata.org/data/owid-covid-data.csv'
# csv_data = requests.get(CSV_URL).content
# df = pd.read_csv(io.StringIO(csv_data.decode('latin1')), sep=',')

df = pd.read_csv("Erdbebendaten_USA_1965-2016.csv")
df['time'] = pd.to_datetime(df['time'])
df['Jahr'] = df['time'].dt.year

lats=df['latitude'].to_list()
lons=df['longitude'].to_list()
coords=list(zip(lats,lons))



app.layout = html.Div(children=[

    html.H1("Erdbeben Dashboard USA mit Dash and Plotly Express", style={'text-align': 'center'}),

    html.H4("Zahlen und Fakten zu den Erdbeben von 1965-2016", style={'text-align': 'left'}),

    dcc.Dropdown(id='location',
                 options=[
                     {"label": "Germany", "value": 'Germany'},
                     {"label": "India", "value": 'India'},
                     {"label": "France", "value": 'France'},
                     {"label": "Austria", "value": 'Austria'},
                     {"label": "Slovenia", "value": 'Slovenia'},
                     {"label": "Netherlands", "value": 'Netherlands'},
                     {"label": "Nigeria", "value": 'Nigeria'},
                     {"label": "Switzerland", "value": 'Switzerland'}],
                 multi=False,
                 value='Germany',
                 style={"width": "40%"}),

    dcc.Slider(id='my-slider', min=0, max=100000, step=1000, value=0,
               tooltip={'always_visible': True},
               marks={5000 * i: '{}'.format(5000 * i) for i in range(21)}, ),

    html.Div(children=[
        dcc.Graph(id='covidplot', figure={}),
        dcc.Graph(id='covidplot2', figure={})],
        style={'display': 'inline-block',
               'vertical-align': 'top',
               'margin-left': '3vw', 'margin-top': '3vw',
               'width': '40vw', 'height': '40vh'}),

    html.Div(children=[
        dcc.Graph(id='covidplot3', figure={}),
        dcc.Graph(id='covidplot4', figure={})],
        style={'display': 'inline-block',
               'vertical-align': 'top',
               'margin-left': '3vw', 'margin-top': '3vw',
               'width': '40vw', 'height': '40vh'})

])


@app.callback(

    [Output(component_id='covidplot', component_property='figure'),
     Output(component_id='covidplot2', component_property='figure'),
     Output(component_id='covidplot3', component_property='figure'),
     Output(component_id='covidplot4', component_property='figure')],

    [Input(component_id='location', component_property='value'),
     Input(component_id='my-slider', component_property='value')]

)


def update_graph(option_slctd, option_slctd2):
    dff = df.copy()
    dff = dff[dff["location"] == option_slctd]
    dff = dff[dff["new_cases"] > option_slctd2]

    # Plotly Express
    fig = px.line(dff, x='date',
                  y=['new_cases', 'new_deaths', 'new_vaccinations',
                     'total_vaccinations_per_hundred'],
                  title="Line Graphs for Several Relevant Attributes for " + option_slctd)

    fig2 = px.scatter(dff, x="new_cases", y="new_deaths",
                      color="new_deaths", size="new_cases", hover_data=['date'],
                      marginal_x="box", marginal_y="violin", trendline="ols",
                      title="Correlations Between New Cases and New Deaths for " + option_slctd)

    fig3 = px.box(dff, x="new_cases", title="Distribution of New Cases for " + option_slctd)

    fig4 = px.choropleth(df, locations="iso_code",
                         color="total_deaths_per_million",
                         hover_name="location",
                         animation_frame="date",
                         title="Deaths per Million in the World",
                         color_continuous_scale=px.colors.sequential.PuRd)

    return fig, fig2, fig3, fig4


if __name__ == '__main__':
    app.run_server(debug=True)


