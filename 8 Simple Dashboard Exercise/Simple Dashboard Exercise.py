#######
# Objective: build a dashboard that imports OldFaithful.csv
# from the data directory, and displays a scatterplot.
# The field names are:
# 'D' = date of recordings in month (in August),
# 'X' = duration of the current eruption in minutes (to nearest 0.1 minute),
# 'Y' = waiting time until the next eruption in minutes (to nearest minute).
######

# Perform imports here
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd 

# Launch the application
app = dash.Dash()

# Create a DataFrame from the .csv file
df = pd.read_csv('../data/OldFaithful.csv')
df.columns = ['day', 'waiting', 'duration']

####################################

# Create the scatter plot with duration vs waiting
scatterplot_data = [go.Scatter(
  x=df['duration'],
  y=df['waiting'],
  mode='markers',
  marker = {
    'size':12,
    'color': 'rgb(66, 235, 244)',
    'symbol':'circle',
    'line':{'color':'rgb(65, 134, 244)', 'width':2}
  }
)]

scatterplot_layout = go.Layout(
  title='Old Faithful Geiser Duration Time vs Waiting Time',
  xaxis = {'title':'Duration (minutes)'},
  yaxis = {'title':'Waiting time (minutes)'}
)

####################################

# Create the boxplots with duration per day

boxplot_duration_data = [
    go.Box(
        y = df[df['day']==day]['duration'],
        name = day,
        marker = {'color' : 'rgb(66, 235, 244)'}
    )
    for day in range(1,24) 
]

# add a layout
boxplot_duration_layout = go.Layout(
    title = 'Old Faithful Geiser Duration Time by Day',
    showlegend = False 
)

####################################

# Create the boxplots with waiting per day

boxplot_waiting_data = [
    go.Box(
        y = df[df['day']==day]['waiting'],
        name = day,
        marker = {'color' : 'rgb(65, 134, 244)'}
    )
    for day in range(1,24) 
]

# add a layout
boxplot_waiting_layout = go.Layout(
    title = 'Old Faithful Geiser Waiting Time by Day',
    showlegend = False 
)

####################################

# Create a Dash layout that contains a Graph component
app.layout = html.Div([
  dcc.Graph(id='scatterplot',
    figure = {
     'data' : scatterplot_data,
     'layout' : scatterplot_layout
    }
  ),
  dcc.Graph(id='boxplot_duration',
    figure = {
     'data' : boxplot_duration_data,
     'layout' : boxplot_duration_layout
    }
  ),
  dcc.Graph(id='boxplot_waiting',
    figure = {
     'data' : boxplot_waiting_data,
     'layout' : boxplot_waiting_layout
    }
  )
])

# Add the server clause
if __name__ == '__main__':
  app.run_server()