import ScrapeWebsite
import WriteJson

# This will be the main function to run everything.

countries = ['USA','Indai','France','Germany','Brazil','S. Korea','Italy','UK','Japan','Russia']
websites = ["worldometer","nytimes"]
ScrapeWebsite.ScrapeAll(countries,websites)

dataAll = WriteJson.readJson()

number = WriteJson.getData(dataAll,'nytimes','USA','21/11/2022',"daily death")

print(number)