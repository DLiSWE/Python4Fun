import pandas as pd
import chart_studio.plotly as py
import plotly.graph_objs as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot

df = pd.read_csv('2011_US_AGRI_Exports')

print(df.head())
data = dict(type='choropleth',
            colorscale = 'ylorbr',
            locations = df['code'],
            locationmode = 'USA-states',
            z = df['total exports'],
            text = df['text'],
            marker = dict(line = dict(color = 'rgb(255,255,255)', width=1)),
            colorbar = {'title': 'Millions USD'}
            )

layout = dict(title = '2011 US Agriculture Exports by State',
            geo = dict(scope='usa',showlakes = True, lakecolor = 'rgb(85,173,240)'))

choromap2 = go.Figure(data = [data],layout=layout)
iplot(choromap2)
