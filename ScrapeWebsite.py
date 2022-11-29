import requests
from bs4 import BeautifulSoup as soup
import WriteJson


def scrape_country(Country,url):
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
            
# Url we want to scrape
url = "https://www.worldometers.info/coronavirus/"
Country = "France"
scrape_country(Country,url)