#######
# Objective: Create a bubble chart that compares three other features
# from the mpg.csv dataset. Fields include: 'mpg', 'cylinders', 'displacement'
# 'horsepower', 'weight', 'acceleration', 'model_year', 'origin', 'name'
######

# Perform imports here:
import pandas as pd
import plotly.offline as pyo
import plotly.graph_objs as go

# create a DataFrame from the .csv file:
df = pd.read_csv('../data/mpg.csv')

# Add columns to the DataFrame to convert model year to a string and
# then combine it with name so that hover text shows both:
df['year_string']=pd.Series(df['model_year'],dtype=str)
df['model_year']="'"+df['year_string']+" "+df['name']

# create data by choosing fields for x, y and marker size attributes
data = [go.Scatter(
            x = df['horsepower'],
            y = df['mpg'],
            name = 'Cars',
            text = df['model_year'],
            mode = 'markers',
            marker = dict(
                size = 0.005*df['weight'],
                color = df['cylinders']
              )
          )]

# create a layout with a title and axis labels
layout = go.Layout(
    title = 'CARS',
    xaxis = dict(title = 'HP'), 
    yaxis = dict(title = 'MPG'),
    hovermode ='closest' 
)

# create a fig from data & layout, and plot the fig
fig = go.Figure(data=data, layout=layout)
pyo.plot(fig, filename='Bubble_Chart_Exercise.html')