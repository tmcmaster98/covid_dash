import requests
from bs4 import BeautifulSoup as soup
import WriteJson

def ScrapeAll(countrylist,websitelist):
    for i in range(len(countrylist)):
        for j in range(len(websitelist)):
            scrape_country(countrylist[i],websitelist[j])

    return 1

def scrape_country(country_name,website_name):
    if website_name == "worldometer":
        print("Getting data from Worldometer")
        url = "https://www.worldometers.info/coronavirus/"
        data = scrape_countryWorld(country_name,url)
        datao = data[0]
        WriteJson.data2json(website_name,country_name,string2num(datao[2]),string2num(datao[1]),string2num(datao[3]))
        return 1
    elif website_name == "nytimes":
        print("Getting data from NYTimes")
        dailyD = 1
        cumulativeD = 1
        norm_comulativeD = 1
        WriteJson.data2json(website_name,country_name,dailyD,cumulativeD,norm_comulativeD)
        return 1
    else:
        print("Unknow Website")
        return 0

def string2num(data):
    if len(data) == 0:
        return 0
    return int(data.replace(',',''))

def scrape_countryWorld(Country,url):
    #requesting to access url
    url_req = requests.get(url, allow_redirects = True)

    #will check to see if request was successful
    if url_req.status_code ==  200:
        print("Request was successful")

    #using beautifulsoup to parse data
    url_soup = soup(url_req.text,"html.parser")
    #finds the data table with all country info
    data_table = url_soup.find("table", id = "main_table_countries_today").find("tbody")
    #splitting up table into rows with each country
    country_rows = data_table.find_all("tr", style = "")


    country_wanted = []
    #loops into each row and seperates the data from each column and then appends the data
    #if the first column matches with the specified country of interest 
    #also deletes any unwanted columsn 
    for row in country_rows:
        country_columns = row.find_all("td")
        country_info = [column.text.strip() for column in country_columns]
        #deletes first column
        del country_info[0]
        #deletes total cases and new cases
        del country_info[1:3]
        #deletes other unwanted data
        del country_info[3:8]
        del country_info[4:14]
        if country_info[0] == Country:
            country_wanted.append(country_info)
            print(country_wanted)
            return country_wanted
            

#Country = "France"
#scrape_country(Country,"worldometer")