import plotly.express as px
import pandas as pd
import datetime

# Aufgabenblatt 3 - Aufgabe 6a) & 6b)
df = pd.read_csv("Erdbebendaten_USA_1965-2016.csv")
df['time'] = pd.to_datetime(df['time'])
df['Jahr'] = df['time'].dt.year


# Aufgabeblatt 3 - Aufgabe 7a)
fig_scatter = px.scatter(df, title="Magnitude & Depth Earthquakes in the USA", x="depth", y="mag", color="mag",
                 size='mag', hover_data=['place'], labels=dict(depth="Depth", mag="Magnitude"))
fig_scatter.update_layout(title_font_size=40)
fig_scatter.show()


# Aufgabeblatt 3 - Aufgabe 7b)
fig_scattermatrix = px.scatter_matrix(df, title="Scatter-Matrix Earthquakes in the USA",
    dimensions=["depth", "mag", "latitude", "longitude"], hover_data=['place'],
    color="mag", labels=dict(depth="Depth", mag="Magnitude", latitude="Latitude", longitude="Longitude"))
fig_scattermatrix.update_layout(title_font_size=40)
fig_scattermatrix.show()

