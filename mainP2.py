import ScrapeWebsite
import WriteJson
from datetime import datetime
from bokeh.layouts import layout, column, row
from bokeh.models import Div, CustomJS, Select, DateRangeSlider, ColumnDataSource, Legend, Range1d, FactorRange, Slider,SetValue,RangeSlider
from bokeh.plotting import figure, show
import math
from bokeh.palettes import Category20c
# Functions used below
def str2date(dates):
    #function creates a list of the dates from the json file 
    
    output = [0]*len(dates)
    for i in range(len(dates)):
        brokenlist = dates[i].split('/')
        output[i] = datetime(int(brokenlist[2]),int(brokenlist[1]),int(brokenlist[0]),0,0,0)
    return output

def getdatalist(data,countrylist,website,dates,datetype,dates2):
    #function creates a dictionary where the keys are the countries and a variable x, within each key it holds the dates, total deaths,
    #and normalized death rates
    max = 0
    output = dict()
    outputline = [0]*len(dates)
    for i in range(0,len(countrylist)):
        for j in range(0,len(dates)):
            outputline[j] = WriteJson.getData(data,website,countrylist[i],dates[j],datetype)
            if outputline[j] > max:
                max = outputline[j]
        output[countrylist[i]] = outputline
        outputline = [0]*len(dates)
    output['x'] = dates2
    max = max*1.05
    return output,max

def getdataPercent(data,countrylist,website,dates,datatype,colors):
    
    output = dict()
    #function creates two different dictionaries that are used for the pie graph
    #the keys vary from country names, to the dates, and colors needed to produce the pie graph
    
    for j,day in enumerate(dates):
        total = 0
        outputline = [0]*len(countrylist)
        percentages = [0]*len(countrylist)
        pieValues = [0]*len(countrylist)
        inner = dict()
        for j,country in enumerate(countrylist):
            outputline[j] = WriteJson.getData(data,website,country,day,datatype)
            total = total + outputline[j]
        for x1,x in enumerate(outputline):
            percentages[x1] = (x/total)*100
            pieValues[x1] = x
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
        inner['value'] = pieValues
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
Wtd,maxWtd = getdatalist(dataAll,countries,websites[0],dates_str,"cumulative death",dates)
Wntd,maxWntd = getdatalist(dataAll,countries,websites[0],dates_str,"normalized comulative death",dates)
Ntd,maxNtd = getdatalist(dataAll,countries,websites[-1],dates_str,"cumulative death",dates)
Nntd,maxNntd = getdatalist(dataAll,countries,websites[-1],dates_str,"normalized comulative death",dates)
Wdd,maxWdd = getdatalist(dataAll,countries,websites[0],dates_str,"daily death",dates)
Ndd,maxNdd = getdatalist(dataAll,countries,websites[-1],dates_str,"daily death",dates)

divtop = Div(text="<b>Welcome to your Covid Dashboard </b>")
divtop2 = Div(text="Created by Thomas Mcmaster, Jason Hernandez and Zachary Hunzeker")
breakline = Div(text = "_________________________________________________________________________________________________________________________________________________________________________________________________________________________",height = 50)
sourcedata1 = Wtd
source1 = ColumnDataSource(data = sourcedata1)

#drop down buttons to select the website and type of data wanted to be displayed
selectWebsite = Select(title="Website",value=websites[0],options=websites)
selectoutput = Select(title = "Value of interest",value = "Total Deaths", options=["Deaths Per Day","Total Deaths","Normalized Total Deaths"])
yaxis_slider = RangeSlider(start = 0, end = 1,value=(0,1),step = .01,title='Zoom Percent in y direction')
#data range slider used to select the dates wanted to be displayed 
date_range_slider1 = DateRangeSlider(title= "Choose date range",value = (dates[0],dates[-1]),start = dates[0] ,end = dates[-1])
#start of line graph 
p1 = figure(width = 1000, height = 500,x_axis_type="datetime",title = 'Deaths Over time',y_axis_label = "Total Deaths",x_axis_label = "Time")
p1.x_range = Range1d(date_range_slider1.value[0],date_range_slider1.value[1])
p1.y_range = Range1d(start = 0,end = maxWtd)
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

callbackData = CustomJS(args=dict(source=source1, selectWebsite=selectWebsite,selectoutput=selectoutput,yaxis_slider=yaxis_slider,yaxis= p1.yaxis[0],y_range = p1.y_range,Wtd=Wtd,Wntd=Wntd,Wdd=Wdd,Ntd=Ntd,Nntd=Nntd,Ndd=Ndd,maxWtd=maxWtd,maxWntd=maxWntd,maxWdd=maxWdd,maxNtd=maxNtd,maxNntd=maxNntd,maxNdd=maxNdd),code="""                const outputW = selectoutput.value
                const web = selectWebsite.value
                const output = selectoutput.value
                const valueMin = yaxis_slider.value[0]
                const valueMax = yaxis_slider.value[1]
                if (web == "worldometer"){
                    if (output == "Total Deaths"){
                        source.data = Wtd
                        yaxis.axis_label = "Total Deaths"
                        y_range.end = maxWtd*valueMax
                        y_range.start = maxWtd*valueMin
                    }
                    else if (output == "Deaths Per Day"){
                        source.data = Wdd
                        yaxis.axis_label = "Daily Deaths"  
                        y_range.end = maxWdd*valueMax
                        y_range.start = maxWdd*valueMin
                    }
                    else{
                        source.data = Wntd
                        yaxis.axis_label = "Normalized Total Deaths"  
                        y_range.end = maxWntd*valueMax
                        y_range.start = maxWntd*valueMin
                    }    
                }
                else{
                    if (output == "Total Deaths"){
                        source.data = Ntd
                        yaxis.axis_label = "Total Deaths"
                        y_range.end = maxNtd*valueMax
                        y_range.start = maxNtd*valueMin
                    }
                    else if (output == "Deaths Per Day"){
                        source.data = Ndd
                        yaxis.axis_label = "Average Daily Deaths"  
                        y_range.end = maxNdd*valueMax
                        y_range.start = maxNdd*valueMin
                    }
                    else{
                        source.data = Nntd
                        yaxis.axis_label = "Normalized Total Deaths"
                        y_range.end = maxNntd*valueMax
                        y_range.start = maxNntd*valueMin
                    }
                }     
                        """)


