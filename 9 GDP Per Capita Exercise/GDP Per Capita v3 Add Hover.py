# Create a dashboard with a scatter plot showing configurable x and y axis

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
import json

# read data
df = pd.read_csv('../data/gapminderDataFiveYear.csv')

# set features to show in x/y axis
features = ['pop','lifeExp','gdpPercap']

# Launch the application
app = dash.Dash()

# Setup app layout
app.layout = html.Div([

  # dropdown to select xaxis
  html.Div([
    dcc.Dropdown(
      id='xaxis',
      options=[{'label': i.title(), 'value': i} for i in features],
      value='gdpPercap'
    )
  ],
  style={'width': '20%', 'display': 'inline-block'}),

  # dropdown to select yaxis
  html.Div([
    dcc.Dropdown(
      id='yaxis',
      options=[{'label': i.title(), 'value': i} for i in features],
      value='lifeExp'
    )
  ],
  style={'width': '20%', 'display': 'inline-block'}),

  # button to apply change of axis
  html.Div([
    html.Button(
      id='submit-axis',
      n_clicks=0,
      children='Apply',
      style={'fontSize':16}
    ),
  ],
  style={'width': '10%', 'display': 'inline-block'}),

  # slider for year-picker  
  html.P([
    dcc.Slider(
      id = 'year-picker',
      min = df['year'].min(),
      max = df['year'].max(),
      step = 5,
      marks = {str(y): '{}'.format(y) for y in df['year'].unique()},
      value=df['year'].max()
    )
  ],
  style={'width': '90%'}),

  # scatterplot
  html.Div([
    dcc.Graph(
      id='scatterplot'
      # figure will be added by the decorated update_scatterplot_year function
    )
  ]),

  # country info
  html.Div(id='country_info', children='No country selected')

])

# Setup scatterplot interaction through callback function
@app.callback(
  Output('scatterplot', 'figure'), 
  [Input('submit-axis', 'n_clicks'), Input('year-picker', 'value')],
  [State('xaxis', 'value'), State('yaxis', 'value')]
)
def update_scatterplot(n_clicks, year, xaxis, yaxis):
  # filter by year
  filtered_df = df[df['year'] == year]  

  # create data traces by continent
  data = []
  for continent in filtered_df['continent'].unique():
    df_by_continent = filtered_df[filtered_df['continent'] == continent]
    data.append(go.Scatter(
      name = continent,
      x = df_by_continent[xaxis],
      y = df_by_continent[yaxis],
      text = df_by_continent['country'],
      mode = 'markers',
      marker = {
        'size': 15, 
        'opacity': 0.7, 
        'line': {
          'width': 0.5, 
          'color': 'white'
        }
      },
    ))

  # return figure (data & layout)
  return {
    'data': data,
    'layout': go.Layout(
      xaxis={'type': 'log', 'title': xaxis.title()},
      yaxis={'title': yaxis.title()},
      hovermode='closest'
    )
  }

# Setup country info interaction through callback function
@app.callback(
    Output('country_info', 'children'),
    [Input('scatterplot', 'hoverData')])
def print_country_info(hoverData):
  if hoverData is not None:
    country_name = hoverData['points'][0]['text']
    return country_name
  else:
    return 'Select a country'
    
# run the server
if __name__ == '__main__': 
  app.run_server()