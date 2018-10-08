#######
# Objective: Using the file 2010YumaAZ.csv, develop a Line Chart
# that plots seven days worth of temperature data on one graph.
# You can use a for loop to assign each day to its own trace.
######

# Perform imports here:
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# Create a pandas DataFrame from 2010YumaAZ.csv
df = pd.read_csv('../data/2010YumaAZ.csv')
days = ['TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY','MONDAY']

# select columns we are interested in
df_ready = df[['DAY','LST_TIME','T_HR_AVG']]

# create traces for the data list
data = [go.Scatter(
  x = df_ready[df_ready['DAY'] == day]['LST_TIME'],
  y = df_ready[df_ready['DAY'] == day]['T_HR_AVG'],
  mode = 'lines',
  name = day
  ) for day in days]

# Define the layout
layout = go.Layout(
    title = 'AVERAGE TEMPERATURES', # Graph title
    xaxis = dict(title = 'HOUR'), # x-axis label
    yaxis = dict(title = 'TEMPERATURE'), # y-axis label
    hovermode ='closest' # handles multiple points landing on the same vertical
)

# Create a fig from data and layout, and plot the fig
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='Line_Chart_Exercise.html')