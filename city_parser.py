import unittest
import mock

def population_parser():
    #Open a csv data file and parses the data into Ruby hash format along with the KEYS from the dictionary of state abbreviations 
    
    #A dictionary of keys that are integers and values that are state abbreviations plus DC alphabetized
    
    import csv
    
    abbs = [line.strip() for line in open('abbr.txt')]
    
    nums = [n for n in range(1, 52)]
    
    abb_hash = dict(zip(nums, abbs))
    
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
            
            main_data.append({"city":city_parse, "state":state_abb, "state_id": str(state_id), "population":population, "unemployment":0.0})
            hash_format = "name: " + city_parse + ", population: " + population + ", state: " + state_abb + ", state_id: " + str(state_id)
            
            #if need to print to file
            #city_file = open('cities.txt', 'a')
            #print >>city_file, hash_format


    return main_data
    
    
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
        
    main_data = []

    unemp_data = unemployment_parser()
    pop_data = population_parser()


    for u in unemp_data:
        for p in pop_data:
            if u["city"] == p["city"] and u["state"] == p["state"]:
                p["unemployment"] = u["unemployment"]
                #print p
                main_data.append(p)


    print main_data


main_parser()    


#currently unused helper functions

def find_duplicates(cities):
    #check for duplicate city names
    
    from collections import Counter
    for city in cities: 
        k = city[:3]
        duplicates = [k for k,v in Counter(cities).items() if v>1]
        
    return duplicates    
    
def find_shortest(cities):    
        
    return min(cities, key=len)
    
def update_values_against_duplicates(unemp_data, main_data):
    #insert unemployment values for the cities that have them
    #check that duplicate cities get the right values inserted
    
    for u in unemp_data:
        for m in main_data:
            for duplicate in duplicates:
                if u["city"] == duplicate:
                    if u["city"] == m["city"] and u["state"] == m["state"]:
                        m["unemployment"] = u["unemployment"]
                        print m
                elif u["city"] == m["city"]:
                    m["unemployment"] = u["unemployment"]
                    print m   
      
class TestUM(unittest.TestCase):
     
    def setUp(self):
        pass
    
    def test_main_parser1(self): 

        mock.unemployment_parser.return_value = [{'city': 'Austin', 'state': 'TX', 'unemployment': ' 3.7'}, {'city': 'Boulder', 'state': 'CO', 'unemployment': ' 3.7'}, 
        {'city': 'College Station', 'state': 'TX', 'unemployment': ' 3.7'}]   
        mock.population_parser.return_value = [{'unemployment': 0.0, 'city': 'Austin', 'state': 'TX', 'population': '1,716,289', 'state_id': '43'}, 
        {'unemployment': 0.0, 'city': 'Bakersfield', 'state': 'CA', 'population': '839,631', 'state_id': '5'}]
        
        self.assertEqual(main_parser(), [{'unemployment': 3.7, 'city': 'Austin', 'state': 'TX', 'population': '1,716,289', 'state_id': '43'}])
            
       
        if __name__ == '__main__':
            unittest.main(exit=False)              
                    