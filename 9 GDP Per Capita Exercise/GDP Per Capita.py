# Create a dashboard with a scatter plot showing GDP per capita vs life expectancy

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import pandas as pd

# read data
df = pd.read_csv('../data/gapminderDataFiveYear.csv')

# Launch the application
app = dash.Dash()

# Setup app layout
app.layout = html.Div([
  # scatterplot
  dcc.Graph(
    id='scatterplot'
    # figure will be added by the decorated update_scatterplot_year function
  ),
  # dropdown
  #dcc.Dropdown(
  #  id = 'year-picker',
  #  options = [{'label':str(y), 'value':y} for y in df['year'].unique()],
  #  value = df['year'].max()
  #),
  #slider
  dcc.Slider(
    id = 'year-picker',
    min = df['year'].min(),
    max = df['year'].max(),
    step = 5,
    marks = {str(y): '{}'.format(y) for y in df['year'].unique()},
    value=df['year'].max()
  )
])

# Setup year_picker-scatterplot interaction through callback function
@app.callback(Output('scatterplot', 'figure'), [Input('year-picker', 'value')])
def update_scatterplot_year(year):
  # filter by year
  filtered_df = df[df['year'] == year]  

  # create data traces by continent
  data = []
  for continent in filtered_df['continent'].unique():
    df_by_continent = filtered_df[filtered_df['continent'] == continent]
    data.append(go.Scatter(
      name = continent,
      x = df_by_continent['gdpPercap'],
      y = df_by_continent['lifeExp'],
      text = df_by_continent['country'],
      mode = 'markers',
      opacity = 0.7,
      marker = {'size': 15},
    ))

  # return figure (data & layout)
  return {
    'data': data,
    'layout': go.Layout(
      xaxis={'type': 'log', 'title': 'GDP Per Capita'},
      yaxis={'title': 'Life Expectancy'},
      hovermode='closest'
    )
  }

# run the server
if __name__ == '__main__': 
  app.run_server()