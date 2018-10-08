#######
# Objective: Create a stacked bar chart from
# the file ../data/mocksurvey.csv. Note that questions appear in
# the index (and should be used for the x-axis), while responses
# appear as column labels.  Extra Credit: make a horizontal bar chart!
######

# Perform imports here
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# create a DataFrame from the .csv file:
df = pd.read_csv('../data/mocksurvey.csv', index_col=0)

# auxiliar structures
colors = { 
  'Strongly Agree' : '#0000ff',
  'Somewhat Agree' : '#8787ff',
  'Neutral' : '#dbdbdb',
  'Somewhat Disagree' : '#ff8787',
  'Strongly Disagree' : '#ff0000',
}

# create traces using a list comprehension
data = [go.Bar(
    y = df.index,
    x = df[response],
    name = response,
    marker = dict(color=colors[response]),
    orientation='h'
  ) for response in df.columns]
print(data)

# create a layout, remember to set the barmode here
layout = go.Layout(
    title = 'SURVEY RESULTS',
    xaxis = dict(title = 'QUESTION'),
    yaxis = dict(title = 'AVERAGE RESULT'),
    barmode='stack'
)

# create a fig from data & layout, and plot the fig.
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='Bar_Chart_Exercise.html')