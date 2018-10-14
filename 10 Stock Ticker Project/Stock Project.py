#######
# First Milestone Project: Develop a Stock Ticker
# dashboard that either allows the user to enter
# a ticker symbol into an input box, or to select
# item(s) from a dropdown list, and uses pandas_datareader
# to look up and display stock data on a graph.
######

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime
import json
import pandas_datareader.data as web_data

# Launch the application
app = dash.Dash()


# read list of symbols and create the 'options' element for the dropdown
nsdq = pd.read_csv('../data/NASDAQcompanylist.csv')
nsdq.set_index('Symbol', inplace=True)
stock_symbols = [{'label':'{} {}'.format(s, nsdq.loc[s]['Name']), 'value':s} for s in nsdq.index]
#stock_symbols = [{'label':'AAPL', 'value':'AAPL'}, {'label':'MSFT', 'value':'MSFT'}, {'label':'NFLX', 'value':'NFLX'}]

# Setup app layout
app.layout = html.Div([

  html.H1('Stock Ticker Dashboard'),

  # dropdown to select stock symbols
  html.Div([

    html.H3('Select stock symbols'),

    dcc.Dropdown(
      id = 'stock_symbols',
      options = stock_symbols,
      value = 'AAPL',
      multi = True
    )
  ], style = {'width': '50%', 'display': 'inline-block', 'vertical-align': 'top'}),

  # date-pickers
  html.Div([
    
    html.H3('Select start and end dates:'),
    
    dcc.DatePickerRange(
      id = 'date_picker',
      min_date_allowed = datetime(2015, 1, 1),
      max_date_allowed = datetime.today().date(),
      start_date = datetime(2018, 1, 1),
      end_date = datetime.today().date(),
      display_format='DD/MM/YYYY'
    )
  ], style={'display':'inline-block', 'marginLeft':'20px'}),

  # button to apply stock symbols and dates to plot
  html.Div([
    html.Button(
      id = 'submit_button',
      n_clicks = 0,
      children = 'Apply',
      style = {'fontSize':18}
    )
  ], style={'display':'inline-block', 'marginLeft':'20px'}),

  # line plot to display stock symbols data
  html.Div([
    dcc.Graph(
      id='stock_data_plot'
    )
  ]),

])

# Setup callback for interation between data pickers and plot
@app.callback(
  Output('stock_data_plot', 'figure'),
  [Input('submit_button', 'n_clicks')],
  [
    State('stock_symbols', 'value'),
    State('date_picker', 'start_date'), 
    State('date_picker', 'end_date'),
  ]
)
def update_stock_data(submit_n_clicks, stock_symbols, start_date, end_date):

  # create auxiliar variables
  if type(stock_symbols) == list:
    stock_symbols_string = ', '.join(stock_symbols)
    stock_symbols_list = stock_symbols
  else:
    stock_symbols_string = stock_symbols
    stock_symbols_list = [stock_symbols]

  # construct data traces getting stock data from  pandas DataReader
  data = []
  for s in stock_symbols_list:

    # get data from DataReader
    df = web_data.DataReader(s,'iex', start_date, end_date)

    # append trace to data
    data.append(go.Scatter(
      x = df.index, 
      y = df.close,
      name = s,
      mode = 'lines'
    ))

  # create figure
  figure = {
    'data': data,
    'layout': go.Layout(
      title = 'Closing Prices of "{}" from {} to {}'.format(
        stock_symbols_string,
        start_date,
        end_date
      ),
      xaxis=dict(
        rangeselector=dict(
          buttons=list([
            dict(count=1,
              label='1m',
              step='month',
              stepmode='backward'),
            dict(count=6,
              label='6m',
              step='month',
              stepmode='backward'),
            dict(step='all')
          ])
        ),
        rangeslider=dict(
          visible = True
        ),
        type='date'
    )
    )
  }

  return figure

# run the server
if __name__ == '__main__': 
  app.run_server()