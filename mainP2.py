import ScrapeWebsite
import WriteJson
from datetime import datetime
from bokeh.layouts import layout, column, row
from bokeh.models import Div, CustomJS, Select, DateRangeSlider, ColumnDataSource, Legend, Range1d
from bokeh.plotting import figure, show

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
## This is where the rest of the code goes





output = layout([[divtop],[divtop2],[breakline],[layoutfigure1],[breakline]])

show(output)