#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pylab as plt

import plotly as py
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

import webbrowser

import io 
import requests


# In[2]:


#load dataframe
df = pd.read_csv('Citymapper_Mobility_Index_20200424.csv')


# In[3]:


#couldn't find a great city/country/geography package (found some but meh, didn't love them)
#download the kaggle dataset: https://www.kaggle.com/max-mind/world-cities-database/data
cities = pd.read_csv('worldcitiespop.csv')


# In[4]:


#clean it (remove first two rows)
df = df.drop([0, 1])
df.head(50)


# In[5]:


#make the first row the column headers
new_header = df.iloc[0] #grab the first row for the header
df = df[1:] #take the data less the header row
df.columns = new_header #set the header row as the df header
df.head(20)


# In[6]:


df.fillna(0, inplace=True)
df.head(20)


# In[7]:


#stack the dataframe
df1 = df.stack().reset_index()
df1.head()


# In[8]:


#drop all rows like Date and rename columns
df1 = df1.drop(df1[df1[2].str.contains('Date')].index)
df1.columns = ['Date','City','Percent_of_City_Moving']
df1.head(20)


# In[9]:


#create a variable/dictionary with the index and the Date
mapping = dict(df['Date'])
mapping


# In[10]:


#create a new column called Date and map to the mappings dictionary
df1['Date'] = df1['Date'].map(mapping)
df1.head()


# In[11]:


#bring in population data
pop = pd.read_csv('pop.csv')
df1 = pd.merge(df1,pop,left_on='City',right_on='Name')


# In[12]:


#convert to number/remove $ and , signs
df1['2020 Population '] = df1["2020 Population "].replace('[\$,]', '', regex=True).astype(float)
df1["2019 Population"] = df1["2019 Population"].replace('[\$,]', '', regex=True).astype(float)
df1["Percent_of_City_Moving"] = df1["Percent_of_City_Moving"].replace('[\$,]', '', regex=True).astype(float)


# In[13]:


df1.City.unique()


# In[14]:


#join the dataframes on City
join = pd.merge(df1, cities, how='inner', left_on="City", right_on="City")

Analysis
# In[15]:


df1.dtypes


# In[16]:


df1.shape


# In[17]:


#create an index column
df1['index'] = df1.index


# In[18]:


df1.index.unique()


# In[19]:


#create frequency of percent of city moving column
df1['count_percent_moving'] = df1.groupby('Percent_of_City_Moving')['Percent_of_City_Moving'].transform('count')


# In[20]:


df1.head(50)


# In[21]:


#line plot
layout = "Percent of City Moving"
fig = px.line(df1,
              title=layout,
              x="Date",
              y="Percent_of_City_Moving", 
              color="City", 
              hover_name="City",
              line_shape="spline",
              render_mode="svg"
             )
fig.show()


# In[22]:


#scatter plot
layout = "Percent of City Moving Scatter"
fig = px.scatter(df1, 
                 title=layout,
                 x="Date", 
                 y="Percent_of_City_Moving", 
                 color="City",
                 size="Percent_of_City_Moving", 
                 hover_name="City"
                )
fig.show()


# In[23]:


#scatter plot (cant have nulls or zeros - plotly will just use the first non null as the animated point to plot)
fig = px.scatter(df1, 
                 x="index", 
                 y="Percent_of_City_Moving", 
                 animation_frame="Date", #this is right
                 #animation_group="City", #this is right
                 color="City",
                 size="2020 Population ", 
                 hover_data=['Percent_of_City_Moving'],
                 #log_x=True, 
                 #size_max=55
                 range_x=[1,4100],
                 range_y=[0,1.5]
)

fig.show()


# In[24]:


fig = px.density_heatmap(df1,
                         x="Date",
                         y="Percent_of_City_Moving",
                         marginal_x="rug",
                         marginal_y="histogram")
fig.show()


# In[25]:


fig = px.scatter_geo(df1,
                     locations="Country",
                     size="Percent_of_City_Moving",
                     projection="natural earth")
fig.show()


# In[26]:


fig = px.choropleth(df1,
                    locations="Country",
                    color="Percent_of_City_Moving",
                    hover_name="Country",
                    animation_frame="Date",
                    range_color=[0,1.5])
fig.show()


# In[27]:


df3 = px.data.gapminder()
fig = px.choropleth(
    df3,
    locations="iso_alpha",
    color="lifeExp",
    hover_name="country",
    animation_frame="year",
    range_color=[20,80])
fig.show()


# In[28]:


fig = px.area(df1,
              x="Date",
              y="Percent_of_City_Moving",
              color="City",
              line_group="City")
fig.show()


# In[1]:


get_ipython().system('jt -t monokai')

