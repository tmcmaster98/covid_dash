import ScrapeWebsite
import WriteJson
from datetime import datetime
from bokeh.layouts import layout
from bokeh.models import Div, CustomJS, Select, DateRangeSlider, ColumnDataSource, Legend
from bokeh.plotting import figure, show

# Functions used below
def str2date(dates):
    output = [0]*len(dates)
    for i in range(len(dates)):
        brokenlist = dates[i].split('/')
        output[i] = datetime(int(brokenlist[2]),int(brokenlist[1]),int(brokenlist[0]),0,0,0)
    return output

def getdatalist(data,countrylist,website,dates,datetype):
    output = dict()
    outputline = [0]*len(dates)
    for i in range(0,len(countrylist)):
        for j in range(0,len(dates)):
            outputline[j] = WriteJson.getData(data,website,countrylist[i],dates[j],datetype)
        output[countrylist[i]] = outputline
        outputline = [0]*len(dates)
    return output
# This will be the main function to run everything.

countries = ['United States','India','France','Germany','Brazil','South Korea','Italy','U.K.','Japan','Russia']
colorslist = ['black','blue','brown','cyan','green','orange','red','purple','yellow','pink']
websites = ["worldometer","nytimes"]

#ScrapeWebsite.ScrapeAll(countries,websites)

dataAll = WriteJson.readJson()
dates_str = dataAll["Dates"]
dates = str2date(dates_str)
Wtd = getdatalist(dataAll,countries,websites[0],dates_str,"cumulative death")
Wntd = getdatalist(dataAll,countries,websites[0],dates_str,"normalized comulative death")
Ntd = getdatalist(dataAll,countries,websites[-1],dates_str,"cumulative death")
Nntd = getdatalist(dataAll,countries,websites[-1],dates_str,"normalized comulative death")

divtop = Div(text="<b>Welcome to your Covid Dashboard </b>")
divtop2 = Div(text="Created by Thomas Mcmaster, Jason Hernandez and Zachary Hunzeker")
breakline = Div(text = "_________________________________________________________________________________________________________________________________________________________________________________________________________________________",height = 50)
sourcedata1 = Wtd
sourcedata1['x'] = dates
source1 = ColumnDataSource(data = sourcedata1)
selectWebsite = Select(title="Website",value=websites[0],options=websites)
p1 = figure(width = 800, height = 500,x_axis_type="datetime")

for z in range(0,len(countries)):
    line = countries[z]
    p1.line('x',line,source=source1,legend_label = countries[z],color = colorslist[z])

p1.add_layout(Legend(),'right')
p1.legend.click_policy = "hide"

date_range_slider1 = DateRangeSlider(title= "Choose date range",value = (dates[0],dates[-1]),start = dates[0] ,end = dates[-1])
date_range_slider1.js_link('value',p1.x_range,'start',attr_selector=0)
date_range_slider1.js_link('value',p1.x_range,'end',attr_selector=1)



output = layout([[divtop],[divtop2],[breakline],[selectWebsite],[date_range_slider1],[p1]])

show(output)