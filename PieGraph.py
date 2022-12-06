import ScrapeWebsite
import WriteJson
from datetime import datetime
from bokeh.layouts import layout, column, row
from bokeh.models import Div, CustomJS, Select, DateRangeSlider, ColumnDataSource, Legend, Slider
from bokeh.plotting import figure, show
from math import pi

import pandas as pd

from bokeh.io import output_file, show
from bokeh.palettes import Category20c
from bokeh.transform import cumsum
import numpy as np

# Functions used below
def str2date(dates):
    output = [0]*len(dates)
    for i in range(len(dates)):
        brokenlist = dates[i].split('/')
        output[i] = datetime(int(brokenlist[2]),int(brokenlist[1]),int(brokenlist[0]),0,0,0)
    return output

def getdatalist(data,countrylist,website,dates,datetype,dates2):
    output = dict()
    outputline = [0]*len(dates)
    for i in range(0,len(countrylist)):
        for j in range(0,len(dates)):
            outputline[j] = WriteJson.getData(data,website,countrylist[i],dates[j],datetype)
        output[countrylist[i]] = outputline
        outputline = [0]*len(dates)
    output['x'] = dates2
    return output
# This will be the main function to run everything.

countries = ['United States','India','France','Germany','Brazil','South Korea','Italy','U.K.','Japan','Russia']
colorslist = ['black','blue','brown','cyan','green','orange','red','purple','yellow','pink']
websites = ["worldometer","nytimes"]

#ScrapeWebsite.ScrapeAll(countries,websites)

dataAll = WriteJson.readJson()
dates_str = dataAll["Dates"]
dates = str2date(dates_str)
Wtd = getdatalist(dataAll,countries,websites[0],dates_str,"cumulative death",dates)
Wntd = getdatalist(dataAll,countries,websites[0],dates_str,"normalized comulative death",dates)
Ntd = getdatalist(dataAll,countries,websites[-1],dates_str,"cumulative death",dates)
Nntd = getdatalist(dataAll,countries,websites[-1],dates_str,"normalized comulative death",dates)

#used to get the length of the data 
count= 0
keyValues = []
for i in Wtd['United States']:
    count += 1
print(count)
#gets the value of key(country)
for j in range(0,count):
    for i in Wtd.values():
        keyValues.append(i[j])
print("key values",keyValues)

# Wtddict={}
sections = [keyValues[i:i+11] for i in range(0,len(keyValues),11)]
# print("sections",sections)
# print("length",len(sections))
# for count,val in enumerate(countries):
#     for j in sections[0]:
#         Wtddict[val] = sections[0][count]

# print("dict",Wtddict)

#creates the day list to turn into a dictionary 
WtdDayList = []
WntdDayList = []
NtdDayList = []
NntdDayList = []
#goes through the lenght of the sections and creates a new day
for i in range(0,len(sections)):
    WtdDayList.append("Day" + str(i))
# print(WtdDayList)
for i in range(0,len(sections)):
    WntdDayList.append("Day" + str(i))
# print(WntdDayList)
for i in range(0,len(sections)):
    NtdDayList.append("Day" + str(i))
# print(NtdDayList)
for i in range(0,len(sections)):
    NntdDayList.append("Day" + str(i))
# print(NntdDayList)


#turns the day list into a nested dictionary 
WtdDayDict = {}
WntdDayDict = {}
NtdDayDict = {}
NntdDayDict = {}
for i in WtdDayList:
    WtdDayDict[i] = {}
for i in WtdDayList:
    WntdDayDict[i] = {}
for i in WtdDayList:
    NtdDayDict[i] = {}
for i in WtdDayList:
    NntdDayDict[i] = {}

# print(WtdDayDict)
# print(WntdDayDict)
# print(NtdDayDict)
# print(NntdDayDict)

#loops through each dictionary in the days
#Wtd
for j,val1 in enumerate(WtdDayDict):
    # print(WtdDayDict[val1])
    # print(sections[j])
    #loops through each country in the list
    for count,val in enumerate(countries):
        #  print(val)
         #inserts the country with value of each value of the section
         WtdDayDict[val1][val] = sections[j][count]
        #  print(WtdDayDict[i])
#Wntd
for j,val1 in enumerate(WtdDayDict):
    # print(WntdDayDict[val1])
    # print(sections[j])
    #loops through each country in the list
    for count,val in enumerate(countries):
        #  print(val)
         #inserts the country with value of each value of the section
         WntdDayDict[val1][val] = sections[j][count]
        #  print(WntdDayDict[i])
#Ntd
for j,val1 in enumerate(WtdDayDict):
    # print(NtdDayDict[val1])
    # print(sections[j])
    #loops through each country in the list
    for count,val in enumerate(countries):
        #  print(val)
         #inserts the country with value of each value of the section
         NtdDayDict[val1][val] = sections[j][count]
        #  print(NtdDayDict[i])
#Nntd
for j,val1 in enumerate(WtdDayDict):
    # print(NntdDayDict[val1])
    # print(sections[j])
    #loops through each country in the list
    for count,val in enumerate(countries):
        #  print(val)
         #inserts the country with value of each value of the section
         NntdDayDict[val1][val] = sections[j][count]
        #  print(NntdDayDict[i])
#prints the new dictionary
# print("wtd",WtdDayDict)
# print("first dictionary",WtdDayDict['Day0'])
# print("Wntd",WntdDayDict)
# print("Ntd",NtdDayDict)
# print("Nntd",NntdDayDict)


data = pd.Series(WtdDayDict['Day0']).reset_index(name='value').rename(columns={'index': 'country'})
data['angle'] = data['value']/data['value'].sum() * 2*pi
data['color'] = Category20c[len(WtdDayDict['Day0'])]

pie = figure(height=350, title="Pie Chart", toolbar_location=None,
           tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))

pie.wedge(x=0, y=1, radius=0.4,
        start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
        line_color="white", fill_color='color', legend_field='country', source=data)

pie.axis.axis_label = None
pie.axis.visible = False
pie.grid.grid_line_color = None

show(pie)

    
    