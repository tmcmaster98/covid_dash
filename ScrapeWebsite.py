

def scrape_country(country_name,website_name):
    if website_name == "worldometer":
        print("Getting data from Worldometer")
        return 1
    elif website_name == "nytimes":
        print("Getting data from NYTimes")
        return 1
    else:
        print("Unknow Website")
        return 0