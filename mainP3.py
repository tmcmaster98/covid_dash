import ScrapeWebsite
import WriteJson
from datetime import datetime
from bokeh.layouts import layout, column, row
from bokeh.models import Div, CustomJS, Select, DateRangeSlider, ColumnDataSource, Legend, Range1d, FactorRange
from bokeh.plotting import figure, show
from bokeh.palettes import BrBG10
from bokeh.transform import factor_mark

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
websites = ["worldometer","nytimes"]

#ScrapeWebsite.ScrapeAll(countries,websites)

dataAll = WriteJson.readJson()
dates_str = dataAll["Dates"]
dates = str2date(dates_str)
Wtd = getdatalist(dataAll,countries,websites[0],dates_str,"cumulative death",dates)
Wntd = getdatalist(dataAll,countries,websites[0],dates_str,"normalized comulative death",dates)
Ntd = getdatalist(dataAll,countries,websites[-1],dates_str,"cumulative death",dates)
Nntd = getdatalist(dataAll,countries,websites[-1],dates_str,"normalized comulative death",dates)

x = [(country, date) for country in countries for date in dates_str]
counts = []
source = Ntd
to_hash = []
for country in countries:
    bar = source[country]
    counts = counts + bar

src = ColumnDataSource(data=dict(x=x,counts=counts,color=BrBG10*len(dates)))

p = figure(x_range=FactorRange(*x), height=700, width=1500, title="Death Counts by Day", toolbar_location=None, tools="")
p.vbar(x='x', top='counts', width=0.9, source=src, line_color= "white",color='color')

p.y_range.start = 0
p.x_range.range_padding = 0.2
p.xaxis.major_label_orientation = 1
p.xgrid.grid_line_color = None



layoutfigure1 = row(p)

output = layout(layoutfigure1)
show(output)
