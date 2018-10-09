#######
# Objective: Using the iris dataset, develop a Distplot
# that compares the petal lengths of each class.
# File: '../data/iris.csv'
# Fields: 'sepal_length','sepal_width','petal_length','petal_width','class'
# Classes: 'Iris-setosa','Iris-versicolor','Iris-virginica'
######

# Perform imports here:
import pandas as pd
import plotly.offline as pyo
import plotly.figure_factory as ff

# create a DataFrame from the .csv file
df = pd.read_csv('../data/iris.csv')

# auxiliar arrays
species = ['Iris-setosa','Iris-versicolor','Iris-virginica']

# Define the traces
data = []
labels = []
for s in species:
  data.append(df[df['class']==s]['petal_length'])
  labels.append(s)

# Create a fig from data and layout, and plot the fig
fig = ff.create_distplot(data, labels)
pyo.plot(fig, filename='distplot_chart_exercise.html')