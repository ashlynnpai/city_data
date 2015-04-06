import csv

#A dictionary of keys that are integers and values that are state abbreviations plus DC alphabetized 

abbs = [line.strip() for line in open('abbr.txt')]

nums = [n for n in range(1, 52)]

abb_hash = dict(zip(nums, abbs))



#Open a csv data file and parse the data into Ruby hash format along with the KEYS from the dictionary of state abbreviations 

f = open("citypop.csv")
csv_f = csv.reader(f)

for row in csv_f:
    if len(row) > 4:
        state_abb = row[0][-2:]
        state_id = [key for key,value in abb_hash.iteritems() if value == state_abb][0]
        comma = row[0].find(",")
        city_parse = row[0][:comma]
        population = row[3]
        hash_format = "name: " + city_parse + ", population: " + population + ", state: " + state_abb + ", state_id: " + str(state_id)
        city_file = open('cities.txt', 'a')
        print >>city_file, hash_format
