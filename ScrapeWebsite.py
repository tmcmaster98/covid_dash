import WriteJson

def scrape_country(country_name,website_name):
    if website_name == "worldometer":
        print("Getting data from Worldometer")
        dailyD = 1
        cumulativeD = 1
        norm_dailyD = 1
        norm_comulativeD = 1
        WriteJson.data2json(website_name,country_name,dailyD,cumulativeD,norm_dailyD,norm_comulativeD)
        return 1
    elif website_name == "nytimes":
        print("Getting data from NYTimes")
        dailyD = 1
        cumulativeD = 1
        norm_dailyD = 1
        norm_comulativeD = 1
        WriteJson.data2json(website_name,country_name,dailyD,cumulativeD,norm_dailyD,norm_comulativeD)
        return 1
    else:
        print("Unknow Website")
        return 0