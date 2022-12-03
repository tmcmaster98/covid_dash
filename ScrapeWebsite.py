import requests
from bs4 import BeautifulSoup as soup
import WriteJson

def ScrapeAll(countrylist,websitelist):
    for i in range(len(countrylist)):
        for j in range(len(websitelist)):
            d1,d2,d3 = scrape_country(countrylist[i],websitelist[j])
            WriteJson.data2json(websitelist[j],countrylist[i],d1,d2,d3)
    return 1

def scrape_country(country_name,website_name):
    if website_name == "worldometer":
        #print("Getting data from Worldometer")
        if country_name == 'United States':
            country_name = 'USA'
        if country_name == 'South Korea':
            country_name = 'S. Korea'
        if country_name == 'U.K.':
            country_name = 'UK'
        url = "https://www.worldometers.info/coronavirus/"
        data = scrape_countryWorld(country_name,url)
        datao = data[0]
        return string2num(datao[2]), string2num(datao[1]), string2num(datao[3])
    elif website_name == "nytimes":
        #print("Getting data from NYTimes")
        dailyD = scrape_country_NYT(country_name,'NYT_12_01_2022_dd.html',1)
        cumulativeD,norm_comulativeD = scrape_country_NYT(country_name,'NYT_12_01_2022_td.html',2)
        return string2num(dailyD), string2num(cumulativeD), string2num(norm_comulativeD)*10
    else:
        print("Unknow Website")
        return 0,0,0

def string2num(data):
    if len(data) == 0:
        return 0
    return float(data.replace(',',''))

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
            #print(country_wanted)
            return country_wanted
            
def scrape_country_NYT(country,filename,type):
    with open(filename) as fp:
        soup1 = soup(fp,'html5lib') #soup = soup.BeautifulSoup(fp,'html5lib')
    table = soup1.find("table")
    table_rows = table.find_all('tr')
    data = []
    for tr in table_rows:
        td = tr.find_all('td')
        row = [i.text.strip() for i in td]
        data.append(row)
    data.remove([])
    for idx, coun in enumerate(data):
        if('â€º' in coun[0]):
            coun[0] = coun[0].split()[:-1]
            coun[0] = " ".join(coun[0])
        #print(coun[0])
        if(str(coun[0]) not in str(country)):
            continue
        if type == 2:
            return coun[4], coun[5]
        else:
            return coun[4]

#Country = ["France"]
#ScrapeAll(Country,["nytimes"])