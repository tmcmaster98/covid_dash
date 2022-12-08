import ScrapeWebsite
import WriteJson
from datetime import datetime
from bokeh.layouts import layout, column, row
from bokeh.models import Div, CustomJS, Select, DateRangeSlider, ColumnDataSource, Legend, Range1d, FactorRange, Slider,SetValue
from bokeh.plotting import figure, show
import math
from bokeh.palettes import Category20c
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
        inner['value'] = percentages
        output[day] = inner
    return output

# This will be the main function to run everything.

countries = ['United States','India','France','Germany','Brazil','South Korea','Italy','U.K.','Japan','Russia']
colorslist = Category20c[len(countries)] #['black','blue','brown','cyan','green','orange','red','purple','yellow','pink']
websites = ["worldometer","nytimes"]

#ScrapeWebsite.ScrapeAll(countries,websites)

dataAll = WriteJson.readJson()
dates_str = dataAll["Dates"]
dates = str2date(dates_str)
Wtd = getdatalist(dataAll,countries,websites[0],dates_str,"cumulative death",dates)
Wntd = getdatalist(dataAll,countries,websites[0],dates_str,"normalized comulative death",dates)
Ntd = getdatalist(dataAll,countries,websites[-1],dates_str,"cumulative death",dates)
Nntd = getdatalist(dataAll,countries,websites[-1],dates_str,"normalized comulative death",dates)

divtop = Div(text="<b>Welcome to your Covid Dashboard </b>")
divtop2 = Div(text="Created by Thomas Mcmaster, Jason Hernandez and Zachary Hunzeker")
breakline = Div(text = "_________________________________________________________________________________________________________________________________________________________________________________________________________________________",height = 50)
sourcedata1 = Wtd
source1 = ColumnDataSource(data = sourcedata1)
selectWebsite = Select(title="Website",value=websites[0],options=websites)
selectoutput = Select(title = "Value of interest",value = "Total Deaths", options=["Total Deaths","Normalized Total Deaths"])
date_range_slider1 = DateRangeSlider(title= "Choose date range",value = (dates[0],dates[-1]),start = dates[0] ,end = dates[-1])
p1 = figure(width = 1000, height = 500,x_axis_type="datetime",title = 'Deaths Over time',y_axis_label = "Total Deaths",x_axis_label = "Time")
p1.x_range = Range1d(date_range_slider1.value[0],date_range_slider1.value[1])
legend_it = []
for z in range(0,len(countries)):
    line = countries[z]
    c = p1.line('x',line,source=source1, color = colorslist[z],name = countries[z])
    legend_it.append((countries[z],[c]))
legend = Legend(items= legend_it)
p1.add_layout(legend,'right')
p1.legend.click_policy = "hide"
divnote1 = Div(text = "Click on legend name to hide/reappear that countries data.")
divnote2 = Div(text = "With the choose date range you can't have it be a single day.")

callbackData = CustomJS(args=dict(source=source1, selectWebsite=selectWebsite,selectoutput=selectoutput,yaxis= p1.yaxis[0],Wtd=Wtd,Wntd=Wntd,Ntd=Ntd,Nntd=Nntd),code="""
                const outputW = selectoutput.value
                const web = selectWebsite.value

                if (web == "worldometer"){
                    if (outputW == "Total Deaths"){
                        source.data = Wtd
                        yaxis.axis_label = "Total Deaths"
                    }
                    else{
                        source.data = Wntd
                        yaxis.axis_label = "Normalized Total Deaths"  
                    }    
                }
                else{
                    if (outputW == "Total Deaths"){
                        source.data = Ntd
                        yaxis.axis_label = "Total Deaths"
                    }
                    else{
                        source.data = Nntd
                        yaxis.axis_label = "Normalized Total Deaths"
                    }
                }      
                        """)


date_range_slider1.js_link('value',p1.x_range,'start',attr_selector=0)
date_range_slider1.js_link('value',p1.x_range,'end',attr_selector=1)
selectWebsite.js_on_change('value',callbackData)
selectoutput.js_on_change('value',callbackData)
layoutfigure1 = row(p1,column(selectoutput,selectWebsite,date_range_slider1,divnote1,divnote2))
## Start of bar graph

# define array of tuples. This contains every x position where there is a data point
x = [(country, date) for country in countries for date in dates_str]

# initialize vector to store daily death numbers
counts = []

# loop through each country, extracting data for the bar graph
for country in countries:
    bar = source1.data[country]
    counts = counts + bar

src = ColumnDataSource(data=dict(x=x,counts=counts,color=colorslist*len(dates)))
p2 = figure(x_range=FactorRange(*x), height=700, width=1500, title="Death Counts by Day")
p2.vbar(x='x', top='counts', width=0.9, source=src, line_color= "white",color='color')

p2.y_range.start = 0
p2.x_range.range_padding = 0.2
p2.xaxis.major_label_orientation = 1
p2.xgrid.grid_line_color = None

### Pie Graph Code
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
           tools="hover", tooltips="@names: @value", x_range=(-0.5, 1.0))
source2 = ColumnDataSource(data = WtdP[dates_str[0]])


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


output = layout([[divtop],[divtop2],[breakline],[layoutfigure1],[breakline],[p2],[breakline],[layoutfigure2],[breakline]])
show(output)