date_range_slider1.js_link('value',p1.x_range,'start',attr_selector=0)
date_range_slider1.js_link('value',p1.x_range,'end',attr_selector=1)
selectWebsite.js_on_change('value',callbackData)
selectoutput.js_on_change('value',callbackData)
yaxis_slider.js_on_change('value',callbackData)
layoutfigure1 = row(p1,column(selectoutput,selectWebsite,date_range_slider1,yaxis_slider,divnote1,divnote2))
## Start of bar graph

# define array of tuples. This contains every x position where there is a data point
x = [(country, date) for country in countries for date in dates_str]

# initialize vector to store daily death numbers
counts1 = []
counts2 = []
counts3 = []
counts4 = []

# loop through each country, extracting data for the bar graph
for country in countries:
    bar1 = Wtd[country]
    bar2 = Wntd[country]
    bar3 = Ntd[country]
    bar4 = Nntd[country]
    counts1 = counts1 + bar1
    counts2 = counts2 + bar2
    counts3 = counts3 + bar3
    counts4 = counts4 + bar4

wtd_bar = dict()
wntd_bar = dict()
ntd_bar = dict()
nntd_bar = dict()
wtd_bar['counts'] = counts1
wntd_bar['counts'] = counts2
ntd_bar['counts'] = counts3
nntd_bar['counts'] = counts4
wtd_bar['x'] = x
wntd_bar['x'] = x
ntd_bar['x'] = x
nntd_bar['x'] = x
wtd_bar['color'] = colorslist*len(dates)
wntd_bar['color'] = colorslist*len(dates)
ntd_bar['color'] = colorslist*len(dates)
nntd_bar['color'] = colorslist*len(dates)

src = ColumnDataSource(data=wtd_bar)
p2 = figure(x_range=FactorRange(*x), height=700, width=1500, title="Death Counts by Day")
p2.vbar(x='x', top='counts', width=0.9, source=src, line_color= "white",color='color')

p2.y_range.start = 0
p2.x_range.range_padding = 0.2
p2.xaxis.major_label_orientation = 1
p2.xgrid.grid_line_color = None

selectWebsite3 = Select(title="Website",value=websites[0],options=websites)
selectoutput3 = Select(title = "Value of interest",value = "Total Deaths", options=["Total Deaths","Normalized Total Deaths"])


callbackData3 = CustomJS(args=dict(source=src, selectWebsite=selectWebsite3,selectoutput=selectoutput3,Wtd=wtd_bar,Wntd=wntd_bar,Ntd=ntd_bar,Nntd=nntd_bar),code="""
                const outputW = selectoutput.value
                const web = selectWebsite.value
                if (web == "worldometer"){              
                    if (outputW == "Total Deaths"){
                            source.data = Wtd
                              
                    }
                    else{
                        source.data = Wntd
                        
                    }    
                }
                else{
                    if (outputW == "Total Deaths"){
                        source.data = Ntd
                    }
                    else{
                        source.data = Nntd
                    }
                }        
                      """  )

selectWebsite3.js_on_change('value',callbackData3)
selectoutput3.js_on_change('value',callbackData3)

layoutfigure3 = column(p2,row(selectWebsite3,selectoutput3))

### Pie Graph Code
WtdP = getdataPercent(dataAll,countries,websites[0],dates_str,"cumulative death",colorslist)
WntdP = getdataPercent(dataAll,countries,websites[0],dates_str,"normalized comulative death",colorslist)
NtdP = getdataPercent(dataAll,countries,websites[-1],dates_str,"cumulative death",colorslist)
NntdP = getdataPercent(dataAll,countries,websites[-1],dates_str,"normalized comulative death",colorslist)

#A for loop to count the amount date entries in the json file that will be used later
count= 0
keyValues = []
for i in Wtd['United States']:
    count += 1
# print(count)

#This creates the pie graph figure
pie = figure(height=350, title="Pie Chart", toolbar_location=None,
           tools="hover", tooltips="@names: @value", x_range=(-0.5, 1.0))
source2 = ColumnDataSource(data = WtdP[dates_str[0]])

#creates the each wedge of the pie graph 
pie.wedge(x=0, y=1, radius=0.4, source = source2, start_angle= 'start' , end_angle= 'end', fill_color= 'color', legend_field= 'names')

pie.axis.axis_label = None
pie.axis.visible = False
pie.grid.grid_line_color = None

#slider that is used to select which day of data wants to be displayed
slider = Slider(start = 0, end = count - 1, value = 0, step = 1, title = "Day")

#drop down bars that are used to select from which website and what type of data wants to be displayed
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


#this outputs all three figures onto a single html page
output = layout([[divtop],[divtop2],[breakline],[layoutfigure1],[breakline],[layoutfigure3],[breakline],[layoutfigure2],[breakline]])
show(output)