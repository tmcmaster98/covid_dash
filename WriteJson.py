import json
from datetime import date


def write_json(data,filename = 'CovidData.json'):
    with open(filename,'w') as file:
        json.dump(data,file,indent=4)

def data2json(website,country,daily,cumulative,norm_comulative):
    today = date.today()
    todays = today.strftime("%d/%m/%Y") # get the current date
    with open('CovidData.json') as json_file:
        try:
            # see if there is anything in the file
            data = json.load(json_file)
            dates = data["Dates"]
            if todays not in dates:
                dates.append(todays) # add the date to a list of dates to make some of the next steps easier
            if country not in data: 
                # see if the country exist in the data set
                data[country] = {todays:{website:{"daily death":daily,"cumulative death":cumulative,"normalized comulative death":norm_comulative}}}
            else:
                datac = data[country]
                if todays not in datac:
                    # see if the current date is in the data set
                    # this is here so we can seperate out the websites it will still update the information if the date is alread there.
                    datac[todays] = {website:{"daily death":daily,"cumulative death":cumulative,"normalized comulative death":norm_comulative}}
                else:
                    dataw = datac[todays]
                    dataw[website] = {"daily death":daily,"cumulative death":cumulative,"normalized comulative death":norm_comulative}
                        
        except:
            # this will only run if there is nothing in the json file. 
            data = {"Dates" : [todays],country:{todays:{website:{"daily death":daily,"cumulative death":cumulative,"normalized comulative death":norm_comulative}}}}
    write_json(data)

#data2json('nytimes','France',3,24,34.5,234)

def readJson():
    with open('CovidData.json') as json_file:
        data = json.load(json_file)
        return data

def getData(data,website,country,date,datatype):
    number = data[country][date][website][datatype]
    return number