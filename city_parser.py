import csv

def unemployment_parser():
    import json
    import unicodedata

    with open("unemp.json") as data_file:    
        data = json.load(data_file)
    
    results = data["results"]
    unemployment_states = []


    for result in results:

        description = result["description"]
        
        #if the first hyphen occurs before the first comma, parse up to the first dash
        #otherwise parse to the first comma
        
        if "-" in description and description.find("-") < description.find(","):
            comma = description.find("-")
        else:
            comma = description.find(",")
        space = description.find(" ")
        
        #convert unicode values
        
        city = str(description[space + 1:comma])
        state = str(description[comma + 2:comma + 4])
        last_space = description.rfind(" ")
        unemployment = description[last_space:]
        
        #trying to convert unicode to float
        #unemployment = float(unemployment.strip(u'% \n\t\r\xa0'))
        
        unemployment = str(unemployment)
 
        
        #print "city: " + city + ", state: " + state + ", unemployment rate: " + rate

        unemployment_states.append({"city":city, "state":state, "unemployment":unemployment})

    return unemployment_states


def main_parser():
        
    #A dictionary of keys that are integers and values that are state abbreviations plus DC alphabetized 
    
    abbs = [line.strip() for line in open('abbr.txt')]
    
    nums = [n for n in range(1, 52)]
    
    abb_hash = dict(zip(nums, abbs))
    
    
    
    #Open a csv data file and parses the data into Ruby hash format along with the KEYS from the dictionary of state abbreviations 
    
    main_data = []
    cities = []
    f = open("citypop.csv")
    csv_f = csv.reader(f)
    
    for row in csv_f:
        if len(row) > 4:
            state_abb = row[0][-2:]
            state_id = [key for key,value in abb_hash.iteritems() if value == state_abb][0]
            
            #if the first hyphen occurs before the first comma, parse up to the first dash
            #otherwise parse to the first comma
            
            if "-" in row[0] and row[0].find("-") < row[0].find(","):
                comma = row[0].find("-")
            else:    
                comma = row[0].find(",")
            city_parse = row[0][:comma]
            cities.append(city_parse)

            population = row[3]
            
            main_data.append({"city":city_parse, "state":state_abb, "state_id": str(state_id), "population":population, "unemployment:":"NA"})
            hash_format = "name: " + city_parse + ", population: " + population + ", state: " + state_abb + ", state_id: " + str(state_id)

            
            #if need to print to file
            #city_file = open('cities.txt', 'a')
            #print >>city_file, hash_format

    shortest =  min(cities, key=len)
    
    #check for duplicate city names
    
    from collections import Counter
    for city in cities: 
        k = city[:3]
        duplicates = [k for k,v in Counter(cities).items() if v>1]
 

    unemp_data = unemployment_parser()

    #check that duplicate cities get the right values inserted
    #insert unemployment values for the cities that have them
    
    for u in unemp_data:
        for m in main_data:
            for duplicate in duplicates:
                if u["city"] == duplicate:
                    if u["city"] == m["city"] and u["state"] == m["state"]:
                        m["unemployment"] = u["unemployment"]
                        #print m
                elif u["city"] == m["city"]:
                    m["unemployment"] = u["unemployment"]
                    #print m

  
            
main_parser()    