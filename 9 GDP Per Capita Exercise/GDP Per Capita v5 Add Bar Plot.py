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
    )
  ]),

  # markdown with selection stats
  html.Div([
    dcc.Markdown(
      id='selection_info', 
      children='-',
      )
  ]),

  # barplot
  html.Div([
    dcc.Graph(
      id='barplot'
    )
  ])

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

# Setup callback to update the barplot
@app.callback(
  Output('barplot', 'figure'),
  [Input('scatterplot', 'selectedData')])
def update_barplot(selectedData):
  if selectedData is not None:

    # get the indexes of the countries to show
    countries = [c['text'] for c in selectedData['points']]

    # filter the dataframe (only countries to show)
    df_filtered = df[df['country'].isin(countries)].sort_values(by='gdpPercap', ascending=False)

    # create figure
    figure = {
      'data': [go.Bar(
        x = df_filtered['country'],
        y = df_filtered['gdpPercap'],
        name = 'GDP per country'
      )], 
      'layout': go.Layout(
        title='GDP of selected countries',
        xaxis = dict(title = 'Country'),
        yaxis = dict(title = 'GDP')
      )
    }

    return figure 

  else:
    return ''

# Setup country info interaction through callback function
@app.callback(
    Output('selection_info', 'children'),
    [Input('scatterplot', 'selectedData')])
def print_stats_of_selected_countries(selectedData):
  if selectedData is not None:

    # get the indexes of the countries to show
    countries = [c['text'] for c in selectedData['points']]

    # filter the dataframe (only countries to show)
    df_filtered = df[df['country'].isin(countries)].sort_values(by='gdpPercap', ascending=False)

    # construct items to show in the markdown
    countries = ", ".join(str(c) for c in df_filtered['country'].unique())
    avg_gdp = df_filtered['gdpPercap'].mean()
    avg_life_exp = df_filtered['lifeExp'].mean()
    avg_pop = df_filtered['pop'].mean()

    return """
        {}
        - Avg GDP per Capita  {} 
        - Avg Life Expectancy {} 
        - Avg Population      {} 
        """.format(countries,avg_gdp,avg_life_exp,avg_pop)

  else:
    return 'Select some countries'

# run the server
if __name__ == '__main__': 
  app.run_server()