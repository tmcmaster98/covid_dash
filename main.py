import ScrapeWebsite
import WriteJson
import bs4 as BeautifulSoup
import urllib.request

# This will be the main function to run everything.

countries = ['United States','India','France','Germany','Brazil','South Korea','Italy','U.K.','Japan','Russia']
websites = ["worldometer","nytimes"]

ScrapeWebsite.ScrapeAll(countries,websites)

dataAll = WriteJson.readJson()

