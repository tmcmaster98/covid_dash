import ScrapeWebsite
import WriteJson
from bokeh.layouts import layout
from bokeh.models import Div, CustomJS, Select
from bokeh.plotting import figure, show

# This will be the main function to run everything.

countries = ['United States','India','France','Germany','Brazil','South Korea','Italy','U.K.','Japan','Russia']
websites = ["worldometer","nytimes"]

#ScrapeWebsite.ScrapeAll(countries,websites)

dataAll = WriteJson.readJson()
dates = dataAll["Dates"]
print(dates)

divtop = Div(text="<b>Welcome to your Covid Dashboard </b>")
divtop2 = Div(text="Created by Thomas Mcmaster, Jason Hernandez and Zachary Hunzeker")

selectWebsite = Select(title="Website",value=websites[0],options=websites)
selectWebsite.js_on_change("value", CustomJS(code="""
    console.log('select: value=' + this.value1, this.toString())
"""))



output = layout([[divtop],[divtop2],[selectWebsite]])

show(output)