import ScrapeWebsite
import WriteJson
from datetime import datetime
from bokeh.layouts import layout, column, row
from bokeh.models import Div, CustomJS, Select, DateRangeSlider, ColumnDataSource, Legend, Slider
from bokeh.plotting import figure, show
import math

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

def getdataPercent(data,countrylist,website,dates,datatype,colors):
    output = dict()
    for j,day in enumerate(dates):
        total = 0
        outputline = [0]*len(countrylist)
        percentages = [0]*len(countrylist)
        inner = dict()
        for j,country in enumerate(countrylist):
            outputline[j] = WriteJson.getData(data,website,country,day,datatype)
            total = total + outputline[j]
        print(total)
        for x1,x in enumerate(outputline):
            percentages[x1] = (x/total)*100
        radians = [math.radians((percent/100)*360) for percent in percentages]
        start_angle = [math.radians(0)]
        prev = start_angle[0]
        for i in radians[:-1]:
            start_angle.append(i+prev)
            prev = i + prev
        end_angle = start_angle[1:] + [math.radians(0)]
        inner['start'] = start_angle
        inner['end'] = end_angle
        inner['color'] = colors
        inner['names'] = countrylist
        output[day] = inner
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
WtdP = getdataPercent(dataAll,countries,websites[0],dates_str,"cumulative death",colorslist)
WntdP = getdataPercent(dataAll,countries,websites[0],dates_str,"normalized comulative death",colorslist)
NtdP = getdataPercent(dataAll,countries,websites[-1],dates_str,"cumulative death",colorslist)
NntdP = getdataPercent(dataAll,countries,websites[-1],dates_str,"normalized comulative death",colorslist)

count= 0
keyValues = []
for i in Wtd['United States']:
    count += 1
print(count)

pie = figure(height=350, title="Pie Chart", toolbar_location=None,
           tools="hover", tooltips="@country: @value", x_range=(-0.5, 1.0))
source2 = ColumnDataSource(data = WtdP[dates_str[0]])

# print("source2",source2)
print("WtdP",WtdP)
pie.wedge(x=0, y=1, radius=0.4, source = source2, start_angle= 'start' , end_angle= 'end', fill_color= 'color', legend_field= 'names')

pie.axis.axis_label = None
pie.axis.visible = False
pie.grid.grid_line_color = None

slider = Slider(start = 0, end = count - 1, value = 0, step = 1, title = "Day")
selectWebsite2 = Select(title="Website",value=websites[0],options=websites)
selectoutput2 = Select(title = "Value of interest",value = "Total Deaths", options=["Total Deaths","Normalized Total Deaths"])

callbackData2 = CustomJS(args=dict(source=source2, selectWebsite=selectWebsite2,selectoutput=selectoutput2,Wtd=WtdP,Wntd=WntdP,Ntd=NtdP,Nntd=NntdP,dates_str=dates_str,slider=slider),code="""
                const outputW = selectoutput.value
                const web = selectWebsite.value
                const a = slider.value
                if (web == "worldometer"){              
                    if (outputW == "Total Deaths"){
                            source.data = Wtd[dates_str[a]]  
                    }
                    else{
                        source.data = Wntd[dates_str[a]]
                        
                    }    
                }
                else{
                    if (outputW == "Total Deaths"){
                        source.data = Ntd[dates_str[a]]
                    }
                    else{
                        source.data = Nntd[dates_str[a]]
                    }
                }        
                      """  )

slider.js_on_change('value',callbackData2)
selectWebsite2.js_on_change('value',callbackData2)
selectoutput2.js_on_change('value',callbackData2)
layoutfigure2 = row(pie,column(selectoutput2,selectWebsite2,slider))

show(layoutfigure2)