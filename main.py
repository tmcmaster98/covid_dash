import ScrapeWebsite
import WriteJson
import bs4 as BeautifulSoup
import urllib.request

# This will be the main function to run everything.
'''
countries = ['USA','India','France','Germany','Brazil','S. Korea','Italy','UK','Japan','Russia']
websites = ["worldometer","nytimes"]

ScrapeWebsite.ScrapeAll(countries,websites)

dataAll = WriteJson.readJson()

number = WriteJson.getData(dataAll,'nytimes','USA','21/11/2022',"daily death")

print(number)
'''
with urllib.request.urlopen("https://www.nytimes.com/interactive/2021/us/covid-cases.html") as fp:
    soup = BeautifulSoup.BeautifulSoup(fp,'html5lib')

print(soup.title)
print('Reported cases, deaths' in str(soup.get_text))
"""
with open("Data/NYT_11-26-2022.html") as fp:
    data = BeautifulSoup(fp,'html5lib')
data = BeautifulSoup("<html>a web page</html>", 'html.parser')
"""
#data = BeautifulSoup(fp,'html5lib')

#    data = BeautifulSoup(fp, "html.parser")
#print(data)
