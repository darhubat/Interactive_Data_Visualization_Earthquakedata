import plotly.graph_objects as go
import pandas as pd

df = pd.read_csv("Erdbebendaten_1965-2015_Ereignisse.csv")
df['time'] = pd.to_datetime(df['time'])
df['Jahr'] = df['time'].dt.year
df['number'] = 1 #add a new colum with the value 1 for each earthquake
df['id'] = df.index
df['store_num'] = [(num+1) for num in range(len(df))]

data = []
layout = dict(
    title = 'Erdbeben in der Jahresentwicklung<br>',
    # showlegend = False,
    autosize = False,
    width = 1000,
    height = 900,
    hovermode = False,
    legend = dict(
        x=0.7,
        y=-0.1,
        bgcolor="rgba(255, 255, 255, 0)",
        font = dict( size=11 ),
    )
)
years = df['Jahr'].unique()

for i in range(len(years)):
    geo_key = 'geo'+str(i+1) if i != 0 else 'geo'
    lons = list(df[ df['Jahr'] == years[i] ]['longitude'])
    lats = list(df[ df['Jahr'] == years[i] ]['latitude'])
    # Walmart store data
    data.append(
        dict(
            type = 'scattergeo',
            showlegend=False,
            lon = lons,
            lat = lats,
            geo = geo_key,
            name = int(years[i]),
            marker = dict(
                color = "rgb(0, 0, 255)",
                opacity = 0.5
            )
        )
    )
    # Year markers
    data.append(
        dict(
            type = 'scattergeo',
            showlegend = False,
            lon = [-78],
            lat = [47],
            geo = geo_key,
            text = [years[i]],
            mode = 'text',
        )
    )
    layout[geo_key] = dict(
        scope = 'usa',
        showland = True,
        landcolor = 'rgb(229, 229, 229)',
        showcountries = False,
        domain = dict( x = [], y = [] ),
        subunitcolor = "rgb(255, 255, 255)",
    )


def draw_sparkline( domain, lataxis, lonaxis ):
    ''' Returns a sparkline layout object for geo coordinates  '''
    return dict(
        showland = False,
        showframe = False,
        showcountries = False,
        showcoastlines = False,
        domain = domain,
        lataxis = lataxis,
        lonaxis = lonaxis,
        bgcolor = 'rgba(255,200,200,0.0)'
    )

"""
# Stores per year sparkline
layout['geo50'] = draw_sparkline({'x':[0.6,0.8], 'y':[0,0.15]}, \
                                 {'range':[-5.0, 30.0]}, {'range':[0.0, 40.0]} )
data.append(
    dict(
        type = 'scattergeo',
        mode = 'lines',
        lat = list(df.groupby(by=['Jahr']).count()['store_num']/1e1),
        lon = list(range(len(df.groupby(by=['Jahr']).count()['store_num']/1e1))),
        line = dict( color = "rgb(0, 0, 255)" ),
        name = "New stores per year<br>Peak of 178 stores per year in 1990",
        geo = 'geo50',
    )
)

# Cumulative sum sparkline
layout['geo51'] = draw_sparkline({'x':[0.8,1], 'y':[0,0.15]},
                                 {'range':[-5.0, 50.0]}, {'range':[0.0, 50.0]} )
data.append(
    dict(
        type = 'scattergeo',
        mode = 'lines',
        lat = list(df.groupby(by=['Jahr']).count().cumsum()['store_num']/1e2),
        lon = list(range(len(df.groupby(by=['Jahr']).count()['store_num']/1e1))),
        line = dict( color = "rgb(214, 39, 40)" ),
        name ="Cumulative sum<br>3176 stores total in 2006",
        geo = 'geo51',
    )
)
"""

z = 0
COLS = 7
ROWS = 8
for y in reversed(range(ROWS)):
    for x in range(COLS):
        geo_key = 'geo'+str(z+1) if z != 0 else 'geo'
        layout[geo_key]['domain']['x'] = [float(x)/float(COLS), float(x+1)/float(COLS)]
        layout[geo_key]['domain']['y'] = [float(y)/float(ROWS), float(y+1)/float(ROWS)]
        z=z+1
        if z > 50:
            break

fig = go.Figure(data=data, layout=layout)
fig.update_layout(width=800)
fig.show()