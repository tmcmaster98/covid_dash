import ScrapeWebsite
import WriteJson
from datetime import date
from bokeh.layouts import layout
from bokeh.models import Div, CustomJS, Select, DateRangeSlider
from bokeh.plotting import figure, show

# This will be the main function to run everything.

countries = ['United States','India','France','Germany','Brazil','South Korea','Italy','U.K.','Japan','Russia']
websites = ["worldometer","nytimes"]

#ScrapeWebsite.ScrapeAll(countries,websites)

dataAll = WriteJson.readJson()
dates = dataAll["Dates"]


divtop = Div(text="<b>Welcome to your Covid Dashboard </b>")
divtop2 = Div(text="Created by Thomas Mcmaster, Jason Hernandez and Zachary Hunzeker")
breakline = Div(text = "_________________________________________________________________________________________________________________________________________________________________________________________________________________________",height = 50)

selectWebsite = Select(title="Website",value=websites[0],options=websites)
startdate = dates[0].split('/')
enddate = dates[-1].split('/')
date_range_slider1 = DateRangeSlider(title= "Choose date range",value = (date(int(startdate[2]),int(startdate[1]),int(startdate[0])),date(int(enddate[2]),int(enddate[1]),int(enddate[0]))),start = date(int(startdate[2]),int(startdate[1]),int(startdate[0])) ,end = date(int(enddate[2]),int(enddate[1]),int(enddate[0])))




output = layout([[divtop],[divtop2],[breakline],[selectWebsite],[date_range_slider1]])

show(output)